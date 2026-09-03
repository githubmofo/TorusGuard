#!/usr/bin/env python3
"""
TorusGuard v0.9.2 Dual-Track Architecture Validation Suite
Tests:
  1. Track 1: Universal AI Skill in-memory autonomy (zero .torusguard dependency)
  2. Track 2: NPM Package scaffolding, full command registration (/torusguard-*)
  3. Track 3: Dual-track coexistence and token budgets (1,000–1,500 tokens)
Pure Python 3.10+ (zero external dependencies).
"""

import sys
import os
import json
import tempfile
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / ".torusguard" / "scripts"
SKILL_DIR = ROOT_DIR / "skills" / "torusguard"


def test_dual_track_architecture():
    print("=" * 80)
    print("TORUSGUARD v0.9.2 DUAL-TRACK ARCHITECTURE TEST SUITE")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. Test Track 1: Universal Autonomous AI Skill (Zero-Footprint Mode)
    # -------------------------------------------------------------------------
    print("\n--- 1. Testing Track 1: Universal AI Agent Skill ---")
    skill_file = SKILL_DIR / "SKILL.md"
    assert skill_file.is_file(), "Missing skills/torusguard/SKILL.md"
    skill_content = skill_file.read_text(encoding="utf-8")

    assert "Workspace Bootstrap Check" in skill_content, "Missing Workspace Bootstrap Check in SKILL.md"
    assert "Autonomous AI Mode" in skill_content or "Autonomous" in skill_content, "Missing Autonomous AI mode handling"
    assert "npx torusguard init" in skill_content, "Missing upgrade guidance to npx torusguard init"

    # Verify line count constraint for skill
    skill_lines = skill_content.splitlines()
    assert len(skill_lines) <= 60, f"SKILL.md exceeds 60 lines: {len(skill_lines)}"
    print(f"  [PASS] Universal Skill is concise ({len(skill_lines)} lines) and handles standalone operation")

    # -------------------------------------------------------------------------
    # 2. Test Track 2: NPM Package Scaffolding & Command Registration
    # -------------------------------------------------------------------------
    print("\n--- 2. Testing Track 2: NPM Package Scaffolding & Command Expansion ---")
    package_json_file = ROOT_DIR / "package.json"
    assert package_json_file.is_file(), "Missing root package.json"
    pkg_data = json.loads(package_json_file.read_text(encoding="utf-8"))
    assert pkg_data.get("name") == "torusguard", f"Invalid package name: {pkg_data.get('name')}"
    assert pkg_data.get("version") in ("0.9.2", "0.9.3"), f"Invalid version: {pkg_data.get('version')}"
    assert "bin" in pkg_data and "torusguard" in pkg_data["bin"], "Missing bin.torusguard entry"
    print("  [PASS] package.json verified (name: torusguard, version: 0.9.3, bin configured)")

    cli_file = ROOT_DIR / "bin" / "torusguard.js"
    assert cli_file.is_file(), "Missing bin/torusguard.js CLI runner"

    # Test running CLI status
    res_status = subprocess.run(["node", str(cli_file), "status"], capture_output=True, text=True)
    assert res_status.returncode == 0, f"CLI status failed: {res_status.stderr}"
    assert "TORUSGUARD ACTIVE POSTURE STATUS" in res_status.stdout
    assert ("0.9.2" in res_status.stdout or "0.9.3" in res_status.stdout)
    print("  [PASS] bin/torusguard.js status executed cleanly")

    # Test full scaffolding in a clean temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        # Create mock .agents directory as created by npx skills add
        (tmp_path / ".agents").mkdir(parents=True, exist_ok=True)

        bootstrap_script = SKILL_DIR / "bootstrap.py"
        res_scaffold = subprocess.run(
            [sys.executable, str(bootstrap_script), "--target", str(tmp_path), "--force", "--full-commands"],
            capture_output=True,
            text=True
        )
        assert res_scaffold.returncode == 0, f"Scaffolding failed: {res_scaffold.stderr}"

        # Assert .torusguard was formed
        assert (tmp_path / ".torusguard").is_dir(), ".torusguard directory not created"
        assert (tmp_path / ".torusguard" / "config" / "torusguard.json").is_file(), "Missing torusguard.json"

        # Assert all 11 individual slash command files were installed
        wf_dir = tmp_path / ".agents" / "workflows"
        assert wf_dir.is_dir(), "Missing .agents/workflows directory"

        expected_commands = [
            "torusguard.md",
            "torusguard-init.md",
            "torusguard-authorize.md",
            "torusguard-audit.md",
            "torusguard-verify.md",
            "torusguard-web-validate.md",
            "torusguard-exploit-check.md",
            "torusguard-harden.md",
            "torusguard-apply.md",
            "torusguard-recheck.md",
            "torusguard-report.md",
            "torusguard-status.md",
        ]
        for cmd in expected_commands:
            assert (wf_dir / cmd).is_file(), f"Missing individual slash command: {cmd}"
        print(f"  [PASS] Scaffolding created .torusguard/ and unlocked all {len(expected_commands)} slash commands")

    # -------------------------------------------------------------------------
    # 3. Test Token Budgets (Strictly 1,000–1,500 Tokens)
    # -------------------------------------------------------------------------
    print("\n--- 3. Testing Command Token Budgets (1,000–1,500 Tokens) ---")
    commands = [
        ('init', '.torusguard/workflows/init.md', 'skills/torusguard-init/SKILL.md'),
        ('authorize', '.torusguard/workflows/authorize.md', 'skills/torusguard-authorize/SKILL.md'),
        ('audit', '.torusguard/workflows/audit.md', 'skills/torusguard-audit/SKILL.md'),
        ('verify', '.torusguard/workflows/verify.md', 'skills/torusguard-verify/SKILL.md'),
        ('web-validate', '.torusguard/workflows/web-validate.md', 'skills/torusguard-web-validate/SKILL.md'),
        ('exploit-check', '.torusguard/workflows/exploit-check.md', 'skills/torusguard-exploit-check/SKILL.md'),
        ('harden', '.torusguard/workflows/harden.md', 'skills/torusguard-harden/SKILL.md'),
        ('apply', '.torusguard/workflows/apply.md', 'skills/torusguard-apply/SKILL.md'),
        ('recheck', '.torusguard/workflows/recheck.md', 'skills/torusguard-recheck/SKILL.md'),
        ('report', '.torusguard/workflows/report.md', 'skills/torusguard-report/SKILL.md'),
        ('status', '.torusguard/workflows/status.md', 'skills/torusguard-status/SKILL.md'),
    ]

    for cmd, w_rel, s_rel in commands:
        w_path = ROOT_DIR / w_rel
        s_path = ROOT_DIR / s_rel
        w_tok = len(w_path.read_text(encoding="utf-8")) // 4
        s_tok = len(s_path.read_text(encoding="utf-8")) // 4
        total = w_tok + s_tok
        assert 1000 <= total <= 1500, f"Command {cmd} failed token budget: {total} (expected 1000-1500)"
        print(f"  [PASS] Command /{cmd:<13}: {total} tokens (Workflow: {w_tok} | Skill: {s_tok})")

    print("\n" + "=" * 80)
    print("ALL DUAL-TRACK ARCHITECTURE VALIDATION CHECKS PASSED (100%)")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        test_dual_track_architecture()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected exception: {e}")
        sys.exit(2)
