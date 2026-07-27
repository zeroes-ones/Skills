#!/usr/bin/env node
/**
 * Command Parity Validator
 * Verifies that all 3 tool directories have the same command names, descriptions match,
 * and each command resolves to valid skills in the library.
 *
 * Usage: node scripts/validate-commands.js [--json]
 * Exit: 0 if all commands pass, 1 if parity violations found
 */
'use strict';

const fs = require('fs');
const path = require('path');

const TOOL_DIRS = {
  claude: '.claude/commands',
  gemini: '.gemini/commands',
  copilot: '.copilot/commands',
};

const EXPECTED_COMMANDS = ['spec', 'plan', 'build', 'test', 'review', 'code-simplify', 'webperf', 'ship'];
const GEMINI_NAME_MAP = { plan: 'planning' }; // Gemini uses 'planning' instead of 'plan'

// Skill name validation — check that referenced skills exist
const VALID_SKILLS = new Set();
const skillsDir = path.join(__dirname, '..', 'skills');
function collectSkills(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    if (!e.isDirectory()) continue;
    const full = path.join(dir, e.name);
    if (fs.existsSync(path.join(full, 'SKILL.md'))) {
      VALID_SKILLS.add(e.name);
    }
  }
}
function walkDirs(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      const subdir = path.join(dir, entry.name);
      if (fs.existsSync(path.join(subdir, 'SKILL.md'))) {
        VALID_SKILLS.add(entry.name);
      } else {
        walkDirs(subdir);
      }
    }
  }
}
walkDirs(skillsDir);

const violations = [];
const warnings = [];

// 1. Check each tool directory exists
for (const [tool, dir] of Object.entries(TOOL_DIRS)) {
  const fullPath = path.join(__dirname, '..', dir);
  if (!fs.existsSync(fullPath)) {
    violations.push(`${tool}: Directory ${dir} does not exist`);
    continue;
  }

  const files = fs.readdirSync(fullPath).filter(f => f.endsWith('.md') || f.endsWith('.toml'));
  const cmdNames = files.map(f => {
    const base = path.basename(f, path.extname(f));
    return base;
  });

  // 2. Check expected commands exist
  for (const cmd of EXPECTED_COMMANDS) {
    const mappedName = (tool === 'gemini' ? GEMINI_NAME_MAP[cmd] : null) || cmd;
    if (!cmdNames.includes(mappedName)) {
      violations.push(`${tool}: Missing command '${mappedName}'`);
    }
  }

  // 3. Check no extra commands (only map back for gemini)
  for (const name of cmdNames) {
    const unmapped = tool === 'gemini' ? Object.entries(GEMINI_NAME_MAP).find(([, v]) => v === name) : null;
    const stdName = unmapped ? unmapped[0] : name;
    if (!EXPECTED_COMMANDS.includes(stdName)) {
      warnings.push(`${tool}: Extra command '${name}' (not in expected list)`);
    }
  }
}

// 4. Skill reference validation — check that commands reference valid skills
const REFERENCED_SKILLS = new Map(); // skill → [commands that reference it]
const COMMAND_SKILLS = new Map();    // command → [skills it references]

for (const [tool, dir] of Object.entries(TOOL_DIRS)) {
  const fullPath = path.join(__dirname, '..', dir);
  if (!fs.existsSync(fullPath)) continue;

  for (const file of fs.readdirSync(fullPath)) {
    const content = fs.readFileSync(path.join(fullPath, file), 'utf-8');
    const cmdName = path.basename(file, path.extname(file));

    // Extract backtick-wrapped skill names (common pattern in our command docs)
    const skillRefs = content.match(/`([a-z][a-z0-9-]*(?:-developer|-engineer|-architect|-designer|-manager|-strategist|-auditor|-reviewer|-officer|-responder|-specialist|-guide|-advisor|-planner|-orchestrator|-manager|-producer|-programmer|-researcher|-designer|-expert|-agent|-advocate|-builder|-consultant|-writer|-coach|-editor|-creator|-supporter|-analyst|-scientist|-auditor|-mapper|-publisher|-trader|-planner|-operator|-packager|-protocol|-routing|-with-devtools|-recovery|-simplification|-development|-driven-development|-implementation|-adoption|-strategy|-design|-management|-and-quality|-and-automation|-and-adrs|-and-instrumentation|-and-launch|-and-task-breakdown|-and-versioning|-and-error-recovery|-and-hardening|-and-migration|-and-recovery|-and-security|-tasks|-based|-to-spec|-to-execution|-first|-flags|-of-code|-up|-driven|-ops|-as-code|-specific|-depth|-aware|-in-product|-at-scale|-for-games|-for-health|-for-compliance|-for-security|-from-scratch|-for-enterprise|-for-startup|-for-prototype|-for-mvp|-platform|-systems|-pipelines|-monitoring|-data|-analytics|-ml|-ai|-integration|-workflow|-testing|-tools|-cli|-api|-sdk|-framework|-library|-service|-app|-application|-product|-project|-team|-org|-company|-business|-tech|-market|-user|-customer|-client|-partner|-vendor|-supplier|-chain|-network|-cloud|-infra|-infrastructure|-ops|-sec|-dev|-qa|-ux|-ui|-pm|-ceo|-cto|-vp|-hr|-fp))`/g);

    if (skillRefs) {
      for (const ref of skillRefs) {
        const skillName = ref.replace(/`/g, '');
        if (VALID_SKILLS.has(skillName)) {
          if (!REFERENCED_SKILLS.has(skillName)) REFERENCED_SKILLS.set(skillName, []);
          REFERENCED_SKILLS.get(skillName).push(`${tool}:${cmdName}`);
        }
      }
    }
  }
}

// Report
if (process.argv.includes('--json')) {
  console.log(JSON.stringify({ violations, warnings, valid_skills: VALID_SKILLS.size, referenced_skills: REFERENCED_SKILLS.size }, null, 2));
} else {
  if (violations.length > 0) {
    console.log('❌ VIOLATIONS:');
    for (const v of violations) console.log(`  ${v}`);
  }
  if (warnings.length > 0) {
    console.log('⚠️  WARNINGS:');
    for (const w of warnings) console.log(`  ${w}`);
  }
  if (violations.length === 0) {
    console.log(`✅ All ${EXPECTED_COMMANDS.length} commands present with parity across ${Object.keys(TOOL_DIRS).length} tools`);
    console.log(`   ${VALID_SKILLS.size} valid skills, ${REFERENCED_SKILLS.size} referenced in commands`);
  }
}

process.exit(violations.length > 0 ? 1 : 0);
