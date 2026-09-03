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

// ANSI Color Helpers
const BOLD = '\x1b[1m';
const RESET = '\x1b[0m';
const CYAN = '\x1b[36m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const GRAY = '\x1b[90m';
const DIM = '\x1b[2m';

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
  ${CYAN}╭──────────────────────────────────────────────────────────────────────────╮${RESET}
  ${CYAN}│${RESET}  ${BOLD}🛡️  TORUSGUARD CLI v0.9.4${RESET}                     ${GRAY}[Autonomous Security Engine]${RESET} ${CYAN}│${RESET}
  ${CYAN}│${RESET}  ${DIM}Governed Remediation & Security Guardrails for AI Web Applications${RESET}      ${CYAN}│${RESET}
  ${CYAN}╰──────────────────────────────────────────────────────────────────────────╯${RESET}

  ${BOLD}Usage:${RESET}
    ${GREEN}npx torusguard${RESET} [command] [options]

  ${BOLD}Commands:${RESET}
    ${CYAN}init${RESET}          Scaffold ${BOLD}.torusguard/${RESET} workspace and unlock all 11 slash commands
    ${CYAN}status${RESET}        Display active security posture, configured rules, and stack
    ${CYAN}audit${RESET}         Execute static security AST audit on target project
    ${CYAN}report${RESET}        Export OASIS SARIF v2.1.0 security telemetry
    ${CYAN}help${RESET}          Show this interactive command guide

  ${BOLD}Options:${RESET}
    ${GRAY}--target <dir>${RESET}  Target directory to analyze or scaffold ${DIM}(default: .)${RESET}
    ${GRAY}--force${RESET}         Overwrite existing configuration and re-scaffold templates
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
      console.log(`
  ${CYAN}╭──────────────────────────────────────────────────────────────────────────╮${RESET}
  ${CYAN}│${RESET}  ${BOLD}🛡️  TORUSGUARD ACTIVE SECURITY POSTURE${RESET}                          ${GRAY}v0.9.4${RESET} ${CYAN}│${RESET}
  ${CYAN}╰──────────────────────────────────────────────────────────────────────────╯${RESET}

  ${BOLD}▸ Workspace Location:${RESET}   ${GREEN}${cwd}${RESET}
  ${BOLD}▸ Governance Mode:${RESET}      ${GREEN}Full Local Governance (.torusguard/)${RESET}

  ${BOLD}⏺ Environment & Stack:${RESET}
    ${GRAY}⎿ Language:${RESET}          ${BOLD}${cfg.detected_stack?.language || 'TypeScript'}${RESET}
    ${GRAY}⎿ Framework:${RESET}         ${BOLD}${cfg.detected_stack?.framework || 'None (Generic Web)'}${RESET}
    ${GRAY}⎿ Data Layer:${RESET}        ${BOLD}${cfg.detected_stack?.data_layer || 'None'}${RESET}
    ${GRAY}⎿ Rules Catalog:${RESET}     ${GREEN}71 Canonical Security Rules Active${RESET}

  ${BOLD}⏺ Governance Telemetry:${RESET}
    ${GRAY}⎿ Severity Floor:${RESET}    ${YELLOW}${cfg.severity_threshold || 'medium'}${RESET}
    ${GRAY}⎿ Runs Directory:${RESET}    ${CYAN}${cfg.runs_dir || '.torusguard/runs'}${RESET}
    ${GRAY}⎿ Ponytail Bounds:${RESET}   ${GREEN}≤ 35 additions, ≤ 25 deletions${RESET}

  ${CYAN}╭──────────────────────────────────────────────────────────────────────────╮${RESET}
  ${CYAN}│${RESET}  ${BOLD}💡 Quick Action:${RESET} In your AI chat, run ${CYAN}/torusguard-audit${RESET} to scan.      ${CYAN}│${RESET}
  ${CYAN}╰──────────────────────────────────────────────────────────────────────────╯${RESET}
`);
      process.exit(0);
    } catch (e) {
      // Fallback to python runner
    }
  } else {
    console.log(`
  ${YELLOW}Notice:${RESET} No .torusguard workspace found in current directory.
  Run ${GREEN}npx torusguard init${RESET} to scaffold full workspace governance.
`);
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
  scriptArgs.push(...args.slice(1));
} else {
  scriptArgs.push(...args);
}

const proc = spawnSync(pythonCmd, scriptArgs, {
  stdio: 'inherit',
  cwd: cwd,
});

process.exit(proc.status !== null ? proc.status : 0);
