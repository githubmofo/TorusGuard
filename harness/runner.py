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
import tempfile
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
        self.test_v74_rule_coverage_and_living_report()
        self.test_dual_ledger_sync_and_atomic_swapping()
        self.test_interactive_html_dashboard_and_exporters()
        self.test_cli_and_polyglot_integration()
        self.test_wave5_visual_e2e_and_cryptographic_manifest()
        self.test_wave6_remediation_hub_and_compliance_matrix()

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
            skill_file = self.root_dir / "skills" / "torusguard" / "SKILL.md"
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
        if not refs_dir.exists():
            refs_dir = self.root_dir / "skills" / "torusguard" / "references"
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
            raw_snippet="User.objects.raw('SELECT * FROM users WHERE name = %s')",
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

    def test_v74_rule_coverage_and_living_report(self):
        print("\n15. Testing TorusGuard v1.3.5 74-Rule Catalog Coverage & Living Report Engine...")
        temp_dir = Path(tempfile.mkdtemp(prefix="tg-v74-test-"))
        try:
            # 1. Test 74 Rule Coverage in audit_runner.py
            sys.path.insert(0, str(self.root_dir / ".torusguard" / "scripts"))
            import audit_runner
            rule_ids = [r["rule_id"] for r in audit_runner.RULE_PATTERNS]
            unique_ids = set(rule_ids)
            self.log_test("v1.3.5 AST Engine Rule Count (74 Rules)", len(unique_ids) == 74 and len(rule_ids) == 74)

            # 2. Test 18 Rule Families Coverage
            families = set(r.split("-")[1] for r in unique_ids)
            expected_families = {"SEC", "AUTH", "DB", "INPUT", "RATE", "AGENT", "SSRF", "WEBHOOK", "WS", "CSRF", "GQL", "SUPPLY", "BIZ", "CACHE", "CLIENT", "PLATFORM", "DIFF", "EDGE"}
            self.log_test("v1.3.5 Complete Rule Family Representation (18 Families)", families == expected_families)

            # 3. Test Living Report Sync Lifecycle (Discovery -> Candidate -> Applied -> Resolved)
            import report_sync
            dummy_f = [{
                "finding_id": "TG-RATE-001-f1",
                "rule_id": "TG-RATE-001",
                "title": "Unlimited Authentication Endpoint",
                "severity": "High",
                "file_path": "server/auth.js",
                "line_number": 25,
                "description": "Unprotected auth route lacking rate limiting.",
                "snippet": "app.post('/login', async (req, res) => {})",
                "confidence_score": 85,
                "confidence_band": "High Confidence"
            }]

            # Discovery
            rep_path = report_sync.record_audit_findings(temp_dir, dummy_f, "run-audit-1")
            content1 = rep_path.read_text(encoding="utf-8")
            self.log_test("v1.3.5 Living Report Discovery State (OPEN 🔴)", "🔴 OPEN" in content1 and "TG-RATE-001" in content1)

            # Harden
            dummy_b = [{
                "finding_id": "TG-RATE-001-f1",
                "rule_id": "TG-RATE-001",
                "target_file": "server/auth.js",
                "line_number": 25,
                "bundle_id": "bnd-rate-001",
                "what_should_change": "Injected authLimiter",
                "proposed_diff": "+ app.post('/login', authLimiter, ...)",
                "additions": 1,
                "deletions": 0
            }]
            report_sync.record_harden_bundles(temp_dir, dummy_b, "run-harden-1")
            content2 = rep_path.read_text(encoding="utf-8")
            self.log_test("v1.3.5 Living Report Candidate State (CANDIDATE 🟡)", "🟡 CANDIDATE" in content2 and "Injected authLimiter" in content2)

            # Apply
            report_sync.record_applied_patches(temp_dir, dummy_b, temp_dir / "snapshots" / "snap1", "run-apply-1")
            content3 = rep_path.read_text(encoding="utf-8")
            self.log_test("v1.3.5 Living Report Applied State (APPLIED 🔵)", "🔵 APPLIED" in content3)

            # Recheck Fixed
            report_sync.record_recheck_results(temp_dir, {
                "fixed": [{"finding_id": "TG-RATE-001-f1"}],
                "regressed": [],
                "remaining": []
            }, "run-recheck-1")
            content4 = rep_path.read_text(encoding="utf-8")
            self.log_test("v1.3.5 Living Report Verified Closure (RESOLVED 🟢)", "🟢 RESOLVED" in content4 and "Closure Verified" in content4)

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_dual_ledger_sync_and_atomic_swapping(self):
        print("\n16. Testing Dual-Ledger Sync & Lifecycle State Machine Transitions...")
        temp_dir = Path(tempfile.mkdtemp(prefix="tg-dual-ledger-test-"))
        try:
            sys.path.insert(0, str(self.root_dir / ".torusguard" / "scripts"))
            import report_sync
            import html_reporter

            # 1. Atomic Write Test
            test_file = temp_dir / "atomic_test.txt"
            res_write = report_sync.atomic_write_text(test_file, "ATOMIC_PASS")
            self.log_test("Wave 2: Atomic File Swapping Engine", res_write and test_file.read_text(encoding="utf-8") == "ATOMIC_PASS")

            # 2. Fresh Audit creates security_report.md but NOT report.html
            dummy_f = [{
                "finding_id": "TG-DB-001-sync1",
                "rule_id": "TG-DB-001",
                "title": "Unparameterized Raw SQL",
                "severity": "Critical",
                "file_path": "api/users.py",
                "line_number": 42,
                "description": "Raw string concatenation in database query.",
                "snippet": "db.execute(f'SELECT * FROM users WHERE id={uid}')",
                "confidence_score": 90,
                "confidence_band": "Confirmed",
                "cluster": "database-isolation"
            }]
            rep_path = report_sync.record_audit_findings(temp_dir, dummy_f, "run-sync-01")
            root_html = temp_dir / "report.html"
            self.log_test("Wave 2: Audit forms security_report.md without unprompted report.html", rep_path.is_file() and not root_html.exists())

            # 3. Explicit HTML Generation creates report.html
            runs_dir = temp_dir / ".torusguard" / "runs" / "run-sync-01"
            runs_dir.mkdir(parents=True, exist_ok=True)
            (runs_dir / "findings.json").write_text(json.dumps(dummy_f), encoding="utf-8")
            html_res = html_reporter.emit_html_report(target_path=root_html, root_dir=temp_dir)
            self.log_test("Wave 2: Explicit on-demand report.html emission", root_html.is_file() and html_res["status"] == "success")

            # 4. Patch Application updates BOTH files in lockstep
            dummy_bundle = [{
                "finding_id": "TG-DB-001-sync1",
                "rule_id": "TG-DB-001",
                "target_file": "api/users.py",
                "line_number": 42,
                "bundle_id": "bnd-db-001",
                "what_should_change": "Parameterized query substitution",
                "proposed_diff": "+ db.execute('SELECT * FROM users WHERE id=:id', {'id': uid})",
                "additions": 1,
                "deletions": 1
            }]
            snap_dir = temp_dir / ".torusguard" / "snapshots" / "run-sync-01"
            snap_dir.mkdir(parents=True, exist_ok=True)
            report_sync.record_applied_patches(temp_dir, dummy_bundle, snap_dir, "run-apply-01")
            md_content = rep_path.read_text(encoding="utf-8")
            self.log_test("Wave 2: Patch application synchronizes both Markdown and HTML ledgers", "🔵 APPLIED" in md_content and root_html.stat().st_size > 0)

            # 5. Rollback updates BOTH files back to OPEN
            report_sync.record_rollback_results(temp_dir, ["api/users.py"], "run-rollback-01")
            md_content_rb = rep_path.read_text(encoding="utf-8")
            self.log_test("Wave 2: Rollback restoration synchronizes finding reversion across ledgers", "🔴 OPEN" in md_content_rb)

            # 6. Recheck updates BOTH files to RESOLVED
            report_sync.record_recheck_results(temp_dir, {
                "fixed": [{"finding_id": "TG-DB-001-sync1"}],
                "regressed": [],
                "remaining": []
            }, "run-recheck-01")
            md_content_rc = rep_path.read_text(encoding="utf-8")
            self.log_test("Wave 2: Recheck closure synchronizes verified state across ledgers", "🟢 RESOLVED" in md_content_rc)

            # 7. Self-Healing from run artifacts when markdown report is absent
            rep_path.unlink()
            healed_report = report_sync.parse_existing_report(rep_path)
            self.log_test("Wave 2: Self-healing reconciliation restores state from run artifacts", "TG-DB-001-sync1" in healed_report.get("findings", {}))

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_interactive_html_dashboard_and_exporters(self):
        print("\n17. Testing Wave 3 Interactive HTML Dashboard Engine & Exporters...")
        temp_dir = Path(tempfile.mkdtemp(prefix="tg-wave3-html-test-"))
        try:
            sys.path.insert(0, str(self.root_dir / ".torusguard" / "scripts"))
            import html_reporter

            # Seed sample run with 1 critical finding and 1 high finding
            runs_dir = temp_dir / ".torusguard" / "runs" / "run-w3-01"
            runs_dir.mkdir(parents=True, exist_ok=True)
            dummy_findings = [
                {
                    "finding_id": "TG-DB-001-w3",
                    "rule_id": "TG-DB-001",
                    "title": "Unparameterized Raw SQL",
                    "severity": "Critical",
                    "file_path": "api/users.py",
                    "line_number": 42,
                    "description": "Raw string concatenation in database query.",
                    "snippet": "db.execute(f'SELECT * FROM users WHERE id={uid}')",
                    "confidence_score": 92,
                    "confidence_band": "Confirmed",
                    "cluster": "database-isolation"
                },
                {
                    "finding_id": "TG-AUTH-002-w3",
                    "rule_id": "TG-AUTH-002",
                    "title": "Client-Only Authorization Enforcement",
                    "severity": "High",
                    "file_path": "client/App.tsx",
                    "line_number": 15,
                    "description": "Client-side route guard lacking backend check.",
                    "snippet": "if (!user.isAdmin) return <Redirect />",
                    "confidence_score": 85,
                    "confidence_band": "High Confidence",
                    "cluster": "cluster-auth-bypass"
                }
            ]
            (runs_dir / "findings.json").write_text(json.dumps(dummy_findings), encoding="utf-8")

            # Emit HTML report
            out_html = temp_dir / "report.html"
            res = html_reporter.emit_html_report(target_path=out_html, root_dir=temp_dir)
            html_content = out_html.read_text(encoding="utf-8")

            # 1. Output emission
            self.log_test("Wave 3: Standalone report.html generated successfully", out_html.is_file() and res["status"] == "success")

            # 2. Zero-CDN invariant
            has_remote_tags = bool(re.findall(r'<(?:script|link)[^>]*(?:src|href)=["\']https?://[^>]*>', html_content, re.IGNORECASE))
            has_remote_fonts = bool(re.findall(r'@import\s+url\(["\']https?://', html_content, re.IGNORECASE))
            self.log_test("Wave 3: Zero-CDN Invariant (100% offline self-contained)", not has_remote_tags and not has_remote_fonts)

            # 3. Defended Invariants Inventory (Safe vs Harmed)
            self.log_test("Wave 3: Defended Invariants Inventory rendered", "Active Defenses &amp; Protected Invariants" in html_content and "Guards Defended" in html_content)

            # 4. Interactive Directory Heatmap with filter
            self.log_test("Wave 3: Interactive Directory Heatmap (Click-to-Filter)", "Directory Attack Surface Heatmap" in html_content and "filterByDirectory" in html_content)

            # 5. In-Browser Exporters (SARIF & CSV)
            self.log_test("Wave 3: In-Browser Artifact Exporters (SARIF & CSV Blobs)", "downloadSarif" in html_content and "downloadCsv" in html_content and "torusguard-report.sarif" in html_content)

            # 6. Prescriptive Defenses & Golden Recipes
            self.log_test("Wave 3: Prescriptive Next Best Defenses Advisory", "Next Best Defenses Advisory" in html_content and "npx torusguard harden" in html_content)
            self.log_test("Wave 3: Golden Fix Recipes Explorer", "Golden Fix Recipes" in html_content and "Copy Pattern" in html_content)

            # 7. Print & PDF CSS Engine
            self.log_test("Wave 3: Executive Print & PDF CSS Engine", "@media print" in html_content and ".drawer-row { display: table-row !important; }" in html_content)

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_cli_and_polyglot_integration(self):
        print("\n18. Testing CLI & AI Slash Command Integration, Polyglot Stack Detection & Dual-Mode Parity...")
        temp_dir = Path(tempfile.mkdtemp(prefix="tg-cli-polyglot-test-"))
        try:
            scripts_dir = self.root_dir / ".torusguard" / "scripts"
            if str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))
            import stack_detect
            import html_reporter
            import sarif_exporter

            # 1. Polyglot Framework Profiling: Fastify
            fastify_dir = temp_dir / "fastify_proj"
            fastify_dir.mkdir(parents=True, exist_ok=True)
            (fastify_dir / "package.json").write_text(json.dumps({"dependencies": {"fastify": "^4.0.0"}}), encoding="utf-8")
            prof_fastify = stack_detect.detect_stack(fastify_dir)
            self.log_test("Wave 4: Polyglot Stack Detection (Fastify)", "Fastify" in prof_fastify.get("frameworks_found", []))

            # 2. Polyglot Framework Profiling: Blazor (.NET)
            blazor_dir = temp_dir / "blazor_proj"
            blazor_dir.mkdir(parents=True, exist_ok=True)
            (blazor_dir / "App.razor").write_text("<h1>Blazor App</h1>", encoding="utf-8")
            (blazor_dir / "test.csproj").write_text("<Project Sdk=\"Microsoft.NET.Sdk.Web\"></Project>", encoding="utf-8")
            prof_blazor = stack_detect.detect_stack(blazor_dir)
            self.log_test("Wave 4: Polyglot Stack Detection (Blazor .NET)", "Blazor" in prof_blazor.get("frameworks_found", []))

            # 3. Polyglot Framework Profiling: Tornado (Python)
            tornado_dir = temp_dir / "tornado_proj"
            tornado_dir.mkdir(parents=True, exist_ok=True)
            (tornado_dir / "app.py").write_text("import tornado.web\napp = tornado.web.Application()", encoding="utf-8")
            prof_tornado = stack_detect.detect_stack(tornado_dir)
            self.log_test("Wave 4: Polyglot Stack Detection (Tornado Python)", "Tornado" in prof_tornado.get("frameworks_found", []))

            # 4. Polyglot Framework Profiling: WordPress (PHP)
            wp_dir = temp_dir / "wp_proj"
            wp_dir.mkdir(parents=True, exist_ok=True)
            (wp_dir / "wp-config.php").write_text("<?php define('DB_NAME', 'wp_db');", encoding="utf-8")
            prof_wp = stack_detect.detect_stack(wp_dir)
            self.log_test("Wave 4: Polyglot Stack Detection (WordPress PHP)", "WordPress" in prof_wp.get("frameworks_found", []))

            # 5. Default Emission Path: report.html at project root + mirror in .torusguard/runs/
            mock_proj = temp_dir / "mock_proj"
            mock_proj.mkdir(parents=True, exist_ok=True)
            (mock_proj / ".torusguard" / "runs").mkdir(parents=True, exist_ok=True)
            res_def = html_reporter.emit_html_report(root_dir=mock_proj)
            root_report = mock_proj / "report.html"
            run_mirror = mock_proj / ".torusguard" / "runs" / "report-latest.html"
            self.log_test("Wave 4: Default HTML Emission to Root & Mirror Sync", root_report.is_file() and run_mirror.is_file() and root_report.stat().st_size > 1000)

            # 6. Combined HTML and SARIF Execution
            sarif_out = mock_proj / ".torusguard" / "runs" / "results-latest.sarif"
            sarif_data = sarif_exporter.generate_sarif([], run_id="run-test")
            with open(sarif_out, "w", encoding="utf-8") as f:
                json.dump(sarif_data, f, indent=2)
            self.log_test("Wave 4: Combined Multi-Artifact Emission (HTML + SARIF)", root_report.is_file() and sarif_out.is_file() and sarif_data.get("version") == "2.1.0")

            # 7. Subproject Monorepo Scoping (--target)
            sub_dir = mock_proj / "apps" / "api"
            sub_dir.mkdir(parents=True, exist_ok=True)
            res_scoped = html_reporter.emit_html_report(target_path=sub_dir / "report.html", root_dir=mock_proj)
            scoped_report = sub_dir / "report.html"
            self.log_test("Wave 4: Subproject Scoping Isolation (--target)", scoped_report.is_file() and scoped_report.stat().st_size > 1000)

            # 8. 75-Column Terminal Visual Width Constraint
            import term_ui as tui
            sample_lines = [
                tui.format_box_line("Posture Score:     100/100 (Optimal Defense)"),
                tui.format_box_line("Invariants:        74 Defended · 0 Harmed (74 Rules)"),
                tui.format_box_line("Dashboard Size:    44612 bytes (Zero CDN, 100% Offline)"),
            ]
            all_75 = all(tui.get_visual_width(l) == 75 for l in sample_lines)
            self.log_test("Wave 4: Standardized 75-Column Visual Terminal Invariant", all_75)

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_wave5_visual_e2e_and_cryptographic_manifest(self):
        print("\n19. Testing Wave 5 Visual Polish, Multi-Language E2E Verification & Cryptographic Manifest Integrity...")
        temp_dir = Path(tempfile.mkdtemp(prefix="tg-wave5-e2e-test-"))
        try:
            scripts_dir = self.root_dir / ".torusguard" / "scripts"
            if str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))
            import manifest_builder
            import html_reporter
            import audit_runner
            import report_sync

            # 1. Cryptographic Manifest Check on Active .torusguard Workspace
            m_pass = manifest_builder.check_manifest(self.root_dir / ".torusguard")
            self.log_test("Wave 5: Cryptographic Workspace Manifest Verification (100% SHA-256 Match)", m_pass)

            # 2. Cryptographic Manifest Check on skills/torusguard/payload
            payload_dir = self.root_dir / "skills" / "torusguard" / "payload"
            if not payload_dir.exists():
                payload_dir = self.root_dir / "skills" / "TorusGuard" / "payload"
            m_payload_pass = manifest_builder.check_manifest(payload_dir)
            self.log_test("Wave 5: Distributed Skill Payload Manifest Cryptographic Parity", m_payload_pass)

            # 3. Posture Gauge Dynamic Tokens, Gradient Defs & SVG Glow
            mock_proj = temp_dir / "mock_app"
            mock_proj.mkdir(parents=True, exist_ok=True)
            res_html = html_reporter.emit_html_report(root_dir=mock_proj)
            html_text = (mock_proj / "report.html").read_text(encoding="utf-8")
            has_svg_defs = 'linearGradient id="gaugeGradient"' in html_text and 'filter id="gaugeGlow"' in html_text
            has_gauge_ids = 'id="gaugeCircleFill"' in html_text and 'id="postureScoreText"' in html_text
            has_countup_anim = 'initPostureGauge' in html_text and 'requestAnimationFrame' in html_text
            self.log_test("Wave 5: Dynamic Circular SVG Posture Gauge (Gradient, Glow & Count-Up)", has_svg_defs and has_gauge_ids and has_countup_anim)

            # 4. Multi-Dimensional Quick-Filters (Severity, Status, Search Clear & Live Counter)
            has_filter_pills = 'data-sev-filter' in html_text and 'data-status-filter' in html_text
            has_filter_funcs = 'filterBySeverity' in html_text and 'filterByStatus' in html_text and 'resetAllFilters' in html_text
            has_search_clear = 'id="searchClearBtn"' in html_text and 'clearSearch' in html_text
            has_live_counts = 'id="visibleCount"' in html_text and 'id="totalCount"' in html_text
            self.log_test("Wave 5: Multi-Dimensional Quick Filters & Live Visibility Counters", has_filter_pills and has_filter_funcs and has_search_clear and has_live_counts)

            # 5. Multi-Language E2E: Python / FastAPI Fixture (Raw SQL Concatenation -> TG-INPUT-002)
            py_proj = temp_dir / "py_app"
            py_proj.mkdir(parents=True, exist_ok=True)
            (py_proj / "app.py").write_text("def query(db, uid): return db.execute(f'SELECT * FROM users WHERE id={uid}')\n", encoding="utf-8")
            r_py = audit_runner.execute_audit(py_proj, json_output=True)
            has_py_finding = any(f.get("rule_id") == "TG-INPUT-002" for f in r_py.get("findings", []))
            self.log_test("Wave 5: Multi-Language E2E - Python AST Invariant Detection (TG-INPUT-002)", has_py_finding)

            # 6. Multi-Language E2E: TypeScript / React Fixture (Public Client Secret -> TG-SEC-002)
            ts_proj = temp_dir / "ts_app"
            ts_proj.mkdir(parents=True, exist_ok=True)
            (ts_proj / "Page.tsx").write_text("export const clientSecret = process.env.NEXT_PUBLIC_SUPABASE_SECRET;\n", encoding="utf-8")
            r_ts = audit_runner.execute_audit(ts_proj, json_output=True)
            has_ts_finding = any(f.get("rule_id") == "TG-SEC-002" for f in r_ts.get("findings", []))
            self.log_test("Wave 5: Multi-Language E2E - TypeScript AST Invariant Detection (TG-SEC-002)", has_ts_finding)

            # 7. Multi-Language E2E: Server / API Fixture (User-Controlled SSRF -> TG-SSRF-001)
            srv_proj = temp_dir / "srv_app"
            srv_proj.mkdir(parents=True, exist_ok=True)
            (srv_proj / "proxy.js").write_text('const fetch = require("node-fetch");\nasync function proxy(req) { return fetch(req.query.target_url); }\n', encoding="utf-8")
            r_srv = audit_runner.execute_audit(srv_proj, json_output=True)
            has_srv_finding = any(f.get("rule_id") == "TG-SSRF-001" for f in r_srv.get("findings", []))
            self.log_test("Wave 5: Multi-Language E2E - Server AST Invariant Detection (TG-SSRF-001)", has_srv_finding)

            # 8. Multi-Language E2E Lifecycle: Dual-Ledger Sync
            py_report_md = py_proj / "security_report.md"
            self.log_test("Wave 5: Multi-Language E2E - Automatic Living Security Report Synchronization", py_report_md.is_file() and "TG-INPUT-002" in py_report_md.read_text(encoding="utf-8"))

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_wave6_remediation_hub_and_compliance_matrix(self):
        print("\n20. Testing Wave 6 Remediation Hub, Defended Invariants Matrix, Compliance Frameworks & Theme Switcher...")
        temp_dir = Path(tempfile.mkdtemp(prefix="tg-wave6-test-"))
        try:
            scripts_dir = self.root_dir / ".torusguard" / "scripts"
            if str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))
            import html_reporter

            # Seed project with findings to test both Findings table and Simulator
            runs_dir = temp_dir / ".torusguard" / "runs" / "run-w6-01"
            runs_dir.mkdir(parents=True, exist_ok=True)
            dummy_findings = [
                {
                    "finding_id": "TG-SEC-001-w6",
                    "rule_id": "TG-SEC-001",
                    "title": "Hardcoded Secret Token in Source",
                    "severity": "Critical",
                    "file_path": "backend/auth.py",
                    "line_number": 12,
                    "description": "Hardcoded secret token detected.",
                    "snippet": "SECRET_KEY = 'sk_live_12345'",
                    "confidence_score": 95,
                    "confidence_band": "Confirmed",
                    "cluster": "cluster-credentials-exposure"
                },
                {
                    "finding_id": "TG-INPUT-001-w6",
                    "rule_id": "TG-INPUT-001",
                    "title": "Missing Schema Validation on Endpoint",
                    "severity": "High",
                    "file_path": "backend/routes.py",
                    "line_number": 45,
                    "description": "Payload unvalidated before access.",
                    "snippet": "data = req.get_json()",
                    "confidence_score": 85,
                    "confidence_band": "High Confidence",
                    "cluster": "cluster-injection"
                }
            ]
            (runs_dir / "findings.json").write_text(json.dumps(dummy_findings), encoding="utf-8")

            # Emit report
            res = html_reporter.emit_html_report(root_dir=temp_dir)
            report_file = temp_dir / "report.html"
            html_text = report_file.read_text(encoding="utf-8")

            # 1. Golden Recipes Memory Unpacking & Churn Bounds
            has_diff_snippet = 'class="diff-line-header"' in html_text or 'class="diff-line-add"' in html_text or 'diff-line-del' in html_text
            has_ponytail_churn = 'Ponytail line churn budget' in html_text
            no_placeholders = ('// Parameterized pattern' not in html_text) and ('Verified fix pattern' not in html_text)
            self.log_test("Wave 6: Golden Recipes Memory Unpacking & Ponytail Line Churn Verification", has_diff_snippet and has_ponytail_churn and no_placeholders)

            # 2. Golden Recipes Dual-View Switcher & Category Filtering
            has_dual_view = 'setRecipeView' in html_text and 'Unified Diff' in html_text and 'Before / After' in html_text
            has_cat_filters = 'filterRecipeCategory' in html_text and 'data-recipe-cat-filter' in html_text
            self.log_test("Wave 6: Golden Recipes Dual-View Switcher (Diff vs Split) & Category Filter Tabs", has_dual_view and has_cat_filters)

            # 3. 5-Layer Architectural Invariant Matrix
            has_layers = all(layer_name in html_text for layer_name in [
                "Application & LLM Defense",
                "Identity, Auth & Real-Time",
                "Database, GraphQL & Cache",
                "Network, SSRF & Webhooks",
                "Platform, Supply Chain & Secrets"
            ])
            has_inv_search = 'filterInvariants' in html_text and 'id="invSearchInput"' in html_text
            has_74_chips = html_text.count('class="inv-chip') == 74
            self.log_test("Wave 6: 5-Layer Architectural Invariant Matrix (74 Rules & Live Search)", has_layers and has_inv_search and has_74_chips)

            # 4. Interactive Invariant Inspection Modal
            has_inv_modal = 'id="invariantModal"' in html_text and 'inspectInvariant' in html_text and 'closeInvariantModal' in html_text
            self.log_test("Wave 6: Interactive Invariant Security Guarantee Inspection Modal", has_inv_modal)

            # 5. Complete AI Prompt Removal
            ai_prompt_absent = 'btnAiPrompt' not in html_text and 'copyAIPrompt' not in html_text and 'ai_prompt' not in html_text
            self.log_test("Wave 6: Complete AI Prompt Button & Dead Code Removal", ai_prompt_absent)

            # 6. Interactive "What-If" Posture Score Simulator
            has_simulator_card = 'What-If" Posture Score Simulator' in html_text
            has_sim_funcs = 'updateSimulatedScore' in html_text and 'simulateFixAll' in html_text and 'resetSimulatedFixes' in html_text
            has_sim_chk = 'class="sim-fix-chk"' in html_text
            self.log_test("Wave 6: Interactive What-If Posture Simulator with Live Dynamic Recalculation", has_simulator_card and has_sim_funcs and has_sim_chk)

            # 7. Enterprise Compliance Framework Mapping (SOC 2, ISO 27001, HIPAA)
            has_compliance_grid = 'Enterprise Compliance Framework Mapping' in html_text
            has_frameworks = 'SOC 2 Type II' in html_text and 'ISO/IEC 27001:2022' in html_text and 'HIPAA Security Rule' in html_text
            self.log_test("Wave 6: Enterprise Compliance Framework Mapping (SOC 2, ISO 27001, HIPAA)", has_compliance_grid and has_frameworks)

            # 8. Zero-CDN Executive Dark / Light Mode Theme Switcher
            has_theme_btn = 'id="themeToggleBtn"' in html_text and 'toggleTheme' in html_text
            has_theme_css = 'body.light-theme' in html_text
            has_theme_storage = 'localStorage.getItem(\'tg_theme\')' in html_text or "localStorage.getItem('tg_theme')" in html_text
            self.log_test("Wave 6: Zero-CDN Executive Dark / Light Mode Switcher with LocalStorage Persistence", has_theme_btn and has_theme_css and has_theme_storage)

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    runner = ValidationHarnessRunner()
    success = runner.run_all()
    sys.exit(0 if success else 1)