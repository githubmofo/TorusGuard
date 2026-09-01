"""
TorusGuard v0.7.0 Runtime Validation & Bounded Exploitability Harness
Validates all capabilities of the v0.7.0 runtime verification engine:
1. Authorization & Scope Gate Enforcement
2. Safety Review Gates (Auto-Allowed, Approval Required, Manual Only)
3. Web Validation & Token/Credential Redaction
4. Bounded Exploitability Confirmation (Auth bypass, IDOR, Header trust, Debug exposure)
5. Browser-Assisted Route Guard & DOM Evidence Verification
6. Multi-Agent Role Governance & Handoff Audit Trail
7. Replay Trace Recording & Deterministic Replay Execution
8. Unified v0.7.0 End-to-End Workflow, Reporting, and Multi-Analysis SARIF
"""

import sys
import json
import time
import shutil
import tempfile
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.authorization import (
    AuthorizationManager,
    AuthorizationRecord,
    TargetScope,
    AuthorizationError
)
from core.safety_gate import SafetyGate, SafetyReviewLevel
from core.runtime_evidence import EvidenceCollector, RedactionEngine
from core.runtime_validator import WebValidator
from core.exploit_checker import ExploitChecker, ExploitabilityStatus
from core.browser_verifier import BrowserVerifier
from core.agent_roles import RoleOrchestrator, AgentRole
from core.replay_trace import ReplayManager
from core.v070_workflow import V070Workflow
from core.v070_reporter import V070Reporter
from core.sarif import SarifExporter


class MockEducationalServerHandler(BaseHTTPRequestHandler):
    """
    Educational mock server simulating authentic backend responses for testing:
    - /api/public/ping: Public open route
    - /api/protected/invoices: Vulnerable to auth bypass (leaks invoice without auth)
    - /api/secure/invoices: Secure route (returns 401 unauthenticated)
    - /api/tenants/invoice-101: Vulnerable to cross-tenant IDOR
    - /api/tenants/scoped/invoice-101: Secure tenant-isolated route (returns 403 on cross-tenant)
    - /api/headers/profile: Vulnerable to X-Tenant-ID header trust injection
    - /debug/env: Exposed internal debug configuration
    - /admin/delete/user: Critical destructive path
    """

    def do_GET(self):
        url_path = self.path.split("?")[0]

        if url_path == "/api/public/ping":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "pong"}')

        elif url_path == "/api/protected/invoices":
            # Vulnerable to auth bypass: leaks invoice data
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"invoice_id": "INV-001", "amount": 999.00, "customer": "Alice"}')

        elif url_path == "/api/secure/invoices":
            # Secure: requires Authorization header
            auth_header = self.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer valid_token"):
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Unauthorized"}')
            else:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"invoice_id": "INV-SEC", "amount": 500.00}')

        elif url_path == "/api/tenants/invoice-101":
            # Cross-tenant IDOR: returns Tenant A data even if requested by Tenant B
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"invoice_id": "101", "tenant_owner": "tenant-alpha", "amount": 4200.00}')

        elif url_path == "/api/tenants/scoped/invoice-101":
            # Scoped query: checks tenant token
            auth_header = self.headers.get("Authorization", "")
            if "tenant-beta" in auth_header:
                self.send_response(403)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Forbidden: Tenant mismatch"}')
            else:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"invoice_id": "101", "tenant_owner": "tenant-alpha"}')

        elif url_path == "/api/headers/profile":
            # Header trust: trusts X-Tenant-ID header directly
            tenant_header = self.headers.get("X-Tenant-ID", "tenant-guest")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(f'{{"active_tenant": "{tenant_header}"}}'.encode("utf-8"))

        elif url_path == "/debug/env":
            # Exposed debug config
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"DEBUG": true, "DATABASE_URL": "sqlite:////app/db.sqlite3"}')

        elif url_path == "/admin/delete/user":
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'{"error": "Blocked"}')

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not Found"}')

    def log_message(self, format, *args):
        # Silence console log noise during test runs
        return


