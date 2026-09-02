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
import subprocess
from pathlib import Path


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


def scaffold_workspace(target_root=None, force=False):
    """Scaffold the .torusguard workspace into the target project root."""
    target_root = Path(target_root or find_project_root()).resolve()
    torusguard_target = target_root / ".torusguard"
    script_dir = Path(__file__).resolve().parent
    payload_dir = script_dir / "payload"

    print("================================================================================")
    print("TORUSGUARD WORKSPACE BOOTSTRAPPER")
    print("================================================================================")
    print(f"Target Directory: {target_root}")
    print(f"Destination:      {torusguard_target}")

    if torusguard_target.exists() and not force:
        print(f"\n[INFO] Workspace already exists at {torusguard_target}")
        config_file = torusguard_target / "config" / "torusguard.json"
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                print(f"Current Version:   {cfg.get('version', 'unknown')}")
                print(f"Severity Minimum:  {cfg.get('severity_threshold', 'medium')}")
            except Exception:
                pass
        print("\nUse --force to re-scaffold or refresh templates.")
        return True

    # 1. Unpack Payload Template
    if payload_dir.is_dir():
        print("\n1. Unpacking bundled offline workspace payload...")
        try:
            if torusguard_target.exists() and force:
                shutil.rmtree(torusguard_target)
            shutil.copytree(
                payload_dir,
                torusguard_target,
                ignore=shutil.ignore_patterns("runs", "*.pyc", "__pycache__", ".git*")
            )
            print("  [SUCCESS] Copied template tree from local skill payload.")
        except Exception as e:
            print(f"  [ERROR] Failed to unpack payload: {e}")
            return False
    else:
        # Fallback: create base structure
        print("\n1. Bundled payload not found. Creating core skeleton...")
        subdirs = [
            "config", "agents", "workflows", "scripts", "templates",
            "schemas", "references", "rules/active", "runs"
        ]
        for s in subdirs:
            (torusguard_target / s).mkdir(parents=True, exist_ok=True)
        print("  [WARN] Bare skeleton created; full assets should be pulled from repository.")

    # 2. Ensure runs and rules/active directories exist
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

    # 3. Stack Detection & Tailoring
    print("\n2. Executing stack detection on target project...")
    stack_detect_script = torusguard_target / "scripts" / "stack_detect.py"
    detected_stack = {"language": "Unknown", "framework": "None", "data_layer": "None", "confidence": "Uncertain"}
    
    if stack_detect_script.exists():
        try:
            res = subprocess.run(
                [sys.executable, str(stack_detect_script), str(target_root), "--json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if res.returncode == 0 and res.stdout.strip():
                detected_stack = json.loads(res.stdout)
                print(f"  [DETECTED] Language:   {detected_stack.get('language')}")
                print(f"  [DETECTED] Framework:  {detected_stack.get('framework')}")
                print(f"  [DETECTED] Data Layer: {detected_stack.get('data_layer')}")
        except Exception as e:
            print(f"  [WARN] Stack detection encountered error: {e}")

    # 4. Update torusguard.json configuration
    config_file = torusguard_target / "config" / "torusguard.json"
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            cfg["detected_stack"] = {
                "language": detected_stack.get("language"),
                "framework": detected_stack.get("framework"),
                "data_layer": detected_stack.get("data_layer")
            }
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
            print("  [SUCCESS] Configured .torusguard/config/torusguard.json")
        except Exception as e:
            print(f"  [WARN] Failed to write stack details to config: {e}")

    # 5. Register Slash Commands for AI IDEs (.agent, .claude, .cursor)
    print("\n3. Registering slash commands with AI IDE environments...")
    registered_ides = []
    tg_workflow_content = """---
description: TorusGuard Autonomous Security Command Engine — run static security audits, authorized runtime web validation, governed remediation, and SARIF exports.
version: 0.9.2
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
    if (target_root / ".agents").exists():
        agents_wf = target_root / ".agents" / "workflows"
        agents_wf.mkdir(parents=True, exist_ok=True)
        (agents_wf / "torusguard.md").write_text(tg_workflow_content, encoding="utf-8")
        registered_ides.append("Antigravity (.agents/workflows/torusguard.md)")

    agent_wf = target_root / ".agent" / "workflows"
    agent_wf.mkdir(parents=True, exist_ok=True)
    (agent_wf / "torusguard.md").write_text(tg_workflow_content, encoding="utf-8")
    registered_ides.append("Antigravity (.agent/workflows/torusguard.md)")

    # Claude Code (.claude/commands)
    claude_dir = target_root / ".claude"
    if claude_dir.exists():
        claude_commands = claude_dir / "commands"
        claude_commands.mkdir(parents=True, exist_ok=True)
        (claude_commands / "torusguard.md").write_text(tg_workflow_content, encoding="utf-8")
        registered_ides.append("Claude Code (.claude/commands/torusguard.md)")

    # Cursor (.cursor/rules)
    cursor_dir = target_root / ".cursor"
    if cursor_dir.exists():
        cursor_rules = cursor_dir / "rules"
        cursor_rules.mkdir(parents=True, exist_ok=True)
        (cursor_rules / "torusguard.mdc").write_text(tg_workflow_content, encoding="utf-8")
        registered_ides.append("Cursor (.cursor/rules/torusguard.mdc)")

    for r in registered_ides:
        print(f"  [REGISTERED] Slash command registered in {r}")

    print("\n================================================================================")
    print("[SUCCESS] TORUSGUARD WORKSPACE SCAFFOLDED SUCCESSFULLY!")
    print("================================================================================")
    print(f"Workspace Path: {torusguard_target}")
    print("\nNext Steps:")
    print("  1. Run `/torusguard audit` in your AI IDE to scan the project.")
    print("  2. Run `/torusguard status` to verify active security posture.")
    print("================================================================================")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TorusGuard Autonomous Workspace Bootstrapper")
    parser.add_argument("--target", type=str, help="Target project root directory")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing workspace")
    args = parser.parse_args()

    success = scaffold_workspace(target_root=args.target, force=args.force)
    sys.exit(0 if success else 1)
