"""
TorusGuard Validation Harness Runner (v0.5.1)
Executes automated rule schema checks, provenance chain assertions, confidence scoring tests, fixture differentials, and retest lifecycle validations.
"""

import os
import sys
import json
import re
import glob
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
    FindingStatus,
    LifecycleStage,
    TaxonomyCategory,
    EvidenceType,
    AuditReport,
)
from core.lifecycle import FindingLifecycleManager, LifecycleTransitionError
from core.formatter import ReportFormatter


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
        print("TORUSGUARD v0.5.1 REPEATABLE VALIDATION HARNESS")
        print("=" * 80)

        self.test_schema_integrity()
        self.test_rule_catalog()
        self.test_skill_definition()
        self.test_confidence_scoring_model()
        self.test_provenance_and_evidence_hashing()
        self.test_retest_lifecycle_closure()
        self.test_stack_detection_fixtures()
        self.test_educational_differential_fixtures()
        self.test_regression_fixtures()
        self.test_report_formatting()

        print("-" * 80)
        print(f"SUMMARY: {self.passed_tests} Passed | {self.failed_tests} Failed")
        print("=" * 80)
        return self.failed_tests == 0

    def test_schema_integrity(self):
        print("\n1. Testing Formal Schema Integrity (v0.5.1)...")
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

        self.log_test(f"Total Rules Cataloged ({len(rule_ids)})", len(rule_ids) >= 60, f"Found {len(rule_ids)} rules")

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

        has_commands = all(cmd in content for cmd in ["/torusguard init", "/torusguard audit", "/torusguard harden", "/torusguard verify", "/torusguard recheck"])
        self.log_test("SKILL.md Core Commands Documented (including recheck)", has_commands)

        refs_dir = self.root_dir / "skills" / "TorusGuard" / "references"
        ref_files = list(refs_dir.glob("*.md"))
        self.log_test(f"Skill Reference Modules ({len(ref_files)})", len(ref_files) >= 7)

    def test_confidence_scoring_model(self):
        print("\n4. Testing Auditable Confidence Scoring Model...")
        # 1. High-evidence test (Score >= 90 -> Confirmed)
        c_confirmed = ConfidenceScore.calculate(
            evidence_quality=35,
            reproduction_success=25,
            independent_confirmations=15,
            environmental_clarity=15,
            manual_review_status=5,
            rationale="Direct AST match with deterministic reproduction.",
        )
        self.log_test("Confidence calculation: Confirmed band (>= 90)", c_confirmed.score == 95 and c_confirmed.band == ConfidenceBand.CONFIRMED)

        # 2. Medium-evidence test (Score 70-89 -> High Confidence)
        c_high = ConfidenceScore.calculate(
            evidence_quality=30,
            reproduction_success=20,
            independent_confirmations=10,
            environmental_clarity=15,
            manual_review_status=0,
            rationale="Strong static indicator without manual validation.",
        )
        self.log_test("Confidence calculation: High Confidence band (70-89)", c_high.score == 75 and c_high.band == ConfidenceBand.HIGH_CONFIDENCE)

        # 3. Weak-evidence test (Score < 50 -> Low Confidence)
        c_low = ConfidenceScore.calculate(
            evidence_quality=15,
            reproduction_success=10,
            independent_confirmations=5,
            environmental_clarity=5,
            manual_review_status=0,
            rationale="Indirect indicator with unverified service delegation.",
        )
        self.log_test("Confidence calculation: Low Confidence band (< 50)", c_low.score == 35 and c_low.band == ConfidenceBand.LOW_CONFIDENCE)

    def test_provenance_and_evidence_hashing(self):
        print("\n5. Testing Provenance Chain & SHA-256 Evidence Integrity...")
        ev = Evidence(
            type=EvidenceType.SOURCE,
            location="server/auth.py:42",
            raw_snippet="SECRET_KEY = 'hardcoded_jwt_secret_value'",
            rationale="Hardcoded secret credential.",
            confidence_level=ConfidenceBand.CONFIRMED,
            is_sufficient_for_confirmed=True,
        )
        has_hash = bool(ev.sha256_checksum) and len(ev.sha256_checksum) == 64
        self.log_test("Evidence SHA-256 Checksum Computed", has_hash)

        prov = ProvenanceChain(
            discovery_module="rules/secrets/TG-SEC-001-hardcoded-secrets.md",
            triggering_input="AST Assignment: SECRET_KEY string literal",
            evidence_collected=["server/auth.py:42"],
            decision_path=[
                "1. Scanned server/auth.py for variable assignment 'SECRET_KEY'",
                "2. Confirmed hardcoded non-env string literal value",
                "3. Verified reachability in JWT encoding function",
            ],
            verification_step="Extract raw string literal and assert absence of os.environ lookup.",
        )
        self.log_test("Provenance Chain Structured Decision Path", len(prov.decision_path) == 3)

    def test_retest_lifecycle_closure(self):
        print("\n6. Testing Retest Execution & Closure State Machine...")
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

        # Progression: Detect -> Classify -> Verify -> Remediate
        FindingLifecycleManager.transition(finding, LifecycleStage.CLASSIFY)
        FindingLifecycleManager.transition(finding, LifecycleStage.VERIFY)
        FindingLifecycleManager.transition(finding, LifecycleStage.REMEDIATE)

        # Retest execution (Safe fix applied)
        ok, msg = FindingLifecycleManager.execute_retest(
            finding,
            post_fix_code="User.objects.raw('SELECT * FROM users WHERE name = %s', [name])",
            safe_pattern_verified=True,
            verifier_notes="Verified parameterized binding query.",
        )
        self.log_test("Retest execution -> Verified Fixed", ok and finding.status == FindingStatus.VERIFIED_FIXED)
        self.log_test("Retest evidence hash recorded", bool(finding.retest_result.retest_evidence_hash))

    def test_stack_detection_fixtures(self):
        print("\n7. Testing Stack Detection Layouts...")
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
        print("\n8. Testing Educational Differential Fixtures...")
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
        print("\n9. Testing Python Regression Fixtures Suite...")
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
        print("\n10. Testing Canonical v0.5.1 Markdown Report Rendering...")
        ev = Evidence(
            type=EvidenceType.SOURCE,
            location="settings.py:10",
            raw_snippet="DEBUG = True",
            rationale="Production debug mode exposure.",
            confidence_level=ConfidenceBand.CONFIRMED,
            is_sufficient_for_confirmed=True,
        )
        sev = SeverityInfo(
            level=SeverityLevel.HIGH,
            rationale="Exposes internal stack traces and server environment.",
            rubric_justification="High because stack traces leak paths and secrets.",
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
            problem_statement="Debug mode is enabled in configuration.",
            risk_explanation="Stack traces leak environment variables and code paths.",
            recommended_fix="Set DEBUG = False in production.",
            framework_pattern=FrameworkPattern(
                framework="Django",
                unsafe_snippet="DEBUG = True",
                safe_snippet="DEBUG = False",
            ),
            verification_method="Assert DEBUG is False.",
            residual_risk_notes="Ensure 500.html template exists.",
        )
        f = Finding(
            rule_id="TG-PLATFORM-003",
            title="Production Stack Trace Exposure",
            category=TaxonomyCategory.CLIENT_PLATFORM,
            severity=sev,
            confidence=conf,
            status=FindingStatus.CONFIRMED,
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
        has_title = "# TorusGuard Security Audit & Provenance Report" in md_output
        has_score = "Auditable Confidence Score Breakdown" in md_output
        has_prov = "Provenance Chain" in md_output
        has_hash = "SHA-256 Checksum" in md_output
        has_diff = "+ DEBUG = False" in md_output

        self.log_test("Render v0.5.1 Provenance Markdown Report", has_title and has_score and has_prov and has_hash and has_diff)


if __name__ == "__main__":
    runner = ValidationHarnessRunner()
    success = runner.run_all()
    sys.exit(0 if success else 1)
