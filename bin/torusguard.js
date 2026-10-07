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
const command = args[0];
const rootDir = path.resolve(__dirname, '..');
const cwd = process.cwd();

let PKG_VERSION = '2.2.0';
try {
  const pkg = JSON.parse(fs.readFileSync(path.join(rootDir, 'package.json'), 'utf-8'));
  PKG_VERSION = pkg.version || PKG_VERSION;
} catch (e) {}

// Parse version flag immediately
if (command === '--version' || command === '-v' || command === 'version') {
  console.log(`torusguard v${PKG_VERSION}`);
  process.exit(0);
}

function findNativeBinary() {
  const candidates = [
    path.join(rootDir, 'torusguard.exe'),
    path.join(rootDir, 'torusguard'),
    path.join(cwd, 'torusguard.exe'),
    path.join(cwd, 'torusguard'),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

function parseTargetAndArgs(cliArgs) {
  let target = '.';
  const remaining = [];
  for (let i = 1; i < cliArgs.length; i++) {
    const a = cliArgs[i];
    if (a === '--target' || a === '-t' || a === '--root') {
      if (i + 1 < cliArgs.length) {
        target = cliArgs[i + 1];
        i++;
      }
    } else if (a.startsWith('--target=') || a.startsWith('--root=')) {
      target = a.split('=')[1];
    } else {
      remaining.push(a);
    }
  }
  if (target === '.' && remaining.length > 0 && !remaining[0].startsWith('-')) {
    target = remaining.shift();
  }
  return { target, remaining };
}

function compareSemver(a, b) {
  const pa = a.replace(/^v/, '').split('.').map(n => parseInt(n, 10) || 0);
  const pb = b.replace(/^v/, '').split('.').map(n => parseInt(n, 10) || 0);
  for (let i = 0; i < 3; i++) {
    const na = pa[i] || 0;
    const nb = pb[i] || 0;
    if (na > nb) return 1;
    if (na < nb) return -1;
  }
  return 0;
}

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

function cardHeader(title, subtitle = '', version = `v${PKG_VERSION}`, borderColor = CYAN) {
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
  console.log(cardHeader('🛡️  T O R U S G U A R D   C L I', 'Autonomous Security Engine for AI-Built Applications', `v${PKG_VERSION}`));
  console.log(`\n  ${BOLD}Usage:${RESET}  ${GREEN}npx torusguard${RESET} ${WHITE}[command]${RESET} ${GRAY}[options]${RESET}\n`);

  console.log(cardBorderTop('Commands'));
  console.log(formatBoxLine(`${GREEN}init${RESET}        Scaffold ${BOLD}.torusguard/${RESET} workspace + unlock slash commands`));
  console.log(formatBoxLine(`${GREEN}status${RESET}      Display active security posture, memory, rules, & stack`));
  console.log(formatBoxLine(`${GREEN}update${RESET}      Check npm registry for updates (--install to auto-upgrade)`));
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
  console.log(formatBoxLine(`${WHITE}report --sarif${RESET}   ${DIM}[--out <path>] OASIS SARIF v2.1.0 GitHub Scanning log${RESET}`));
  console.log(formatBoxLine(`${WHITE}memory context${RESET}   ${DIM}[--role auditor|remediator|reviewer] [--file <f>]${RESET}`));
  console.log(formatBoxLine(`${WHITE}memory hook${RESET}      ${DIM}[install|uninstall] Git pre-commit regression hook${RESET}`));
  console.log(formatBoxLine(`${WHITE}memory learn${RESET}     ${DIM}[--commits <range>] Ingest security commit fixes${RESET}`));
  console.log(formatBoxLine(`${WHITE}memory export${RESET}    ${DIM}[--path <file>] [--sanitized] Safe team sharing${RESET}`));
  console.log(cardDivider('Options'));
  console.log(formatBoxLine(`${GRAY}--target <dir>${RESET}   Target directory to analyze or scaffold ${DIM}(default: .)${RESET}`));
  console.log(formatBoxLine(`${GRAY}--force${RESET}          Overwrite existing workspace and re-scaffold`));
  console.log(formatBoxLine(`${GRAY}--yes, -y${RESET}        Non-interactive auto-approval for patch application`));
  console.log(formatBoxLine(`${GRAY}--version, -v${RESET}    Display TorusGuard package version`));
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

if (!command) {
  if (process.stdin.isTTY) {
    const readline = require('readline');
    console.log();
    console.log(cardHeader('🛡️  TORUSGUARD COMMAND CENTER', 'Interactive Security Engine', `v${PKG_VERSION}`));
    console.log(cardBorderTop('Quick Actions'));
    console.log(formatBoxLine(`${GREEN}[1]${RESET}  🚀 Audit Workspace          ${GRAY}(Full AST & Taint Scan)${RESET}`));
    console.log(formatBoxLine(`${GREEN}[2]${RESET}  👁️  OCR Vision Scan          ${GRAY}(Images & Diagram Secrets)${RESET}`));
    console.log(formatBoxLine(`${GREEN}[3]${RESET}  📊 Posture Status           ${GRAY}(Active Posture & Rules)${RESET}`));
    console.log(formatBoxLine(`${GREEN}[4]${RESET}  🐳 Container Audit          ${GRAY}(Dockerfile & Compose Scan)${RESET}`));
    console.log(formatBoxLine(`${GREEN}[5]${RESET}  ⚡ ReDoS Complexity Scan    ${GRAY}(Catastrophic Regex Scan)${RESET}`));
    console.log(formatBoxLine(`${GREEN}[6]${RESET}  🤖 AI & RAG Defense         ${GRAY}(Prompt Injection & Vectors)${RESET}`));
    console.log(formatBoxLine(`${GREEN}[7]${RESET}  🔍 Git History Mine         ${GRAY}(Committed Leaks & Tokens)${RESET}`));
    console.log(formatBoxLine(`${GREEN}[8]${RESET}  🛡️  Harden Candidates       ${GRAY}(Ponytail Bounded Patches)${RESET}`));
    console.log(formatBoxLine(`${GREEN}[9]${RESET}  📑 Posture Report           ${GRAY}(Generate Visual HTML Report)${RESET}`));
    console.log(formatBoxLine(`${GREEN}[10]${RESET} 📖 Awesome Rules Catalog    ${GRAY}(88 Rules Across 22 Families)${RESET}`));
    console.log(formatBoxLine(`${RED}[0]${RESET}  ❌ Exit`));
    console.log(cardBorderBottom());

    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question(`\n  ${BOLD}Select option [0-10]${RESET}: `, (ans) => {
      rl.close();
      const choice = ans.trim();
      const cmdMap = {
        '1': 'audit', '2': 'ocr-scan', '3': 'status', '4': 'container',
        '5': 'redos', '6': 'ai-guard', '7': 'git-mine', '8': 'harden',
        '9': 'report', '10': 'recipes'
      };
      if (choice === '0' || choice === 'q' || choice === 'exit') {
        console.log(`\n  ${GREEN}Exiting TorusGuard.${RESET}\n`);
        process.exit(0);
      }
      const selectedCmd = cmdMap[choice];
      if (selectedCmd) {
        const nativeBin = findNativeBinary();
        if (nativeBin) {
          const subArgs = choice === '9' ? ['report', '--html'] : [selectedCmd];
          const p = spawnSync(nativeBin, subArgs, { stdio: 'inherit', cwd });
          process.exit(p.status !== null ? p.status : 0);
        } else {
          const subArgs = choice === '9' ? [process.argv[1], 'report', '--html'] : [process.argv[1], selectedCmd];
          const p = spawnSync(process.execPath, subArgs, { stdio: 'inherit', cwd });
          process.exit(p.status !== null ? p.status : 0);
        }
      } else {
        console.log(`\n  ${YELLOW}Invalid selection '${choice}'. Enter 0-10.${RESET}\n`);
        process.exit(1);
      }
    });
    return;
  } else {
    printHelp();
    process.exit(0);
  }
}

if (command === 'help' || command === '--help' || command === '-h') {
  printHelp();
  process.exit(0);
}

if (command === 'status') {
  const { target, remaining } = parseTargetAndArgs(args);
  const targetDir = path.resolve(cwd, target);
  const statusScript = path.join(targetDir, '.torusguard', 'scripts', 'status_runner.py');
  const fallbackStatusScript = path.join(rootDir, '.torusguard', 'scripts', 'status_runner.py');
  const actualStatusScript = fs.existsSync(statusScript) ? statusScript : fallbackStatusScript;

  if (fs.existsSync(actualStatusScript)) {
    const proc = spawnSync(pythonCmd, [actualStatusScript, targetDir, ...remaining], { stdio: 'inherit', cwd: targetDir });
    process.exit(proc.status !== null ? proc.status : 0);
  }

  const cfgPath = path.join(targetDir, '.torusguard', 'config', 'torusguard.json');
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
      console.log(cardHeader('🛡️  TORUSGUARD SECURITY POSTURE', '', `v${PKG_VERSION}`));
      console.log(`\n  ${BOLD}▸ Workspace:${RESET}        ${GREEN}${cwd}${RESET}`);
      console.log(`  ${BOLD}▸ Governance:${RESET}       ${GREEN}Full Local Governance (.torusguard/)${RESET}`);
      console.log(`  ${BOLD}▸ Living Report:${RESET}    ${CYAN}security_report.md${RESET}\n`);

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
      console.log(formatBoxLine(`Rules Catalog:     ${GREEN}88 Canonical Security Rules${RESET} (22 families)`));
      console.log(formatBoxLine(`Severity Floor:    ${YELLOW}${cfg.severity_threshold || 'medium'}${RESET}`));
      console.log(formatBoxLine(`Runs Directory:    ${DIM}${cfg.runs_dir || '.torusguard/runs'}${RESET}`));
      console.log(formatBoxLine(`Ponytail Bounds:   ${GREEN}<= 35 additions, <= 25 deletions${RESET}`));
      console.log(formatBoxLine(`Living Report:     ${CYAN}security_report.md (ground truth)${RESET}`));
      console.log(cardBorderBottom());
      console.log();

      console.log(cardBorderTop('Rule Families (22 Families / 88 Rules)'));
      console.log(formatBoxLine(`${YELLOW}TG-SEC${RESET}     Secrets & Tokens (7)     ${YELLOW}TG-AUTH${RESET}    Authentication (8)`));
      console.log(formatBoxLine(`${YELLOW}TG-DB${RESET}      Database Isolation (4)   ${YELLOW}TG-INPUT${RESET}   Input & Traversal (8)`));
      console.log(formatBoxLine(`${YELLOW}TG-RATE${RESET}    Rate Limiting (3)        ${YELLOW}TG-AGENT${RESET}   AI Agent Security (4)`));
      console.log(formatBoxLine(`${YELLOW}TG-SSRF${RESET}    Server-Side Request (4)  ${YELLOW}TG-WEBHOOK${RESET} Webhook Signature (4)`));
      console.log(formatBoxLine(`${YELLOW}TG-WS${RESET}      WebSocket Safety (4)     ${YELLOW}TG-CSRF${RESET}    Cross-Site Request (2)`));
      console.log(formatBoxLine(`${YELLOW}TG-GQL${RESET}     GraphQL Introspection (4)${YELLOW}TG-SUPPLY${RESET}  Supply Chain Health (6)`));
      console.log(formatBoxLine(`${YELLOW}TG-BIZ${RESET}     Business Logic (4)       ${YELLOW}TG-CACHE${RESET}   Cache Poisoning (3)`));
      console.log(formatBoxLine(`${YELLOW}TG-CLIENT${RESET}  Client Bundle Secrets (2)${YELLOW}TG-PLATFORM${RESET}Platform Hardening (4)`));
      console.log(formatBoxLine(`${YELLOW}TG-DIFF${RESET}    Polyglot Bypass Guard (3)${YELLOW}TG-EDGE${RESET}    Edge & Serverless (2)`));
      console.log(formatBoxLine(`${YELLOW}TG-CONT${RESET}    Container Hardening (4)  ${YELLOW}TG-GIT${RESET}     Git Secret Mining (3)`));
      console.log(formatBoxLine(`${YELLOW}TG-REDOS${RESET}   ReDoS Complexity Guard (2)${YELLOW}TG-RAG${RESET}    RAG & Vector Scoping (3)`));
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
  const { target, remaining } = parseTargetAndArgs(args);
  const targetDir = path.resolve(cwd, target);
  const auditScript = path.join(targetDir, '.torusguard', 'scripts', 'audit_runner.py');
  const fallbackAuditScript = path.join(rootDir, '.torusguard', 'scripts', 'audit_runner.py');
  const actualAuditScript = fs.existsSync(fallbackAuditScript) ? fallbackAuditScript : auditScript;

  const proc = spawnSync(pythonCmd, [actualAuditScript, targetDir, ...remaining], { stdio: 'inherit', cwd: targetDir });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: report
if (command === 'report') {
  const wantHtml = args.includes('--html') || args[1] === 'html' || args.includes('--out');
  const wantSarif = args.includes('--sarif') || (!wantHtml && args[1] !== 'html');

  // Resolve target directory (supports --target and --root)
  const rootIdx = args.indexOf('--root') !== -1 ? args.indexOf('--root') : (args.indexOf('--target') !== -1 ? args.indexOf('--target') : args.indexOf('-t'));
  let targetRoot = cwd;
  if (rootIdx !== -1 && args[rootIdx + 1]) {
    targetRoot = path.resolve(cwd, args[rootIdx + 1]);
  }

  let exitCode = 0;

  // 1. If SARIF export is requested
  if (wantSarif) {
    const sarifScript = path.join(targetRoot, '.torusguard', 'scripts', 'sarif_exporter.py');
    const fallbackSarifScript = path.join(rootDir, '.torusguard', 'scripts', 'sarif_exporter.py');
    const actualSarifScript = fs.existsSync(fallbackSarifScript) ? fallbackSarifScript : sarifScript;

    const sarifArgs = [actualSarifScript, '--root', targetRoot];
    const sarifOutIdx = args.indexOf('--sarif-out');
    if (sarifOutIdx !== -1 && args[sarifOutIdx + 1]) {
      sarifArgs.push('--output', args[sarifOutIdx + 1]);
    } else if (!wantHtml) {
      const outIdx = args.indexOf('--out');
      if (outIdx !== -1 && args[outIdx + 1]) {
        sarifArgs.push('--output', args[outIdx + 1]);
      }
    }
    const runIdIdx = args.indexOf('--run');
    if (runIdIdx !== -1 && args[runIdIdx + 1]) {
      sarifArgs.push('--run-id', args[runIdIdx + 1]);
    }

    const proc = spawnSync(pythonCmd, sarifArgs, { stdio: 'inherit', cwd: targetRoot });
    if (proc.status !== 0 && proc.status !== null) {
      exitCode = proc.status;
    }
  }

  // 2. If Visual HTML dashboard is requested
  if (wantHtml) {
    const htmlScript = path.join(targetRoot, '.torusguard', 'scripts', 'html_reporter.py');
    const fallbackHtmlScript = path.join(rootDir, '.torusguard', 'scripts', 'html_reporter.py');
    const actualHtmlScript = fs.existsSync(fallbackHtmlScript) ? fallbackHtmlScript : htmlScript;

    let pyArgs = [actualHtmlScript, '--root', targetRoot];
    const outIdx = args.indexOf('--out');
    if (outIdx !== -1 && args[outIdx + 1]) {
      pyArgs.push('--out', path.resolve(cwd, args[outIdx + 1]));
    } else {
      pyArgs.push('--out', path.join(targetRoot, 'report.html'));
    }
    if (args.includes('--json')) {
      pyArgs.push('--json');
    }

    const proc = spawnSync(pythonCmd, pyArgs, { stdio: 'inherit', cwd: targetRoot });
    if (proc.status !== 0 && proc.status !== null) {
      exitCode = proc.status;
    }
  }

  process.exit(exitCode);
}

// Subcommand: harden
if (command === 'harden') {
  const { target, remaining } = parseTargetAndArgs(args);
  const targetDir = path.resolve(cwd, target);
  const scriptPath = path.join(targetDir, '.torusguard', 'scripts', 'harden_runner.py');
  const fallbackScript = path.join(rootDir, '.torusguard', 'scripts', 'harden_runner.py');
  const actualScript = fs.existsSync(fallbackScript) ? fallbackScript : scriptPath;

  const proc = spawnSync(pythonCmd, [actualScript, targetDir, ...remaining], { stdio: 'inherit', cwd: targetDir });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: apply
if (command === 'apply') {
  const { target, remaining } = parseTargetAndArgs(args);
  const targetDir = path.resolve(cwd, target);
  const scriptPath = path.join(targetDir, '.torusguard', 'scripts', 'apply_runner.py');
  const fallbackScript = path.join(rootDir, '.torusguard', 'scripts', 'apply_runner.py');
  const actualScript = fs.existsSync(fallbackScript) ? fallbackScript : scriptPath;

  const proc = spawnSync(pythonCmd, [actualScript, targetDir, ...remaining], { stdio: 'inherit', cwd: targetDir });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: rollback
if (command === 'rollback') {
  const { target, remaining } = parseTargetAndArgs(args);
  const targetDir = path.resolve(cwd, target);
  const scriptPath = path.join(targetDir, '.torusguard', 'scripts', 'apply_runner.py');
  const fallbackScript = path.join(rootDir, '.torusguard', 'scripts', 'apply_runner.py');
  const actualScript = fs.existsSync(fallbackScript) ? fallbackScript : scriptPath;

  const proc = spawnSync(pythonCmd, [actualScript, targetDir, '--rollback', ...remaining], { stdio: 'inherit', cwd: targetDir });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: recheck / verify
if (command === 'recheck' || command === 'verify') {
  const { target, remaining } = parseTargetAndArgs(args);
  const targetDir = path.resolve(cwd, target);
  const scriptPath = path.join(targetDir, '.torusguard', 'scripts', 'recheck_runner.py');
  const fallbackScript = path.join(rootDir, '.torusguard', 'scripts', 'recheck_runner.py');
  const actualScript = fs.existsSync(fallbackScript) ? fallbackScript : scriptPath;

  const proc = spawnSync(pythonCmd, [actualScript, targetDir, ...remaining], { stdio: 'inherit', cwd: targetDir });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: recipes
if (command === 'recipes') {
  const { target, remaining } = parseTargetAndArgs(args);
  const targetDir = path.resolve(cwd, target);
  const scriptPath = path.join(targetDir, '.torusguard', 'scripts', 'recipes_runner.py');
  const fallbackScript = path.join(rootDir, '.torusguard', 'scripts', 'recipes_runner.py');
  const actualScript = fs.existsSync(fallbackScript) ? fallbackScript : scriptPath;

  const proc = spawnSync(pythonCmd, [actualScript, targetDir, ...remaining], { stdio: 'inherit', cwd: targetDir });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: init (scaffold workspace)
if (command === 'init') {
  const { target, remaining } = parseTargetAndArgs(args);
  const targetDir = path.resolve(cwd, target);
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }
  const localBootstrap = path.join(rootDir, 'skills', 'torusguard', 'bootstrap.py');
  const localInstall = path.join(rootDir, 'install.py');
  const scriptToRun = fs.existsSync(localBootstrap) ? localBootstrap : localInstall;

  const scriptArgs = [scriptToRun, '--full-commands', '--target', targetDir, ...remaining];
  const proc = spawnSync(pythonCmd, scriptArgs, {
    stdio: 'inherit',
    cwd: targetDir,
  });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Subcommand: update
if (command === 'update') {
  const https = require('https');
  const currentVersion = PKG_VERSION;

  console.log();
  console.log(cardHeader('🛡️  TORUSGUARD UPDATE CHECK', 'Package Distribution & Registry Verifier', `v${currentVersion}`));
  console.log(`\n  ${DIM}Checking npm registry for updates...${RESET}`);

  const autoInstall = args.includes('--install') || args.includes('-i') || args.includes('--yes') || args.includes('-y');

  function printUpdateOffline(reason) {
    console.log();
    console.log(cardBorderTop('Offline / Registry Unreachable', YELLOW));
    console.log(formatBoxLine(`Current:    ${WHITE}v${currentVersion}${RESET}`, 67, '│', YELLOW));
    console.log(formatBoxLine(`Notice:     ${DIM}${reason}${RESET}`, 67, '│', YELLOW));
    console.log(formatBoxLine(`Manual:     ${BOLD}${CYAN}npm update torusguard${RESET} or ${BOLD}${CYAN}npm i -g torusguard@latest${RESET}`, 67, '│', YELLOW));
    console.log(cardBorderBottom(YELLOW));
    console.log();
    process.exit(0);
  }

  const req = https.get('https://registry.npmjs.org/torusguard/latest', {
    headers: { 'User-Agent': `torusguard-cli/${currentVersion}` },
    timeout: 6000
  }, (res) => {
    let raw = '';
    res.on('data', chunk => raw += chunk);
    res.on('end', () => {
      try {
        const data = JSON.parse(raw);
        const latestVersion = data.version;
        if (!latestVersion) {
          printUpdateOffline('No version field returned in npm registry response');
          return;
        }

        const isNewer = compareSemver(latestVersion, currentVersion) > 0;
        console.log();
        console.log(cardBorderTop('Version Telemetry', CYAN));
        console.log(formatBoxLine(`Installed Version: ${WHITE}v${currentVersion}${RESET}`));
        console.log(formatBoxLine(`Latest on NPM:     ${BOLD}${GREEN}v${latestVersion}${RESET}`));
        console.log(cardBorderBottom(CYAN));
        console.log();

        if (isNewer) {
          console.log(cardBorderTop('Update Available', YELLOW, true));
          console.log(formatBoxLine(`${YELLOW}A new version of TorusGuard is available!${RESET}`, 67, '║', YELLOW));
          console.log(formatBoxLine(`Global:  ${BOLD}${WHITE}npm install -g torusguard@latest${RESET}`, 67, '║', YELLOW));
          console.log(formatBoxLine(`Local:   ${BOLD}${WHITE}npm install torusguard@latest${RESET}`, 67, '║', YELLOW));
          console.log(cardBorderBottom(YELLOW, true));
          console.log();

          if (autoInstall) {
            console.log(`  ${CYAN}Auto-installing latest version via npm...${RESET}`);
            const npmProc = spawnSync('npm', ['install', '-g', 'torusguard@latest'], { stdio: 'inherit' });
            if (npmProc.status === 0) {
              console.log(`\n  ${GREEN}✔ Successfully upgraded TorusGuard to v${latestVersion}!${RESET}\n`);
            } else {
              console.error(`\n  ${RED}✖ Failed to auto-install update. Run: npm install -g torusguard@latest${RESET}\n`);
            }
          } else {
            console.log(`  ${DIM}Tip: Run with ${CYAN}npx torusguard update --install${DIM} to auto-upgrade.${RESET}\n`);
          }
        } else {
          console.log(cardBorderTop('Status: Up To Date', GREEN, true));
          console.log(formatBoxLine(`${GREEN}✔ TorusGuard is up to date (v${currentVersion})${RESET}`, 67, '║', GREEN));
          console.log(cardBorderBottom(GREEN, true));
          console.log();
        }
        process.exit(0);
      } catch (err) {
        printUpdateOffline(err.message);
      }
    });
  });

  req.on('error', (err) => printUpdateOffline(err.message));
  req.on('timeout', () => {
    req.destroy();
    printUpdateOffline('npm registry request timed out (6000ms)');
  });
}

// Native & Extended Command Dispatcher with Pure Fallbacks
const EXTENDED_COMMANDS = new Set([
  'ocr-scan', 'container', 'git-mine', 'redos', 'ai-guard',
  'threatmodel', 'benchmark', 'authorize', 'web-validate',
  'exploit-check', 'mcp', 'full', 'review'
]);

if (EXTENDED_COMMANDS.has(command)) {
  const nativeBin = findNativeBinary();
  if (nativeBin) {
    const proc = spawnSync(nativeBin, args, { stdio: 'inherit', cwd });
    process.exit(proc.status !== null ? proc.status : 0);
  }

  // Pure Node/JS Fallback Handlers
  const { target } = parseTargetAndArgs(args);
  const targetDir = path.resolve(cwd, target);

  if (command === 'ocr-scan') {
    const imageExtensions = new Set(['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.tif', '.svg']);
    const ocrSecretPatterns = [
      { id: 'TG-SEC-001', desc: 'Hardcoded API Key / Secret Token', regex: /(api[_-]?key|secret[_-]?key|access[_-]?token|bearer|auth[_-]?token)\s*[:=]\s*["']?([a-zA-Z0-9_\-\.]{12,})["']?/i },
      { id: 'TG-SEC-001', desc: 'OpenAI / Stripe Secret API Key', regex: /\b(sk-(?:live-)?[a-zA-Z0-9_\-\.]{20,})\b/ },
      { id: 'TG-SEC-002', desc: 'AWS Access Key ID', regex: /\b(AKIA[0-9A-Z]{16})\b/ },
      { id: 'TG-SEC-003', desc: 'GitHub Personal Access Token', regex: /\b(ghp_[a-zA-Z0-9]{30,40}|github_pat_[a-zA-Z0-9_]{60,90})\b/ },
      { id: 'TG-SEC-004', desc: 'Database Connection URI with credentials', regex: /(?:postgres(?:ql)?|mysql|mongodb|redis):\/\/[a-zA-Z0-9_\-]+:[^@\s]+@[a-zA-Z0-9_\-\.]+/i },
      { id: 'TG-SEC-005', desc: 'Private Key block header', regex: /-----BEGIN\s+(?:(?:RSA|OPENSSH|EC|DSA)\s+)?(?:PRIVATE\s+)?KEY-----/i },
      { id: 'TG-SEC-007', desc: 'Generic Password / Secret credential assignment', regex: /(password|passwd|pwd)\s*[:=]\s*["']?([^\s"']{6,})["']?/i }
    ];

    let imageFiles = [];
    const stat = fs.existsSync(targetDir) ? fs.statSync(targetDir) : null;
    if (stat && stat.isFile()) {
      imageFiles.push(targetDir);
    } else {
      function findImages(dir) {
        if (!fs.existsSync(dir)) return;
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const e of entries) {
          if (['.git', 'node_modules', '.torusguard', 'vendor'].includes(e.name)) continue;
          const full = path.join(dir, e.name);
          if (e.isDirectory()) findImages(full);
          else if (imageExtensions.has(path.extname(e.name).toLowerCase())) imageFiles.push(full);
        }
      }
      findImages(fs.existsSync(targetDir) ? targetDir : cwd);
    }

    let hasTesseract = false;
    try {
      const tCheck = spawnSync('tesseract', ['--version'], { encoding: 'utf-8' });
      hasTesseract = tCheck.status === 0;
    } catch (e) {}

    const findings = [];
    for (const img of imageFiles.slice(0, 100)) {
      let text = '';
      try {
        const buf = fs.readFileSync(img);
        const printable = buf.toString('latin1').replace(/[^\x20-\x7E\t\n\r]/g, '\n');
        text += printable + '\n';
        if (hasTesseract) {
          const tProc = spawnSync('tesseract', [img, 'stdout', '-l', 'eng'], { encoding: 'utf-8' });
          if (tProc.stdout) text += tProc.stdout + '\n';
        }
      } catch (err) {}

      const rel = path.relative(cwd, img);
      for (const pat of ocrSecretPatterns) {
        const match = pat.regex.exec(text);
        if (match) {
          let red = match[0];
          if (red.length > 40) red = red.slice(0, 37) + '...';
          findings.push(`[${pat.id}] [OCR] ${pat.desc} in ${rel} (Evidence: ${red})`);
        }
      }
    }

    console.log();
    console.log(cardHeader('👁️   OCR VISION & ASSET SCAN', 'First-Principles + Neural Extraction', `v${PKG_VERSION}`));
    console.log(formatBoxLine(`${hasTesseract ? GREEN + 'Engine:' + RESET + ' Neural Tesseract + First-Principles' : YELLOW + 'Engine:' + RESET + ' First-Principles Stream & Chunk Extractor'}`));
    console.log(formatBoxLine(`Scanned:  ${imageFiles.length} image asset(s) in workspace`));
    console.log(cardDivider('Findings'));
    if (findings.length === 0) {
      console.log(formatBoxLine(`${GREEN}✔ Zero leaked secrets detected in image assets.${RESET}`));
    } else {
      findings.forEach(f => console.log(formatBoxLine(f)));
    }
    if (!hasTesseract) {
      console.log(cardDivider('Neural OCR Setup Hint'));
      console.log(formatBoxLine('To enable optical character recognition on screenshots:'));
      console.log(formatBoxLine('Windows: winget install UB-Mannheim.TesseractOCR'));
      console.log(formatBoxLine('macOS:   brew install tesseract'));
      console.log(formatBoxLine('Linux:   sudo apt-get install tesseract-ocr'));
    }
    console.log(cardBorderBottom());
    console.log();
    process.exit(0);
  }

  if (command === 'threatmodel') {
    const strideScript = path.join(rootDir, '.torusguard', 'scripts', 'stride_generator.py');
    const proc = spawnSync(pythonCmd, [strideScript, targetDir], { stdio: 'inherit', cwd: targetDir });
    process.exit(proc.status !== null ? proc.status : 0);
  }

  if (command === 'container') {
    console.log();
    console.log(cardHeader('🐳  CONTAINER AUDIT', 'Dockerfile & Compose Hardening', `v${PKG_VERSION}`));
    const dockerfilePath = path.join(targetDir, 'Dockerfile');
    const composePath = path.join(targetDir, 'docker-compose.yml');
    const cFindings = [];
    if (fs.existsSync(dockerfilePath)) {
      const content = fs.readFileSync(dockerfilePath, 'utf-8');
      if (!/USER\s+[^\s]+/i.test(content) || /USER\s+root/i.test(content)) {
        cFindings.push('[TG-CONT-001] Container runs as root user in Dockerfile');
      }
    }
    if (fs.existsSync(composePath)) {
      const content = fs.readFileSync(composePath, 'utf-8');
      if (/privileged:\s*true/i.test(content)) {
        cFindings.push('[TG-CONT-003] Privileged mode enabled in docker-compose.yml');
      }
    }
    if (cFindings.length === 0) {
      console.log(formatBoxLine(`${GREEN}✔ Zero container vulnerabilities detected.${RESET}`));
    } else {
      cFindings.forEach(f => console.log(formatBoxLine(f)));
    }
    console.log(cardBorderBottom());
    console.log();
    process.exit(0);
  }

  // Fallback for git-mine, redos, ai-guard, full, review
  console.log(`\n  ${CYAN}Running ${command} via TorusGuard engine...${RESET}`);
  const pyAudit = path.join(rootDir, '.torusguard', 'scripts', 'audit_runner.py');
  const proc = spawnSync(pythonCmd, [pyAudit, targetDir, `--rule-family=${command.toUpperCase()}`], { stdio: 'inherit', cwd: targetDir });
  process.exit(proc.status !== null ? proc.status : 0);
}

// Unknown command fallback
const KNOWN_COMMANDS = new Set([
  'init', 'status', 'rules', 'memory', 'diff-guard', 'audit',
  'report', 'harden', 'apply', 'rollback', 'recheck', 'verify',
  'recipes', 'update', 'help', '--help', '-h', '--version', '-v', 'version',
  'ocr-scan', 'container', 'git-mine', 'redos', 'ai-guard',
  'threatmodel', 'benchmark', 'authorize', 'web-validate',
  'exploit-check', 'mcp', 'full', 'review'
]);

if (!KNOWN_COMMANDS.has(command)) {
  console.error(`\n  ${RED}✖ Unknown command:${RESET} ${WHITE}${command}${RESET}`);
  console.error(`  Run ${GREEN}npx torusguard help${RESET} for available commands.\n`);
  process.exit(1);
}
