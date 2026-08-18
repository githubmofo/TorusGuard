#!/usr/bin/env node
/**
 * Validates TorusGuard skill structure and required files.
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const SKILL_DIR = path.join(ROOT, 'skills', 'torusguard');
const SKILL_FILE = path.join(SKILL_DIR, 'SKILL.md');

const REQUIRED_REFERENCES = [
  'secrets-and-config.md',
  'frontend-no-db.md',
  'input-and-injection.md',
  'auth-and-sessions.md',
  'rate-limit-and-abuse.md',
  'client-code-exposure.md',
  'platform-hardening.md',
];

const REQUIRED_ROOT_FILES = [
  'README.md',
  'LICENSE',
  'CONTRIBUTING.md',
  'SECURITY.md',
  'CHANGELOG.md',
  'package.json',
];

let errors = [];
let warnings = [];

function checkFileExists(filePath, label) {
  if (!fs.existsSync(filePath)) {
    errors.push(`Missing ${label}: ${path.relative(ROOT, filePath)}`);
    return false;
  }
  return true;
}

// Root files
for (const file of REQUIRED_ROOT_FILES) {
  checkFileExists(path.join(ROOT, file), 'root file');
}

// SKILL.md
if (checkFileExists(SKILL_FILE, 'skill file')) {
  const content = fs.readFileSync(SKILL_FILE, 'utf8');

  if (!content.startsWith('---')) {
    errors.push('SKILL.md missing YAML frontmatter');
  } else {
    const frontmatter = content.split('---')[1];
    if (!frontmatter.includes('name: torusguard')) {
      errors.push('SKILL.md frontmatter missing name: torusguard');
    }
    if (!frontmatter.includes('description:')) {
      errors.push('SKILL.md frontmatter missing description');
    }
  }

  const lineCount = content.split('\n').length;
  if (lineCount > 500) {
    warnings.push(`SKILL.md is ${lineCount} lines (recommended max: 500)`);
  }

  const requiredSections = [
    'Hard Bans',
    'Pre-Flight Release Gate',
    '/torusguard init',
    '/torusguard audit',
    '/torusguard harden',
  ];
  for (const section of requiredSections) {
    if (!content.includes(section)) {
      errors.push(`SKILL.md missing section: ${section}`);
    }
  }
}

// Reference modules
const refsDir = path.join(SKILL_DIR, 'references');
for (const ref of REQUIRED_REFERENCES) {
  const refPath = path.join(refsDir, ref);
  if (checkFileExists(refPath, 'reference module')) {
    const refContent = fs.readFileSync(refPath, 'utf8');
    const requiredRefSections = ['Hard Bans', 'Verification Checklist'];
    for (const section of requiredRefSections) {
      if (!refContent.includes(section)) {
        warnings.push(`${ref} missing section: ${section}`);
      }
    }

    // Verify SKILL.md links to this reference
    const skillContent = fs.readFileSync(SKILL_FILE, 'utf8');
    if (!skillContent.includes(ref)) {
      errors.push(`SKILL.md does not link to ${ref}`);
    }
  }
}

// Examples
const examples = [
  'examples/vulnerable-express-react-app',
  'examples/hardened-express-react-app',
];
for (const example of examples) {
  checkFileExists(path.join(ROOT, example, 'package.json'), 'example package.json');
  checkFileExists(path.join(ROOT, example, 'README.md'), 'example README');
}

console.log('TorusGuard Skill Validation\n');

if (warnings.length) {
  console.log('Warnings:');
  warnings.forEach((w) => console.log(`  ⚠ ${w}`));
  console.log('');
}

if (errors.length) {
  console.log('Errors:');
  errors.forEach((e) => console.log(`  ✗ ${e}`));
  console.log(`\nValidation FAILED (${errors.length} error(s))`);
  process.exit(1);
}

console.log('✓ All checks passed');
if (warnings.length) {
  console.log(`  (${warnings.length} warning(s))`);
}
