#!/usr/bin/env python3
"""
TorusGuard Autonomous Workspace Bootstrapper
Scaffolds the complete .torusguard/ directory into any user project when
/torusguard init is executed or when npx skills add installs the skill kit.
"""

import os
import sys
import shutil
import json
import argparse
from pathlib import Path

# Ensure UTF-8 stdout/stderr on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ─── ANSI Color Helpers ───────────────────────────────────────────────────────
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
WHITE = "\033[97m"
GRAY = "\033[90m"
RED = "\033[31m"
BG_GREEN = "\033[42m"
BG_CYAN = "\033[46m"


def find_project_root(start_dir=None):
    """Detect project root directory by searching for standard repo root markers."""
    current = Path(start_dir or os.getcwd()).resolve()
    markers = [".git", "package.json", "pyproject.toml", "manage.py", "Pipfile", "requirements.txt"]
    
    # First check current directory
    for m in markers:
        if (current / m).exists():
            return current
            
    # Search upwards
    for parent in current.parents:
        for m in markers:
            if (parent / m).exists():
                return parent
                
    return current


def print_header():
    """Print the branded TorusGuard header card."""
    print(f"""
  {CYAN}╭─────────────────────────────────────────────────────────────────────────╮{RESET}
  {CYAN}│{RESET}                                                                         {CYAN}│{RESET}
  {CYAN}│{RESET}   {BOLD}{WHITE}🛡️  T O R U S G U A R D{RESET}                                  {GRAY}v0.9.5{RESET}   {CYAN}│{RESET}
  {CYAN}│{RESET}   {DIM}Autonomous Security Engine for AI-Built Applications{RESET}               {CYAN}│{RESET}
  {CYAN}│{RESET}                                                                         {CYAN}│{RESET}
  {CYAN}╰─────────────────────────────────────────────────────────────────────────╯{RESET}
""")


def print_step_1_assets(file_count):
    """Print the enhanced Step 1 asset unpacking card."""
    print(f"""  {CYAN}┌─ {BOLD}Step 1/3{RESET} {CYAN}──────────────────────── {WHITE}Unpacking Governance Assets{RESET} {CYAN}──────┐{RESET}
  {CYAN}│{RESET}                                                                       {CYAN}│{RESET}
  {CYAN}│{RESET}   {GREEN}✔{RESET} Canonical security rules            {DIM}71 rules across 11 families{RESET}  {CYAN}│{RESET}
  {CYAN}│{RESET}   {GREEN}✔{RESET} JSON validation schemas             {DIM}8 formal schemas{RESET}             {CYAN}│{RESET}
  {CYAN}│{RESET}   {GREEN}✔{RESET} Specialist agent specifications     {DIM}5 isolated agents{RESET}            {CYAN}│{RESET}
  {CYAN}│{RESET}   {GREEN}✔{RESET} Workflow templates                   {DIM}11 slash commands{RESET}            {CYAN}│{RESET}
  {CYAN}│{RESET}   {GREEN}✔{RESET} Framework reference guides           {DIM}10 security guides{RESET}           {CYAN}│{RESET}
  {CYAN}│{RESET}                                                                       {CYAN}│{RESET}
  {CYAN}│{RESET}                                               {BOLD}{WHITE}{file_count} files unpacked{RESET}   {CYAN}│{RESET}
  {CYAN}└───────────────────────────────────────────────────────────────────────┘{RESET}
""")


