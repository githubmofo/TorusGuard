#!/usr/bin/env node

/**
 * TorusGuard CLI Runner (NPM Distribution)
 * Provides zero-dependency command orchestration for TorusGuard governance.
 * Adheres to Ponytail principles: concise, surgical, zero fluff.
 */

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
const command = args[0] || 'init';
const rootDir = path.resolve(__dirname, '..');
const cwd = process.cwd();

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

function printHelp() {
  console.log(`
================================================================================
TORUSGUARD NPM PACKAGE — CLI COMMANDS (v0.9.2)
================================================================================
Usage:
  npx torusguard [command] [options]

Commands:
  init          Scaffold .torusguard/ and register all 11 individual slash commands
  audit         Run security audit against target workspace
  status        Display active security posture and configuration
  report        Export SARIF security report
  help          Display this help message

Options:
  --force       Overwrite existing configuration and re-scaffold templates
  --target <d>  Target project directory (default: current working directory)
================================================================================
`);
}

if (command === 'help' || command === '--help' || command === '-h') {
  printHelp();
  process.exit(0);
}

if (command === 'status') {
  const cfgPath = path.join(cwd, '.torusguard', 'config', 'torusguard.json');
  if (fs.existsSync(cfgPath)) {
    try {
      const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf-8'));
      console.log('================================================================================');
      console.log('TORUSGUARD ACTIVE POSTURE STATUS');
      console.log('================================================================================');
      console.log(`Version:            ${cfg.version || '0.9.2'}`);
      console.log(`Product:            ${cfg.product || 'TorusGuard'}`);
      console.log(`Severity Threshold: ${cfg.severity_threshold || 'medium'}`);
      console.log(`Runs Directory:     ${cfg.runs_dir || '.torusguard/runs'}`);
      console.log(`Detected Language:  ${cfg.detected_stack?.language || 'auto'}`);
      console.log(`Detected Framework: ${cfg.detected_stack?.framework || 'auto'}`);
      console.log('================================================================================');
      process.exit(0);
    } catch (e) {
      // Fallback to python runner
    }
  } else {
    console.log('[INFO] .torusguard workspace not found in current directory.');
    console.log('Run "npx torusguard init" to scaffold the workspace.');
    process.exit(0);
  }
}

// Locate bootstrap / runner scripts
const localBootstrap = path.join(rootDir, 'skills', 'torusguard', 'bootstrap.py');
const localInstall = path.join(rootDir, 'install.py');
const scriptToRun = fs.existsSync(localBootstrap) ? localBootstrap : localInstall;

// Pass flags: when init is executed, include --full-commands to unlock all slash commands
let scriptArgs = [scriptToRun];
if (command === 'init') {
  scriptArgs.push('--full-commands');
  // Forward remaining arguments
  scriptArgs.push(...args.slice(1));
} else {
  scriptArgs.push(...args);
}

const proc = spawnSync(pythonCmd, scriptArgs, {
  stdio: 'inherit',
  cwd: cwd,
});

process.exit(proc.status !== null ? proc.status : 0);
