"""
Validation Harness for TorusGuard v0.8.0 - Part 1 (Foundation & Configuration)
Verifies:
1. Directory skeleton in .torusguard/
2. TORUSGUARD.md master rules file
3. JSON configurations (torusguard.json, slash-commands.json, scope.json)
4. Schema files in .torusguard/schemas/
5. SKILL.md refactor to thin bootstrapper
"""

import sys
import json
from pathlib import Path

def test_part1_foundation():
    root = Path(__file__).resolve().parent.parent
    torusguard_dir = root / ".torusguard"
    
    print("=== TorusGuard v0.8.0 Part 1 Validation ===")
    
    # 1. Check directories
    required_dirs = [
        torusguard_dir / "config",
        torusguard_dir / "schemas",
        torusguard_dir / "runs",
        torusguard_dir / "rules" / "active",
    ]
    for d in required_dirs:
        assert d.is_dir(), f"Missing required directory: {d}"
        print(f"  [PASS] Directory exists: {d.relative_to(root)}")

    # 2. Check TORUSGUARD.md
    tg_md = torusguard_dir / "TORUSGUARD.md"
    assert tg_md.is_file(), "Missing .torusguard/TORUSGUARD.md"
    content = tg_md.read_text(encoding="utf-8")
    assert "trigger: always_on" in content, "Missing always_on trigger in TORUSGUARD.md"
    assert "Command Routing Table" in content, "Missing Command Routing Table in TORUSGUARD.md"
    assert "Agent Role Routing" in content, "Missing Agent Role Routing in TORUSGUARD.md"
    assert "0–100 Confidence Scoring Rubric" in content, "Missing scoring rubric in TORUSGUARD.md"
    print("  [PASS] .torusguard/TORUSGUARD.md master rules verified")

    # 3. Check JSON configurations
    config_file = torusguard_dir / "config" / "torusguard.json"
    assert config_file.is_file(), "Missing torusguard.json"
    with open(config_file, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    assert cfg.get("version") == "0.8.0"
    assert "governance" in cfg
    print("  [PASS] .torusguard/config/torusguard.json is valid v0.8.0 config")

    slash_file = torusguard_dir / "config" / "slash-commands.json"
    assert slash_file.is_file(), "Missing slash-commands.json"
    with open(slash_file, "r", encoding="utf-8") as f:
        slash_data = json.load(f)
    commands = slash_data.get("commands", [])
    assert len(commands) == 11, f"Expected 11 commands in slash-commands.json, got {len(commands)}"
    cmd_names = {c["name"] for c in commands}
    expected_cmds = {
        "/torusguard init",
        "/torusguard authorize",
        "/torusguard audit",
        "/torusguard verify",
        "/torusguard web-validate",
        "/torusguard exploit-check",
        "/torusguard harden",
        "/torusguard apply",
        "/torusguard recheck",
        "/torusguard report",
        "/torusguard status"
    }
    assert cmd_names == expected_cmds, f"Command mismatch: {expected_cmds - cmd_names}"
    print(f"  [PASS] .torusguard/config/slash-commands.json contains all 11 commands")

    scope_file = torusguard_dir / "config" / "scope.json"
    assert scope_file.is_file(), "Missing scope.json"
    with open(scope_file, "r", encoding="utf-8") as f:
        scope_data = json.load(f)
    assert "authorization" in scope_data
    print("  [PASS] .torusguard/config/scope.json is valid scope template")

    # 4. Check schemas
    schema_dir = torusguard_dir / "schemas"
    required_schemas = [
        "finding.schema.json",
        "authorization.schema.json",
        "remediation.schema.json",
        "runtime-evidence.schema.json",
        "confidence.schema.json",
        "evidence.schema.json",
        "provenance.schema.json",
        "retest.schema.json"
    ]
    for sf in required_schemas:
        fp = schema_dir / sf
        assert fp.is_file(), f"Missing schema file: {sf}"
        with open(fp, "r", encoding="utf-8") as f:
            json.load(f)
    print(f"  [PASS] All {len(required_schemas)} schema files verified and valid JSON")

    # 5. Check SKILL.md refactor
    skill_file = root / "skills" / "torusguard" / "SKILL.md"
    assert skill_file.is_file(), "Missing skills/torusguard/SKILL.md"
    skill_lines = skill_file.read_text(encoding="utf-8").splitlines()
    assert len(skill_lines) <= 60, f"SKILL.md expected to be <= 60 lines, got {len(skill_lines)}"
    assert "Workspace Bootstrap Check" in "\n".join(skill_lines), "Missing Bootstrap Check in SKILL.md"
    print(f"  [PASS] skills/torusguard/SKILL.md is a clean bootstrapper ({len(skill_lines)} lines)")

    # 6. Check .gitkeep files
    assert (torusguard_dir / "runs" / ".gitkeep").is_file(), "Missing .torusguard/runs/.gitkeep"
    assert (torusguard_dir / "rules" / "active" / ".gitkeep").is_file(), "Missing .torusguard/rules/active/.gitkeep"
    print("  [PASS] Gitkeep files in runs/ and rules/active/ verified")

    print("\n>>> ALL TORUSGUARD v0.8.0 PART 1 CHECKS PASSED (100%) <<<\n")

if __name__ == "__main__":
    try:
        test_part1_foundation()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected exception: {e}")
        sys.exit(2)
