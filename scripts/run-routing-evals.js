#!/usr/bin/env node
/**
 * TF-IDF Routing Evaluator (Tier 2)
 * Builds a TF-IDF index from all skill descriptions and tests routing precision
 * against realistic user prompts. Measures rank-1 hit rate, MRR, description
 * collisions, and false-positive routing.
 *
 * Usage: node scripts/run-routing-evals.js [--suite id] [--json] [--threshold 0.1]
 * Exit: 0 if rank-1 hit rate >= 80%, 1 otherwise
 *
 * Inspired by addyosmani/agent-skills TF-IDF routing evals.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------
const SKILLS_DIR = path.join(__dirname, '..', 'skills');
const EVALS_DIR = path.join(__dirname, '..', 'evals');
const TIER2_FILE = path.join(EVALS_DIR, 'tier2-routing-evals.json');
const TARGET_RANK1_RATE = 0.80; // 80% rank-1 hit rate target
const TARGET_MRR = 0.90;        // 90% MRR target

// ---------------------------------------------------------------------------
// CLI args
// ---------------------------------------------------------------------------
const args = process.argv.slice(2);
const targetSuite = (() => {
  const idx = args.indexOf('--suite');
  return idx >= 0 ? args[idx + 1] : null;
})();
const jsonOutput = args.includes('--json');
const threshold = (() => {
  const idx = args.indexOf('--threshold');
  return idx >= 0 ? parseFloat(args[idx + 1]) : 0.15;
})();

// ---------------------------------------------------------------------------
// 1. Collect all skills and their descriptions
// ---------------------------------------------------------------------------
// Parse a multi-line YAML value that starts after a key like "description: >"
// Returns the folded string content (indented continuation lines unwrapped)
function parseYamlMultiline(fm, key) {
  const lines = fm.split('\n');
  let inValue = false;
  let result = '';
  let baseIndent = null;

  for (const line of lines) {
    if (inValue) {
      // Check if we've hit another top-level key (no indent) or end
      if (/^[a-zA-Z]/.test(line) && !line.startsWith(' ') && !line.startsWith('\t')) {
        break;
      }
      // Skip empty lines, collect indented content
      const trimmed = line.trim();
      if (trimmed) {
        result += (result ? ' ' : '') + trimmed;
      }
    } else {
      // Match "key: >" or "key: >-" or "key: value" patterns
      const re = new RegExp('^' + key + ':\\s*(.+)$');
      const m = line.match(re);
      if (m) {
        const val = m[1].trim();
        if (val === '>' || val === '>-' || val === '|' || val === '|-') {
          inValue = true;
        } else if (val) {
          // Single-line value
          return val;
        }
      }
    }
  }
  return result.trim();
}

function collectSkills(dir) {
  const skills = [];

  // Walk ALL subdirectories recursively to find SKILL.md files
  function walk(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const subdir = path.join(currentDir, entry.name);
      const skillPath = path.join(subdir, 'SKILL.md');

      if (fs.existsSync(skillPath)) {
        const content = fs.readFileSync(skillPath, 'utf-8');
        const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
        if (fmMatch) {
          const fm = fmMatch[1];
          const nameMatch = fm.match(/^name:\s*(.+)$/m);
          const desc = parseYamlMultiline(fm, 'description');

          const name = nameMatch ? nameMatch[1].trim() : entry.name;
          const tagsMatch = fm.match(/^tags:\s*\n((?:\s*-\s*.+\n?)*)/m);
          let tags = [];
          if (tagsMatch) {
            tags = tagsMatch[1].split('\n')
              .filter(l => l.trim().startsWith('-'))
              .map(l => l.replace(/^\s*-\s*/, '').trim());
          }

          if (desc) {
            skills.push({ name, desc, tags, domain: path.relative(SKILLS_DIR, subdir) });
          }
        }
      }

      // Recurse
      walk(subdir);
    }
  }

  walk(dir);
  return skills;
}

