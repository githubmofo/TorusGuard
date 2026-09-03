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

// ─── ANSI Color Helpers ───────────────────────────────────────────────────────
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';
const RESET = '\x1b[0m';
const CYAN = '\x1b[36m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const WHITE = '\x1b[97m';
const GRAY = '\x1b[90m';
const RED = '\x1b[31m';

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
  ${CYAN}╭─────────────────────────────────────────────────────────────────────────╮${RESET}
  ${CYAN}│${RESET}                                                                         ${CYAN}│${RESET}
  ${CYAN}│${RESET}   ${BOLD}${WHITE}🛡️  T O R U S G U A R D   C L I${RESET}                          ${GRAY}v0.9.5${RESET}   ${CYAN}│${RESET}
  ${CYAN}│${RESET}   ${DIM}Autonomous Security Engine for AI-Built Applications${RESET}               ${CYAN}│${RESET}
  ${CYAN}│${RESET}                                                                         ${CYAN}│${RESET}
  ${CYAN}╰─────────────────────────────────────────────────────────────────────────╯${RESET}

  ${BOLD}Usage:${RESET}  ${GREEN}npx torusguard${RESET} ${WHITE}[command]${RESET} ${GRAY}[options]${RESET}

  ${CYAN}┌─────────────────────────────────────────────────────────────────────────┐${RESET}
  ${CYAN}│${RESET}  ${BOLD}Commands${RESET}                                                              ${CYAN}│${RESET}
  ${CYAN}├─────────────────────────────────────────────────────────────────────────┤${RESET}
  ${CYAN}│${RESET}  ${GREEN}init${RESET}      Scaffold ${BOLD}.torusguard/${RESET} workspace + unlock 11 slash commands   ${CYAN}│${RESET}
  ${CYAN}│${RESET}  ${GREEN}status${RESET}    Display active security posture, rules, and stack info      ${CYAN}│${RESET}
  ${CYAN}│${RESET}  ${GREEN}audit${RESET}     Run static AST security scan on the target project          ${CYAN}│${RESET}
  ${CYAN}│${RESET}  ${GREEN}report${RESET}    Export OASIS SARIF v2.1.0 structured telemetry              ${CYAN}│${RESET}
  ${CYAN}│${RESET}  ${GREEN}help${RESET}      Show this interactive command guide                         ${CYAN}│${RESET}
  ${CYAN}├─────────────────────────────────────────────────────────────────────────┤${RESET}
  ${CYAN}│${RESET}  ${BOLD}Options${RESET}                                                               ${CYAN}│${RESET}
  ${CYAN}├─────────────────────────────────────────────────────────────────────────┤${RESET}
  ${CYAN}│${RESET}  ${GRAY}--target <dir>${RESET}   Target directory to analyze or scaffold ${DIM}(default: .)${RESET}  ${CYAN}│${RESET}
  ${CYAN}│${RESET}  ${GRAY}--force${RESET}          Overwrite existing workspace and re-scaffold          ${CYAN}│${RESET}
  ${CYAN}└─────────────────────────────────────────────────────────────────────────┘${RESET}

  ${BOLD}AI Chat Commands:${RESET}
    ${DIM}In your AI IDE chat, use any of these slash commands:${RESET}
    ${CYAN}/torusguard${RESET}          Main orchestrator (status, audit, harden, etc.)
    ${CYAN}/torusguard-audit${RESET}    Static AST security scan
    ${CYAN}/torusguard-harden${RESET}   Generate governed fix patches
    ${CYAN}/torusguard-apply${RESET}    Apply patches with rollback snapshots
    ${CYAN}/torusguard-report${RESET}   Executive security posture report
    ${CYAN}/torusguard-status${RESET}   Read-only workspace diagnostic

  ${DIM}Documentation:${RESET}  ${CYAN}https://github.com/githubmofo/TorusGuard${RESET}
  ${DIM}NPM Package:${RESET}   ${CYAN}https://npmjs.com/package/torusguard${RESET}
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
      const stackLang = cfg.detected_stack?.language || 'Not yet detected';
      const stackFw = cfg.detected_stack?.framework || 'Not yet detected';
      const stackDb = cfg.detected_stack?.data_layer || 'Not yet detected';
      const stackStatus = cfg.detected_stack ? `${GREEN}Detected${RESET}` : `${YELLOW}Pending first audit${RESET}`;

      console.log(`
  ${CYAN}╭─────────────────────────────────────────────────────────────────────────╮${RESET}
  ${CYAN}│${RESET}                                                                         ${CYAN}│${RESET}
  ${CYAN}│${RESET}   ${BOLD}${WHITE}🛡️  TORUSGUARD SECURITY POSTURE${RESET}                        ${GRAY}v0.9.5${RESET}   ${CYAN}│${RESET}
  ${CYAN}│${RESET}                                                                         ${CYAN}│${RESET}
  ${CYAN}╰─────────────────────────────────────────────────────────────────────────╯${RESET}

  ${BOLD}▸ Workspace:${RESET}        ${GREEN}${cwd}${RESET}
  ${BOLD}▸ Governance:${RESET}       ${GREEN}Full Local Governance (.torusguard/)${RESET}

  ${CYAN}┌── Environment & Stack ──────────────────────────────────────────────────┐${RESET}
  ${CYAN}│${RESET}  Language:          ${BOLD}${stackLang}${RESET}
  ${CYAN}│${RESET}  Framework:         ${BOLD}${stackFw}${RESET}
  ${CYAN}│${RESET}  Data Layer:        ${BOLD}${stackDb}${RESET}
  ${CYAN}│${RESET}  Stack Detection:   ${stackStatus}
  ${CYAN}└─────────────────────────────────────────────────────────────────────────┘${RESET}

  ${CYAN}┌── Governance Telemetry ─────────────────────────────────────────────────┐${RESET}
  ${CYAN}│${RESET}  Rules Catalog:     ${GREEN}71 Canonical Security Rules${RESET} (11 families)
  ${CYAN}│${RESET}  Severity Floor:    ${YELLOW}${cfg.severity_threshold || 'medium'}${RESET}
  ${CYAN}│${RESET}  Runs Directory:    ${DIM}${cfg.runs_dir || '.torusguard/runs'}${RESET}
  ${CYAN}│${RESET}  Ponytail Bounds:   ${GREEN}<= 35 additions, <= 25 deletions${RESET}
  ${CYAN}└─────────────────────────────────────────────────────────────────────────┘${RESET}

  ${CYAN}┌── Rule Families ────────────────────────────────────────────────────────┐${RESET}
  ${CYAN}│${RESET}  ${YELLOW}TG-SEC${RESET}     Secrets & Credentials    ${YELLOW}TG-DB${RESET}      Database Safety
  ${CYAN}│${RESET}  ${YELLOW}TG-INPUT${RESET}   Input Validation         ${YELLOW}TG-AUTH${RESET}    Authentication
  ${CYAN}│${RESET}  ${YELLOW}TG-CLIENT${RESET}  Client Bundle Leaks      ${YELLOW}TG-DIFF${RESET}    Diff Inspection
  ${CYAN}│${RESET}  ${YELLOW}TG-AGENT${RESET}   AI Agent Security        ${YELLOW}TG-EDGE${RESET}    Serverless
  ${CYAN}│${RESET}  ${YELLOW}TG-SUPPLY${RESET}  Supply Chain & CI/CD     ${YELLOW}TG-SSRF${RESET}    Outbound Net
  ${CYAN}│${RESET}  ${YELLOW}TG-BIZ${RESET}     Business Logic
  ${CYAN}└─────────────────────────────────────────────────────────────────────────┘${RESET}

  ${DIM}Quick Action:${RESET} In your AI chat, run ${CYAN}/torusguard-audit${RESET} to scan.
`);
      process.exit(0);
    } catch (e) {
      // Fallback to python runner
    }
  } else {
    console.log(`
  ${YELLOW}⚠${RESET}  No .torusguard workspace found in current directory.
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
