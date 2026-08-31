"""
TorusGuard v0.6.0 Governed Remediation Test Suite
Tests:
1. Run Folder System & Manifest Generation
2. Stable Finding Identity Across Line Shifts
3. Root-Cause Clustering across Django, FastAPI, Flask, SQLAlchemy
4. Structured Remediation Bundle Generation
5. Minimal Patch Governance (Line churn, file count, high-risk escalation)
6. Targeted Recheck Status Transitions (Confirmed Fixed, Partially Fixed, Regressed, Needs Manual Review)
7. SARIF v2.1.0 JSON Structured Export
8. End-to-End v0.6.0 Governed Remediation Workflow Execution
"""

import unittest
import tempfile
import shutil
import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.identity import IdentityEngine, FindingFingerprint
from core.clustering import ClusteringEngine, RootCauseCluster
from core.bundle import BundleManager, RemediationBundle
from core.governance import PatchGovernor, PatchPolicyDecision
from core.rechecker import TargetedRechecker, TargetedRecheckResult, RecheckOutcome
from core.run_manager import RunManager
from core.sarif import SarifExporter
from core.v6_workflow import V6Workflow


class TestTorusGuardV060(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="torusguard-v0-6-test-"))

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_run_folder_creation_and_manifest(self):
        """Verify RunManager initializes isolated run folder with all standard artifacts."""
        run_mgr = RunManager(
            base_dir=self.test_dir,
            target_name="django-core",
            command="audit",
            run_id="run-20260831-test-01"
        )
        self.assertTrue(run_mgr.run_path.exists())
        self.assertTrue(run_mgr.logs_dir.exists())
        self.assertTrue(run_mgr.patches_dir.exists())
        self.assertTrue(run_mgr.bundles_dir.exists())

        # Write manifest and verify
        run_mgr.write_manifest(
            status_counts={
                "total_findings": 2,
                "confirmed": 1,
                "high_confidence": 1,
                "needs_review": 0,
                "remediated": 0,
                "verified_fixed": 0,
                "regressed": 0,
            }
        )
        self.assertTrue(run_mgr.manifest_file.exists())
        with open(run_mgr.manifest_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["version"], "v0.6.3")
        self.assertEqual(data["run_id"], "run-20260831-test-01")
        self.assertEqual(data["status_counts"]["total_findings"], 2)

    def test_stable_finding_identity_across_line_shifts(self):
        """Verify Finding Fingerprint remains stable when comments or surrounding lines shift."""
        code_v1 = """
        def get_invoice(request, invoice_id):
            # Fetch invoice directly without tenant filter
            invoice = Invoice.objects.get(id=invoice_id)
            return JsonResponse({"id": invoice.id})
        """
        code_v2_shifted = """
        # Added extra docstring at the top of file
        # Lines shifted down by 10 lines
        def get_invoice(request, invoice_id):
            invoice = Invoice.objects.get(id=invoice_id)
            return JsonResponse({"id": invoice.id})
        """

        fp1 = IdentityEngine.generate_identity(
            rule_id="TG-DB-004",
            file_path="invoices/views.py",
            code_snippet=code_v1,
            sink_signature="Invoice.objects.get",
            framework_marker="django",
        )
        fp2 = IdentityEngine.generate_identity(
            rule_id="TG-DB-004",
            file_path="invoices/views.py",
            code_snippet=code_v2_shifted,
            sink_signature="Invoice.objects.get",
            framework_marker="django",
        )

        self.assertEqual(fp1.fingerprint_id, fp2.fingerprint_id)
        self.assertEqual(fp1.region_hash, fp2.region_hash)
        self.assertTrue(fp1.fingerprint_id.startswith("TG-DB-"))

    def test_root_cause_clustering(self):
        """Verify grouping of disparate findings into systemic root-cause clusters."""
        findings = [
            {
                "finding_id": "fnd-01",
                "rule_id": "TG-DB-004",
                "title": "Missing Tenant Filter",
                "severity": "High",
                "target": {"file_path": "backend/api/users.py", "line_start": 20, "line_end": 25},
            },
            {
                "finding_id": "fnd-02",
                "rule_id": "TG-DB-004",
                "title": "Missing Tenant Filter on Invoices",
                "severity": "Critical",
                "target": {"file_path": "backend/api/invoices.py", "line_start": 45, "line_end": 50},
            },
            {
                "finding_id": "fnd-03",
                "rule_id": "TG-INPUT-006",
                "title": "Unsafe Upload Path",
                "severity": "High",
                "target": {"file_path": "backend/services/uploader.py", "line_start": 12, "line_end": 18},
            }
        ]

        clusters = ClusteringEngine.cluster_findings(findings)
        self.assertEqual(len(clusters), 2)

        cluster_map = {c.cluster_id: c for c in clusters}
        self.assertIn("cluster-tenant-isolation", cluster_map)
        self.assertIn("cluster-path-traversal", cluster_map)

        tenant_cluster = cluster_map["cluster-tenant-isolation"]
        self.assertEqual(len(tenant_cluster.finding_ids), 2)
        self.assertEqual(len(tenant_cluster.affected_files), 2)
        self.assertEqual(tenant_cluster.risk_severity, "Critical")

    def test_remediation_bundle_generation(self):
        """Verify structured remediation bundle creates all 5 expected artifacts."""
        finding = {
            "finding_id": "TG-AUTH-008-abc123",
            "rule_id": "TG-AUTH-008",
            "title": "Untrusted Role Header Injection",
            "severity": "High",
            "target": {"file_path": "middleware/auth.py"},
            "what_is_wrong": "Role is read directly from unauthenticated header X-Role.",
            "why_it_matters": "Allows unprivileged users to escalate to Admin role.",
            "what_should_change": "Derive role from verified JWT session payload.",
            "proposed_diff": "--- a/middleware/auth.py\n+++ b/middleware/auth.py\n@@ -1,2 +1,2 @@\n-role = req.headers.get('X-Role')\n+role = req.user.role\n",
            "verification_steps": "Send X-Role header and assert 403 Forbidden.",
        }

        bundle = BundleManager.create_bundle(finding, cluster_id="cluster-header-trust")
        bundle_dir = bundle.write_to_directory(self.test_dir)

        self.assertTrue((bundle_dir / "finding.md").exists())
        self.assertTrue((bundle_dir / "remediation.md").exists())
        self.assertTrue((bundle_dir / "minimal_patch_plan.md").exists())
        self.assertTrue((bundle_dir / "verify-after-change.md").exists())
        self.assertTrue((bundle_dir / "metadata.json").exists())

        with open(bundle_dir / "metadata.json", "r", encoding="utf-8") as f:
            meta = json.load(f)
        self.assertEqual(meta["bundle_id"], "bundle-TG-AUTH-008-abc123")
        self.assertEqual(meta["cluster_id"], "cluster-header-trust")

    def test_minimal_patch_governance(self):
        """Verify governance policy checks on line churn, file limits, and high-risk escalation."""
        governor = PatchGovernor(max_additions_per_file=15, max_deletions_per_file=10)

        # 1. Clean minimal patch
        clean_diff = """--- a/services/helper.py
+++ b/services/helper.py
@@ -10,3 +10,3 @@
-val = raw_input
+val = sanitize(raw_input)
"""
        decision_clean = governor.evaluate_diff(clean_diff, "services/helper.py")
        self.assertTrue(decision_clean.allowed_auto_apply)
        self.assertFalse(decision_clean.escalation_required)
        self.assertEqual(decision_clean.line_additions, 1)

        # 2. Oversized patch (exceeds line additions)
        oversized_lines = ["--- a/services/helper.py", "+++ b/services/helper.py"]
        for i in range(25):
            oversized_lines.append(f"+line_{i} = True")
        oversized_diff = "\n".join(oversized_lines)

        decision_oversized = governor.evaluate_diff(oversized_diff, "services/helper.py")
        self.assertFalse(decision_oversized.allowed_auto_apply)
        self.assertTrue(any("exceed threshold" in r for r in decision_oversized.rejection_reasons))

        # 3. High-risk context (touching auth file with non-trivial churn)
        high_risk_lines = ["--- a/backend/auth/login.py", "+++ b/backend/auth/login.py"]
        for i in range(12):
            high_risk_lines.append(f"+auth_check_{i}()")
        high_risk_diff = "\n".join(high_risk_lines)

        decision_high_risk = governor.evaluate_diff(high_risk_diff, "backend/auth/login.py")
        self.assertTrue(decision_high_risk.escalation_required)
        self.assertFalse(decision_high_risk.allowed_auto_apply)

    def test_targeted_recheck_outcomes(self):
        """Verify recheck transitions: Confirmed Fixed, Regressed, Needs Manual Review."""
        # 1. Confirmed Fixed
        res_fixed = TargetedRechecker.verify_finding(
            finding_id="fnd-01",
            rule_id="TG-DB-004",
            target_file="models/query.py",
            original_code_snippet="return Model.objects.all()",
            post_fix_code_snippet="return Model.objects.filter(tenant=request.tenant)",
            is_safe_pattern_present=True,
            is_unsafe_pattern_present=False,
        )
        self.assertEqual(res_fixed.outcome, RecheckOutcome.CONFIRMED_FIXED)
        self.assertEqual(len(res_fixed.regressions_detected), 0)

        # 2. Regressed (introduced new vulnerability)
        res_regressed = TargetedRechecker.verify_finding(
            finding_id="fnd-02",
            rule_id="TG-INPUT-006",
            target_file="views/upload.py",
            original_code_snippet="file.save(filename)",
            post_fix_code_snippet="os.system(f'cp {filename} /tmp')",
            is_safe_pattern_present=False,
            is_unsafe_pattern_present=True,
            introduced_new_flaws=["TG-CMD-001: Command Injection in upload handler"],
        )
        self.assertEqual(res_regressed.outcome, RecheckOutcome.REGRESSED)
        self.assertIn("Command Injection", res_regressed.regressions_detected[0])

        # 3. Needs Manual Review
        res_manual = TargetedRechecker.verify_finding(
            finding_id="fnd-03",
            rule_id="TG-WEBHOOK-001",
            target_file="webhooks/receiver.py",
            original_code_snippet="verify_sig()",
            post_fix_code_snippet="verify_sig()",
            requires_manual_context=True,
        )
        self.assertEqual(res_manual.outcome, RecheckOutcome.NEEDS_MANUAL_REVIEW)

    def test_sarif_v210_export(self):
        """Verify valid SARIF v2.1.0 output structure and stable fingerprints."""
        findings = [
            {
                "finding_id": "TG-DB-123456",
                "fingerprint_id": "TG-DB-123456",
                "rule_id": "TG-DB-004",
                "title": "Missing Tenant Query Isolation",
                "severity": "High",
                "confidence_score": 95,
                "confidence_band": "Confirmed",
                "cluster_id": "cluster-tenant-isolation",
                "target": {"file_path": "backend/models.py", "line_start": 40, "line_end": 45},
                "evidence": {"code_snippet": "return self.query()"},
            }
        ]

        sarif_obj = SarifExporter.generate_sarif(findings, tool_version="6.0.0")
        self.assertEqual(sarif_obj["version"], "2.1.0")
        self.assertEqual(len(sarif_obj["runs"]), 1)

        driver = sarif_obj["runs"][0]["tool"]["driver"]
        self.assertEqual(driver["name"], "TorusGuard")
        self.assertEqual(driver["semanticVersion"], "6.0.0")

        result = sarif_obj["runs"][0]["results"][0]
        self.assertEqual(result["ruleId"], "TG-DB-004")
        self.assertEqual(result["level"], "error")
        self.assertEqual(result["fingerprints"]["torusguard/v6/stable_identity"], "TG-DB-123456")

    def test_end_to_end_v6_workflow(self):
        """Verify full end-to-end v6 workflow: audit -> harden -> apply -> recheck."""
        workflow = V6Workflow(
            target_root=self.test_dir,
            output_base=self.test_dir / "runs",
        )

        raw_findings = [
            {
                "rule_id": "TG-INPUT-006",
                "title": "Unsafe File Path Traversal",
                "severity": "High",
                "confidence_score": 92,
                "confidence_band": "Confirmed",
                "target": {"file_path": "uploader.py", "line_start": 10, "line_end": 15},
                "evidence": {"code_snippet": "open(os.path.join(DIR, filename), 'wb')"},
                "what_is_wrong": "Filename from client is not sanitized with secure_filename().",
                "what_should_change": "Sanitize with werkzeug secure_filename.",
                "proposed_diff": "--- a/uploader.py\n+++ b/uploader.py\n@@ -1,2 +1,2 @@\n-path = os.path.join(DIR, filename)\n+path = os.path.join(DIR, secure_filename(filename))\n",
                "verification_steps": "Send ../etc/passwd in filename parameter.",
            }
        ]

        # 1. Audit Phase
        run_mgr = workflow.execute_audit(
            raw_findings=raw_findings,
            target_name="flask-uploader",
            run_id="run-e2e-01",
            export_sarif=True,
        )
        self.assertTrue(run_mgr.manifest_file.exists())
        self.assertTrue(run_mgr.summary_file.exists())
        self.assertTrue(run_mgr.findings_file.exists())
        self.assertTrue(run_mgr.sarif_file.exists())

        # 2. Harden Phase
        with open(run_mgr.manifest_file, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        self.assertEqual(manifest_data["status_counts"]["total_findings"], 1)

        bundles = workflow.execute_harden(run_mgr, raw_findings)
        self.assertEqual(len(bundles), 1)
        self.assertTrue(run_mgr.remediation_file.exists())

        # 3. Apply Phase
        decisions = workflow.execute_apply(run_mgr, bundles)
        self.assertEqual(len(decisions), 1)
        self.assertTrue(decisions[0][1].allowed_auto_apply)
        self.assertTrue(run_mgr.apply_plan_file.exists())
        self.assertTrue(run_mgr.diff_summary_file.exists())
        self.assertTrue(run_mgr.changed_files_file.exists())

        # 4. Recheck Phase
        recheck_scenarios = [
            {
                "finding_id": bundles[0].finding_id,
                "rule_id": "TG-INPUT-006",
                "target_file": "uploader.py",
                "orig_snippet": "path = os.path.join(DIR, filename)",
                "post_snippet": "path = os.path.join(DIR, secure_filename(filename))",
                "is_safe": True,
                "is_unsafe": False,
            }
        ]
        recheck_results = workflow.execute_recheck(run_mgr, recheck_scenarios)
        self.assertEqual(len(recheck_results), 1)
        self.assertEqual(recheck_results[0].outcome, RecheckOutcome.CONFIRMED_FIXED)
        self.assertTrue(run_mgr.recheck_file.exists())


if __name__ == "__main__":
    unittest.main()
