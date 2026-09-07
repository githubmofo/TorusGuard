#!/usr/bin/env python3
"""
TorusGuard v1.2.0 Rules Auto-Sync & Visual HTML Report Test Suite
Validates:
1. AI IDE Rules non-destructive sync (.cursorrules, CLAUDE.md, .agent/rules/torusguard.md, .windsurfrules)
2. Marker idempotency and preservation of existing custom user rules
3. Prompt token budget compliance (overhead <= 400 tokens)
4. Format target selection (cursor, claude, agent, windsurf, all)
5. Standalone single-file HTML dashboard generation
6. Zero external HTTP/CDN references (100% air-gapped / offline compliant)
7. SVG posture score gauge calculation and rendering
8. 7-stage closed-loop pipeline visualization
9. CLI subcommand orchestration via bin/torusguard.js
"""

import sys
import json
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import Any

# Ensure UTF-8 stdout/stderr on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / ".torusguard" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import rules_sync  # type: ignore
import html_reporter  # type: ignore


def test_v1_2_0_rules_and_html():
    print("=" * 80)
    print("TORUSGUARD v1.2.0 RULES AUTO-SYNC & HTML REPORT TEST SUITE")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as tmp_dir:
        test_root = Path(tmp_dir).resolve()
        tg_dir = test_root / ".torusguard"
        memory_dir = tg_dir / "memory"
        runs_dir = tg_dir / "runs"
        config_dir = tg_dir / "config"

        memory_dir.mkdir(parents=True, exist_ok=True)
        runs_dir.mkdir(parents=True, exist_ok=True)
        config_dir.mkdir(parents=True, exist_ok=True)

        # Setup mock torusguard.json config
        mock_config: dict[str, Any] = {
            "version": "1.2.0",
            "detected_stack": {
                "language": "Python",
                "framework": "FastAPI",
                "data_layer": "SQLAlchemy"
            },
            "severity_threshold": "medium"
        }
        (config_dir / "torusguard.json").write_text(json.dumps(mock_config, indent=2), encoding="utf-8")

        # Setup mock memory state
        mock_profile: dict[str, Any] = {
            "stack": ["Python", "FastAPI", "SQLAlchemy"],
            "total_events": 12,
            "fix_rate_percentage": 92.5,
            "active_patterns_count": 3
        }
        (memory_dir / "profile.json").write_text(json.dumps(mock_profile, indent=2), encoding="utf-8")

        mock_patterns: list[dict[str, Any]] = [
            {
                "pattern_id": "pat-golden-01",
                "pattern_type": "golden_fix_recipe",
                "rule_id": "TG-SEC-001",
                "description": "Replace os.environ secret fallback with env file",
                "recipe_data": {
                    "diff_snippet": "- API_KEY = os.environ.get('SECRET', 'fallback')\n+ API_KEY = os.environ['SECRET']",
                    "before_snippet": "API_KEY = os.environ.get('SECRET', 'fallback')",
                    "after_snippet": "API_KEY = os.environ['SECRET']",
                    "verified_count": 4,
                    "ponytail_metrics": {"additions": 1, "deletions": 1}
                }
            },
            {
                "pattern_id": "pat-reg-01",
                "pattern_type": "regression_watch",
                "rule_id": "TG-DB-004",
                "description": "Raw string formatting in SQL statement",
                "affected_files": ["src/db/queries.py"],
                "file_type": ".py"
            },
            {
                "pattern_id": "pat-fp-01",
                "pattern_type": "false_positive_class",
                "rule_id": "TG-AUTH-002",
                "description": "Suppressed internal health check route without auth"
            }
        ]
        (memory_dir / "patterns.json").write_text(json.dumps(mock_patterns, indent=2), encoding="utf-8")

        # ---------------------------------------------------------------------
        # 1. AI IDE Rules Auto-Sync: Non-Destructive Injection
        # ---------------------------------------------------------------------
        print("\n--- 1. Testing AI IDE Rules Auto-Sync (Non-Destructive) ---")
        cursor_file = test_root / ".cursorrules"
        custom_user_instructions = "# User's Custom Instructions\n- Always use 2 spaces indentation\n- Prefer functional programming\n"
        cursor_file.write_text(custom_user_instructions, encoding="utf-8")

        res_all = rules_sync.sync_rules(target_format="all", root_dir=test_root)
        assert res_all["status"] == "success", f"Expected success, got {res_all['status']}"
        assert len(res_all["synced_files"]) == 4, f"Expected 4 synced files, got {len(res_all['synced_files'])}"
        assert res_all["within_budget"] is True, f"Token budget exceeded: {res_all['token_estimate']}"
        assert res_all["token_estimate"] <= 400, f"Overhead {res_all['token_estimate']} > 400 tokens"

        # Verify existing user rules are preserved
        updated_cursor = cursor_file.read_text(encoding="utf-8")
        assert "# User's Custom Instructions" in updated_cursor, "User custom instructions were overwritten!"
        assert "- Always use 2 spaces indentation" in updated_cursor, "User indentation preference lost!"
        assert rules_sync.START_MARKER in updated_cursor, "Start marker missing!"
        assert rules_sync.END_MARKER in updated_cursor, "End marker missing!"
        assert "TG-SEC-001" in updated_cursor, "Golden recipe TG-SEC-001 missing from synced rules!"
        assert "TG-DB-004" in updated_cursor, "Regression watch TG-DB-004 missing from synced rules!"

        print(f"  [PASS] Auto-sync injected 4 targets with ~{res_all['token_estimate']} tokens (budget <= 400).")
        print("  [PASS] Preserved pre-existing user rules in .cursorrules.")

        # ---------------------------------------------------------------------
        # 2. Re-Sync Idempotency
        # ---------------------------------------------------------------------
        print("\n--- 2. Testing Sync Idempotency (No Duplicate Blocks) ---")
        rules_sync.sync_rules(target_format="all", root_dir=test_root)
        recheck_cursor = cursor_file.read_text(encoding="utf-8")
        start_count = recheck_cursor.count(rules_sync.START_MARKER)
        end_count = recheck_cursor.count(rules_sync.END_MARKER)
        assert start_count == 1, f"Expected exactly 1 start marker, found {start_count}"
        assert end_count == 1, f"Expected exactly 1 end marker, found {end_count}"
        print("  [PASS] Idempotent sync verified: exactly 1 set of markers preserved.")

        # ---------------------------------------------------------------------
        # 3. Target Format Filtering
        # ---------------------------------------------------------------------
        print("\n--- 3. Testing Format Target Filtering ---")
        res_claude = rules_sync.sync_rules(target_format="claude", root_dir=test_root)
        assert res_claude["status"] == "success"
        assert len(res_claude["synced_files"]) == 1
        assert "CLAUDE.md" in res_claude["synced_files"][0]
        print("  [PASS] Target filtering ('claude') verified.")

        # ---------------------------------------------------------------------
        # 4. Visual Single-File HTML Posture Report Generation
        # ---------------------------------------------------------------------
        print("\n--- 4. Testing HTML Posture Report Generation ---")
        html_out = runs_dir / "report-test.html"
        res_html = html_reporter.emit_html_report(target_path=html_out, root_dir=test_root)

        assert res_html["status"] == "success", f"Report status failed: {res_html}"
        assert html_out.exists(), f"Output HTML file {html_out} does not exist!"
        assert res_html["file_size_bytes"] > 5000, f"HTML file too small ({res_html['file_size_bytes']} bytes)"
        assert 10 <= res_html["posture_score"] <= 100, f"Invalid posture score: {res_html['posture_score']}"

        html_content = html_out.read_text(encoding="utf-8")

        # Basic HTML structure validation
        assert "<!DOCTYPE html>" in html_content, "Missing DOCTYPE"
        assert "<html" in html_content and "</html>" in html_content, "Missing html tags"
        assert "<svg" in html_content, "Missing SVG gauge markup"
        assert "stroke-dashoffset" in html_content, "Missing SVG gauge circular animation math"

        # 7-Stage closed loop pipeline validation
        assert "Scan" in html_content, "Pipeline Scan stage missing"
        assert "Score" in html_content, "Pipeline Score stage missing"
        assert "Harden" in html_content, "Pipeline Harden stage missing"
        assert "Authorize" in html_content, "Pipeline Authorize stage missing"
        assert "Apply" in html_content, "Pipeline Apply stage missing"
        assert "Recheck" in html_content, "Pipeline Recheck stage missing"
        assert "Report" in html_content, "Pipeline Report stage missing"

        # Content validation
        assert "TG-SEC-001" in html_content, "Golden fix recipe not rendered in HTML"
        assert "TG-DB-004" in html_content, "Regression watch not rendered in HTML"
        assert "TG-AUTH-002" in html_content, "False positive not rendered in HTML"

        print(f"  [PASS] HTML report generated ({res_html['file_size_bytes']} bytes, Posture Score: {res_html['posture_score']}/100).")
        print("  [PASS] 7-Stage closed loop pipeline visualized.")

        # ---------------------------------------------------------------------
        # 5. Zero-External-CDN / Air-Gapped Compliance
        # ---------------------------------------------------------------------
        print("\n--- 5. Testing Zero-External-CDN Air-Gapped Compliance ---")
        assert "http://" not in html_content, "Found non-air-gapped http:// link in HTML report!"
        assert "https://" not in html_content, "Found external https:// CDN or asset link in HTML report!"
        print("  [PASS] 100% self-contained: zero external network/CDN references.")

        # ---------------------------------------------------------------------
        # 6. CLI Node.js Dispatch Integration
        # ---------------------------------------------------------------------
        print("\n--- 6. Testing Node.js CLI Orchestration (bin/torusguard.js) ---")
        cli_path = ROOT_DIR / "bin" / "torusguard.js"
        assert cli_path.exists(), f"CLI path {cli_path} not found"

        # Test CLI: rules sync --json
        cmd_rules = ["node", str(cli_path), "rules", "sync", "--json", "--root", str(test_root)]
        proc_rules = subprocess.run(cmd_rules, capture_output=True, text=True, cwd=str(test_root))
        assert proc_rules.returncode == 0, f"CLI rules sync failed: {proc_rules.stderr}"
        parsed_rules = json.loads(proc_rules.stdout.strip())
        assert parsed_rules.get("status") == "success", f"Invalid CLI output: {parsed_rules}"

        # Test CLI: report --html --json
        cli_html_out = test_root / "cli-report.html"
        cmd_report = ["node", str(cli_path), "report", "--html", "--json", "--out", str(cli_html_out), "--root", str(test_root)]
        proc_report = subprocess.run(cmd_report, capture_output=True, text=True, cwd=str(test_root))
        assert proc_report.returncode == 0, f"CLI report --html failed: {proc_report.stderr}"
        parsed_report = json.loads(proc_report.stdout.strip())
        assert parsed_report.get("status") == "success", f"Invalid CLI report output: {parsed_report}"
        assert cli_html_out.exists(), "CLI output HTML file was not created"

        print("  [PASS] CLI 'npx torusguard rules sync' and 'report --html' dispatches verified.")

    print("\n" + "=" * 80)
    print("ALL v1.2.0 TESTS PASSED (100% SUCCESS)")
    print("=" * 80)


if __name__ == "__main__":
    test_v1_2_0_rules_and_html()