// ---------------------------------------------------------------------------
// 2. TF-IDF computation
// ---------------------------------------------------------------------------
function tokenize(text) {
  return text.toLowerCase()
    .replace(/[^a-z0-9\s-]/g, ' ')
    .split(/[\s-]+/)
    .filter(w => w.length > 1)
    .filter(w => !STOP_WORDS.has(w));
}

const STOP_WORDS = new Set([
  'the', 'and', 'for', 'not', 'use', 'when', 'with', 'that', 'this', 'are',
  'from', 'can', 'has', 'was', 'all', 'but', 'its', 'may', 'than', 'into',
  'also', 'does', 'some', 'each', 'over', 'such', 'will', 'just', 'only',
  'been', 'more', 'new', 'any', 'very', 'our', 'about', 'should', 'used',
  'which', 'other', 'being', 'using', 'don', 'because', 'there', 'their',
]);

function computeTF(docTokens) {
  const tf = new Map();
  for (const t of docTokens) tf.set(t, (tf.get(t) || 0) + 1);
  const maxFreq = Math.max(...tf.values());
  for (const [t, v] of tf) tf.set(t, 0.5 + 0.5 * (v / maxFreq)); // augmented TF
  return tf;
}

function computeIDF(docs, totalDocs) {
  const idf = new Map();
  for (const doc of docs) {
    const seen = new Set();
    for (const t of doc) {
      if (!seen.has(t)) {
        idf.set(t, (idf.get(t) || 0) + 1);
        seen.add(t);
      }
    }
  }
  for (const [t, v] of idf) {
    idf.set(t, Math.log(1 + totalDocs / v));
  }
  return idf;
}

// ---------------------------------------------------------------------------
// 3. Build the routing index
// ---------------------------------------------------------------------------
function buildIndex(skills) {
  const docs = skills.map(s => tokenize(s.desc + ' ' + (s.tags || []).join(' ')));
  const idf = computeIDF(docs, skills.length);

  const vectors = docs.map((tokens, i) => {
    const tf = computeTF(tokens);
    const vec = new Map();
    for (const [t, tfVal] of tf) {
      vec.set(t, tfVal * (idf.get(t) || 0));
    }
    return { name: skills[i].name, vector: vec, doc: tokens };
  });

  return { vectors, idf, skills };
}

function cosineSimilarity(queryVec, docVec) {
  let dot = 0, queryMag = 0, docMag = 0;

  for (const [t, qVal] of queryVec) {
    queryMag += qVal * qVal;
    dot += qVal * (docVec.get(t) || 0);
  }

  for (const [, val] of docVec) {
    docMag += val * val;
  }

  if (queryMag === 0 || docMag === 0) return 0;
  return dot / (Math.sqrt(queryMag) * Math.sqrt(docMag));
}

function route(index, prompt) {
  const queryTokens = tokenize(prompt);
  // Build IDF-weighted query vector (same weighting as doc vectors)
  const queryTf = computeTF(queryTokens);
  const queryVec = new Map();
  for (const [t, tfVal] of queryTf) {
    queryVec.set(t, tfVal * (index.idf.get(t) || 0));
  }

  const scored = index.vectors.map(v => ({
    name: v.name,
    score: cosineSimilarity(queryVec, v.vector),
  }));
  scored.sort((a, b) => b.score - a.score);
  return scored;
}

// ---------------------------------------------------------------------------
// 4. Load test cases
// ---------------------------------------------------------------------------
function loadTestCases() {
  if (!fs.existsSync(TIER2_FILE)) {
    console.warn(`WARNING: ${TIER2_FILE} not found. Using built-in test cases.`);
    return DEFAULT_TEST_CASES;
  }

  const data = JSON.parse(fs.readFileSync(TIER2_FILE, 'utf-8'));
  const cases = [];

  for (const suite of data.suites) {
    if (targetSuite && suite.id !== targetSuite) continue;
    for (const sc of suite.scenarios) {
      cases.push({
        suiteId: suite.id,
        scenarioId: sc.id,
        prompt: sc.input,
        expected: sc.expected,    // expected skill name
        mustNotRoute: sc.must_not_route || [],
        allowTopN: sc.allow_top_n || 1,
        weight: sc.weight || 1.0,
      });
    }
  }

  return cases;
}

