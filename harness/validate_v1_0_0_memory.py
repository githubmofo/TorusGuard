#!/usr/bin/env python3
"""
TorusGuard v1.0.0 Adaptive Security Memory Engine Test Suite
Validates:
1. Memory directory scaffolding & privacy isolation (.gitignore)
2. Event recording across all 6 event types
3. Pattern distillation (amplification & categorization)
4. Pre-computed context window computation (JSON cards & token budget <= 2000)
5. False positive suppression
6. Memory decay (TTL enforcement)
7. Export and Import roundtrip
8. Memory compaction (events archive)
9. Privacy verification (npm tarball & git status)
10. Memory-augmented confidence scoring
11. Content-aware diff regression detection (TG-DIFF-004)
"""

import os
import sys
import json
import shutil
import tempfile
import datetime
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

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / ".torusguard" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import memory_engine  # type: ignore
import finding_scorer  # type: ignore
import diff_guard  # type: ignore


def test_v1_0_0_memory_engine():
    print("=" * 80)
    print("TORUSGUARD v1.0.0 ADAPTIVE SECURITY MEMORY ENGINE TEST SUITE")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as tmp_dir:
        test_root = Path(tmp_dir).resolve()
        tg_dir = test_root / ".torusguard"
        tg_dir.mkdir(parents=True, exist_ok=True)

        # ---------------------------------------------------------------------
        # 1. Test Scaffolding & Memory Directory Structure
        # ---------------------------------------------------------------------
        print("\n--- 1. Testing Memory Scaffolding & Structure ---")
        paths = memory_engine.ensure_memory_structure(root_dir=test_root)
        assert paths["memory"].is_dir(), "Memory directory not created"
        assert paths["events"].is_dir(), "Events directory not created"
        assert paths["gitignore"].is_file(), "Missing memory/.gitignore"
        assert paths["gitignore"].read_text(encoding="utf-8").strip() == "*", "memory/.gitignore must contain *"
        assert paths["patterns"].is_file(), "Missing patterns.json"
        assert paths["context"].is_file(), "Missing context.json"
        assert paths["profile"].is_file(), "Missing profile.json"
        assert paths["decay"].is_file(), "Missing decay.json"
        assert (paths["events"] / ".gitkeep").is_file(), "Missing events/.gitkeep"
        print("  [PASS] Memory directory structure, files, and isolation .gitignore created cleanly")

        # ---------------------------------------------------------------------
        # 2. Test Event Recording Across All 6 Types
        # ---------------------------------------------------------------------
        print("\n--- 2. Testing Event Recording (All 6 Event Types) ---")
        event_types = [
            ("audit_finding", {"rule_id": "TG-DB-004", "file_path": "src/views.py", "line_number": 42, "severity": "high", "confidence_score": 85, "code_hash": "abc123hash"}),
            ("fix_applied", {"rule_id": "TG-DB-004", "file_path": "src/views.py", "line_number": 42, "fix_strategy": "tenant_filter_added"}),
            ("fix_verified", {"rule_id": "TG-DB-004", "file_path": "src/views.py", "verification_result": "fixed"}),
            ("false_positive", {"rule_id": "TG-INPUT-002", "file_path": "tests/mock.py", "suppression_reason": "Test fixture intentional sink"}),
            ("pattern_learned", {"rule_id": "TG-SEC-001", "metadata": {"note": "Learned from manual review"}}),
            ("stack_changed", {"metadata": {"old": "Flask", "new": "FastAPI"}})
        ]

        recorded_events = []
        for etype, edata in event_types:
            evt = memory_engine.record_event(etype, edata, root_dir=test_root)
            assert evt.get("event_type") == etype, f"Recorded wrong type: {etype}"
            assert evt.get("event_id", "").startswith("evt-"), "Missing or invalid event_id"
            assert evt.get("timestamp"), "Missing timestamp"
            assert evt.get("version") in ("1.0.0", memory_engine.VERSION), "Version mismatch in event"
            recorded_events.append(evt)

        all_events = memory_engine.load_all_events(root_dir=test_root)
        assert len(all_events) == 6, f"Expected 6 events, found {len(all_events)}"
        print(f"  [PASS] All 6 event types successfully logged and validated ({len(all_events)} events)")

        # ---------------------------------------------------------------------
        # 3. Test Pattern Distillation & Confidence Amplification
        # ---------------------------------------------------------------------
        print("\n--- 3. Testing Pattern Distillation & Confidence Amplification ---")
        # Add repeated fixes across multiple files to test amplification
        memory_engine.record_event("audit_finding", {"rule_id": "TG-DB-004", "file_path": "src/models.py", "severity": "high"}, root_dir=test_root)
        memory_engine.record_event("fix_applied", {"rule_id": "TG-DB-004", "file_path": "src/models.py", "fix_strategy": "tenant_filter_added"}, root_dir=test_root)
        memory_engine.record_event("fix_verified", {"rule_id": "TG-DB-004", "file_path": "src/models.py", "verification_result": "fixed"}, root_dir=test_root)

        patterns = memory_engine.distill_patterns(root_dir=test_root)
        assert len(patterns) >= 2, f"Expected at least 2 patterns, found {len(patterns)}"

        # Find recurring fix pattern for TG-DB-004
        db_pats = [p for p in patterns if p.get("rule_id") == "TG-DB-004"]
        assert len(db_pats) >= 1, "TG-DB-004 pattern not distilled"
        tg_pat = db_pats[0]
        assert tg_pat.get("occurrences", 0) >= 2, "Expected multiple occurrences"
        assert len(tg_pat.get("affected_files", [])) >= 2, "Expected multi-file tracking"
        assert tg_pat.get("confidence", 0) >= 70, f"Confidence not amplified: {tg_pat.get('confidence')}"
        print(f"  [PASS] Distilled {len(patterns)} patterns with multi-file confidence amplification (Score: {tg_pat.get('confidence')})")

        # ---------------------------------------------------------------------
        # 4. Test Pre-Computed Context Window (JSON Cards & Budget Enforcement)
        # ---------------------------------------------------------------------
        print("\n--- 4. Testing Context Window Generation & Token Budget ---")
        ctx = memory_engine.compute_context_window(max_tokens=2000, root_dir=test_root)
        assert ctx.get("version") in ("1.0.0", memory_engine.VERSION), "Context version mismatch"
        assert ctx.get("token_estimate", 0) <= 2000, "Context exceeds 2000 token budget"
        assert len(ctx.get("cards", [])) >= 2, "Context missing intelligence cards"

        # Check card format: card_id, card_type, priority, title, summary, card_data
        for c in ctx["cards"]:
            assert "card_id" in c and "card_type" in c and "priority" in c
            assert "title" in c and "summary" in c and "card_data" in c
            assert c["card_type"] in ("profile", "pattern", "regression_watch", "false_positive", "false_positive_suppression", "fix_idiom", "common_vulnerability", "golden_recipe")

        print(f"  [PASS] Generated {len(ctx['cards'])} structured JSON cards within budget ({ctx['token_estimate']}/2000 tokens)")

        # ---------------------------------------------------------------------
        # 5. Test False Positive Suppression
        # ---------------------------------------------------------------------
        print("\n--- 5. Testing False Positive Suppression ---")
        fp_evt = memory_engine.record_false_positive("TG-SEC-999", file_path="config/test.py", reason="Mock test token", root_dir=test_root)
        assert fp_evt.get("rule_id") == "TG-SEC-999"

        fp_pats = [p for p in memory_engine.distill_patterns(root_dir=test_root) if p.get("rule_id") == "TG-SEC-999"]
        assert len(fp_pats) == 1, "False positive pattern not found"
        assert fp_pats[0]["pattern_type"] == "false_positive_class"
        print("  [PASS] False positive suppression successfully cataloged into pattern store")

        # ---------------------------------------------------------------------
        # 6. Test Memory Decay (TTL Expiration)
        # ---------------------------------------------------------------------
        print("\n--- 6. Testing Memory Decay (TTL Enforcement) ---")
        # Artificially age a pattern's last_seen and decay_checkpoint by 100 days
        pats = json.loads(paths["patterns"].read_text(encoding="utf-8"))
        old_dt = (datetime.datetime.utcnow() - datetime.timedelta(days=100)).isoformat() + "Z"
        for p in pats:
            if p.get("rule_id") == "TG-DB-004":
                p["last_seen"] = old_dt
                p["decay_checkpoint"] = old_dt
                p["confidence"] = 80
        paths["patterns"].write_text(json.dumps(pats, indent=2), encoding="utf-8")

        decayed = memory_engine.decay_stale_entries(ttl_days=90, root_dir=test_root)
        assert decayed >= 1, f"Expected decay of aged pattern, decayed: {decayed}"

        pats_after = json.loads(paths["patterns"].read_text(encoding="utf-8"))
        db_after = [p for p in pats_after if p.get("rule_id") == "TG-DB-004"][0]
        assert db_after["confidence"] < 80, f"Confidence did not decay: {db_after['confidence']}"
        print(f"  [PASS] Memory decay correctly reduced confidence of 100-day-old pattern ({80} -> {db_after['confidence']})")

        # ---------------------------------------------------------------------
        # 7. Test Export and Import Roundtrip
        # ---------------------------------------------------------------------
        print("\n--- 7. Testing Export and Import Roundtrip ---")
        export_file = test_root / "export_test.json"
        exp_res = memory_engine.export_memory(str(export_file), root_dir=test_root)
        assert export_file.is_file(), "Export file not created"
        assert exp_res["exported_events_count"] > 0, "No events exported"

        with open(export_file, "r", encoding="utf-8") as f:
            exp_data = json.load(f)
        assert exp_data.get("format") == "torusguard-memory-bundle"
        assert len(exp_data.get("events", [])) > 0

        # Import into fresh workspace
        fresh_root = Path(tempfile.mkdtemp()).resolve()
        try:
            imp_res = memory_engine.import_memory(str(export_file), root_dir=fresh_root)
            assert imp_res["imported_events_count"] == exp_res["exported_events_count"]
            fresh_pats = memory_engine.distill_patterns(root_dir=fresh_root)
            assert len(fresh_pats) > 0, "No patterns distilled after import"
            print(f"  [PASS] Export/Import roundtrip verified: {imp_res['imported_events_count']} events transferred cleanly")
        finally:
            shutil.rmtree(fresh_root, ignore_errors=True)

        # ---------------------------------------------------------------------
        # 8. Test Memory Compaction
        # ---------------------------------------------------------------------
        print("\n--- 8. Testing Memory Compaction ---")
        # Artificially age several loose event files by 40 days
        old_ts = (datetime.datetime.utcnow() - datetime.timedelta(days=40)).isoformat() + "Z"
        for evt_f in paths["events"].glob("*.json"):
            if evt_f.name == "compacted_archive.json":
                continue
            try:
                data = json.loads(evt_f.read_text(encoding="utf-8"))
                data["timestamp"] = old_ts
                evt_f.write_text(json.dumps(data, indent=2), encoding="utf-8")
            except Exception:
                pass

        compacted = memory_engine.compact_events(older_than_days=30, root_dir=test_root)
        assert compacted > 0, "No events compacted"
        assert paths["compacted"].is_file(), "Missing compacted_archive.json"
        print(f"  [PASS] Compacted {compacted} aged event files into single archive")

        # ---------------------------------------------------------------------
        # 9. Test Memory-Augmented Finding Scorer
        # ---------------------------------------------------------------------
        print("\n--- 9. Testing Memory-Augmented Finding Scorer ---")
        # Case A: False positive rule should receive negative boost (-30)
        score_fp, band_fp, factors_fp = finding_scorer.compute_confidence_score(
            evidence_quality=35,
            reproduction_success=0,
            independent_confirmations=15,
            environmental_clarity=15,
            rule_id="TG-SEC-999",
            root_dir=test_root
        )
        assert factors_fp["memory_boost"] <= -20, f"False positive was not suppressed: {factors_fp}"
        assert score_fp < 50, f"Suppressed rule score too high: {score_fp}"

        # Case B: Recurring pattern receives positive boost
        score_rec, band_rec, factors_rec = finding_scorer.compute_confidence_score(
            evidence_quality=35,
            reproduction_success=25,
            independent_confirmations=15,
            environmental_clarity=15,
            rule_id="TG-DB-004",
            file_path="src/views.py",
            root_dir=test_root
        )
        assert factors_rec["memory_boost"] >= 10, f"Recurring pattern boost not applied: {factors_rec}"
        print(f"  [PASS] Finding scorer correctly applies memory boost: Suppressed={factors_fp['memory_boost']}pts, Recurring=+{factors_rec['memory_boost']}pts")

        # ---------------------------------------------------------------------
        # 10. Test Diff Guard Regression Detection (TG-DIFF-004)
        # ---------------------------------------------------------------------
        print("\n--- 10. Testing Diff Guard Regression Detection ---")
        # Add regression watch pattern to memory
        memory_engine.record_event("fix_verified", {
            "rule_id": "TG-DB-004",
            "file_path": "src/billing.py",
            "verification_result": "regressed"
        }, root_dir=test_root)
        memory_engine.distill_patterns(root_dir=test_root)

        # Diff modifying src/billing.py
        regression_diff = """--- a/src/billing.py
+++ b/src/billing.py
@@ -12,2 +12,2 @@
-def get_bill(id, tenant):
-    return Bill.objects.filter(id=id, tenant=tenant)
+def get_bill(id):
+    return Bill.objects.get(id=id)
"""
        res_reg = diff_guard.audit_diff(regression_diff, check_memory=True, root_dir=test_root)
        assert res_reg["status"] == "BLOCKED", f"Expected diff to be blocked by regression check: {res_reg}"
        rule_ids = [v["rule_id"] for v in res_reg["violations"]]
        assert "TG-DIFF-004" in rule_ids, f"Expected TG-DIFF-004 violation, got: {rule_ids}"
        print(f"  [PASS] Diff Guard caught TG-DIFF-004 regression on file tracked in memory")

        # ---------------------------------------------------------------------
        # 11. Test Privacy Invariants (.gitignore and NPM pack isolation)
        # ---------------------------------------------------------------------
        print("\n--- 11. Testing Privacy & NPM Pack Isolation ---")
        root_gi = (ROOT_DIR / ".gitignore").read_text(encoding="utf-8")
        assert ".torusguard/memory/" in root_gi, "Root .gitignore missing .torusguard/memory/"

        # Check npm pack does not include memory
        import subprocess
        npm_bin = "npm.cmd" if sys.platform == "win32" else "npm"
        pack_res = subprocess.run([npm_bin, "pack", "--dry-run"], cwd=str(ROOT_DIR), capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert pack_res.returncode == 0, f"npm pack failed: {pack_res.stderr}"
        assert ".torusguard/memory" not in pack_res.stdout and ".torusguard/memory" not in pack_res.stderr, "Memory leaked into npm package!"
        print("  [PASS] Memory directory completely excluded from git and npm release package")

    print("\n" + "=" * 80)
    print(">>> ALL 11 TORUSGUARD v1.0.0 MEMORY ENGINE CHECKS PASSED (100%) <<<")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        test_v1_0_0_memory_engine()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(2)
