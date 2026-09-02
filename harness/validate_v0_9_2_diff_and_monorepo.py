#!/usr/bin/env python3
"""
TorusGuard v0.9.2 Feature Validation Suite (Diff Guard & Monorepo Detector)
Validates Content-Aware Diff Safety (diff_guard.py), Monorepo Detector,
Playground Fixtures, and Command Token Budgets (1,000–1,500 tokens).
Pure Python 3.10+ (zero external dependencies).
"""

import sys
import os
import json
from pathlib import Path

import importlib.util

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / ".torusguard" / "scripts"


def _load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit_diff = _load_script("diff_guard", SCRIPTS_DIR / "diff_guard.py").audit_diff
scan_workspace = _load_script("monorepo_detector", SCRIPTS_DIR / "monorepo_detector.py").scan_workspace


def test_v0_9_2_features():
    print("=" * 80)
    print("TORUSGUARD v0.9.2 DIFF GUARD & MONOREPO ENGINE TEST SUITE")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. Test Content-Aware Diff Line Scanner (diff_guard.py)
    # -------------------------------------------------------------------------
    print("\n--- 1. Testing Content-Aware Diff Line Scanner (diff_guard.py) ---")

    clean_diff = """--- a/src/views.py
+++ b/src/views.py
@@ -20,2 +20,2 @@
-def fetch(id):
-    return db.query("SELECT * FROM items WHERE id = " + id)
+def fetch(id, tenant_id):
+    return db.query("SELECT * FROM items WHERE id = %s AND tenant_id = %s", (id, tenant_id))
"""
    res_clean = audit_diff(clean_diff)
    assert res_clean["status"] == "PASSED", f"Clean diff failed: {res_clean}"
    print("  [PASS] Clean unified diff accepted with status PASSED")

    bypass_diff = """--- a/src/auth.py
+++ b/src/auth.py
@@ -15,2 +15,3 @@
 def authenticate_user(token):
+    # TODO: bypass auth check for debugging
+    verify = False
     return True
"""
    res_bypass = audit_diff(bypass_diff)
    assert res_bypass["status"] == "BLOCKED"
    rule_ids = [v["rule_id"] for v in res_bypass["violations"]]
    assert "TG-DIFF-001" in rule_ids, "TG-DIFF-001 bypass not caught"
    print(f"  [PASS] TG-DIFF-001: Caught bypass comments and verify=False ({res_bypass['total_violations']} violations)")

    mock_key = "sk" + "_live_" + "99887766554433221100aabbccdd"
    secret_diff = f"""--- a/src/config.py
+++ b/src/config.py
@@ -5,1 +5,2 @@
-API_KEY = os.environ.get('API_KEY')
+API_KEY = "{mock_key}"
"""
    res_secret = audit_diff(secret_diff)
    assert res_secret["status"] == "BLOCKED"
    rule_ids = [v["rule_id"] for v in res_secret["violations"]]
    assert "TG-DIFF-002" in rule_ids, "TG-DIFF-002 secret ingestion not caught"
    print(f"  [PASS] TG-DIFF-002: Caught live secret injection in patch (+{res_secret['additions_count']})")

    del_tenant_diff = """--- a/src/queries.py
+++ b/src/queries.py
@@ -10,3 +10,2 @@
 def list_orders(user):
-    return Order.objects.filter(tenant=user.tenant).all()
+    return Order.objects.all()
"""
    res_del = audit_diff(del_tenant_diff)
    assert res_del["status"] == "BLOCKED"
    rule_ids = [v["rule_id"] for v in res_del["violations"]]
    assert "TG-DIFF-003" in rule_ids, "TG-DIFF-003 tenant deletion not caught"
    print(f"  [PASS] TG-DIFF-003: Caught unmitigated tenant filter deletion (-{res_del['deletions_count']})")

    # -------------------------------------------------------------------------
    # 2. Test Monorepo Workspace Detector (monorepo_detector.py)
    # -------------------------------------------------------------------------
    print("\n--- 2. Testing Monorepo Workspace Detector ---")
    pg_dir = ROOT_DIR / "demo" / "playground"
    assert pg_dir.is_dir(), "Missing demo/playground directory"

    mono_res = scan_workspace(str(pg_dir))
    assert mono_res["is_monorepo"] is True, "Failed to identify demo/playground as monorepo"
    assert mono_res["package_count"] >= 2, f"Expected >= 2 packages, found {mono_res['package_count']}"

    pkg_names = [p["name"] for p in mono_res["packages"]]
    assert "vulnerable_fastapi" in pkg_names, "Missing vulnerable_fastapi package"
    assert "vulnerable_nextjs" in pkg_names, "Missing vulnerable_nextjs package"

    fastapi_pkg = next(p for p in mono_res["packages"] if p["name"] == "vulnerable_fastapi")
    assert fastapi_pkg["language"] == "python"
    assert fastapi_pkg["framework"] == "fastapi"

    nextjs_pkg = next(p for p in mono_res["packages"] if p["name"] == "vulnerable_nextjs")
    assert nextjs_pkg["language"] == "typescript"
    assert nextjs_pkg["framework"] == "nextjs"
    print(f"  [PASS] Successfully profiled {mono_res['package_count']} packages (FastAPI + Next.js)")

    # -------------------------------------------------------------------------
    # 3. Test Playground Fixtures Quality & Flaw Sinks
    # -------------------------------------------------------------------------
    print("\n--- 3. Testing Playground Fixture Sinks ---")
    fastapi_file = pg_dir / "vulnerable_fastapi" / "main.py"
    assert fastapi_file.is_file(), "Missing main.py in vulnerable_fastapi"
    fa_code = fastapi_file.read_text(encoding="utf-8")
    assert "TG-INPUT-001" in fa_code and "SELECT id" in fa_code
    assert "TG-DB-004" in fa_code and "Invoice" in fa_code
    assert "TG-AGENT-001" in fa_code and "system_prompt" in fa_code
    print("  [PASS] vulnerable_fastapi fixture contains TG-INPUT-001, TG-DB-004, and TG-AGENT-001 sinks")

    nextjs_file = pg_dir / "vulnerable_nextjs" / "actions.ts"
    assert nextjs_file.is_file(), "Missing actions.ts in vulnerable_nextjs"
    nx_code = nextjs_file.read_text(encoding="utf-8")
    assert "TG-CLIENT-001" in nx_code and "SUPABASE_SERVICE_ROLE_KEY" in nx_code
    assert "TG-AUTH-003" in nx_code and "use server" in nx_code
    print("  [PASS] vulnerable_nextjs fixture contains TG-CLIENT-001 and TG-AUTH-003 sinks")

    # -------------------------------------------------------------------------
    # 4. Test New Rule Files in .torusguard/rules/active/
    # -------------------------------------------------------------------------
    print("\n--- 4. Testing Rule Definitions ---")
    active_rules_dir = ROOT_DIR / ".torusguard" / "rules" / "active"
    for r_id in ["TG-DIFF-001", "TG-DIFF-002", "TG-DIFF-003"]:
        rf = active_rules_dir / f"{r_id}.md"
        assert rf.is_file(), f"Missing rule file: {rf}"
        content = rf.read_text(encoding="utf-8")
        assert f"id: {r_id}" in content
        assert "Detection Invariants" in content
        print(f"  [PASS] Verified active rule definition: {r_id}.md")

    # -------------------------------------------------------------------------
    # 5. Test Command Token Budget (1,000–1,500 Tokens)
    # -------------------------------------------------------------------------
    print("\n--- 5. Testing Strict Command Token Budgets (1,000–1,500 Tokens) ---")
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
    print("ALL v0.9.2 FEATURE & SAFETY VALIDATION CHECKS PASSED (100%)")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        test_v0_9_2_features()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected exception: {e}")
        sys.exit(2)
