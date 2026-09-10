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

const ANSI_REGEX = /\x1b\[[0-9;]*m/g;

function getVisualWidth(text) {
  const clean = text.replace(ANSI_REGEX, '');
  let width = 0;
  for (let i = 0; i < clean.length; i++) {
    const cp = clean.codePointAt(i);
    if (cp > 0xffff) i++;
    if ((cp >= 0xfe00 && cp <= 0xfe0f) || (cp >= 0xe0100 && cp <= 0xe01ef)) continue;
    if (cp === 0x200b || cp === 0x200c || cp === 0x200d || cp === 0x00ad) continue;
    if (cp >= 0x1f300 || (cp >= 0x1100 && (
      cp <= 0x115f || cp === 0x2329 || cp === 0x232a ||
      (cp >= 0x2e80 && cp <= 0xa4cf && cp !== 0x303f) ||
      (cp >= 0xac00 && cp <= 0xd7a3) ||
      (cp >= 0xf900 && cp <= 0xfaff) ||
      (cp >= 0xfe10 && cp <= 0xfe19) ||
      (cp >= 0xfe30 && cp <= 0xfe6f) ||
      (cp >= 0xff00 && cp <= 0xff60) ||
      (cp >= 0xffe0 && cp <= 0xffe6)
    ))) {
      width += 2;
    } else {
      width += 1;
    }
  }
  return width;
}

function truncateVisual(text, maxW = 67) {
  if (getVisualWidth(text) <= maxW) return text;
  let currW = 0;
  let out = '';
  let inAnsi = false;
  let ansiBuf = '';
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === '\x1b') {
      inAnsi = true;
      ansiBuf = ch;
      continue;
    }
    if (inAnsi) {
      ansiBuf += ch;
      if (ch === 'm') {
        inAnsi = false;
        out += ansiBuf;
      }
      continue;
    }
    const cp = text.codePointAt(i);
    if (cp > 0xffff) i++;
    if ((cp >= 0xfe00 && cp <= 0xfe0f) || (cp >= 0xe0100 && cp <= 0xe01ef) || cp === 0x200b || cp === 0x200c || cp === 0x200d || cp === 0x00ad) {
      out += String.fromCodePoint(cp);
      continue;
    }
    const cw = cp >= 0x1f300 ? 2 : 1;
    if (currW + cw > maxW - 3) {
      out += '\x1b[0m...';
      currW += 3;
      break;
    }
    out += String.fromCodePoint(cp);
    currW += cw;
  }
  out += '\x1b[0m';
  return out;
}

function formatBoxLine(content, width = 67, border = '│', borderColor = CYAN) {
  const trunc = truncateVisual(content, width);
  const vis = getVisualWidth(trunc);
  const pad = ' '.repeat(Math.max(0, width - vis));
  return `  ${borderColor}${border}${RESET}  ${trunc}${pad}  ${borderColor}${border}${RESET}`;
}

function cardBorderTop(title = '', borderColor = CYAN, double = false) {
  const left = double ? '╔' : '┌';
  const right = double ? '╗' : '┐';
  const h = double ? '═' : '─';
  if (title) {
    const vis = getVisualWidth(title);
    const rem = Math.max(0, 68 - vis);
    return `  ${borderColor}${left}${h} ${BOLD}${WHITE}${title}${RESET}${borderColor} ${h.repeat(rem)}${right}${RESET}`;
  }
  return `  ${borderColor}${left}${h.repeat(71)}${right}${RESET}`;
}

function cardBorderBottom(borderColor = CYAN, double = false) {
  const left = double ? '╚' : '└';
  const right = double ? '╝' : '┘';
  const h = double ? '═' : '─';
  return `  ${borderColor}${left}${h.repeat(71)}${right}${RESET}`;
}

function cardDivider(title = '', borderColor = CYAN, double = false) {
  const left = double ? '╠' : '├';
  const right = double ? '╣' : '┤';
  const h = double ? '═' : '─';
  if (title) {
    const vis = getVisualWidth(title);
    const rem = Math.max(0, 68 - vis);
    return `  ${borderColor}${left}${h} ${BOLD}${WHITE}${title}${RESET}${borderColor} ${h.repeat(rem)}${right}${RESET}`;
  }
  return `  ${borderColor}${left}${h.repeat(71)}${right}${RESET}`;
}

