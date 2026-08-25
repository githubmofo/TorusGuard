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
    AffectedArea,
    VerificationStep,
    LifecycleStage,
    ConfidenceLevel,
    SeverityLevel,
    FindingStatus,
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
        print("TORUSGUARD v0.5.0 REPEATABLE VALIDATION HARNESS")
        print("=" * 80)

        self.test_schema_integrity()
        self.test_rule_catalog()
        self.test_skill_definition()
        self.test_lifecycle_state_machine()
        self.test_stack_detection_fixtures()
        self.test_educational_differential_fixtures()
        self.test_regression_fixtures()
        self.test_report_formatting()

        print("-" * 80)
        print(f"SUMMARY: {self.passed_tests} Passed | {self.failed_tests} Failed")
        print("=" * 80)
        return self.failed_tests == 0

    def test_schema_integrity(self):
        print("\n1. Testing Formal Schema Integrity...")
        schemas_dir = self.root_dir / "schemas"
        required_schemas = [
            "finding.schema.json",
            "evidence.schema.json",
            "remediation.schema.json",
            "rule.schema.json",
            "lifecycle.schema.json",
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

        has_commands = all(cmd in content for cmd in ["/torusguard init", "/torusguard audit", "/torusguard harden", "/torusguard verify"])
        self.log_test("SKILL.md Core Commands Documented", has_commands)

        refs_dir = self.root_dir / "skills" / "TorusGuard" / "references"
        ref_files = list(refs_dir.glob("*.md"))
        self.log_test(f"Skill Reference Modules ({len(ref_files)})", len(ref_files) >= 7)

    def test_lifecycle_state_machine(self):
        print("\n4. Testing Finding Lifecycle State Machine...")
        # Create test finding
        ev = Evidence(
            type=EvidenceType.SOURCE,
            location="app/views.py:25",
            snippet="Invoice.objects.get(id=pk)",
            rationale="Unscoped primary key lookup without tenant boundary.",
            confidence_level=ConfidenceLevel.CONFIRMED,
            is_sufficient_for_confirmed=True,
        )
        rem = Remediation(
            problem_statement="Missing owner filter in invoice lookup.",
            risk_explanation="Attackers can access arbitrary tenant invoices via IDOR.",
            recommended_fix="Scope queryset to request.user.",
            framework_pattern=FrameworkPattern(
                framework="Django",
                unsafe_snippet="Invoice.objects.get(id=pk)",
                safe_snippet="Invoice.objects.get(id=pk, owner=request.user)",
            ),
            verification_method="Test with cross-tenant user ID.",
            residual_risk_notes="Ensure database index exists on owner column.",
        )
        finding = Finding(
            rule_id="TG-AUTH-007",
            title="Missing Object-Level Authorization",
            category=TaxonomyCategory.AUTH,
            severity=SeverityLevel.HIGH,
            confidence=ConfidenceLevel.CONFIRMED,
            lifecycle_stage=LifecycleStage.DETECT,
            status=FindingStatus.OPEN,
            affected_area=AffectedArea(component="InvoiceAPI", target_path="app/views.py", start_line=25),
            rationale="IDOR risk on invoice lookup.",
            evidence=[ev],
            remediation=rem,
            verification_steps=[VerificationStep(step_number=1, action="Run test", expected_result="404 on cross-user id")],
        )

        # Progression: Detect -> Classify -> Verify -> Remediate -> Recheck -> Archive
        try:
            FindingLifecycleManager.transition(finding, LifecycleStage.CLASSIFY)
            self.log_test("Transition: Detect -> Classify", finding.lifecycle_stage == LifecycleStage.CLASSIFY)

            FindingLifecycleManager.transition(finding, LifecycleStage.VERIFY)
            self.log_test("Transition: Classify -> Verify", finding.lifecycle_stage == LifecycleStage.VERIFY)

            FindingLifecycleManager.transition(finding, LifecycleStage.REMEDIATE)
            self.log_test("Transition: Verify -> Remediate", finding.lifecycle_stage == LifecycleStage.REMEDIATE)

            # Recheck verification
            ok, msg = FindingLifecycleManager.verify_remediation(finding, "fixed code", fix_pattern_present=True)
            self.log_test("Remediation Verification Assertion", ok and finding.status == FindingStatus.VERIFIED_SAFE)

            FindingLifecycleManager.transition(finding, LifecycleStage.ARCHIVE)
            self.log_test("Transition: Recheck -> Archive", finding.lifecycle_stage == LifecycleStage.ARCHIVE)

            # Assert invalid transition from Archive
            try:
                FindingLifecycleManager.transition(finding, LifecycleStage.DETECT)
                self.log_test("Block Invalid Transition from Archive", False, "Should have raised LifecycleTransitionError")
            except LifecycleTransitionError:
                self.log_test("Block Invalid Transition from Archive", True)

        except Exception as e:
            self.log_test("Lifecycle Progression Flow", False, str(e))

    def test_stack_detection_fixtures(self):
        print("\n5. Testing Stack Detection Fixtures...")
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
        print("\n6. Testing Educational Differential Fixtures...")
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
        print("\n7. Testing Python Regression Fixtures Suite...")
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
        print("\n8. Testing Normalized Markdown Report Formatting...")
        ev = Evidence(
            type=EvidenceType.SOURCE,
            location="views.py:10",
            snippet="DEBUG = True",
            rationale="Production debug mode exposure.",
            confidence_level=ConfidenceLevel.CONFIRMED,
            is_sufficient_for_confirmed=True,
        )
        rem = Remediation(
            problem_statement="Debug mode is enabled.",
            risk_explanation="Exposes stack traces and environment secrets.",
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
            severity=SeverityLevel.HIGH,
            confidence=ConfidenceLevel.CONFIRMED,
            lifecycle_stage=LifecycleStage.VERIFY,
            status=FindingStatus.OPEN,
            affected_area=AffectedArea(component="Config", target_path="settings.py", start_line=10),
            rationale="Debug mode leaks internal code paths.",
            evidence=[ev],
            remediation=rem,
            verification_steps=[VerificationStep(step_number=1, action="Check config", expected_result="DEBUG=False")],
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
        has_title = "# TorusGuard Security Audit Report" in md_output
        has_finding = "TG-PLATFORM-003" in md_output
        has_badge = "🔴 Critical" in md_output or "🟠 High" in md_output
        has_diff = "+ DEBUG = False" in md_output

        self.log_test("Render Markdown Audit Report", has_title and has_finding and has_badge and has_diff)


if __name__ == "__main__":
    runner = ValidationHarnessRunner()
    success = runner.run_all()
    sys.exit(0 if success else 1)
