"""
TorusGuard Validation Harness & Engine Runner (v0.5.4)
Executes comprehensive validation engine cycles: deterministic replay, differential comparison, regression tracking, and schema validation.
"""

import os
import sys
import json
import re
import glob
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.models import (
    Finding,
    Evidence,
    Remediation,
    FrameworkPattern,
    AffectedComponent,
    ReproductionMethod,
    RetestRecord,
    NotesRecord,
    FindingTimestamps,
    ProvenanceChain,
    ConfidenceScore,
    ConfidenceFactors,
    ConfidenceBand,
    SeverityLevel,
    SeverityInfo,
    RemediationPriority,
    FindingStatus,
    LifecycleStage,
    TaxonomyCategory,
    EvidenceType,
    AuditReport,
    mask_sensitive_data,
)
from core.lifecycle import FindingLifecycleManager, LifecycleTransitionError
from core.formatter import ReportFormatter

from harness.engine.models import (
    ValidationOutcome,
    FixtureDefinition,
    FixtureVariant,
    ReplayResult,
    ComparisonResult,
    RegressionRecord,
    ValidationRunReport,
)
from harness.engine.fixture_manager import FixtureManager
from harness.engine.replay_runner import ReplayRunner
from harness.engine.comparator import ResultComparator
from harness.engine.regression_tracker import RegressionTracker
from harness.engine.fp_analyzer import FalsePositiveAnalyzer
from harness.engine.evidence_collector import ValidationEvidenceCollector
from harness.engine.report_emitter import ValidationReportEmitter

from core.run_folder import RunFolder