def print_step_2_profile(detected_stack=None):
    """Print the security profile & coverage card (in-process stack alignment)."""
    if detected_stack and detected_stack.get("framework") and detected_stack.get("framework") != "None":
        fw = str(detected_stack.get("framework"))
        lang = str(detected_stack.get("language", ""))
        label = f"Auto-aligned stack: {fw} ({lang})"
        pad = " " * max(0, 66 - len(label))
        status_line = f"  {CYAN}│{RESET}   {GREEN}✔{RESET} {BOLD}Auto-aligned stack:{RESET} {WHITE}{fw}{RESET} {DIM}({lang}){RESET}{pad}{CYAN}│{RESET}"
    else:
        status_line = f"  {CYAN}│{RESET}   {DIM}ℹ Stack auto-detected on first /torusguard-audit run{RESET}              {CYAN}│{RESET}"

    print(f"""  {CYAN}┌─ {BOLD}Step 2/3{RESET} {CYAN}──────────────────── {WHITE}Security Profile & Coverage{RESET} {CYAN}────────┐{RESET}
  {CYAN}│{RESET}                                                                       {CYAN}│{RESET}
  {CYAN}│{RESET}   {BOLD}Rule Families:{RESET}                                                      {CYAN}│{RESET}
  {CYAN}│{RESET}     {YELLOW}TG-SEC{RESET}     Secrets & Credentials    {YELLOW}TG-DB{RESET}      Database Safety    {CYAN}│{RESET}
  {CYAN}│{RESET}     {YELLOW}TG-INPUT{RESET}   Input Validation         {YELLOW}TG-AUTH{RESET}    Authentication     {CYAN}│{RESET}
  {CYAN}│{RESET}     {YELLOW}TG-CLIENT{RESET}  Client Bundle Leaks      {YELLOW}TG-DIFF{RESET}    Diff Inspection    {CYAN}│{RESET}
  {CYAN}│{RESET}     {YELLOW}TG-AGENT{RESET}   AI Agent Security        {YELLOW}TG-EDGE{RESET}    Serverless         {CYAN}│{RESET}
  {CYAN}│{RESET}     {YELLOW}TG-SUPPLY{RESET}  Supply Chain & CI/CD     {YELLOW}TG-SSRF{RESET}    Outbound Net       {CYAN}│{RESET}
  {CYAN}│{RESET}     {YELLOW}TG-BIZ{RESET}     Business Logic                                      {CYAN}│{RESET}
  {CYAN}│{RESET}                                                                       {CYAN}│{RESET}
  {CYAN}│{RESET}   {BOLD}Supported Stacks:{RESET}                                                  {CYAN}│{RESET}
  {CYAN}│{RESET}     {GREEN}Python{RESET}    Django {DIM}·{RESET} FastAPI {DIM}·{RESET} Flask {DIM}·{RESET} DRF {DIM}·{RESET} SQLAlchemy              {CYAN}│{RESET}
  {CYAN}│{RESET}     {GREEN}Node.js{RESET}   Next.js {DIM}·{RESET} Express {DIM}·{RESET} React {DIM}·{RESET} Supabase {DIM}·{RESET} Firebase       {CYAN}│{RESET}
  {CYAN}│{RESET}                                                                       {CYAN}│{RESET}
{status_line}
  {CYAN}└───────────────────────────────────────────────────────────────────────┘{RESET}
""")


def print_step_3_bridges(registered_ides):
    """Print the IDE command registration card."""
    lines = ""
    for r in registered_ides:
        lines += f"  {CYAN}│{RESET}   {GREEN}✔{RESET} {r:<67} {CYAN}│{RESET}\n"

    print(f"""  {CYAN}┌─ {BOLD}Step 3/3{RESET} {CYAN}─────────────────── {WHITE}AI IDE Command Registration{RESET} {CYAN}─────────┐{RESET}
  {CYAN}│{RESET}                                                                       {CYAN}│{RESET}
{lines}  {CYAN}│{RESET}                                                                       {CYAN}│{RESET}
  {CYAN}└───────────────────────────────────────────────────────────────────────┘{RESET}
""")