// Default test cases if no tier2-routing-evals.json exists
const DEFAULT_TEST_CASES = [
  { suiteId: 'routing-precision', scenarioId: 'default-1', prompt: 'Build me a REST API with authentication', expected: 'backend-developer', mustNotRoute: [], allowTopN: 3, weight: 1.0 },
  { suiteId: 'routing-precision', scenarioId: 'default-2', prompt: 'Design a database schema for an e-commerce platform', expected: 'database-designer', mustNotRoute: [], allowTopN: 3, weight: 1.0 },
  { suiteId: 'routing-precision', scenarioId: 'default-3', prompt: 'Review my pull request for bugs and security issues', expected: 'code-reviewer', mustNotRoute: [], allowTopN: 3, weight: 1.0 },
];

// ---------------------------------------------------------------------------
// 5. Run evaluations
// ---------------------------------------------------------------------------
function runEval(index, testCase) {
  const results = route(index, testCase.prompt);
  const topN = testCase.allowTopN || 1;

  // Rank-1 hit
  const rank1Hit = results.length > 0 && results[0].name === testCase.expected;

  // Top-N hit
  const topNNames = results.slice(0, topN).map(r => r.name);
  const topNHit = topNNames.includes(testCase.expected);

  // MRR (Mean Reciprocal Rank)
  const expectedRank = results.findIndex(r => r.name === testCase.expected);
  const rr = expectedRank >= 0 ? 1 / (expectedRank + 1) : 0;

  // Must-not-route check
  let mustNotViolation = null;
  if (testCase.mustNotRoute && testCase.mustNotRoute.length > 0) {
    for (const banned of testCase.mustNotRoute) {
      const bannedIdx = topNNames.indexOf(banned);
      if (bannedIdx >= 0 && bannedIdx < topN) {
        mustNotViolation = `${banned} in top-${topN} at position ${bannedIdx + 1}`;
      }
    }
  }

  return {
    ...testCase,
    results: results.slice(0, 5),
    rank1Hit,
    topNHit,
    rr,
    mustNotViolation,
  };
}

