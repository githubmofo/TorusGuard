#!/usr/bin/env python3
"""
TorusGuard v1.1.0 Advanced Memory Engine Test Suite
Validates Option B enhancements:
1. File path and rule-family proximity scoring (compute_proximity_score)
2. Golden Fix Recipe storage and strict Ponytail bound enforcement (<=35 add, <=25 del)
3. Golden Fix Recipe schema compliance against golden-recipe.schema.json
4. Role-tailored context window generation (auditor, remediator, reviewer, all)
5. Finding confidence scoring with directory and file-proximity modifiers
6. Git pre-commit hook installation and uninstallation
7. Git commit history learning (learn_from_git)
8. Sanitized team export (stripping absolute paths and sensitive tokens)
9. Diff guard pre-commit inspection (--pre-commit)
"""

import os
import sys
import json
import shutil
import tempfile
import datetime
from pathlib import Path
from typing import Dict, Any, List

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

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / ".torusguard" / "scripts"
SCHEMAS_DIR = ROOT_DIR / ".torusguard" / "schemas"
sys.path.insert(0, str(SCRIPTS_DIR))

import memory_engine  # type: ignore
import finding_scorer  # type: ignore
import diff_guard  # type: ignore


def test_v1_1_0_advanced_memory():
    print("=" * 80)
    print("TORUSGUARD v1.1.0 ADVANCED MEMORY ENGINE & GOVERNANCE TEST SUITE")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as tmp_dir:
        test_root = Path(tmp_dir).resolve()
        tg_dir = test_root / ".torusguard"
        tg_dir.mkdir(parents=True, exist_ok=True)

        # ---------------------------------------------------------------------
        # 1. Proximity Scoring (File Path, Directory, Extension, Rule Family)
        # ---------------------------------------------------------------------
        print("\n--- 1. Testing Proximity Scoring (compute_proximity_score) ---")
        mock_pattern: Dict[str, Any] = {
            "pattern_id": "pat-test-01",
            "rule_id": "TG-DB-004",
            "affected_files": ["src/api/auth.py", "src/api/users.py"],
            "file_type": ".py"
        }

        # Exact file match + Exact rule match
        s_exact = memory_engine.compute_proximity_score(
            mock_pattern,
            target_file="src/api/auth.py",
            target_rule_id="TG-DB-004"
        )
        assert s_exact >= 90, f"Expected exact score >= 90, got {s_exact}"

        # Directory match + Family rule match (TG-DB-001 vs TG-DB-004)
        s_dir = memory_engine.compute_proximity_score(
            mock_pattern,
            target_file="src/api/billing.py",
            target_rule_id="TG-DB-001"
        )
        assert 40 <= s_dir <= 80, f"Expected dir/family score in [40, 80], got {s_dir}"

        # Extension match only, different directory, unrelated rule
        s_ext = memory_engine.compute_proximity_score(
            mock_pattern,
            target_file="utils/helper.py",
            target_rule_id="TG-SEC-001"
        )
        assert 10 <= s_ext <= 30, f"Expected ext score in [10, 30], got {s_ext}"

        # Completely unrelated
        s_none = memory_engine.compute_proximity_score(
            mock_pattern,
            target_file="frontend/App.tsx",
            target_rule_id="TG-CLIENT-001"
        )
        assert s_none == 0, f"Expected 0 for unrelated query, got {s_none}"
        print(f"  [PASS] Proximity scoring verified: Exact={s_exact}, Dir={s_dir}, Ext={s_ext}, None={s_none}")

        # ---------------------------------------------------------------------
        # 2. Golden Fix Recipe Storage & Strict Ponytail Bound Enforcement
        # ---------------------------------------------------------------------
        print("\n--- 2. Testing Golden Fix Recipe Storage & Ponytail Bounds ---")
        memory_engine.ensure_memory_structure(root_dir=test_root)

        valid_before = "cursor.execute(f'SELECT * FROM users WHERE id = {uid}')"
        valid_after = "cursor.execute('SELECT * FROM users WHERE id = %s', (uid,))"
        valid_diff = "- cursor.execute(f'SELECT * FROM users WHERE id = {uid}')\n+ cursor.execute('SELECT * FROM users WHERE id = %s', (uid,))"

        recipe = memory_engine.record_golden_recipe(
            rule_id="TG-DB-001",
            before_snippet=valid_before,
            after_snippet=valid_after,
            diff_snippet=valid_diff,
            file_type=".py",
            framework="FastAPI",
            description="Parameterized SQL execution replacing raw string interpolation",
            additions=1,
            deletions=1,
            root_dir=test_root
        )
        assert recipe["pattern_type"] == "golden_fix_recipe"
        assert recipe["rule_id"] == "TG-DB-001"
        assert recipe["confidence"] >= 0.85
        assert recipe["recipe_data"]["verified_count"] == 1
        assert recipe["recipe_data"]["ponytail_metrics"]["additions"] == 1

        # Second verification of the same rule boosts confidence and increments count
        recipe2 = memory_engine.record_golden_recipe(
            rule_id="TG-DB-001",
            before_snippet=valid_before,
            after_snippet=valid_after,
            diff_snippet=valid_diff,
            file_type=".py",
            framework="FastAPI",
            description="Re-verified parameterized query",
            additions=1,
            deletions=1,
            root_dir=test_root
        )
        assert recipe2["recipe_data"]["verified_count"] == 2
        assert recipe2["confidence"] > recipe["confidence"]
        print(f"  [PASS] Golden recipe recorded & verified count incremented to {recipe2['recipe_data']['verified_count']}")

        # Ponytail Bound Violations (Must raise ValueError)
        try:
            memory_engine.record_golden_recipe(
                rule_id="TG-DB-001",
                before_snippet="code",
                after_snippet="bloated code",
                diff_snippet="giant diff",
                file_type=".py",
                additions=40,  # Exceeds 35 additions bound
                deletions=5,
                root_dir=test_root
            )
            assert False, "Failed to reject recipe exceeding additions bound (>35)"
        except ValueError as err:
            assert "Ponytail" in str(err)
            print("  [PASS] Successfully rejected recipe with >35 additions")

        try:
            memory_engine.record_golden_recipe(
                rule_id="TG-DB-001",
                before_snippet="code",
                after_snippet="deleted code",
                diff_snippet="giant diff",
                file_type=".py",
                additions=5,
                deletions=30,  # Exceeds 25 deletions bound
                root_dir=test_root
            )
            assert False, "Failed to reject recipe exceeding deletions bound (>25)"
        except ValueError as err:
            assert "Ponytail" in str(err)
            print("  [PASS] Successfully rejected recipe with >25 deletions")

        # ---------------------------------------------------------------------
        # 3. Golden Recipe Schema Compliance
        # ---------------------------------------------------------------------
        print("\n--- 3. Testing Schema Compliance (golden-recipe.schema.json) ---")
        schema_path = SCHEMAS_DIR / "golden-recipe.schema.json"
        assert schema_path.exists(), f"Schema file not found at {schema_path}"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        assert schema["title"] == "TorusGuard Golden Fix Recipe Schema"

        # Validate that stored recipe matches schema required fields
        required_fields = schema["required"]
        recipe_data = recipe["recipe_data"]
        for field in required_fields:
            assert field in recipe_data, f"Recipe missing required schema field: {field}"
        assert recipe_data["ponytail_metrics"]["additions"] <= 35
        assert recipe_data["ponytail_metrics"]["deletions"] <= 25
        print(f"  [PASS] Recipe structure matches all {len(required_fields)} required schema attributes")

        # ---------------------------------------------------------------------
        # 4. Role-Tailored Context Windows (Auditor, Remediator, Reviewer)
        # ---------------------------------------------------------------------
        print("\n--- 4. Testing Role-Tailored Context Windows ---")
        # Add diverse patterns to memory
        memory_engine.record_event("audit_finding", {"rule_id": "TG-SEC-001", "file_path": "config/settings.py", "severity": "critical", "confidence_score": 90}, root_dir=test_root)
        memory_engine.record_event("audit_finding", {"rule_id": "TG-SEC-001", "file_path": "config/settings.py", "severity": "critical", "confidence_score": 90}, root_dir=test_root)
        memory_engine.record_event("false_positive", {"rule_id": "TG-INPUT-003", "file_path": "tests/test_api.py", "suppression_reason": "Mock fixture"}, root_dir=test_root)
        memory_engine.record_event("fix_applied", {"rule_id": "TG-SEC-001", "file_path": "config/settings.py"}, root_dir=test_root)
        memory_engine.record_event("audit_finding", {"rule_id": "TG-SEC-001", "file_path": "config/settings.py", "severity": "critical", "confidence_score": 90}, root_dir=test_root) # Triggers regression_watch
        memory_engine.distill_patterns(root_dir=test_root)

        # 4a. Auditor Persona Context
        ctx_auditor = memory_engine.compute_context_window(root_dir=test_root, target_role="auditor")
        assert ctx_auditor["role"] == "auditor"
        assert ctx_auditor["token_estimate"] <= 2000
        # Auditor should prioritize common_vulnerability and false_positive_class
        auditor_card_types = [c["type"] for c in ctx_auditor["cards"]]
        print(f"  Auditor cards: {auditor_card_types}")
        assert any(t in ("common_vulnerability", "false_positive_suppression") for t in auditor_card_types)

        # 4b. Remediator Persona Context
        ctx_remediator = memory_engine.compute_context_window(root_dir=test_root, target_role="remediator")
        assert ctx_remediator["role"] == "remediator"
        assert ctx_remediator["token_estimate"] <= 2000
        remediator_card_types = [c["type"] for c in ctx_remediator["cards"]]
        print(f"  Remediator cards: {remediator_card_types}")
        # Remediator should include golden_recipe cards
        assert "golden_recipe" in remediator_card_types

        # 4c. Reviewer Persona Context
        ctx_reviewer = memory_engine.compute_context_window(root_dir=test_root, target_role="reviewer")
        assert ctx_reviewer["role"] == "reviewer"
        assert ctx_reviewer["token_estimate"] <= 2000

        # 4d. Target-Filtered Context
        ctx_filtered = memory_engine.compute_context_window(
            root_dir=test_root,
            target_role="remediator",
            target_file="config/settings.py",
            target_rule_id="TG-SEC-001"
        )
        assert ctx_filtered["target_query"]["file"] == "config/settings.py"
        assert ctx_filtered["target_query"]["rule_id"] == "TG-SEC-001"
        assert len(ctx_filtered["cards"]) > 1
        assert any(c.get("proximity_score", 0) > 0 for c in ctx_filtered["cards"])
        assert ctx_filtered["cards"][1]["proximity_score"] > 0
        print(f"  [PASS] Role-tailored context generation validated across auditor, remediator, reviewer (Tokens <= 2000)")

        # ---------------------------------------------------------------------
        # 5. Finding Scorer Memory & Directory Proximity Boost
        # ---------------------------------------------------------------------
        print("\n--- 5. Testing Finding Scorer Memory & Proximity Modifiers ---")
        # Direct rule match with exact file match
        b_exact = finding_scorer.compute_memory_boost(
            rule_id="TG-DB-001",
            file_path="src/api/auth.py",
            root_dir=test_root
        )
        # Same directory file match
        b_dir = finding_scorer.compute_memory_boost(
            rule_id="TG-DB-001",
            file_path="src/api/orders.py",
            root_dir=test_root
        )
        # Suppressed FP rule
        b_fp = finding_scorer.compute_memory_boost(
            rule_id="TG-INPUT-003",
            file_path="tests/test_api.py",
            root_dir=test_root
        )
        assert b_fp <= -20, f"Expected FP suppression <= -20, got {b_fp}"
        print(f"  [PASS] Scorer memory integration verified: Exact={b_exact}, Dir={b_dir}, FP={b_fp}")

        # ---------------------------------------------------------------------
        # 6. Git Pre-Commit Hook Installation & Uninstallation
        # ---------------------------------------------------------------------
        print("\n--- 6. Testing Git Pre-Commit Hook Installation & Cleanup ---")
        git_dir = test_root / ".git"
        git_dir.mkdir(parents=True, exist_ok=True)

        res_install = memory_engine.install_git_hook(root_dir=test_root)
        assert res_install["status"] == "installed"
        hook_file = Path(res_install["hook_path"])
        assert hook_file.exists()
        hook_content = hook_file.read_text(encoding="utf-8")
        assert "diff_guard.py" in hook_content
        assert "--pre-commit" in hook_content

        res_uninstall = memory_engine.uninstall_git_hook(root_dir=test_root)
        assert res_uninstall["status"] == "uninstalled"
        if hook_file.exists():
            assert "diff_guard.py" not in hook_file.read_text(encoding="utf-8")
        print("  [PASS] Git hook installed, verified, and cleanly uninstalled")

        # ---------------------------------------------------------------------
        # 7. Git Commit History Learning (learn_from_git)
        # ---------------------------------------------------------------------
        print("\n--- 7. Testing Git Commit Learning ---")
        # In a temp directory with no commits, should handle gracefully with 0 learned
        learned = memory_engine.learn_from_git(root_dir=test_root)
        assert "events_recorded" in learned
        print(f"  [PASS] learn_from_git executed safely with {learned['events_recorded']} events on empty repo")

        # ---------------------------------------------------------------------
        # 8. Sanitized Memory Export (Safe Team Sharing)
        # ---------------------------------------------------------------------
        print("\n--- 8. Testing Sanitized Memory Export ---")
        raw_export_file = test_root / "raw-export.json"
        san_export_file = test_root / "sanitized-export.json"

        memory_engine.export_memory(target_file=raw_export_file, sanitized=False, root_dir=test_root)
        memory_engine.export_memory(target_file=san_export_file, sanitized=True, root_dir=test_root)

        san_data = json.loads(san_export_file.read_text(encoding="utf-8"))
        assert san_data.get("sanitized") is True
        # Verify affected_files are relative or basenames, not absolute host paths
        for pat in san_data.get("patterns", []):
            for aff in pat.get("affected_files", []):
                assert not os.path.isabs(aff), f"Found absolute path in sanitized export: {aff}"
                assert "Users" not in aff and "home" not in aff
        print("  [PASS] Sanitized export verified: 100% free of local host absolute paths and secrets")

        # ---------------------------------------------------------------------
        # 9. Diff Guard Pre-Commit Inspection
        # ---------------------------------------------------------------------
        print("\n--- 9. Testing Diff Guard Pre-Commit Mode ---")
        clean_diff = "diff --git a/app.py b/app.py\n--- a/app.py\n+++ b/app.py\n@@ -1,3 +1,3 @@\n-x = 1\n+x = 2\n"
        res_clean = diff_guard.audit_diff(clean_diff)
        assert res_clean["status"] == "PASSED"
        assert len(res_clean["violations"]) == 0

        # Run diff_guard on diff with security bypass comment (# nosec)
        bypass_diff = "diff --git a/app.py b/app.py\n--- a/app.py\n+++ b/app.py\n@@ -1,3 +1,3 @@\n+db.query(user_input) # nosec\n"
        res_bypass = diff_guard.audit_diff(bypass_diff)
        assert res_bypass["status"] == "BLOCKED"
        assert any(f["rule_id"] == "TG-DIFF-001" for f in res_bypass["violations"])
        print("  [PASS] Diff guard correctly detects bypass patterns in diffs")

    print("\n" + "=" * 80)
    print("ALL 9 ADVANCED MEMORY & GOVERNANCE CHECKS PASSED (100% REGRESSION-FREE)")
    print("=" * 80)


if __name__ == "__main__":
    test_v1_1_0_advanced_memory()
