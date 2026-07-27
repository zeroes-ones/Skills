#!/usr/bin/env node
/**
 * Behavioral Eval Runner (Tier 3)
 * Validates that agent output satisfies behavioral expectations: follows skill
 * constraints, avoids anti-patterns, includes required sections, and stays within
 * token budgets. Designed to run against pre-recorded agent sessions or freshly
 * generated outputs.
 *
 * Usage: node scripts/run-behavioral-evals.js [--suite id] [--json] [--output-dir path]
 *
 * Inspired by addyosmani/agent-skills tier-3 behavioral evals.
 */
'use strict';

const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------
const EVALS_DIR = path.join(__dirname, '..', 'evals');
const BEHAVIORAL_DIR = path.join(EVALS_DIR, 'tier3-behavioral');
const SKILLS_DIR = path.join(__dirname, '..', 'skills');

const args = process.argv.slice(2);
const targetSuite = (() => { const i = args.indexOf('--suite'); return i >= 0 ? args[i + 1] : null; })();
const jsonOutput = args.includes('--json');

// Output directory for fresh eval runs (pre-recorded sessions avoid this)
const outputDirIdx = args.indexOf('--output-dir');
const outputDir = outputDirIdx >= 0 ? args[outputDirIdx + 1] : null;

// ---------------------------------------------------------------------------
// Scenario types
// ---------------------------------------------------------------------------
const SCENARIO_TYPES = {
  checklist_coverage: {
    description: 'Output must satisfy all items in the skill production checklist',
    validate(checklist, output) {
      const missing = [];
      for (const item of checklist) {
        const patterns = Array.isArray(item.patterns) ? item.patterns : [item.toLowerCase()];
        const found = patterns.some(p => output.toLowerCase().includes(p.toLowerCase()));
        if (!found) missing.push(item.label || item);
      }
      return {
        passed: missing.length === 0,
        details: missing.length > 0 ? `Missing: ${missing.join(', ')}` : 'All checklist items satisfied',
        coverage: checklist.length > 0
          ? Math.round((1 - missing.length / checklist.length) * 100)
          : 100,
      };
    },
  },

  anti_pattern_avoidance: {
    description: 'Output must not contain known anti-patterns',
    validate(antiPatterns, output) {
      const violations = [];
      for (const ap of antiPatterns) {
        const patterns = Array.isArray(ap.patterns) ? ap.patterns : [ap.toLowerCase()];
        for (const p of patterns) {
          if (output.toLowerCase().includes(p.toLowerCase())) {
            violations.push(ap.label || ap);
            break;
          }
        }
      }
      return {
        passed: violations.length === 0,
        details: violations.length > 0 ? `Anti-patterns found: ${violations.join(', ')}` : 'No anti-patterns detected',
      };
    },
  },

  section_presence: {
    description: 'Output must include specified sections',
    validate(requiredSections, output) {
      const missing = [];
      for (const section of requiredSections) {
        const patterns = Array.isArray(section.patterns) ? section.patterns : [`## ${section}`, `### ${section}`, section];
        const found = patterns.some(p => output.includes(p));
        if (!found) missing.push(section.label || section);
      }
      return {
        passed: missing.length === 0,
        details: missing.length > 0 ? `Missing sections: ${missing.join(', ')}` : 'All required sections present',
      };
    },
  },

  negative_constraint: {
    description: 'Output must NOT contain prohibited content based on Do NOT rules',
    validate(constraints, output) {
      const violations = [];
      for (const c of constraints) {
        const patterns = Array.isArray(c.patterns) ? c.patterns : [c.toLowerCase()];
        for (const p of patterns) {
          if (output.toLowerCase().includes(p.toLowerCase())) {
            violations.push(c.label || c);
            break;
          }
        }
      }
      return {
        passed: violations.length === 0,
        details: violations.length > 0 ? `Prohibited content found: ${violations.join(', ')}` : 'No prohibited content',
      };
    },
  },

  token_budget: {
    description: 'Output must not exceed declared token budget',
    validate(budget, output) {
      const budgetTokens = typeof budget === 'number' ? budget : 2000;
      // Rough token estimation: ~1.3 tokens per word
      const wordCount = output.split(/\s+/).length;
      const estimatedTokens = Math.ceil(wordCount * 1.3);

      return {
        passed: estimatedTokens <= budgetTokens * 1.5, // 50% grace margin
        details: `Estimated ${estimatedTokens} tokens (budget: ${budgetTokens}, margin: +50%)`,
        tokens: estimatedTokens,
        budget: budgetTokens,
      };
    },
  },
};

