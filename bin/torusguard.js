#!/usr/bin/env node

/**
 * TorusGuard CLI Entrypoint
 * Bridges npx/npm executions to the autonomous Python security engine.
 */

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
const rootDir = path.resolve(__dirname, '..');
const bootstrapPy = path.join(rootDir, 'skills', 'torusguard', 'bootstrap.py');
const installPy = path.join(rootDir, 'install.py');

// Detect available Python binary (python or python3)
let pythonCmd = 'python';
try {
  const check = spawnSync('python', ['--version'], { encoding: 'utf-8' });
  if (check.status !== 0) {
    const check3 = spawnSync('python3', ['--version'], { encoding: 'utf-8' });
    if (check3.status === 0) {
      pythonCmd = 'python3';
    }
  }
} catch (e) {
  try {
    const check3 = spawnSync('python3', ['--version'], { encoding: 'utf-8' });
    if (check3.status === 0) {
      pythonCmd = 'python3';
    }
  } catch (err) {}
}

const targetScript = fs.existsSync(bootstrapPy) ? bootstrapPy : installPy;
const proc = spawnSync(pythonCmd, [targetScript, ...args], {
  stdio: 'inherit',
  cwd: process.cwd(),
});

process.exit(proc.status !== null ? proc.status : 0);