// ---------------------------------------------------------------------------
// 6. Collision detection
// ---------------------------------------------------------------------------
function detectCollisions(skills, threshold) {
  const collisions = [];
  const descs = skills.map(s => ({ name: s.name, tokens: new Set(tokenize(s.desc)) }));

  for (let i = 0; i < descs.length; i++) {
    for (let j = i + 1; j < descs.length; j++) {
      const setA = descs[i].tokens;
      const setB = descs[j].tokens;

      const intersection = new Set([...setA].filter(x => setB.has(x)));
      const union = new Set([...setA, ...setB]);
      const jaccard = intersection.size / union.size;

      if (jaccard > threshold) {
        collisions.push({
          skillA: descs[i].name,
          skillB: descs[j].name,
          jaccard: Math.round(jaccard * 1000) / 1000,
          shared: [...intersection].sort().slice(0, 10),
        });
      }
    }
  }

  collisions.sort((a, b) => b.jaccard - a.jaccard);
  return collisions;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
console.log('=== TF-IDF Routing Evaluator (Tier 2) ===\n');

// Collect skills
const skills = collectSkills(SKILLS_DIR);
console.log(`Collected ${skills.length} skills with descriptions`);

// Build index
const index = buildIndex(skills);
console.log(`Built TF-IDF index with ${index.vectors.length} vectors\n`);

// Load test cases
const testCases = loadTestCases();
console.log(`Loaded ${testCases.length} test cases from ${targetSuite ? targetSuite : 'all suites'}\n`);

// Run evals
const evalResults = testCases.map(tc => runEval(index, tc));

// Compute metrics
const totalWeight = evalResults.reduce((s, r) => s + (r.weight || 1), 0);
const rank1Hits = evalResults.filter(r => r.rank1Hit);
const rank1Rate = rank1Hits.reduce((s, r) => s + (r.weight || 1), 0) / totalWeight;
const mrr = evalResults.reduce((s, r) => s + r.rr * (r.weight || 1), 0) / totalWeight;
const mustNotViolations = evalResults.filter(r => r.mustNotViolation);

// Detect collisions
const collisions = detectCollisions(skills, threshold);

// ---------------------------------------------------------------------------
// Output
// ---------------------------------------------------------------------------
if (jsonOutput) {
  const output = {
    summary: {
      total_cases: evalResults.length,
      rank1_hits: rank1Hits.length,
      rank1_rate: Math.round(rank1Rate * 1000) / 1000,
      mrr: Math.round(mrr * 1000) / 1000,
      must_not_violations: mustNotViolations.length,
      description_collisions: collisions.length,
      skills_indexed: skills.length,
    },
    failures: evalResults.filter(r => !r.rank1Hit).map(r => ({
      suite: r.suiteId,
      scenario: r.scenarioId,
      prompt: r.prompt,
      expected: r.expected,
      top_result: r.results[0]?.name || 'none',
      top_score: r.results[0]?.score || 0,
      rank: r.results.findIndex(x => x.name === r.expected) + 1 || 'not found',
    })),
    collisions: collisions.slice(0, 20),
  };
  console.log(JSON.stringify(output, null, 2));
} else {
  // Text report
  console.log('--- Routing Test Results ---');
  for (const r of evalResults) {
    const icon = r.rank1Hit ? '✅' : '❌';
    const topSkill = r.results[0]?.name || 'none';
    console.log(`${icon} [${r.suiteId}/${r.scenarioId}] "${r.prompt}"`);
    if (!r.rank1Hit) {
      console.log(`   Expected: ${r.expected} | Got: ${topSkill} (rank-${r.results.findIndex(x => x.name === r.expected) + 1 || 'N/A'})`);
      console.log(`   Top-3: ${r.results.slice(0, 3).map(x => `${x.name}(${x.score.toFixed(3)})`).join(', ')}`);
    }
    if (r.mustNotViolation) {
      console.log(`   ⚠️  Must-not-route violation: ${r.mustNotViolation}`);
    }
  }

  // Collision report
  if (collisions.length > 0) {
    console.log(`\n--- Description Collisions (Jaccard > ${threshold}) ---`);
    for (const c of collisions.slice(0, 15)) {
      console.log(`  ${c.skillA} ↔ ${c.skillB}: Jaccard=${c.jaccard} shared=[${c.shared.join(', ')}]`);
    }
    if (collisions.length > 15) {
      console.log(`  ... and ${collisions.length - 15} more collisions`);
    }
  }

  // Summary
  console.log('\n--- Summary ---');
  console.log(`Skills indexed:        ${skills.length}`);
  console.log(`Test cases:            ${evalResults.length}`);
  console.log(`Rank-1 hit rate:       ${(rank1Rate * 100).toFixed(1)}% (target: ${TARGET_RANK1_RATE * 100}%)`);
  console.log(`MRR:                   ${(mrr * 100).toFixed(1)}% (target: ${TARGET_MRR * 100}%)`);
  console.log(`Must-not-route fails:  ${mustNotViolations.length}`);
  console.log(`Description collisions: ${collisions.length}`);
  console.log(`Result: ${rank1Rate >= TARGET_RANK1_RATE ? 'PASS' : 'FAIL'}`);
}

// Exit code
const exitOk = rank1Rate >= TARGET_RANK1_RATE && mustNotViolations.length === 0;
process.exit(exitOk ? 0 : 1);
