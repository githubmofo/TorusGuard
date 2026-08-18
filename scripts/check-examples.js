#!/usr/bin/env node
/**
 * Checks that example apps contain expected TorusGuard demo markers.
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const VULN_DIR = path.join(ROOT, 'examples', 'vulnerable-express-react-app');

const VULN_MARKERS = [
  'TORUSGUARD-DEMO',
  'super-secret-jwt-key',
  "origin: '*'",
  'stack: err.stack',
];

let errors = [];

function readFilesRecursive(dir, extensions = ['.js', '.jsx', '.ts', '.tsx']) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory() && entry.name !== 'node_modules') {
      results.push(...readFilesRecursive(full, extensions));
    } else if (extensions.some((ext) => entry.name.endsWith(ext))) {
      results.push(full);
    }
  }
  return results;
}

const vulnFiles = readFilesRecursive(VULN_DIR);
const allVulnContent = vulnFiles.map((f) => fs.readFileSync(f, 'utf8')).join('\n');

for (const marker of VULN_MARKERS) {
  if (!allVulnContent.includes(marker)) {
    errors.push(`Vulnerable example missing marker: ${marker}`);
  }
}

// Hardened example should NOT contain TORUSGUARD-DEMO markers
const HARD_DIR = path.join(ROOT, 'examples', 'hardened-express-react-app');
const hardFiles = readFilesRecursive(HARD_DIR);
const allHardContent = hardFiles.map((f) => fs.readFileSync(f, 'utf8')).join('\n');

if (allHardContent.includes('TORUSGUARD-DEMO')) {
  errors.push('Hardened example should not contain TORUSGUARD-DEMO markers');
}

// Hardened should use env-based secret
if (!allHardContent.includes('process.env.JWT_SECRET')) {
  errors.push('Hardened example should load JWT_SECRET from environment');
}

console.log('TorusGuard Example Check\n');

if (errors.length) {
  errors.forEach((e) => console.log(`  ✗ ${e}`));
  console.log(`\nExample check FAILED (${errors.length} error(s))`);
  process.exit(1);
}

console.log('✓ Example checks passed');
