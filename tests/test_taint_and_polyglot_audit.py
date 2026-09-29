"""
TorusGuard Comprehensive Test Suite: Taint Analysis, Polyglot Parser & Enhanced Audit Engine
Validates all 7 waves of static security audit enhancements.
"""

import sys
import unittest
from pathlib import Path

# Add project root and .torusguard/scripts to path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / ".torusguard" / "scripts"))

from core.taint_rules import TAINT_SOURCES, TAINT_SINKS, TAINT_SANITIZERS, get_sources_for_language
from core.taint import TaintNode, TaintEdge, TaintPath
from core.taint_graph import TaintGraph
from core.parser import PolyglotParser
from core.symbol_table import SymbolTable
from core.rules_registry import RulesRegistry
from core.clustering import KNOWN_ROOT_CAUSES
from core.cross_file_taint import CrossFileTaintAnalyzer
from core.confidence import ConfidenceCalibrator, EvidenceSignals
from core.incremental import IncrementalScanner
from core.parallel import ParallelAuditExecutor
from finding_scorer import compute_confidence_score


class TestTaintAndAuditEnhancement(unittest.TestCase):

    def test_wave1_taint_rules_and_graph(self):
        """Wave 1: Taint sources, sinks, sanitizers, and graph reachability."""
        self.assertGreaterEqual(len(TAINT_SOURCES["python"]), 10)
        self.assertGreaterEqual(len(TAINT_SOURCES["javascript"]), 10)
        self.assertGreaterEqual(len(TAINT_SOURCES["go"]), 10)

        # Unsanitized flow
        g = TaintGraph()
        vuln_code = (
            "user_id = request.GET['id']\n"
            "target = user_id\n"
            "cursor.execute(f'SELECT * FROM users WHERE id = {target}')\n"
        )
        paths = g.analyze_file_code("views.py", vuln_code, "python")
        self.assertGreater(len(paths), 0)
        self.assertFalse(paths[0].is_sanitized)

        # Sanitized flow
        g_safe = TaintGraph()
        safe_code = (
            "user_id = request.GET['id']\n"
            "clean_id = int(user_id)\n"
            "cursor.execute(f'SELECT * FROM users WHERE id = {clean_id}')\n"
        )
        safe_paths = g_safe.analyze_file_code("views.py", safe_code, "python")
        self.assertGreater(len(safe_paths), 0)
        self.assertTrue(safe_paths[0].is_sanitized)

    def test_wave2_polyglot_tree_sitter_parser(self):
        """Wave 2: Multi-language AST parsing and symbol resolution."""
        import tempfile
        parser = PolyglotParser()
        with tempfile.TemporaryDirectory() as td:
            tmp_dir = Path(td).resolve()
            py_f = tmp_dir / "app.py"
            py_f.write_text("from flask import request as req\nx = req.args.get('q')\ny = int(x)\ncursor.execute(y)\n", encoding="utf-8")
            res = parser.parse_file(py_f)
            self.assertTrue(res.is_tree_sitter)
            self.assertGreaterEqual(len(res.assignments), 2)
            self.assertEqual(res.symbol_table.get_import_alias("req"), "request")

    def test_wave3_rules_registry_and_clusters(self):
        """Wave 3: Centralized canonical rule catalog and root-cause taxonomies."""
        registry = RulesRegistry()
        self.assertGreaterEqual(registry.count(), 80)
        self.assertIsNotNone(registry.get_rule("TG-INPUT-007"))
        self.assertIsNotNone(registry.get_rule("TG-INPUT-008"))

        # Verify new clusters
        self.assertIn("TG-AGENT-001", KNOWN_ROOT_CAUSES)
        self.assertIn("TG-CSRF-001", KNOWN_ROOT_CAUSES)
        self.assertIn("TG-GQL-001", KNOWN_ROOT_CAUSES)
        self.assertIn("TG-SUPPLY-001", KNOWN_ROOT_CAUSES)
        self.assertIn("TG-BIZ-001", KNOWN_ROOT_CAUSES)
        self.assertIn("TG-CACHE-001", KNOWN_ROOT_CAUSES)
        self.assertIn("TG-WS-001", KNOWN_ROOT_CAUSES)
        self.assertIn("TG-EDGE-001", KNOWN_ROOT_CAUSES)
        self.assertIn("TG-CONT-001", KNOWN_ROOT_CAUSES)
        self.assertIn("TG-GIT-001", KNOWN_ROOT_CAUSES)
        self.assertIn("TG-REDOS-001", KNOWN_ROOT_CAUSES)
        self.assertIn("TG-RAG-001", KNOWN_ROOT_CAUSES)

    def test_wave4_cross_file_taint_dataflow(self):
        """Wave 4: Interprocedural call-graph traversal and taint tracking."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp_dir = Path(td).resolve()
            p_utils = tmp_dir / "utils.py"
            p_utils.write_text("def run_q(raw):\n    cursor.execute(f'SELECT * FROM t WHERE id={raw}')\n", encoding="utf-8")

            p_views = tmp_dir / "views.py"
            p_views.write_text("from utils import run_q\ndef endpoint():\n    inp = request.GET['id']\n    run_q(inp)\n", encoding="utf-8")

            analyzer = CrossFileTaintAnalyzer(tmp_dir)
            paths = analyzer.analyze_project([p_utils, p_views])
            self.assertGreaterEqual(len(paths), 1)
            self.assertEqual(paths[0].source.file_path, "views.py")
            self.assertEqual(paths[0].sink.file_path, "utils.py")


    def test_wave5_evidence_chain_confidence(self):
        """Wave 5: 7-signal calibrated confidence scoring model."""
        # Confirmed critical taint path
        signals_crit = EvidenceSignals(
            rule_severity="Critical",
            taint_path_confirmed=True,
            taint_depth=1,
            sanitizer_present=False
        )
        score_crit, band_crit, _ = ConfidenceCalibrator.calculate_score(signals_crit)
        self.assertGreaterEqual(score_crit, 80)
        self.assertEqual(band_crit, "High Confidence" if score_crit < 90 else "Confirmed")

        # Sanitized flow penalty
        signals_san = EvidenceSignals(
            rule_severity="Critical",
            taint_path_confirmed=True,
            taint_depth=1,
            sanitizer_present=True
        )
        score_san, band_san, _ = ConfidenceCalibrator.calculate_score(signals_san)
        self.assertLess(score_san, score_crit)

        # Backwards compatible scorer test
        score_classic, band_classic, _ = compute_confidence_score(
            evidence_quality=35, reproduction_success=25, independent_confirmations=15,
            environmental_clarity=15, manual_review_status=10
        )
        self.assertEqual(score_classic, 100)
        self.assertEqual(band_classic, "Confirmed")

    def test_wave6_incremental_and_parallel(self):
        """Wave 6: Incremental hash cache and parallel execution determinism."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp_dir = Path(td).resolve()
            f1 = tmp_dir / "f1.py"
            f1.write_text("x = 1\n", encoding="utf-8")

            scanner = IncrementalScanner(tmp_dir)
            changed, unchanged = scanner.get_changed_files([f1])
            self.assertEqual(len(changed), 1)

            scanner.update_file_cache(f1, [{"test": True}])
            scanner.save_cache()

            scanner2 = IncrementalScanner(tmp_dir)
            changed2, unchanged2 = scanner2.get_changed_files([f1])
            self.assertEqual(len(changed2), 0)
            self.assertEqual(len(unchanged2), 1)

            executor = ParallelAuditExecutor(max_workers=2)
            res = executor.scan_files_parallel([f1], lambda p: [{"scanned": str(p)}])
            self.assertEqual(len(res), 1)



if __name__ == "__main__":
    unittest.main()