// ---------------------------------------------------------------------------
// Load test cases
// ---------------------------------------------------------------------------
function loadBehavioralScenarios() {
  const scenarios = [];

  if (!fs.existsSync(BEHAVIORAL_DIR)) {
    console.warn(`WARNING: ${BEHAVIORAL_DIR} not found`);
    return scenarios;
  }

  const files = fs.readdirSync(BEHAVIORAL_DIR).filter(f => f.endsWith('.json'));

  for (const file of files) {
    const data = JSON.parse(fs.readFileSync(path.join(BEHAVIORAL_DIR, file), 'utf-8'));
    for (const suite of data.suites || []) {
      if (targetSuite && suite.id !== targetSuite) continue;
      for (const sc of suite.scenarios || []) {
        scenarios.push({
          file,
          suiteId: suite.id,
          scenarioId: sc.id,
          type: sc.type,
          skill: sc.skill,
          input: sc.input,
          expected_behavior: sc.expected_behavior,
          validation: sc.validation,
          output: sc.recorded_output || null,
          weight: sc.weight || 1.0,
        });
      }
    }
  }

  return scenarios;
}

// ---------------------------------------------------------------------------
// Run validation
// ---------------------------------------------------------------------------
function runScenario(scenario) {
  if (!scenario.output) {
    return {
      ...scenario,
      status: 'skipped',
      reason: 'No recorded output — run agent with this scenario to generate output',
      score: 0,
    };
  }

  // If manually marked as passed/failed in the JSON
  if (scenario.validation && scenario.validation.manual_result) {
    return {
      ...scenario,
      status: scenario.validation.manual_result,
      reason: scenario.validation.manual_note || 'Manual validation',
      score: scenario.validation.manual_result === 'pass' ? 1 : 0,
    };
  }

  // Auto-validate based on type
  const validator = SCENARIO_TYPES[scenario.type];
  if (!validator) {
    return {
      ...scenario,
      status: 'unknown',
      reason: `Unknown scenario type: ${scenario.type}`,
      score: 0,
    };
  }

  const result = validator.validate(scenario.validation, scenario.output);
  return {
    ...scenario,
    status: result.passed ? 'pass' : 'fail',
    reason: result.details,
    score: result.passed ? 1 : 0,
    metrics: result,
  };
}

// ---------------------------------------------------------------------------
// Skill constraint extraction (used for auto-generating scenarios)
// ---------------------------------------------------------------------------
function extractSkillConstraints(skillName) {
  // Find the skill file
  const skillPath = findSkillFile(skillName);
  if (!skillPath) return null;

  const content = fs.readFileSync(skillPath, 'utf-8');

  // Extract Do NOT patterns
  const doNotPatterns = [];
  const doNotRegex = /Do NOT use for\s+(.+?)(?:\.|$)/gm;
  let match;
  while ((match = doNotRegex.exec(content)) !== null) {
    doNotPatterns.push(match[1].trim());
  }

  // Extract anti-patterns
  const antiPatterns = [];
  const apSection = content.match(/^## Anti-Patterns?\n([\s\S]*?)(?=^## |\Z)/m);
  if (apSection) {
    const items = apSection[1].match(/^[-*]\s+(.+)$/gm);
    if (items) {
      for (const item of items) {
        antiPatterns.push(item.replace(/^[-*]\s+/, '').trim());
      }
    }
  }

  // Extract checklist items
  const checklist = [];
  const clSection = content.match(/^## (Production Checklist|Verification|Checklist)\n([\s\S]*?)(?=^## |\Z)/m);
  if (clSection) {
    const items = clSection[2].match(/^[-*]\s+(.+)$/gm);
    if (items) {
      for (const item of items) {
        checklist.push(item.replace(/^[-*]\s+/, '').trim());
      }
    }
  }

  // Extract token budget
  const tbMatch = content.match(/^token_budget:\s*(\d+)/m);
  const tokenBudget = tbMatch ? parseInt(tbMatch[1], 10) : null;

  return { doNotPatterns, antiPatterns, checklist, tokenBudget };
}

function findSkillFile(name) {
  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const e of entries) {
      if (e.isDirectory()) {
        const subdir = path.join(dir, e.name);
        if (fs.existsSync(path.join(subdir, 'SKILL.md'))) {
          // Check if this is the skill we want
          const content = fs.readFileSync(path.join(subdir, 'SKILL.md'), 'utf-8');
          const nmMatch = content.match(/^name:\s*(.+)$/m);
          if (nmMatch && nmMatch[1].trim() === name) return path.join(subdir, 'SKILL.md');
        }
        const result = walk(subdir);
        if (result) return result;
      }
    }
    return null;
  }
  return walk(SKILLS_DIR);
}