class V070ValidationHarness:
    """
    Test suite verifying TorusGuard v0.7.0.
    """

    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.results = []
        self.server: Optional[HTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.port: int = 8998
        self.base_url: str = f"http://127.0.0.1:{self.port}"

    def start_mock_server(self):
        self.server = HTTPServer(("127.0.0.1", self.port), MockEducationalServerHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        time.sleep(0.1)

    def stop_mock_server(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()

    def log_test(self, phase: str, item: str, passed: bool, details: str = ""):
        status_str = "PASS" if passed else "FAIL"
        if passed:
            self.passed_tests += 1
            print(f"  [{status_str}] [{phase}] {item}")
        else:
            self.failed_tests += 1
            print(f"  [{status_str}] [{phase}] {item} -> {details}")

        self.results.append({
            "phase": phase,
            "item": item,
            "passed": passed,
            "details": details
        })

    def run_all(self) -> bool:
        print("=" * 80)
        print("TORUSGUARD v0.7.0 RUNTIME VALIDATION & EXPLOITABILITY HARNESS")
        print("=" * 80)

        self.start_mock_server()
        temp_dir = Path(tempfile.mkdtemp(prefix="tg-v070-qa-"))

        try:
            # Setup Scope & Auth
            scope = TargetScope(
                target_hosts=[f"127.0.0.1:{self.port}", "localhost"],
                allowed_path_prefixes=["/api/", "/debug/"],
                forbidden_paths=["/admin/delete", "/system/shutdown"],
                valid_from="2026-01-01T00:00:00Z",
                valid_until="2027-12-31T23:59:59Z",
                max_depth=3,
                max_requests=50,
                allow_state_changing_methods=False,
                allowed_issue_classes=["auth_bypass", "tenant_isolation", "header_trust", "debug_exposure"]
            )
            auth = AuthorizationRecord(
                authorization_id="AUTH-TEST-2026-01",
                target_name="EducationalMockApp",
                authorized_by="Lead Security Architect",
                authorization_type="ci_sandboxed_test",
                scope=scope
            )

            # Phase 1: Authorization Gate
            print("\n--- Phase 1: Authorization & Scope Gate Enforcement ---")
            self._test_phase_1_authorization(temp_dir, auth)

            # Phase 2: Safety Review Gates
            print("\n--- Phase 2: Safety Review Gates ---")
            self._test_phase_2_safety_gates(temp_dir)

            # Phase 3: Web Validation & Evidence Redaction
            print("\n--- Phase 3: Web Validation & Evidence Redaction ---")
            self._test_phase_3_web_validation(temp_dir, auth)

            # Phase 4: Bounded Exploitability Confirmation
            print("\n--- Phase 4: Bounded Exploitability Confirmation ---")
            self._test_phase_4_exploit_checks(temp_dir, auth)

            # Phase 5: Browser-Assisted Route Guard Verification
            print("\n--- Phase 5: Browser-Assisted Route Guard Verification ---")
            self._test_phase_5_browser_verification(temp_dir, auth)

            # Phase 6: Multi-Agent Role Governance & Replay Trace
            print("\n--- Phase 6: Multi-Agent Roles & Replay Trace ---")
            self._test_phase_6_roles_and_replay(temp_dir, auth)

            # Phase 7: End-to-End Workflow & Multi-Analysis SARIF
            print("\n--- Phase 7: End-to-End Workflow & SARIF Multi-Analysis ---")
            self._test_phase_7_workflow(temp_dir, auth)

        finally:
            self.stop_mock_server()
            shutil.rmtree(temp_dir, ignore_errors=True)

        print("=" * 80)
        print(f"v0.7.0 HARNESS RESULT: {self.passed_tests} Passed | {self.failed_tests} Failed")
        print("=" * 80)

        return self.failed_tests == 0

    def _test_phase_1_authorization(self, temp_dir: Path, auth: AuthorizationRecord):
        run_dir = temp_dir / "phase1_auth"

        # 1. Scope artifact generation
        scope_f, auth_f = AuthorizationManager.write_artifacts(run_dir, auth)
        self.log_test("Phase 1", "Scope JSON and Authorization MD Generated", scope_f.exists() and auth_f.exists())

        # 2. In-scope validation
        valid, msg = AuthorizationManager.validate_url(f"{self.base_url}/api/public/ping", auth.scope)
        self.log_test("Phase 1", "In-Scope URL Approved", valid)

        # 3. Out-of-scope host blocked
        valid_bad_host, _ = AuthorizationManager.validate_url("http://external-evil.com/api/test", auth.scope)
        self.log_test("Phase 1", "Out-of-Scope Host Blocked", not valid_bad_host)

        # 4. Forbidden path blocked
        valid_forbid, _ = AuthorizationManager.validate_url(f"{self.base_url}/admin/delete/user", auth.scope)
        self.log_test("Phase 1", "Forbidden Path Blocked", not valid_forbid)

        # 5. Missing auth check raises AuthorizationError
        raised = False
        try:
            AuthorizationManager.check_authorized_or_raise(f"{self.base_url}/api/public/ping", None)
        except AuthorizationError:
            raised = True
        self.log_test("Phase 1", "Missing Authorization Record Raises AuthorizationError", raised)

    def _test_phase_2_safety_gates(self, temp_dir: Path):
        # 1. Read-only GET on public path -> Auto-Allowed
        d1 = SafetyGate.evaluate_action("A1", "GET", "/api/public/ping")
        self.log_test("Phase 2", "Read-Only GET Assigned 'Auto-Allowed'", d1.review_level == SafetyReviewLevel.AUTO_ALLOWED.value and d1.allowed_to_proceed)

        # 2. Sensitive path (auth/token) -> Approval Required
        d2 = SafetyGate.evaluate_action("A2", "POST", "/api/auth/token", pre_approved=False)
        self.log_test("Phase 2", "Auth POST Assigned 'Approval Required' and Blocked without pre-approval", d2.review_level == SafetyReviewLevel.APPROVAL_REQUIRED.value and not d2.allowed_to_proceed)

        # 3. Pre-approved sensitive action -> Allowed
        d3 = SafetyGate.evaluate_action("A3", "POST", "/api/auth/token", pre_approved=True)
        self.log_test("Phase 2", "Pre-Approved Sensitive Action Permitted", d3.allowed_to_proceed)

        # 4. Critical destructive action -> Manual Only
        d4 = SafetyGate.evaluate_action("A4", "DELETE", "/admin/delete/user")
        self.log_test("Phase 2", "Critical Deletion Path Assigned 'Manual Only' and Strictly Blocked", d4.review_level == SafetyReviewLevel.MANUAL_ONLY.value and not d4.allowed_to_proceed)

    def _test_phase_3_web_validation(self, temp_dir: Path, auth: AuthorizationRecord):
        run_dir = temp_dir / "phase3_web"
        ev_col = EvidenceCollector()
        val = WebValidator(auth_record=auth, evidence_collector=ev_col)

        # Execute probe with Bearer token to test redaction
        status, headers, body, decision = val.execute_probe(
            finding_id="TG-FND-001",
            cluster_id="cluster-auth",
            method="GET",
            target_url=f"{self.base_url}/api/public/ping",
            headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.secret_signature"}
        )
        self.log_test("Phase 3", "Web Validator Probe Successfully Executed (HTTP 200)", status == 200)

        artifacts = val.write_report_artifacts(run_dir)
        self.log_test("Phase 3", "Web Validation Artifacts Emitted (requests, responses, session-notes)", (run_dir / "requests.json").exists() and (run_dir / "web-validation.md").exists())

        # Check Redaction
        with open(run_dir / "requests.json", "r", encoding="utf-8") as f:
            req_data = json.load(f)
        auth_header = req_data[0]["headers"].get("Authorization", "")
        self.log_test("Phase 3", "Bearer JWT Header Redacted in requests.json", "[REDACTED_TOKEN]" in auth_header or "[REDACTED_JWT]" in auth_header)

    def _test_phase_4_exploit_checks(self, temp_dir: Path, auth: AuthorizationRecord):
        val = WebValidator(auth_record=auth)

        # 1. Auth bypass on vulnerable endpoint -> Runtime Confirmed
        r_vuln = ExploitChecker.check_auth_bypass(
            validator=val,
            finding_id="fnd-auth-01",
            cluster_id="cluster-auth",
            endpoint_url=f"{self.base_url}/api/protected/invoices",
            expected_sensitive_marker="INV-001"
        )
        self.log_test("Phase 4", "Auth Bypass Confirmed on Vulnerable Route", r_vuln.status == ExploitabilityStatus.RUNTIME_CONFIRMED.value and r_vuln.confidence_score >= 95)

        # 2. Auth bypass on protected endpoint -> Not Reproducible in Scope
        r_sec = ExploitChecker.check_auth_bypass(
            validator=val,
            finding_id="fnd-auth-02",
            cluster_id="cluster-auth",
            endpoint_url=f"{self.base_url}/api/secure/invoices"
        )
        self.log_test("Phase 4", "Auth Bypass Marked 'Not Reproducible in Scope' on Guarded Route", r_sec.status == ExploitabilityStatus.NOT_REPRODUCIBLE_IN_SCOPE.value)

        # 3. IDOR on cross-tenant endpoint -> Runtime Confirmed
        r_idor = ExploitChecker.check_tenant_isolation(
            validator=val,
            finding_id="fnd-idor-01",
            cluster_id="cluster-tenant-isolation",
            tenant_a_resource_url=f"{self.base_url}/api/tenants/invoice-101",
            tenant_b_auth_headers={"Authorization": "Bearer tenant-beta-token"},
            tenant_a_data_marker="tenant-alpha"
        )
        self.log_test("Phase 4", "Cross-Tenant IDOR Confirmed", r_idor.status == ExploitabilityStatus.RUNTIME_CONFIRMED.value)

        # 4. IDOR on scoped endpoint -> Not Reproducible in Scope
        r_idor_scoped = ExploitChecker.check_tenant_isolation(
            validator=val,
            finding_id="fnd-idor-02",
            cluster_id="cluster-tenant-isolation",
            tenant_a_resource_url=f"{self.base_url}/api/tenants/scoped/invoice-101",
            tenant_b_auth_headers={"Authorization": "Bearer tenant-beta-token"},
            tenant_a_data_marker="tenant-alpha"
        )
        self.log_test("Phase 4", "Tenant Scoping Holds on Properly Guarded Endpoint", r_idor_scoped.status == ExploitabilityStatus.NOT_REPRODUCIBLE_IN_SCOPE.value)

        # 5. Header Trust Injection -> Runtime Confirmed
        r_hdr = ExploitChecker.check_header_trust(
            validator=val,
            finding_id="fnd-hdr-01",
            cluster_id="cluster-header-trust",
            endpoint_url=f"{self.base_url}/api/headers/profile",
            spoofed_headers={"X-Tenant-ID": "spoofed-corp"},
            expected_reflection_marker="spoofed-corp"
        )
        self.log_test("Phase 4", "Header Trust Injection Confirmed", r_hdr.status == ExploitabilityStatus.RUNTIME_CONFIRMED.value)

        # 6. Exposed Debug Configuration -> Runtime Confirmed
        r_dbg = ExploitChecker.check_debug_exposure(
            validator=val,
            finding_id="fnd-dbg-01",
            cluster_id="cluster-config",
            debug_url=f"{self.base_url}/debug/env",
            debug_marker="DATABASE_URL"
        )
        self.log_test("Phase 4", "Exposed Debug Environment Confirmed", r_dbg.status == ExploitabilityStatus.RUNTIME_CONFIRMED.value)

    def _test_phase_5_browser_verification(self, temp_dir: Path, auth: AuthorizationRecord):
        run_dir = temp_dir / "phase5_browser"
        b_ver = BrowserVerifier(auth_record=auth, max_depth=2)

        # Verify route guard failure (leak in unauthenticated DOM)
        res_leak = b_ver.verify_route_guard(
            target_url=f"{self.base_url}/api/protected/invoices",
            authenticated=False,
            protected_dom_marker="Admin Financial Dashboard",
            client_dom_content="<div><h1>Admin Financial Dashboard</h1><p>Confidential revenue data</p></div>"
        )
        self.log_test("Phase 5", "Client Route Guard Leak Detected in DOM", res_leak["leak_detected"])

        # Verify route guard enforcement (no leak)
        res_ok = b_ver.verify_route_guard(
            target_url=f"{self.base_url}/api/secure/invoices",
            authenticated=False,
            protected_dom_marker="Admin Financial Dashboard",
            client_dom_content="<div><p>Please log in to continue</p></div>"
        )
        self.log_test("Phase 5", "Client Route Guard Enforced when Protected View Withheld", res_ok["guard_intact"])

        report = b_ver.write_report(run_dir)
        self.log_test("Phase 5", "Browser Validation Report Written", report.exists())

    def _test_phase_6_roles_and_replay(self, temp_dir: Path, auth: AuthorizationRecord):
        run_dir = temp_dir / "phase6_roles_replay"

        # 1. Role Orchestration
        orch = RoleOrchestrator(run_id="run-role-test-01")
        h1 = orch.record_handoff(
            from_role=AgentRole.PROFILER,
            to_role=AgentRole.VALIDATOR,
            contract_goal="Deliver endpoint ASTs",
            inputs={"endpoints": 5},
            outputs={"targets": 5}
        )
        h2 = orch.record_handoff(
            from_role=AgentRole.VALIDATOR,
            to_role=AgentRole.REMEDIATOR,
            contract_goal="Deliver exploitability evidence",
            inputs={"confirmed": 1},
            outputs={"bundles_needed": 1}
        )
        audit_f, handoff_f = orch.write_artifacts(run_dir)
        self.log_test("Phase 6", "Role Audit and Agent Handoff Artifacts Emitted", audit_f.exists() and handoff_f.exists())

        # 2. Replay Manager & Deterministic Replay Execution
        replay = ReplayManager(
            finding_id="fnd-auth-01",
            target_base_url=self.base_url,
            description="Replay of auth bypass on /api/protected/invoices"
        )
        replay.add_step(
            action_type="http_request",
            target="/api/protected/invoices",
            method="GET",
            expected_status=200,
            expected_pattern="INV-001"
        )
        r_json, r_md = replay.write_artifacts(run_dir)
        self.log_test("Phase 6", "Replay JSON and Replay MD Written", r_json.exists() and r_md.exists())

        val = WebValidator(auth_record=auth)
        trace = replay.to_trace()
        replay_res = ReplayManager.execute_replay(trace, val)
        self.log_test("Phase 6", "Deterministic Replay Successfully Re-verified Vulnerability", replay_res["reproducible"])

    def _test_phase_7_workflow(self, temp_dir: Path, auth: AuthorizationRecord):
        run_dir = temp_dir / "phase7_workflow"

        static_findings = [
            {
                "finding_id": "fnd-audit-01",
                "rule_id": "TG-AUTH-001",
                "title": "Missing Authentication Barrier on Invoice API",
                "severity": "High",
                "target": {"file_path": "apps/invoices/views.py", "line_start": 10, "line_end": 10},
                "evidence": {"code_snippet": "def view_invoice(req): return JsonResponse(inv)"},
                "what_is_wrong": "Unauthenticated access permitted.",
                "what_should_change": "Add authentication dependency.",
                "proposed_diff": "--- a/views.py\n+++ b/views.py\n@@ -1,1 +1,2 @@\n-def view_invoice(req):\n+@login_required\n+def view_invoice(req):\n",
                "verification_steps": "Assert 401 unauthenticated."
            }
        ]

        probes = [
            {
                "finding_id": "fnd-audit-01",
                "cluster_id": "cluster-auth",
                "check_type": "auth_bypass",
                "target_url": f"{self.base_url}/api/protected/invoices",
                "expected_sensitive_marker": "INV-001"
            }
        ]

        wf = V070Workflow(target_root=temp_dir, output_base=run_dir)
        res = wf.execute_runtime_validation(
            target_name="WorkflowVerificationApp",
            auth_record=auth,
            static_findings=static_findings,
            runtime_probes=probes,
            run_id="qa-v070-e2e-01",
            export_sarif=True
        )

        rm = res["run_manager"]
        self.log_test("Phase 7", "End-to-End Workflow Emitted Manifest and Summary", rm.manifest_file.exists() and rm.summary_file.exists())
        self.log_test("Phase 7", "SARIF File Generated with Runtime Analysis Category", rm.sarif_file.exists())

        # Check SARIF multi-analysis category
        with open(rm.sarif_file, "r", encoding="utf-8") as f:
            sarif_data = json.load(f)
        automation_id = sarif_data["runs"][0].get("automationDetails", {}).get("id", "")
        self.log_test("Phase 7", "SARIF automationDetails Contains 'torusguard/runtime/'", "torusguard/runtime" in automation_id)

        # Check summary report mentions Runtime Confirmed
        summary_txt = rm.summary_file.read_text(encoding="utf-8")
        self.log_test("Phase 7", "Combined Report Contains 'Runtime Confirmed Exploitable'", "Runtime Confirmed Exploitable" in summary_txt)


if __name__ == "__main__":
    harness = V070ValidationHarness()
    success = harness.run_all()
    sys.exit(0 if success else 1)