class ValidationHarnessRunner:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.passed_tests = 0
        self.failed_tests = 0
        self.results: List[Dict[str, Any]] = []

    def log_test(self, test_name: str, passed: bool, message: str = ""):
        if passed:
            self.passed_tests += 1
            print(f"  [PASS] {test_name}")
        else:
            self.failed_tests += 1
            print(f"  [FAIL] {test_name}: {message}")
        self.results.append({"name": test_name, "passed": passed, "message": message})

    def run_all(self) -> bool:
        print("=" * 80)
        print("TORUSGUARD v0.5.4 REPORTING USABILITY & VALIDATION HARNESS")
        print("=" * 80)

        self.test_schema_integrity()
        self.test_rule_catalog()
        self.test_skill_definition()
        self.test_confidence_scoring_model()
        self.test_provenance_and_evidence_hashing()
        self.test_sensitive_data_masking()
        self.test_retest_lifecycle_closure()
        self.test_validation_engine_subsystem()
        self.test_stack_detection_fixtures()
        self.test_educational_differential_fixtures()
        self.test_regression_fixtures()
        self.test_report_formatting()
        self.test_run_context_and_ponytail()
        self.test_v6_governed_remediation_suite()

        print("-" * 80)
        print(f"SUMMARY: {self.passed_tests} Passed | {self.failed_tests} Failed")
        print("=" * 80)
        return self.failed_tests == 0

    def test_schema_integrity(self):
        print("\n1. Testing Formal Schema Integrity (v0.5.4)...")
        schemas_dir = self.root_dir / "schemas"
        required_schemas = [
            "finding.schema.json",
            "evidence.schema.json",
            "remediation.schema.json",
            "rule.schema.json",
            "lifecycle.schema.json",
            "provenance.schema.json",
            "confidence.schema.json",
            "retest.schema.json",
            "fixture.schema.json",
            "validation-run.schema.json",
        ]
        for s in required_schemas:
            schema_path = schemas_dir / s
            if not schema_path.exists():
                self.log_test(f"Schema file exists: {s}", False, "File missing")
                continue
            try:
                with open(schema_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                valid = "$schema" in data and "title" in data
                self.log_test(f"Schema valid JSON: {s}", valid, "Missing $schema or title")
            except Exception as e:
                self.log_test(f"Schema valid JSON: {s}", False, str(e))

    def test_rule_catalog(self):
        print("\n2. Testing Rule Catalog & ID Uniqueness...")
        rules_dir = self.root_dir / "rules"
        rule_files = list(rules_dir.glob("**/*.md"))
        rule_ids = {}

        for rf in rule_files:
            if rf.name == "README.md":
                continue
            with open(rf, "r", encoding="utf-8") as f:
                content = f.read()

            match = re.search(r"^(TG-[A-Z0-9]+-[0-9]{3})", rf.name)
            if not match:
                match = re.search(r"#\s+(TG-[A-Z0-9]+-[0-9]{3})", content)

            if match:
                rid = match.group(1)
                if rid in rule_ids:
                    self.log_test(f"Rule ID unique: {rid}", False, f"Duplicate found in {rf.name} and {rule_ids[rid]}")
                else:
                    rule_ids[rid] = rf.name
            else:
                self.log_test(f"Rule ID parseable in {rf.name}", False, "No valid TG-* rule ID found in header")

        self.log_test(f"Total Rules Cataloged ({len(rule_ids)})", len(rule_ids) >= 64, f"Found {len(rule_ids)} rules")

    def test_skill_definition(self):
        print("\n3. Testing Skill Definition & References...")
        skill_file = self.root_dir / "skills" / "TorusGuard" / "SKILL.md"
        if not skill_file.exists():
            self.log_test("SKILL.md exists", False, "Missing skills/TorusGuard/SKILL.md")
            return

        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        has_frontmatter = content.startswith("---") and "name: torusguard" in content
        self.log_test("SKILL.md YAML Frontmatter", has_frontmatter)

        has_commands = all(cmd in content for cmd in ["/torusguard init", "/torusguard audit", "/torusguard harden", "/torusguard apply", "/torusguard verify", "/torusguard recheck"])
        self.log_test("SKILL.md Core Commands Documented (including apply & recheck)", has_commands)

        refs_dir = self.root_dir / "skills" / "TorusGuard" / "references"
        ref_files = list(refs_dir.glob("*.md"))
        self.log_test(f"Skill Reference Modules ({len(ref_files)})", len(ref_files) >= 7)

    def test_confidence_scoring_model(self):
        print("\n4. Testing Auditable Confidence Scoring Model...")
        c_confirmed = ConfidenceScore.calculate(
            evidence_quality=35,
            reproduction_success=25,
            independent_confirmations=15,
            environmental_clarity=15,
            manual_review_status=5,
            rationale="Direct AST match with deterministic reproduction.",
        )
        self.log_test("Confidence calculation: Confirmed band (>= 90)", c_confirmed.score == 95 and c_confirmed.band == ConfidenceBand.CONFIRMED)

        c_high = ConfidenceScore.calculate(
            evidence_quality=30,
            reproduction_success=20,
            independent_confirmations=10,
            environmental_clarity=15,
            manual_review_status=0,
            rationale="Strong static indicator without manual validation.",
        )
        self.log_test("Confidence calculation: High Confidence band (70-89)", c_high.score == 75 and c_high.band == ConfidenceBand.HIGH_CONFIDENCE)

    def test_provenance_and_evidence_hashing(self):
        print("\n5. Testing Provenance Chain & SHA-256 Evidence Integrity...")
        ev = Evidence(
            type=EvidenceType.SOURCE,
            location="server/auth.py:42",
            raw_snippet="SECRET_KEY = 'super_secret_jwt_key'",
            rationale="Hardcoded secret credential.",
            confidence_level=ConfidenceBand.CONFIRMED,
            is_sufficient_for_confirmed=True,
        )
        has_hash = bool(ev.sha256_checksum) and len(ev.sha256_checksum) == 64
        self.log_test("Evidence SHA-256 Checksum Computed", has_hash)

    def test_sensitive_data_masking(self):
        print("\n6. Testing Sensitive Secret & Token Masking...")
        sample_secret = "API_KEY = 'sk_live_998877665544332211'"
        masked = mask_sensitive_data(sample_secret)
        self.log_test("Stripe Secret Key Redaction", "sk_live_***REDACTED***" in masked and "998877665544332211" not in masked)

        sample_jwt = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.doNotLeakSignature"
        masked_jwt = mask_sensitive_data(sample_jwt)
        self.log_test("JWT Token Redaction", "***REDACTED_JWT***" in masked_jwt and "doNotLeakSignature" not in masked_jwt)

    def test_retest_lifecycle_closure(self):
        print("\n7. Testing Retest Execution & Closure State Machine...")
        ev = Evidence(
            type=EvidenceType.SOURCE,
            location="views.py:15",
            raw_snippet="User.objects.raw(f'SELECT * FROM users WHERE name = {name}')",
            rationale="Direct string concatenation into SQL query.",
            confidence_level=ConfidenceBand.CONFIRMED,
            is_sufficient_for_confirmed=True,
        )
        sev = SeverityInfo(
            level=SeverityLevel.CRITICAL,
            rationale="Allows arbitrary SQL execution and data exfiltration.",
            rubric_justification="Critical because unauthenticated user input reaches raw SQL interpreter.",
        )
        conf = ConfidenceScore.calculate(35, 25, 15, 15, 5, "Direct AST concatenation match.")
        prov = ProvenanceChain(
            discovery_module="rules/input/TG-INPUT-002-raw-sql-concatenation.md",
            triggering_input="Raw SQL execution with f-string formatting",
            evidence_collected=["views.py:15"],
            decision_path=["Detected raw SQL method", "Verified unparameterized input"],
            verification_step="Inspect query parameterization.",
        )
        rem = Remediation(
            problem_statement="Raw SQL string concatenation vulnerable to SQL injection.",
            risk_explanation="Attackers can inject malicious SQL payloads.",
            recommended_fix="Use parameterized queries.",
            framework_pattern=FrameworkPattern(
                framework="Django",
                unsafe_snippet="User.objects.raw(f'SELECT * FROM users WHERE name = {name}')",
                safe_snippet="User.objects.raw('SELECT * FROM users WHERE name = %s', [name])",
            ),
            verification_method="Test with quote payload and verify parameterized execution.",
            residual_risk_notes="Ensure database permissions are restricted.",
        )
        finding = Finding(
            rule_id="TG-INPUT-002",
            title="Raw SQL Concatenation",
            category=TaxonomyCategory.INPUT,
            severity=sev,
            confidence=conf,
            status=FindingStatus.CONFIRMED,
            affected_component=AffectedComponent(component_name="UserSearch", target_path="views.py", start_line=15),
            evidence=[ev],
            provenance=prov,
            reproduction_method=ReproductionMethod(step_by_step=["Pass ' OR '1'='1 into search endpoint"], test_command="pytest tests/test_search.py"),
            remediation=rem,
            asvs_control="V5.3.4",
            cwe="CWE-89",
            nist_ssdf="PW.5.1",
        )

        FindingLifecycleManager.transition(finding, LifecycleStage.CLASSIFY)
        FindingLifecycleManager.transition(finding, LifecycleStage.VERIFY)
        FindingLifecycleManager.transition(finding, LifecycleStage.REMEDIATE)

        ok, msg = FindingLifecycleManager.execute_retest(
            finding,
            post_fix_code="User.objects.raw('SELECT * FROM users WHERE name = %s', [name])",
            safe_pattern_verified=True,
            verifier_notes="Verified parameterized binding query.",
        )
        self.log_test("Retest execution -> Verified Fixed", ok and finding.status == FindingStatus.VERIFIED_FIXED)

    def test_validation_engine_subsystem(self):
        print("\n8. Testing Validation Engine Subsystem (v0.5.4)...")
        fm = FixtureManager(str(self.root_dir))
        fixtures = fm.list_fixtures()
        self.log_test(f"Fixture Manager Catalog Loaded ({len(fixtures)} fixtures)", len(fixtures) >= 8)

        rr = ReplayRunner(str(self.root_dir))
        comparator = ResultComparator(str(self.root_dir))
        comparison_results = []

        for f in fixtures:
            replay_res = rr.replay_fixture(f, passes=3)
            self.log_test(f"Deterministic Replay (3 passes): {f.fixture_id}", replay_res.deterministic)

            comp_res = comparator.compare_fixture(f, replay_deterministic=replay_res.deterministic)
            comparison_results.append(comp_res)
            self.log_test(f"Differential Comparison ({comp_res.outcome.value}): {f.fixture_id}", comp_res.diff_verified)

        # Regression tracker
        rt = RegressionTracker(str(self.root_dir))
        reg_records = rt.evaluate_all_regressions()
        all_clean = all(r.regression_status == "Clean" for r in reg_records)
        self.log_test(f"Regression Tracker Verification ({len(reg_records)} baseline cases clean)", all_clean)

        # FP Analyzer
        diagnostics = FalsePositiveAnalyzer.analyze_results(comparison_results)
        self.log_test("False Positive Analyzer Diagnostic Check (0 false alarms)", len(diagnostics) == 0)

        # Evidence Collector & Report Emitter
        collector = ValidationEvidenceCollector(str(self.root_dir))
        env_snap = collector.capture_environment_snapshot()
        self.log_test("Validation Evidence Collector Environment Snapshot", "os" in env_snap and "python_version" in env_snap)

        val_report = ValidationRunReport(
            environment=env_snap,
            fixture_results=comparison_results,
            regression_records=reg_records,
        )
        report_md = ValidationReportEmitter.render_markdown(val_report)
        self.log_test("Validation Report Emitter Markdown Rendering", "# TorusGuard Validation Engine" in report_md and "Execution Summary" in report_md)

    def test_stack_detection_fixtures(self):
        print("\n9. Testing Stack Detection Layouts...")
        stack_dir = self.root_dir / "tests" / "fixtures" / "python" / "stack-detection"
        expected_stacks = [
            "django",
            "django-drf",
            "fastapi",
            "flask",
            "flask-sqlalchemy",
            "python-library",
            "mixed-monorepo",
        ]
        for s in expected_stacks:
            target = stack_dir / s
            exists = target.exists() and any(target.iterdir())
            self.log_test(f"Stack layout fixture: {s}", exists)

    def test_educational_differential_fixtures(self):
        print("\n10. Testing Educational Differential Fixtures...")
        pairs = [
            ("examples/python/django-vuln", "examples/python/django-hardened"),
            ("examples/python/drf-vuln", "examples/python/drf-hardened"),
            ("examples/python/fastapi-vuln", "examples/python/fastapi-hardened"),
            ("examples/python/flask-vuln", "examples/python/flask-hardened"),
            ("examples/python/sqlalchemy-vuln", "examples/python/sqlalchemy-hardened"),
        ]
        for vuln_rel, hard_rel in pairs:
            vuln_path = self.root_dir / vuln_rel
            hard_path = self.root_dir / hard_rel
            exists = vuln_path.exists() and hard_path.exists()
            has_fixes = (hard_path / "fixes.md").exists() or (vuln_path / "README.md").exists()
            self.log_test(f"Paired differential fixture: {Path(vuln_rel).name}", exists and has_fixes)

    def test_regression_fixtures(self):
        print("\n11. Testing Python Regression Fixtures Suite...")
        regression_dir = self.root_dir / "tests" / "fixtures" / "python"
        cases = [
            "django/safe-service-layer-auth",
            "django/missing-owner-scope",
            "drf/safe-read-only-fields",
            "drf/unbounded-pagination",
            "fastapi/safe-pydantic-boundary",
            "fastapi/unsafe-outbound-url",
            "flask/csrf-enabled",
            "flask/unsafe-upload",
            "sqlalchemy/safe-bound-query",
            "sqlalchemy/missing-tenant-scope",
        ]
        for c in cases:
            c_path = regression_dir / c
            exists = c_path.exists() and (c_path / "README.md").exists()
            self.log_test(f"Regression fixture: {c}", exists)

    def test_report_formatting(self):
        print("\n12. Testing Canonical v0.5.4 9-Section Actionable Markdown Report...")
        ev = Evidence(
            type=EvidenceType.SOURCE,
            location="settings.py:10",
            raw_snippet="DEBUG = True\nSECRET_KEY = 'sk_live_secret_key_12345'",
            rationale="Production debug mode exposure and hardcoded secret.",
            confidence_level=ConfidenceBand.CONFIRMED,
            is_sufficient_for_confirmed=True,
        )
        sev = SeverityInfo(
            level=SeverityLevel.CRITICAL,
            rationale="Exposes internal stack traces and hardcoded production secret.",
            rubric_justification="Critical because secret key enables session forgery and debug leaks internals.",
        )
        conf = ConfidenceScore.calculate(35, 25, 15, 15, 5, "Direct settings file check.")
        prov = ProvenanceChain(
            discovery_module="rules/TG-PLATFORM-003-production-stack-trace-exposure.md",
            triggering_input="DEBUG = True assignment in settings.py",
            evidence_collected=["settings.py:10"],
            decision_path=["Loaded Django settings", "Found DEBUG enabled"],
            verification_step="Assert DEBUG is False.",
        )
        rem = Remediation(
            problem_statement="Debug mode is enabled and hardcoded secret present.",
            risk_explanation="Stack traces leak environment variables and secret allows token forgery.",
            recommended_fix="Set DEBUG = False and load secret from environment.",
            framework_pattern=FrameworkPattern(
                framework="Django",
                unsafe_snippet="DEBUG = True",
                safe_snippet="DEBUG = False",
            ),
            verification_method="Assert DEBUG is False in production.",
            residual_risk_notes="Ensure 500.html template exists.",
        )
        f = Finding(
            rule_id="TG-PLATFORM-003",
            title="Production Stack Trace Exposure",
            category=TaxonomyCategory.CLIENT_PLATFORM,
            severity=sev,
            confidence=conf,
            status=FindingStatus.CONFIRMED,
            remediation_priority=RemediationPriority.IMMEDIATE,
            affected_component=AffectedComponent(component_name="Config", target_path="settings.py", start_line=10),
            evidence=[ev],
            provenance=prov,
            reproduction_method=ReproductionMethod(step_by_step=["Trigger 500 error and inspect response body"]),
            remediation=rem,
            asvs_control="V14.4.1",
            cwe="CWE-209",
            nist_ssdf="PW.5.1",
        )
        report = AuditReport(
            project_name="DemoApp",
            detected_stack={"language": "Python", "framework": "Django", "confidence": "Confirmed"},
            findings=[f],
        )

        md_output = ReportFormatter.render_markdown(report)
        has_header = "# TorusGuard Security Audit & Remediation Report" in md_output
        has_exec_summary = "## 1. 📋 Executive Summary" in md_output
        has_scope = "## 2. 🔍 Scope and Methodology" in md_output
        has_summary_table = "## 3. 📑 Key Findings Summary Table" in md_output
        has_detailed = "## 4. 🛡️ Detailed Findings" in md_output
        has_business_context = "🏢 Business Impact & Executive Context" in md_output
        has_remediation_roadmap = "## 5. 🎯 Remediation Priorities & Triage Roadmap" in md_output
        has_ticket_payload = "🎫 Copy-Paste Issue Tracker Payload" in md_output
        has_redaction = "sk_live_***REDACTED***" in md_output

        self.log_test(
            "Render v0.5.4 9-Section Actionable Report",
            has_header and has_exec_summary and has_scope and has_summary_table and has_detailed and has_business_context and has_remediation_roadmap and has_ticket_payload and has_redaction
        )

    def test_run_context_and_ponytail(self):
        print("\n13. Testing v0.5.5 RunFolder Structure...")
        import shutil
        test_root = self.root_dir / ".torusguard" / "runs_test"
        if test_root.exists():
            shutil.rmtree(test_root)
            
        rf = RunFolder(output_root=str(test_root), run_name="test-run-001")
        
        # Test directory initialization
        has_dirs = rf.run_path.exists() and rf.patches_dir.exists() and rf.logs_dir.exists()
        
        # Test metadata file initialization
        has_metadata = rf.metadata_file.exists()
        if has_metadata:
            with open(rf.metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                has_metadata = metadata.get("run_id") == "test-run-001"
                
        self.log_test("RunFolder Initialization", has_dirs and has_metadata)
        
        # Cleanup
        shutil.rmtree(test_root)

    def test_v6_governed_remediation_suite(self):
        print("\n14. Testing TorusGuard v0.6.0 Governed Remediation & Targeted Recheck Engine...")
        import tempfile
        from core.identity import IdentityEngine
        from core.clustering import ClusteringEngine
        from core.bundle import BundleManager
        from core.governance import PatchGovernor
        from core.rechecker import TargetedRechecker, RecheckOutcome
        from core.run_manager import RunManager
        from core.sarif import SarifExporter
        from core.v6_workflow import V6Workflow

        temp_dir = Path(tempfile.mkdtemp(prefix="tg-v0-6-harness-"))
        try:
            # 1. Run Folder
            rm = RunManager(base_dir=temp_dir, target_name="test-target", command="audit", run_id="run-harness-01")
            rm.write_manifest(status_counts={"total_findings": 1, "confirmed": 1, "high_confidence": 0, "needs_review": 0, "remediated": 0, "verified_fixed": 0, "regressed": 0})
            self.log_test("v0.6.0 RunFolder & Manifest.json Generation", rm.manifest_file.exists() and rm.patches_dir.exists())

            # 2. Stable Finding Identity
            code_a = "def view():\n    return Item.objects.get(id=id)"
            code_b = "# Shifted comment\ndef view():\n    return Item.objects.get(id=id)"
            fp1 = IdentityEngine.generate_identity("TG-DB-004", "views.py", code_a, sink_signature="Item.objects.get")
            fp2 = IdentityEngine.generate_identity("TG-DB-004", "views.py", code_b, sink_signature="Item.objects.get")
            self.log_test("v0.6.0 Stable Finding Identity (Line Shift Invariance)", fp1.fingerprint_id == fp2.fingerprint_id and fp1.fingerprint_id.startswith("TG-DB-"))

            # 3. Root-Cause Clustering
            raw_f = [
                {"finding_id": "f1", "rule_id": "TG-DB-004", "title": "Missing Tenant Isolation", "severity": "High", "target": {"file_path": "a.py"}},
                {"finding_id": "f2", "rule_id": "TG-DB-004", "title": "Missing Tenant Isolation", "severity": "High", "target": {"file_path": "b.py"}},
            ]
            clusters = ClusteringEngine.cluster_findings(raw_f)
            self.log_test("v0.6.0 Root-Cause Clustering (Multi-Tenant Pattern)", len(clusters) == 1 and clusters[0].cluster_id == "cluster-tenant-isolation")

            # 4. Remediation Bundle
            bundle = BundleManager.create_bundle(raw_f[0], cluster_id="cluster-tenant-isolation")
            b_dir = bundle.write_to_directory(temp_dir)
            self.log_test("v0.6.0 Remediation Bundle Packaging (5 Artifacts)", (b_dir / "finding.md").exists() and (b_dir / "minimal_patch_plan.md").exists())

            # 5. Patch Governance
            gov = PatchGovernor(max_additions_per_file=10)
            clean_diff = "--- a/x.py\n+++ b/x.py\n@@ -1 +1 @@\n-old()\n+new()\n"
            oversized_diff = "--- a/x.py\n+++ b/x.py\n" + "\n".join(f"+line_{i}()" for i in range(20))
            d_clean = gov.evaluate_diff(clean_diff, "x.py")
            d_over = gov.evaluate_diff(oversized_diff, "x.py")
            self.log_test("v0.6.0 Minimal Patch Governance (Line Churn Policy)", d_clean.allowed_auto_apply and not d_over.allowed_auto_apply)

            # 6. Targeted Recheck
            r_fix = TargetedRechecker.verify_finding("f1", "TG-DB-004", "a.py", "old", "new", is_safe_pattern_present=True, is_unsafe_pattern_present=False)
            r_reg = TargetedRechecker.verify_finding("f2", "TG-DB-004", "b.py", "old", "bad", is_safe_pattern_present=False, is_unsafe_pattern_present=True, introduced_new_flaws=["TG-SEC-001"])
            self.log_test("v0.6.0 Targeted Recheck Transitions (Confirmed Fixed & Regressed)", r_fix.outcome == RecheckOutcome.CONFIRMED_FIXED and r_reg.outcome == RecheckOutcome.REGRESSED)

            # 7. SARIF Export
            sarif = SarifExporter.generate_sarif([{"finding_id": "f1", "rule_id": "TG-DB-004", "title": "Missing Tenant Isolation", "target": {"file_path": "a.py"}}])
            self.log_test("v0.6.0 SARIF v2.1.0 Structured Export", sarif["version"] == "2.1.0" and len(sarif["runs"]) == 1)

            # 8. End-to-End Workflow
            wf = V6Workflow(target_root=temp_dir, output_base=temp_dir / "runs")
            run_wf = wf.execute_audit(raw_f, target_name="e2e-demo", export_sarif=True)
            self.log_test("v0.6.0 End-to-End Workflow Execution", run_wf.manifest_file.exists() and run_wf.sarif_file.exists())

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    runner = ValidationHarnessRunner()
    success = runner.run_all()
    sys.exit(0 if success else 1)