// ---------------------------------------------------------------------------
// Generate scenarios report
// ---------------------------------------------------------------------------
function generateCoverageReport(scenarios) {
  const skillsWithScenarios = new Set();
  const scenariosByType = new Map();

  for (const sc of scenarios) {
    if (sc.skill) skillsWithScenarios.add(sc.skill);
    if (!scenariosByType.has(sc.type)) scenariosByType.set(sc.type, 0);
    scenariosByType.set(sc.type, scenariosByType.get(sc.type) + 1);
  }

  // Count all skills
  let totalSkills = 0;
  function countSkills(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const e of entries) {
      if (e.isDirectory()) {
        if (fs.existsSync(path.join(dir, e.name, 'SKILL.md'))) {
          totalSkills++;
        }
        countSkills(path.join(dir, e.name));
      }
    }
  }
  countSkills(SKILLS_DIR);

  return {
    totalSkills,
    skillsWithScenarios: skillsWithScenarios.size,
    coveragePercent: Math.round((skillsWithScenarios.size / totalSkills) * 100),
    scenariosByType: Object.fromEntries(scenariosByType),
  };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
console.log('=== Behavioral Eval Runner (Tier 3) ===\n');

const scenarios = loadBehavioralScenarios();
console.log(`Loaded ${scenarios.length} behavioral scenarios from ${BEHAVIORAL_DIR}\n`);

const coverage = generateCoverageReport(scenarios);

const results = scenarios.map(runScenario);
const passed = results.filter(r => r.status === 'pass');
const failed = results.filter(r => r.status === 'fail');
const skipped = results.filter(r => r.status === 'skipped');

const totalWeight = results.reduce((s, r) => s + (r.weight || 1), 0);
const passRate = totalWeight > 0
  ? results.reduce((s, r) => s + (r.score || 0) * (r.weight || 1), 0) / totalWeight
  : 0;

if (jsonOutput) {
  console.log(JSON.stringify({
    summary: {
      total: results.length,
      passed: passed.length,
      failed: failed.length,
      skipped: skipped.length,
      pass_rate: Math.round(passRate * 1000) / 1000,
      coverage,
    },
    results: results.map(r => ({
      suite: r.suiteId,
      scenario: r.scenarioId,
      type: r.type,
      skill: r.skill,
      status: r.status,
      reason: r.reason,
      weight: r.weight,
    })),
  }, null, 2));
} else {
  console.log('--- Behavioral Test Results ---');
  for (const r of results) {
    const icon = r.status === 'pass' ? '✅' : r.status === 'skip' ? '⬜' : '❌';
    console.log(`${icon} [${r.suiteId}/${r.scenarioId}] ${r.type} — ${r.skill || 'multi'}`);
    if (r.reason) console.log(`   ${r.reason}`);
  }

  console.log('\n--- Coverage ---');
  console.log(`Skills covered: ${coverage.skillsWithScenarios}/${coverage.totalSkills} (${coverage.coveragePercent}%)`);
  console.log(`Scenario types: ${Object.entries(coverage.scenariosByType).map(([k, v]) => `${k}:${v}`).join(', ')}`);

  console.log('\n--- Summary ---');
  console.log(`Total: ${results.length} | Passed: ${passed.length} | Failed: ${failed.length} | Skipped: ${skipped.length}`);
  console.log(`Pass rate: ${(passRate * 100).toFixed(1)}%`);
  console.log(`Result: ${passRate >= 0.80 ? 'PASS' : 'FAIL'}`);
}

if (skipped.length > 0 && !jsonOutput) {
  console.log(`\n⚠️  ${skipped.length} scenarios skipped — run agent with these scenarios and record output into tier3-behavioral/*.json`);
}

process.exit(failed.length === 0 ? 0 : 1);