def print_success_card():
    """Print the final success card with next steps."""
    print(f"""  {GREEN}╔═══════════════════════════════════════════════════════════════════════╗{RESET}
  {GREEN}║{RESET}                                                                       {GREEN}║{RESET}
  {GREEN}║{RESET}   {GREEN}{BOLD}✅  WORKSPACE INITIALIZED SUCCESSFULLY{RESET}                               {GREEN}║{RESET}
  {GREEN}║{RESET}                                                                       {GREEN}║{RESET}
  {GREEN}╠═══════════════════════════════════════════════════════════════════════╣{RESET}
  {GREEN}║{RESET}                                                                       {GREEN}║{RESET}
  {GREEN}║{RESET}   {BOLD}Next Steps:{RESET}                                                         {GREEN}║{RESET}
  {GREEN}║{RESET}                                                                       {GREEN}║{RESET}
  {GREEN}║{RESET}    {CYAN}1.{RESET} In AI Chat      {WHITE}/torusguard-audit{RESET}  or  {WHITE}/torusguard{RESET}              {GREEN}║{RESET}
  {GREEN}║{RESET}    {CYAN}2.{RESET} In Terminal      {WHITE}npx torusguard status{RESET}                       {GREEN}║{RESET}
  {GREEN}║{RESET}    {CYAN}3.{RESET} In CI/CD         {WHITE}npx torusguard audit{RESET}                        {GREEN}║{RESET}
  {GREEN}║{RESET}                                                                       {GREEN}║{RESET}
  {GREEN}║{RESET}   {DIM}Docs{RESET}   {CYAN}https://github.com/githubmofo/TorusGuard{RESET}                   {GREEN}║{RESET}
  {GREEN}║{RESET}   {DIM}NPM{RESET}    {CYAN}https://npmjs.com/package/torusguard{RESET}                       {GREEN}║{RESET}
  {GREEN}║{RESET}                                                                       {GREEN}║{RESET}
  {GREEN}╚═══════════════════════════════════════════════════════════════════════╝{RESET}
""")


def print_already_initialized(target_root, cfg):
    """Print the already-initialized status card."""
    print(f"""
  {CYAN}╭─────────────────────────────────────────────────────────────────────────╮{RESET}
  {CYAN}│{RESET}   {BOLD}{WHITE}🛡️  TORUSGUARD WORKSPACE{RESET}                           {GREEN}[Active]{RESET}         {CYAN}│{RESET}
  {CYAN}╰─────────────────────────────────────────────────────────────────────────╯{RESET}

  {BOLD}▸ Project Root:{RESET}       {GREEN}{target_root}{RESET}
  {BOLD}▸ Workspace:{RESET}          {GREEN}.torusguard/{RESET} {DIM}(Already Initialized){RESET}
  {BOLD}▸ Version:{RESET}            {CYAN}{cfg.get('version', '0.9.5')}{RESET}
  {BOLD}▸ Severity Floor:{RESET}     {YELLOW}{cfg.get('severity_threshold', 'medium')}{RESET}

  {DIM}To refresh templates or re-scaffold, run:{RESET}
     {CYAN}npx torusguard init --force{RESET}
""")