function cardHeader(title, subtitle = '', version = 'v1.3.4', borderColor = CYAN) {
  const top = `  ${borderColor}╭${'─'.repeat(71)}╮${RESET}`;
  const bottom = `  ${borderColor}╰${'─'.repeat(71)}╯${RESET}`;
  const empty = `  ${borderColor}│${' '.repeat(71)}│${RESET}`;
  const titleVis = getVisualWidth(title);
  const verVis = getVisualWidth(version);
  const spaceCount = Math.max(1, 67 - titleVis - verVis);
  const titleStr = `${BOLD}${WHITE}${title}${RESET}${' '.repeat(spaceCount)}${GRAY}${version}${RESET}`;
  const lines = [top, empty, formatBoxLine(titleStr, 67, '│', borderColor)];
  if (subtitle) {
    lines.push(formatBoxLine(`${DIM}${subtitle}${RESET}`, 67, '│', borderColor));
  }
  lines.push(empty, bottom);
  return lines.join('\n');
}

function printHelp() {
  console.log();
  console.log(cardHeader('🛡️  T O R U S G U A R D   C L I', 'Autonomous Security Engine for AI-Built Applications', 'v1.3.3'));
  console.log(`\n  ${BOLD}Usage:${RESET}  ${GREEN}npx torusguard${RESET} ${WHITE}[command]${RESET} ${GRAY}[options]${RESET}\n`);

  console.log(cardBorderTop('Commands'));
  console.log(formatBoxLine(`${GREEN}init${RESET}        Scaffold ${BOLD}.torusguard/${RESET} workspace + unlock slash commands`));
  console.log(formatBoxLine(`${GREEN}status${RESET}      Display active security posture, memory, rules, & stack`));
  console.log(formatBoxLine(`${GREEN}rules${RESET}       Auto-sync memory to AI IDE rules (.cursorrules, CLAUDE.md)`));
  console.log(formatBoxLine(`${GREEN}memory${RESET}      Manage persistent security memory (export, hook, learn)`));
  console.log(formatBoxLine(`${GREEN}audit${RESET}       Run static AST security scan on target project`));
  console.log(formatBoxLine(`${GREEN}harden${RESET}      Formulate minimal candidate patches (Ponytail bounded)`));
  console.log(formatBoxLine(`${GREEN}apply${RESET}       Apply candidate patches with automatic .bak snapshots`));
  console.log(formatBoxLine(`${GREEN}recheck${RESET}     Targeted differential verification of applied fixes`));
  console.log(formatBoxLine(`${GREEN}recipes${RESET}     List & inspect distilled Golden Fix Recipes in memory`));
  console.log(formatBoxLine(`${GREEN}rollback${RESET}    Instantly revert files from latest pre-apply snapshot`));
  console.log(formatBoxLine(`${GREEN}report${RESET}      Export OASIS SARIF v2.1.0 or single-file visual HTML report`));
  console.log(formatBoxLine(`${GREEN}diff-guard${RESET}  Scan diffs or wire pre-commit hook (--install-hook)`));
  console.log(formatBoxLine(`${GREEN}help${RESET}        Show this interactive command guide`));
  console.log(cardDivider('AI & Memory Subcommands'));
  console.log(formatBoxLine(`${WHITE}rules sync${RESET}       ${DIM}[--format all|cursor|claude|agent|windsurf]${RESET}`));
  console.log(formatBoxLine(`${WHITE}report --html${RESET}    ${DIM}[--out <path>] Self-contained visual HTML dashboard${RESET}`));
  console.log(formatBoxLine(`${WHITE}memory context${RESET}   ${DIM}[--role auditor|remediator|reviewer] [--file <f>]${RESET}`));
  console.log(formatBoxLine(`${WHITE}memory hook${RESET}      ${DIM}[install|uninstall] Git pre-commit regression hook${RESET}`));
  console.log(formatBoxLine(`${WHITE}memory learn${RESET}     ${DIM}[--commits <range>] Ingest security commit fixes${RESET}`));
  console.log(formatBoxLine(`${WHITE}memory export${RESET}    ${DIM}[--path <file>] [--sanitized] Safe team sharing${RESET}`));
  console.log(cardDivider('Options'));
  console.log(formatBoxLine(`${GRAY}--target <dir>${RESET}   Target directory to analyze or scaffold ${DIM}(default: .)${RESET}`));
  console.log(formatBoxLine(`${GRAY}--force${RESET}          Overwrite existing workspace and re-scaffold`));
  console.log(formatBoxLine(`${GRAY}--yes, -y${RESET}        Non-interactive auto-approval for patch application`));
  console.log(cardBorderBottom());

  console.log(`\n  ${BOLD}AI Chat Commands:${RESET}`);
  console.log(`    ${DIM}In your AI IDE chat, use any of these slash commands:${RESET}`);
  console.log(`    ${CYAN}/torusguard${RESET}          Main orchestrator (status, audit, harden, memory)`);
  console.log(`    ${CYAN}/torusguard-audit${RESET}    Static AST security scan`);
  console.log(`    ${CYAN}/torusguard-harden${RESET}   Generate governed fix patches`);
  console.log(`    ${CYAN}/torusguard-apply${RESET}    Apply patches with rollback snapshots`);
  console.log(`    ${CYAN}/torusguard-recheck${RESET}  Differential AST fix closure verification`);
  console.log(`    ${CYAN}/torusguard-report${RESET}   Executive security posture report`);
  console.log(`    ${CYAN}/torusguard-status${RESET}   Read-only workspace diagnostic`);
  console.log(`\n  ${DIM}Documentation:${RESET}  ${CYAN}https://github.com/githubmofo/TorusGuard${RESET}`);
  console.log(`  ${DIM}NPM Package:${RESET}   ${CYAN}https://npmjs.com/package/torusguard${RESET}\n`);
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

      // Memory telemetry
      const memProfilePath = path.join(cwd, '.torusguard', 'memory', 'profile.json');
      const memContextPath = path.join(cwd, '.torusguard', 'memory', 'context.json');
      let memPatterns = 0;
      let memEvents = 0;
      let memTokens = 0;
      let memFixRate = 'N/A';
      if (fs.existsSync(memProfilePath)) {
        try {
          const prof = JSON.parse(fs.readFileSync(memProfilePath, 'utf-8'));
          memPatterns = prof.active_patterns_count || 0;
          memEvents = prof.total_events || 0;
          memFixRate = prof.fix_rate_percentage !== null && prof.fix_rate_percentage !== undefined ? `${prof.fix_rate_percentage}%` : 'N/A';
        } catch (e) {}
      }
      if (fs.existsSync(memContextPath)) {
        try {
          const ctx = JSON.parse(fs.readFileSync(memContextPath, 'utf-8'));
          memTokens = ctx.token_estimate || 0;
        } catch (e) {}
      }

      console.log();
      console.log(cardHeader('🛡️  TORUSGUARD SECURITY POSTURE', '', 'v1.3.3'));
      console.log(`\n  ${BOLD}▸ Workspace:${RESET}        ${GREEN}${cwd}${RESET}`);
      console.log(`  ${BOLD}▸ Governance:${RESET}       ${GREEN}Full Local Governance (.torusguard/)${RESET}\n`);

      console.log(cardBorderTop('Environment & Stack'));
      console.log(formatBoxLine(`Language:          ${BOLD}${stackLang}${RESET}`));
      console.log(formatBoxLine(`Framework:         ${BOLD}${stackFw}${RESET}`));
      console.log(formatBoxLine(`Data Layer:        ${BOLD}${stackDb}${RESET}`));
      console.log(formatBoxLine(`Stack Detection:   ${stackStatus}`));
      console.log(cardBorderBottom());
      console.log();

      console.log(cardBorderTop('Security Memory Engine'));
      console.log(formatBoxLine(`Patterns Learned:  ${GREEN}${memPatterns} active patterns${RESET}`));
      console.log(formatBoxLine(`Events Recorded:   ${WHITE}${memEvents} events (local-first log)${RESET}`));
      console.log(formatBoxLine(`Context Window:    ${CYAN}${memTokens} / 2,000 tokens${RESET} (${Math.round((memTokens / 2000) * 100)}% utilized)`));
      console.log(formatBoxLine(`Fix Velocity Rate: ${YELLOW}${memFixRate}${RESET}`));
      console.log(cardBorderBottom());
      console.log();

      console.log(cardBorderTop('Governance Telemetry'));
      console.log(formatBoxLine(`Rules Catalog:     ${GREEN}71 Canonical Security Rules${RESET} (11 families)`));
      console.log(formatBoxLine(`Severity Floor:    ${YELLOW}${cfg.severity_threshold || 'medium'}${RESET}`));
      console.log(formatBoxLine(`Runs Directory:    ${DIM}${cfg.runs_dir || '.torusguard/runs'}${RESET}`));
      console.log(formatBoxLine(`Ponytail Bounds:   ${GREEN}<= 35 additions, <= 25 deletions${RESET}`));
      console.log(cardBorderBottom());
      console.log();

      console.log(cardBorderTop('Rule Families'));
      console.log(formatBoxLine(`${YELLOW}TG-SEC${RESET}     Secrets & Credentials    ${YELLOW}TG-DB${RESET}      Database Safety`));
      console.log(formatBoxLine(`${YELLOW}TG-INPUT${RESET}   Input Validation         ${YELLOW}TG-AUTH${RESET}    Authentication`));
      console.log(formatBoxLine(`${YELLOW}TG-CLIENT${RESET}  Client Bundle Leaks      ${YELLOW}TG-DIFF${RESET}    Diff Inspection`));
      console.log(formatBoxLine(`${YELLOW}TG-AGENT${RESET}   AI Agent Security        ${YELLOW}TG-EDGE${RESET}    Serverless`));
      console.log(formatBoxLine(`${YELLOW}TG-SUPPLY${RESET}  Supply Chain & CI/CD     ${YELLOW}TG-SSRF${RESET}    Outbound Net`));
      console.log(formatBoxLine(`${YELLOW}TG-BIZ${RESET}     Business Logic`));
      console.log(cardBorderBottom());

      console.log(`\n  ${DIM}Quick Action:${RESET} In your AI chat, run ${CYAN}/torusguard-audit${RESET} to scan.\n`);
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

// Subcommand: memory
if (command === 'memory') {
  const sub = args[1] || 'status';
  const memScript = path.join(cwd, '.torusguard', 'scripts', 'memory_engine.py');
  const fallbackMemScript = path.join(rootDir, '.torusguard', 'scripts', 'memory_engine.py');
  const actualMemScript = fs.existsSync(memScript) ? memScript : fallbackMemScript;

  let pyArgs = [actualMemScript];
  if (sub === 'status') {
    pyArgs.push('--action', 'status');
  } else if (sub === 'context') {
    pyArgs.push('--action', 'context');
    const roleIdx = args.indexOf('--role');
    if (roleIdx !== -1 && args[roleIdx + 1]) {
      pyArgs.push('--role', args[roleIdx + 1]);
    }
    const fileIdx = args.indexOf('--file') !== -1 ? args.indexOf('--file') : args.indexOf('-f');
    if (fileIdx !== -1 && args[fileIdx + 1]) {
      pyArgs.push('--file', args[fileIdx + 1]);
    }
    const ruleIdx = args.indexOf('--rule') !== -1 ? args.indexOf('--rule') : args.indexOf('-r');
    if (ruleIdx !== -1 && args[ruleIdx + 1]) {
      pyArgs.push('--rule-id', args[ruleIdx + 1]);
    }
  } else if (sub === 'distill') {
    pyArgs.push('--action', 'distill');
  } else if (sub === 'decay') {
    pyArgs.push('--action', 'decay');
    const ttlIdx = args.indexOf('--ttl');
    if (ttlIdx !== -1 && args[ttlIdx + 1]) {
      pyArgs.push('--ttl', args[ttlIdx + 1]);
    }
  } else if (sub === 'compact') {
    pyArgs.push('--action', 'compact');
    const ageIdx = args.indexOf('--older-than');
    if (ageIdx !== -1 && args[ageIdx + 1]) {
      pyArgs.push('--older-than', args[ageIdx + 1]);
    }
  } else if (sub === 'export') {
    pyArgs.push('--action', 'export');
    const pathIdx = args.indexOf('--path') !== -1 ? args.indexOf('--path') : args.indexOf('-p');
    if (pathIdx !== -1 && args[pathIdx + 1]) {
      pyArgs.push('--target', args[pathIdx + 1]);
    } else {
      pyArgs.push('--target', 'torusguard-memory-export.json');
    }
    if (args.includes('--sanitized')) {
      pyArgs.push('--sanitized');
    }
  } else if (sub === 'import') {
    pyArgs.push('--action', 'import');
    const pathIdx = args.indexOf('--path') !== -1 ? args.indexOf('--path') : args.indexOf('-p');
    if (pathIdx !== -1 && args[pathIdx + 1]) {
      pyArgs.push('--source', args[pathIdx + 1]);
    } else {
      console.error(`${RED}Error: --path <file> is required for memory import${RESET}`);
      process.exit(1);
    }
  } else if (sub === 'hook') {
    const hookAction = args[2] === 'uninstall' ? 'hook-uninstall' : 'hook-install';
    pyArgs.push('--action', hookAction);
  } else if (sub === 'learn') {
    pyArgs.push('--action', 'learn');
    const commitsIdx = args.indexOf('--commits');
    if (commitsIdx !== -1 && args[commitsIdx + 1]) {
      pyArgs.push('--commits', args[commitsIdx + 1]);
    }
    const daysIdx = args.indexOf('--days');
    if (daysIdx !== -1 && args[daysIdx + 1]) {
      pyArgs.push('--days', args[daysIdx + 1]);
    }
  } else if (sub === 'recipe') {
    pyArgs.push('--action', 'recipe', ...args.slice(2));
  } else if (sub === 'fp') {
    pyArgs.push('--action', 'fp');
    const ruleIdx = args.indexOf('--rule') !== -1 ? args.indexOf('--rule') : args.indexOf('-r');
    if (ruleIdx !== -1 && args[ruleIdx + 1]) {
      pyArgs.push('--rule-id', args[ruleIdx + 1]);
    } else {
      console.error(`${RED}Error: --rule <rule_id> is required for fp suppression${RESET}`);
      process.exit(1);
    }
    const reasonIdx = args.indexOf('--reason');
    if (reasonIdx !== -1 && args[reasonIdx + 1]) {
      pyArgs.push('--reason', args[reasonIdx + 1]);
    }
  } else {
    pyArgs.push('--action', sub, ...args.slice(2));
  }

  const proc = spawnSync(pythonCmd, pyArgs, { stdio: 'inherit', cwd });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: diff-guard
if (command === 'diff-guard') {
  const diffScript = path.join(cwd, '.torusguard', 'scripts', 'diff_guard.py');
  const fallbackDiffScript = path.join(rootDir, '.torusguard', 'scripts', 'diff_guard.py');
  const actualDiffScript = fs.existsSync(fallbackDiffScript) ? fallbackDiffScript : diffScript;

  const proc = spawnSync(pythonCmd, [actualDiffScript, ...args.slice(1)], { stdio: 'inherit', cwd });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: rules
if (command === 'rules') {
  const sub = args[1] || 'sync';
  const rulesScript = path.join(cwd, '.torusguard', 'scripts', 'rules_sync.py');
  const fallbackRulesScript = path.join(rootDir, '.torusguard', 'scripts', 'rules_sync.py');
  const actualRulesScript = fs.existsSync(fallbackRulesScript) ? fallbackRulesScript : rulesScript;

  let pyArgs = [actualRulesScript];
  if (sub === 'sync') {
    const fmtIdx = args.indexOf('--format');
    if (fmtIdx !== -1 && args[fmtIdx + 1]) {
      pyArgs.push('--format', args[fmtIdx + 1]);
    }
    const rootIdx = args.indexOf('--root') !== -1 ? args.indexOf('--root') : args.indexOf('--target');
    if (rootIdx !== -1 && args[rootIdx + 1]) {
      pyArgs.push('--root', args[rootIdx + 1]);
    }
    if (args.includes('--json')) {
      pyArgs.push('--json');
    }
  } else {
    pyArgs.push(...args.slice(1));
  }

  const proc = spawnSync(pythonCmd, pyArgs, { stdio: 'inherit', cwd });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: audit
if (command === 'audit') {
  const auditScript = path.join(cwd, '.torusguard', 'scripts', 'audit_runner.py');
  const fallbackAuditScript = path.join(rootDir, '.torusguard', 'scripts', 'audit_runner.py');
  const actualAuditScript = fs.existsSync(fallbackAuditScript) ? fallbackAuditScript : auditScript;

  const proc = spawnSync(pythonCmd, [actualAuditScript, ...args.slice(1)], { stdio: 'inherit', cwd });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: report
if (command === 'report') {
  if (args.includes('--html') || args[1] === 'html') {
    const htmlScript = path.join(cwd, '.torusguard', 'scripts', 'html_reporter.py');
    const fallbackHtmlScript = path.join(rootDir, '.torusguard', 'scripts', 'html_reporter.py');
    const actualHtmlScript = fs.existsSync(fallbackHtmlScript) ? fallbackHtmlScript : htmlScript;

    let pyArgs = [actualHtmlScript];
    const outIdx = args.indexOf('--out');
    if (outIdx !== -1 && args[outIdx + 1]) {
      pyArgs.push('--out', args[outIdx + 1]);
    }
    const rootIdx = args.indexOf('--root') !== -1 ? args.indexOf('--root') : args.indexOf('--target');
    if (rootIdx !== -1 && args[rootIdx + 1]) {
      pyArgs.push('--root', args[rootIdx + 1]);
    }
    if (args.includes('--json')) {
      pyArgs.push('--json');
    }

    const proc = spawnSync(pythonCmd, pyArgs, { stdio: 'inherit', cwd });
    process.exit(proc.status !== null ? proc.status : 0);
  } else {
    const sarifScript = path.join(cwd, '.torusguard', 'scripts', 'sarif_exporter.py');
    const fallbackSarifScript = path.join(rootDir, '.torusguard', 'scripts', 'sarif_exporter.py');
    const actualSarifScript = fs.existsSync(fallbackSarifScript) ? fallbackSarifScript : sarifScript;

    const proc = spawnSync(pythonCmd, [actualSarifScript, ...args.slice(1)], { stdio: 'inherit', cwd });
    process.exit(proc.status !== null ? proc.status : 0);
  }
}

// Subcommand: harden
if (command === 'harden') {
  const scriptPath = path.join(cwd, '.torusguard', 'scripts', 'harden_runner.py');
  const fallbackScript = path.join(rootDir, '.torusguard', 'scripts', 'harden_runner.py');
  const actualScript = fs.existsSync(fallbackScript) ? fallbackScript : scriptPath;

  const proc = spawnSync(pythonCmd, [actualScript, ...args.slice(1)], { stdio: 'inherit', cwd });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: apply
if (command === 'apply') {
  const scriptPath = path.join(cwd, '.torusguard', 'scripts', 'apply_runner.py');
  const fallbackScript = path.join(rootDir, '.torusguard', 'scripts', 'apply_runner.py');
  const actualScript = fs.existsSync(fallbackScript) ? fallbackScript : scriptPath;

  const proc = spawnSync(pythonCmd, [actualScript, ...args.slice(1)], { stdio: 'inherit', cwd });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: rollback
if (command === 'rollback') {
  const scriptPath = path.join(cwd, '.torusguard', 'scripts', 'apply_runner.py');
  const fallbackScript = path.join(rootDir, '.torusguard', 'scripts', 'apply_runner.py');
  const actualScript = fs.existsSync(fallbackScript) ? fallbackScript : scriptPath;

  const proc = spawnSync(pythonCmd, [actualScript, '--rollback', ...args.slice(1)], { stdio: 'inherit', cwd });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: recheck / verify
if (command === 'recheck' || command === 'verify') {
  const scriptPath = path.join(cwd, '.torusguard', 'scripts', 'recheck_runner.py');
  const fallbackScript = path.join(rootDir, '.torusguard', 'scripts', 'recheck_runner.py');
  const actualScript = fs.existsSync(fallbackScript) ? fallbackScript : scriptPath;

  const proc = spawnSync(pythonCmd, [actualScript, ...args.slice(1)], { stdio: 'inherit', cwd });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: recipes
if (command === 'recipes') {
  const scriptPath = path.join(cwd, '.torusguard', 'scripts', 'recipes_runner.py');
  const fallbackScript = path.join(rootDir, '.torusguard', 'scripts', 'recipes_runner.py');
  const actualScript = fs.existsSync(fallbackScript) ? fallbackScript : scriptPath;

  const proc = spawnSync(pythonCmd, [actualScript, ...args.slice(1)], { stdio: 'inherit', cwd });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: init (scaffold workspace)
if (command === 'init') {
  const localBootstrap = path.join(rootDir, 'skills', 'torusguard', 'bootstrap.py');
  const localInstall = path.join(rootDir, 'install.py');
  const scriptToRun = fs.existsSync(localBootstrap) ? localBootstrap : localInstall;

  const scriptArgs = [scriptToRun, '--full-commands', ...args.slice(1)];
  const proc = spawnSync(pythonCmd, scriptArgs, {
    stdio: 'inherit',
    cwd: cwd,
  });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Unknown command fallback
console.error(`\n  ${RED}✖ Unknown command:${RESET} ${WHITE}${command}${RESET}`);
console.error(`  Run ${GREEN}npx torusguard help${RESET} for available commands.\n`);
process.exit(1);