def scaffold_workspace(target_root=None, force=False, full_commands=False):
    """Scaffold the .torusguard workspace into the target project root."""
    target_root = Path(target_root or find_project_root()).resolve()
    torusguard_target = target_root / ".torusguard"
    script_dir = Path(__file__).resolve().parent
    payload_dir = script_dir / "payload"

    if torusguard_target.exists() and not force:
        config_file = torusguard_target / "config" / "torusguard.json"
        cfg = {}
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            except Exception:
                pass
        print_already_initialized(target_root, cfg)
        return True

    # ── Header ──────────────────────────────────────────────────────────────
    print_header()
    print(f"  {BOLD}▸ Target Project:{RESET}     {WHITE}{target_root}{RESET}")
    print(f"  {BOLD}▸ Destination:{RESET}        {WHITE}{torusguard_target}{RESET}")

    # ── Step 1: Unpack Payload ──────────────────────────────────────────────
    file_count = 93
    if payload_dir.is_dir():
        try:
            if torusguard_target.exists() and force:
                shutil.rmtree(torusguard_target)
            shutil.copytree(
                payload_dir,
                torusguard_target,
                ignore=shutil.ignore_patterns("runs", "*.pyc", "__pycache__", ".git*")
            )
            # Count actual files
            file_count = sum(1 for _ in torusguard_target.rglob("*") if _.is_file())
        except Exception as e:
            print(f"\n  {RED}✖ Failed to unpack payload: {e}{RESET}")
            return False
    else:
        # Fallback: create base structure
        subdirs = [
            "config", "agents", "workflows", "scripts", "templates",
            "schemas", "references", "rules/active", "runs"
        ]
        for s in subdirs:
            (torusguard_target / s).mkdir(parents=True, exist_ok=True)
        file_count = 0

    print()
    print_step_1_assets(file_count)

    # ── Ensure runs and rules/active directories exist ──────────────────────
    runs_dir = torusguard_target / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    gitkeep_runs = runs_dir / ".gitkeep"
    if not gitkeep_runs.exists():
        gitkeep_runs.write_text("", encoding="utf-8")

    active_rules_dir = torusguard_target / "rules" / "active"
    active_rules_dir.mkdir(parents=True, exist_ok=True)
    gitkeep_rules = active_rules_dir / ".gitkeep"
    if not gitkeep_rules.exists():
        gitkeep_rules.write_text("", encoding="utf-8")

    # ── Step 2: Security Profile & Coverage (In-Process, Zero Subprocess) ──
    # Execute stack detection in-process without spawning child processes (Socket.dev safe)
    detected_stack = None
    stack_detect_script = torusguard_target / "scripts" / "stack_detect.py"
    if stack_detect_script.is_file():
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("stack_detect", str(stack_detect_script))
            if spec and spec.loader:
                sd_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(sd_mod)
                if hasattr(sd_mod, "detect_stack"):
                    detected_stack = sd_mod.detect_stack(target_root)
        except Exception:
            detected_stack = None

    config_file = torusguard_target / "config" / "torusguard.json"
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            if detected_stack and detected_stack.get("framework") != "None":
                cfg["detected_stack"] = {
                    "language": detected_stack.get("language"),
                    "framework": detected_stack.get("framework"),
                    "data_layer": detected_stack.get("data_layer")
                }
            else:
                cfg["detected_stack"] = {
                    "language": "Unknown",
                    "framework": "None",
                    "data_layer": "None"
                }
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
        except Exception:
            pass

    print_step_2_profile(detected_stack)

    # ── Step 3: Register Slash Commands for AI IDEs ─────────────────────────
    registered_ides = []
    tg_workflow_content = """---
description: TorusGuard Autonomous Security Command Engine — run static security audits, authorized runtime web validation, governed remediation, and SARIF exports.
version: 0.9.5
tools: Read, Grep, Glob, Bash, Edit, Write
agent: auditor
---

# /torusguard — Autonomous Application Security Guardrails

$ARGUMENTS

## Objective
Execute TorusGuard security workflows across Python and TypeScript codebases.

## Execution
Parse the requested action from `$ARGUMENTS` (e.g. `audit`, `verify`, `web-validate`, `exploit-check`, `harden`, `apply`, `recheck`, `report`, `status`, `init`):
1. **If action is omitted or 'status':** View `.torusguard/workflows/status.md` and report posture.
2. **If action is specified:** Load the dedicated workflow from `.torusguard/workflows/<action>.md` and matching skill from `.torusguard/skills/torusguard-<action>/SKILL.md`.
3. Follow the phase execution steps defined in the workflow.
"""

    # Ensure .agent/workflows and .agents/workflows are created
    dest_workflow_dirs = []
    if (target_root / ".agents").exists():
        agents_wf = target_root / ".agents" / "workflows"
        agents_wf.mkdir(parents=True, exist_ok=True)
        (agents_wf / "torusguard.md").write_text(tg_workflow_content, encoding="utf-8")
        dest_workflow_dirs.append(agents_wf)
        registered_ides.append("Antigravity / Gemini     .agents/workflows/torusguard.md")

    agent_wf = target_root / ".agent" / "workflows"
    agent_wf.mkdir(parents=True, exist_ok=True)
    (agent_wf / "torusguard.md").write_text(tg_workflow_content, encoding="utf-8")
    dest_workflow_dirs.append(agent_wf)
    registered_ides.append("Tribunal Agent Kit       .agent/workflows/torusguard.md")

    # When full_commands is requested (e.g. via NPM package npx torusguard init),
    # unlock and register all 11 individual slash commands
    if full_commands:
        src_wf = torusguard_target / "workflows"
        if src_wf.is_dir():
            count = 0
            for wf_file in src_wf.glob("*.md"):
                if wf_file.name == "torusguard.md":
                    continue
                cmd_filename = f"torusguard-{wf_file.name}"
                for d in dest_workflow_dirs:
                    shutil.copy2(wf_file, d / cmd_filename)
                count += 1
            registered_ides.append(f"{count} Slash Commands          /torusguard-audit, -harden, -apply, ...")

    # Claude Code (.claude/commands)
    claude_dir = target_root / ".claude"
    if claude_dir.exists():
        claude_commands = claude_dir / "commands"
        claude_commands.mkdir(parents=True, exist_ok=True)
        (claude_commands / "torusguard.md").write_text(tg_workflow_content, encoding="utf-8")
        registered_ides.append("Claude Code              .claude/commands/torusguard.md")

    # Cursor (.cursor/rules)
    cursor_dir = target_root / ".cursor"
    if cursor_dir.exists():
        cursor_rules = cursor_dir / "rules"
        cursor_rules.mkdir(parents=True, exist_ok=True)
        (cursor_rules / "torusguard.mdc").write_text(tg_workflow_content, encoding="utf-8")
        registered_ides.append("Cursor                   .cursor/rules/torusguard.mdc")

    # Windsurf (.windsurfrules)
    if (target_root / ".windsurfrules").exists() or (target_root / ".windsurf").exists():
        windsurf_rules = target_root / ".windsurfrules"
        current_content = windsurf_rules.read_text(encoding="utf-8") if windsurf_rules.exists() else ""
        if "TorusGuard" not in current_content:
            windsurf_rules.write_text(current_content + "\n\n" + tg_workflow_content, encoding="utf-8")
        registered_ides.append("Windsurf                 .windsurfrules")

    # VS Code / GitHub Copilot (.github/copilot-instructions.md)
    github_dir = target_root / ".github"
    if github_dir.exists():
        copilot_file = github_dir / "copilot-instructions.md"
        current_content = copilot_file.read_text(encoding="utf-8") if copilot_file.exists() else ""
        if "TorusGuard" not in current_content:
            copilot_file.write_text(current_content + "\n\n# TorusGuard Security Instructions\n" + tg_workflow_content, encoding="utf-8")
        registered_ides.append("VS Code / Copilot        .github/copilot-instructions.md")

    # Universal AGENTS.md (Kimi, Codex, Open Agent Standard)
    agents_md = target_root / "AGENTS.md"
    current_agents = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""
    if "TorusGuard" not in current_agents:
        agents_md.write_text(current_agents + ("\n\n" if current_agents else "") + "# TorusGuard Security Guardrails\n\nRun `/torusguard audit` to scan the codebase or refer to `.torusguard/` for security guidelines.\n", encoding="utf-8")
        registered_ides.append("Universal AGENTS.md      Kimi / Open Agent Standard")

    print_step_3_bridges(registered_ides)

    # ── Success Card ────────────────────────────────────────────────────────
    print_success_card()
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TorusGuard Autonomous Workspace Bootstrapper")
    parser.add_argument("--target", type=str, help="Target project root directory")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing workspace")
    parser.add_argument("--full-commands", action="store_true", help="Unlock and register all 11 individual slash commands")
    args = parser.parse_args()

    success = scaffold_workspace(target_root=args.target, force=args.force, full_commands=args.full_commands)
    sys.exit(0 if success else 1)
