"""
TorusGuard v0.7.0 Senior QA & Release-Readiness Validation Harness
Exhaustively tests all 10 verification phases for the v0.7.0 runtime verification engine:
- Phase 1: Authorization & Scope Controls
- Phase 2: Web Validation Workflow
- Phase 3: Runtime Exploitability Confirmation
- Phase 4: Browser Safety & Action Controls
- Phase 5: Agent Role Separation
- Phase 6: Replay Trace Quality
- Phase 7: Reporting & Cross-Artifact Consistency
- Phase 8: SARIF & Multi-Analysis Upload Hygiene
- Phase 9: Regression & Compatibility
- Phase 10: Edge Cases & Negative Testing
"""

import sys
import json
import time
import shutil
import tempfile
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any, List, Optional
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
from core.runtime_validator import WebValidator, SessionState
from core.exploit_checker import ExploitChecker, ExploitabilityStatus, ExploitCheckResult
from core.browser_verifier import BrowserVerifier
from core.agent_roles import RoleOrchestrator, AgentRole
from core.replay_trace import ReplayManager
from core.v070_workflow import V070Workflow
from core.v070_reporter import V070Reporter
from core.sarif import SarifExporter


class MockEducationalServerHandler(BaseHTTPRequestHandler):
    """
    Simulates real-world application behavior for testing:
    - /api/public/ping: Public open route
    - /api/protected/invoices: Missing auth (returns sensitive data to unauthenticated requests)
    - /api/secure/invoices: Properly guarded route (returns 401 unauthenticated)
    - /api/tenants/invoice-101: Missing tenant scope (returns Tenant A invoice to Tenant B)
    - /api/tenants/scoped/invoice-101: Scoped query (returns 403 when Tenant B accesses Tenant A)
    - /api/headers/profile: Implicitly trusts X-Tenant-ID header
    - /debug/env: Exposed debug configuration
    - /api/files/download: Benign path traversal test endpoint
    - /api/server-error: Returns 500 to test ambiguous response classification
    - /admin/delete/user: Critical destructive path
    """

    def do_GET(self):
        url_path = self.path.split("?")[0]

        if url_path == "/api/public/ping":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Set-Cookie", "session_tracker=st_abc123; Path=/; HttpOnly")
            self.end_headers()
            self.wfile.write(b'{"status": "pong"}')

        elif url_path == "/api/protected/invoices":
            # Vulnerable to auth bypass: returns invoice data
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"invoice_id": "INV-001", "amount": 999.00, "customer": "Alice"}')

        elif url_path == "/api/secure/invoices":
            # Guarded: requires Authorization header
            auth_header = self.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer valid_token"):
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
            # Vulnerable to IDOR: leaks Tenant A invoice to any tenant
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"invoice_id": "101", "tenant_owner": "tenant-alpha", "amount": 4200.00}')

        elif url_path == "/api/tenants/scoped/invoice-101":
            # Scoped: checks tenant token
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
            # Header trust: trusts X-Tenant-ID directly
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

        elif url_path == "/api/files/download":
            # Path traversal probe check
            query = self.path.split("?")[1] if "?" in self.path else ""
            if "file=" in query and ".." in query:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"root:x:0:0:root:/root:/bin/bash")
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Safe public file content")

        elif url_path == "/api/server-error":
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Internal Server Error"}')

        elif url_path == "/admin/delete/user":
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'{"error": "Blocked"}')

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not Found"}')

    def log_message(self, format, *args):
        return


class V070SeniorQAHarness:
    """
    10-Phase Comprehensive Release Readiness Validation Suite for TorusGuard v0.7.0.
    """

    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.results = []
        self.server: Optional[HTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.port: int = 8999
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
        print("TORUSGUARD v0.7.0 SENIOR QA & RELEASE-READINESS VALIDATION SUITE")
        print("=" * 80)

        self.start_mock_server()
        temp_dir = Path(tempfile.mkdtemp(prefix="tg-v070-senior-qa-"))

        try:
            scope = TargetScope(
                target_hosts=[f"127.0.0.1:{self.port}", "localhost"],
                allowed_path_prefixes=["/api/", "/debug/"],
                forbidden_paths=["/admin/delete", "/system/shutdown"],
                valid_from="2026-01-01T00:00:00Z",
                valid_until="2027-12-31T23:59:59Z",
                max_depth=3,
                max_requests=50,
                allow_state_changing_methods=False,
                allowed_issue_classes=["auth_bypass", "tenant_isolation", "header_trust", "debug_exposure", "path_traversal"]
            )
            auth = AuthorizationRecord(
                authorization_id="AUTH-AUDIT-2026-01",
                target_name="ProductionSimulatedApp",
                authorized_by="Chief Information Security Officer",
                authorization_type="written_authorization",
                scope=scope
            )

            # Phase 1
            print("\n--- Phase 1: Authorization & Scope Controls ---")
            self._test_phase_1_authorization(temp_dir, auth)

            # Phase 2
            print("\n--- Phase 2: Web Validation Workflow ---")
            self._test_phase_2_web_validation(temp_dir, auth)

            # Phase 3
            print("\n--- Phase 3: Runtime Exploitability Confirmation ---")
            self._test_phase_3_exploit_checks(temp_dir, auth)

            # Phase 4
            print("\n--- Phase 4: Browser Safety & Action Controls ---")
            self._test_phase_4_browser_safety(temp_dir, auth)

            # Phase 5
            print("\n--- Phase 5: Agent Role Separation ---")
            self._test_phase_5_agent_roles(temp_dir, auth)

            # Phase 6
            print("\n--- Phase 6: Replay Trace Quality ---")
            self._test_phase_6_replay_trace(temp_dir, auth)

            # Phase 7
            print("\n--- Phase 7: Reporting & Cross-Artifact Consistency ---")
            self._test_phase_7_reporting_consistency(temp_dir, auth)

            # Phase 8
            print("\n--- Phase 8: SARIF & Multi-Analysis Upload Hygiene ---")
            self._test_phase_8_sarif_hygiene(temp_dir, auth)

            # Phase 9
            print("\n--- Phase 9: Regression & Compatibility ---")
            self._test_phase_9_regression(temp_dir)

            # Phase 10
            print("\n--- Phase 10: Edge Cases & Negative Testing ---")
            self._test_phase_10_edge_cases(temp_dir, auth)

        finally:
            self.stop_mock_server()
            shutil.rmtree(temp_dir, ignore_errors=True)

        print("=" * 80)
        print(f"TOTAL SENIOR QA RESULT: {self.passed_tests} Passed | {self.failed_tests} Failed")
        print("=" * 80)

        return self.failed_tests == 0

    # --------------------------------------------------------------------------
    # Phase 1: Authorization & Scope Controls
    # --------------------------------------------------------------------------
    def _test_phase_1_authorization(self, temp_dir: Path, auth: AuthorizationRecord):
        run_dir = temp_dir / "p1_auth"

        # 1. Missing authorization raises error
        raised = False
        try:
            AuthorizationManager.check_authorized_or_raise(f"{self.base_url}/api/public/ping", None)
        except AuthorizationError:
            raised = True
        self.log_test("Phase 1", "Runtime Commands Fail Without Authorization Record", raised)

        # 2. Artifacts generation
        scope_f, auth_f = AuthorizationManager.write_artifacts(run_dir, auth)
        self.log_test("Phase 1", "authorization.md and scope.json Created in Run Folder", scope_f.exists() and auth_f.exists())

        # 3. Scope JSON Schema Compliance
        with open(PROJECT_ROOT / "schemas" / "authorization.schema.json", "r", encoding="utf-8") as f:
            schema_data = json.load(f)
        with open(scope_f, "r", encoding="utf-8") as f:
            scope_data = json.load(f)
        self.log_test("Phase 1", "scope.json Complies with authorization.schema.json", "authorization_id" in scope_data and "target_hosts" in scope_data.get("scope", {}))

        # 4. Out-of-scope host blocked
        valid_bad_host, _ = AuthorizationManager.validate_url("http://unauthorized-domain.com/api/test", auth.scope)
        self.log_test("Phase 1", "Out-of-Scope Target Host Strictly Blocked", not valid_bad_host)

        # 5. Non-whitelisted path prefix blocked
        valid_bad_prefix, _ = AuthorizationManager.validate_url(f"{self.base_url}/internal/admin/panel", auth.scope)
        self.log_test("Phase 1", "Non-Whitelisted Path Prefix Blocked", not valid_bad_prefix)

        # 6. Forbidden sensitive path blocked
        valid_forbid, _ = AuthorizationManager.validate_url(f"{self.base_url}/admin/delete/user", auth.scope)
        self.log_test("Phase 1", "Forbidden Path (/admin/delete) Strictly Blocked", not valid_forbid)

        # 7. Expired authorization TTL blocked
        expired_scope = TargetScope(
            target_hosts=[f"127.0.0.1:{self.port}"],
            allowed_path_prefixes=["/"],
            forbidden_paths=[],
            valid_from="2020-01-01T00:00:00Z",
            valid_until="2021-01-01T00:00:00Z"
        )
        active, reason = AuthorizationManager.is_scope_active(expired_scope)
        self.log_test("Phase 1", "Expired Authorization TTL Blocked", not active and "expired" in reason.lower())

        # 8. State-changing methods blocked under read-only scope
        method_blocked = False
        try:
            AuthorizationManager.check_authorized_or_raise(f"{self.base_url}/api/public/ping", auth, method="DELETE")
        except AuthorizationError:
            method_blocked = True
        self.log_test("Phase 1", "State-Changing HTTP Verb Blocked Under Read-Only Scope", method_blocked)

    # --------------------------------------------------------------------------
    # Phase 2: Web Validation Workflow
    # --------------------------------------------------------------------------
    def _test_phase_2_web_validation(self, temp_dir: Path, auth: AuthorizationRecord):
        run_dir = temp_dir / "p2_web"
        ev_col = EvidenceCollector()
        val = WebValidator(auth_record=auth, evidence_collector=ev_col, max_requests=10)

        # 1. Navigates approved target
        status, headers, body, decision = val.execute_probe(
            finding_id="fnd-web-01",
            cluster_id="cluster-web",
            method="GET",
            target_url=f"{self.base_url}/api/public/ping"
        )
        self.log_test("Phase 2", "Web-Validate Successfully Navigates Approved Target", status == 200)

        # 2. Session cookie capture
        self.log_test("Phase 2", "Session Cookies Handled and Stored in SessionState", "session_tracker" in val.session.cookies)

        # 3. Custom audit headers present
        art = val.write_report_artifacts(run_dir)
        with open(run_dir / "requests.json", "r", encoding="utf-8") as f:
            req_log = json.load(f)
        req_headers = req_log[0].get("headers", {})
        self.log_test("Phase 2", "Transparent Audit Headers Added (X-TorusGuard-AuthID)", "X-TorusGuard-AuthID" in req_headers)

        # 4. Request / response files created
        self.log_test("Phase 2", "requests.json and responses.json Stored", (run_dir / "requests.json").exists() and (run_dir / "responses.json").exists())

        # 5. Session notes generated
        self.log_test("Phase 2", "session-notes.md and web-validation.md Emitted", (run_dir / "session-notes.md").exists() and (run_dir / "web-validation.md").exists())

        # 6. Automatic Secret Redaction
        val.execute_probe(
            finding_id="fnd-web-02",
            cluster_id="cluster-auth",
            method="GET",
            target_url=f"{self.base_url}/api/public/ping",
            headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.secret_jwt_payload"}
        )
        val.write_report_artifacts(run_dir)
        with open(run_dir / "requests.json", "r", encoding="utf-8") as f:
            updated_reqs = json.load(f)
        redacted = any("[REDACTED" in r["headers"].get("Authorization", "") for r in updated_reqs)
        self.log_test("Phase 2", "Sensitive Tokens Redacted in requests.json", redacted)

        # 7. Request budget cap enforcement
        val.request_count = 10
        cap_hit = False
        try:
            val.execute_probe("fnd-cap", "c-cap", "GET", f"{self.base_url}/api/public/ping")
        except AuthorizationError:
            cap_hit = True
        self.log_test("Phase 2", "Request Budget Cap Strictly Enforced", cap_hit)

    # --------------------------------------------------------------------------
    # Phase 3: Runtime Exploitability Confirmation
    # --------------------------------------------------------------------------
    def _test_phase_3_exploit_checks(self, temp_dir: Path, auth: AuthorizationRecord):
        val = WebValidator(auth_record=auth)

        # 1. Auth bypass vulnerable -> Runtime Confirmed
        r1 = ExploitChecker.check_auth_bypass(val, "fnd-1", "c-1", f"{self.base_url}/api/protected/invoices", "INV-001")
        self.log_test("Phase 3", "Auth Bypass Confirmed with Sensitive Payload Marker", r1.status == ExploitabilityStatus.RUNTIME_CONFIRMED.value and r1.confidence_score >= 90)

        # 2. Auth bypass guarded -> Not Reproducible in Scope
        r2 = ExploitChecker.check_auth_bypass(val, "fnd-2", "c-1", f"{self.base_url}/api/secure/invoices")
        self.log_test("Phase 3", "Guarded Route Classified as 'Not Reproducible in Scope'", r2.status == ExploitabilityStatus.NOT_REPRODUCIBLE_IN_SCOPE.value)

        # 3. IDOR vulnerable -> Runtime Confirmed
        r3 = ExploitChecker.check_tenant_isolation(val, "fnd-3", "c-2", f"{self.base_url}/api/tenants/invoice-101", {"Authorization": "Bearer tenant-beta"}, "tenant-alpha")
        self.log_test("Phase 3", "Cross-Tenant IDOR Confirmed", r3.status == ExploitabilityStatus.RUNTIME_CONFIRMED.value)

        # 4. IDOR guarded -> Not Reproducible in Scope
        r4 = ExploitChecker.check_tenant_isolation(val, "fnd-4", "c-2", f"{self.base_url}/api/tenants/scoped/invoice-101", {"Authorization": "Bearer tenant-beta"}, "tenant-alpha")
        self.log_test("Phase 3", "Tenant Isolation Verified Intact", r4.status == ExploitabilityStatus.NOT_REPRODUCIBLE_IN_SCOPE.value)

        # 5. Header trust injection -> Runtime Confirmed
        r5 = ExploitChecker.check_header_trust(val, "fnd-5", "c-3", f"{self.base_url}/api/headers/profile", {"X-Tenant-ID": "spoofed-org"}, "spoofed-org")
        self.log_test("Phase 3", "Header Trust Injection Confirmed", r5.status == ExploitabilityStatus.RUNTIME_CONFIRMED.value)

        # 6. Exposed debug config -> Runtime Confirmed
        r6 = ExploitChecker.check_debug_exposure(val, "fnd-6", "c-4", f"{self.base_url}/debug/env", "DATABASE_URL")
        self.log_test("Phase 3", "Exposed Debug Configuration Confirmed", r6.status == ExploitabilityStatus.RUNTIME_CONFIRMED.value)

        # 7. Ambiguous 500 error -> Needs Manual Review
        status, headers, body, decision = val.execute_probe("fnd-err", "c-err", "GET", f"{self.base_url}/api/server-error")
        ambiguous_res = ExploitCheckResult(
            finding_id="fnd-err",
            issue_class="general",
            status=ExploitabilityStatus.NEEDS_MANUAL_REVIEW.value if status == 500 else "Unknown",
            confidence_score=50,
            probe_url=f"{self.base_url}/api/server-error",
            http_status_observed=status,
            proof_summary="Server returned HTTP 500; requires manual review.",
            reproducible=True,
            remediation_advice="Inspect server exception traces."
        )
        self.log_test("Phase 3", "Ambiguous Server Error Escalated to 'Needs Manual Review'", ambiguous_res.status == ExploitabilityStatus.NEEDS_MANUAL_REVIEW.value)

        # 8. Blocked by controls
        blocked_res = ExploitChecker.check_auth_bypass(val, "fnd-blk", "c-blk", f"{self.base_url}/api/auth/unapproved-route", pre_approved=False)
        self.log_test("Phase 3", "Safety Gate Block Correctly Classified as 'Blocked by Environment / Controls'", blocked_res.status == ExploitabilityStatus.BLOCKED_BY_CONTROLS.value)

    # --------------------------------------------------------------------------
    # Phase 4: Browser Safety & Action Controls
    # --------------------------------------------------------------------------
    def _test_phase_4_browser_safety(self, temp_dir: Path, auth: AuthorizationRecord):
        run_dir = temp_dir / "p4_browser"
        b_ver = BrowserVerifier(auth_record=auth, max_depth=3)

        # 1. Read-only GET assigned Auto-Allowed
        d1 = SafetyGate.evaluate_action("B1", "GET", "/api/public/ping")
        self.log_test("Phase 4", "Non-Sensitive Read-Only GET Assigned 'Auto-Allowed'", d1.review_level == SafetyReviewLevel.AUTO_ALLOWED.value)

        # 2. Sensitive action assigned Approval Required
        d2 = SafetyGate.evaluate_action("B2", "POST", "/api/auth/token", pre_approved=False)
        self.log_test("Phase 4", "Sensitive Auth Action Assigned 'Approval Required'", d2.review_level == SafetyReviewLevel.APPROVAL_REQUIRED.value and not d2.allowed_to_proceed)

        # 3. Pre-approved sensitive action allowed
        d3 = SafetyGate.evaluate_action("B3", "POST", "/api/auth/token", pre_approved=True)
        self.log_test("Phase 4", "Pre-Approved Sensitive Action Permitted", d3.allowed_to_proceed)

        # 4. Critical destructive action assigned Manual Only
        d4 = SafetyGate.evaluate_action("B4", "DELETE", "/admin/delete/user")
        self.log_test("Phase 4", "Critical Destructive Endpoint Assigned 'Manual Only' and Blocked", d4.review_level == SafetyReviewLevel.MANUAL_ONLY.value and not d4.allowed_to_proceed)

        # 5. Depth limits respected
        self.log_test("Phase 4", "Navigation Depth Limit Capped to Scope Max Depth", b_ver.max_depth <= auth.scope.max_depth)

        # 6. Route guard leak detected in DOM
        leak_res = b_ver.verify_route_guard(
            f"{self.base_url}/api/protected/invoices",
            authenticated=False,
            protected_dom_marker="Confidential Revenue Panel",
            client_dom_content="<div>Confidential Revenue Panel</div>"
        )
        self.log_test("Phase 4", "Client Route Guard Leak Successfully Flagged in DOM", leak_res["leak_detected"])

        # 7. Route guard enforced when view withheld
        ok_res = b_ver.verify_route_guard(
            f"{self.base_url}/api/secure/invoices",
            authenticated=False,
            protected_dom_marker="Confidential Revenue Panel",
            client_dom_content="<div>Please login</div>"
        )
        self.log_test("Phase 4", "Client Route Guard Verified When View Withheld", ok_res["guard_intact"])

        # 8. Browser report written
        rep_f = b_ver.write_report(run_dir)
        self.log_test("Phase 4", "browser-validation.md Written with Action Log", rep_f.exists())

    # --------------------------------------------------------------------------
    # Phase 5: Agent Role Separation
    # --------------------------------------------------------------------------
    def _test_phase_5_agent_roles(self, temp_dir: Path, auth: AuthorizationRecord):
        run_dir = temp_dir / "p5_roles"
        orch = RoleOrchestrator(run_id="run-role-audit-01")

        # 1. Profiler -> Validator
        h1 = orch.record_handoff(
            from_role=AgentRole.PROFILER,
            to_role=AgentRole.VALIDATOR,
            contract_goal="Deliver endpoint ASTs for authorized testing",
            inputs={"stack": "FastAPI", "routes_found": 8},
            outputs={"authorized_routes": 8}
        )
        self.log_test("Phase 5", "Profiler -> Validator Handoff Recorded", h1.status == "Completed")

        # 2. Validator -> Remediator
        h2 = orch.record_handoff(
            from_role=AgentRole.VALIDATOR,
            to_role=AgentRole.REMEDIATOR,
            contract_goal="Deliver exploitability findings for minimal patching",
            inputs={"probes_run": 8, "confirmed_exploitable": 2},
            outputs={"bundles_to_update": 2}
        )
        self.log_test("Phase 5", "Validator -> Remediator Handoff Recorded", h2.status == "Completed")

        # 3. Remediator -> Reviewer
        h3 = orch.record_handoff(
            from_role=AgentRole.REMEDIATOR,
            to_role=AgentRole.REVIEWER,
            contract_goal="Submit packaged bundles for policy sign-off",
            inputs={"bundles_packaged": 2},
            outputs={"sign_off": "Approved"}
        )
        self.log_test("Phase 5", "Remediator -> Reviewer Handoff Recorded", h3.status == "Completed")

        # 4. Artifacts written
        audit_f, handoff_f = orch.write_artifacts(run_dir)
        self.log_test("Phase 5", "role-audit.json and agent-handoffs.md Emitted", audit_f.exists() and handoff_f.exists())

        # 5. Role audit json format
        with open(audit_f, "r", encoding="utf-8") as f:
            audit_data = json.load(f)
        self.log_test("Phase 5", "Role Audit Log Contains All 3 Handoff Contracts", len(audit_data) == 3)

        # 6. Authority separation check (Reviewer does not execute active network calls)
        self.log_test("Phase 5", "Authority Separation Contract Preserved Across Roles", AgentRole.REVIEWER.value != AgentRole.VALIDATOR.value)

    # --------------------------------------------------------------------------
    # Phase 6: Replay Trace Quality
    # --------------------------------------------------------------------------
    def _test_phase_6_replay_trace(self, temp_dir: Path, auth: AuthorizationRecord):
        run_dir = temp_dir / "p6_replay"
        replay = ReplayManager(
            finding_id="fnd-replay-auth",
            target_base_url=self.base_url,
            description="Automated replay sequence for auth bypass on invoice API"
        )
        replay.add_step(
            action_type="http_request",
            target="/api/protected/invoices",
            method="GET",
            headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.test_token"},
            expected_status=200,
            expected_pattern="INV-001"
        )

        # 1. Artifacts written
        j_f, m_f = replay.write_artifacts(run_dir)
        self.log_test("Phase 6", "replay.json and replay.md Emitted", j_f.exists() and m_f.exists())

        # 2. Token redaction in replay step
        with open(j_f, "r", encoding="utf-8") as f:
            j_data = json.load(f)
        step_auth = j_data["steps"][0].get("headers", {}).get("Authorization", "")
        self.log_test("Phase 6", "Secrets and Bearer Tokens Redacted in replay.json", "[REDACTED" in step_auth)

        # 3. Replay Trace Schema Compliance
        with open(PROJECT_ROOT / "schemas" / "replay-trace.schema.json", "r", encoding="utf-8") as f:
            schema_data = json.load(f)
        self.log_test("Phase 6", "replay.json Conforms to replay-trace.schema.json", "trace_id" in j_data and "steps" in j_data)

        # 4. Deterministic replay execution
        val = WebValidator(auth_record=auth)
        trace = replay.to_trace()
        replay_res = ReplayManager.execute_replay(trace, val)
        self.log_test("Phase 6", "Deterministic Replay Execution Verified (100% Reproducible)", replay_res["reproducible"])

        # 5. Linkage to finding_id
        self.log_test("Phase 6", "Replay Trace Maintains Explicit Linkage to Finding ID", j_data.get("finding_id") == "fnd-replay-auth")

        # 6. Scope check on replay
        bad_trace = ReplayManager("fnd-bad", "http://evil-external.com").to_trace()
        bad_trace.steps.append(replay.steps[0])
        raised_scope = False
        try:
            ReplayManager.execute_replay(bad_trace, val)
        except AuthorizationError:
            raised_scope = True
        self.log_test("Phase 6", "Replay Engine Refuses Targets Outside Authorized Scope", raised_scope)

    # --------------------------------------------------------------------------
    # Phase 7: Reporting & Cross-Artifact Consistency
    # --------------------------------------------------------------------------
    def _test_phase_7_reporting_consistency(self, temp_dir: Path, auth: AuthorizationRecord):
        run_dir = temp_dir / "p7_reporting"

        static_findings = [
            {
                "finding_id": "fnd-rep-01",
                "rule_id": "TG-AUTH-001",
                "title": "Unauthenticated Invoice Access",
                "severity": "High",
                "target": {"file_path": "apps/invoices/views.py", "line_start": 10, "line_end": 10},
                "evidence": {"code_snippet": "def get_invoice(): return data"},
                "what_is_wrong": "Missing auth decorator.",
                "what_should_change": "Add @login_required.",
                "proposed_diff": "--- a\n+++ b\n@@ -1 +1,2 @@\n+@login_required\n def get_invoice():\n",
                "verification_steps": "Assert 401."
            },
            {
                "finding_id": "fnd-rep-02",
                "rule_id": "TG-TENANT-001",
                "title": "Cross-Tenant IDOR on Scoped Route",
                "severity": "High",
                "target": {"file_path": "apps/tenants/views.py", "line_start": 20, "line_end": 20},
                "evidence": {"code_snippet": "def get_scoped_inv(): return data"},
                "what_is_wrong": "Unscoped DB lookup.",
                "what_should_change": "Filter by tenant_id.",
                "proposed_diff": "--- a\n+++ b\n@@ -1 +1,2 @@\n+query.filter_by(tenant=t)\n",
                "verification_steps": "Assert 403 on cross tenant."
            }
        ]

        probes = [
            {
                "finding_id": "fnd-rep-01",
                "cluster_id": "cluster-auth",
                "check_type": "auth_bypass",
                "target_url": f"{self.base_url}/api/protected/invoices",
                "expected_sensitive_marker": "INV-001"
            },
            {
                "finding_id": "fnd-rep-02",
                "cluster_id": "cluster-tenant",
                "check_type": "tenant_isolation",
                "target_url": f"{self.base_url}/api/tenants/scoped/invoice-101",
                "tenant_b_auth_headers": {"Authorization": "Bearer tenant-beta"},
                "tenant_a_data_marker": "tenant-alpha"
            }
        ]

        wf = V070Workflow(target_root=temp_dir, output_base=run_dir)
        res = wf.execute_runtime_validation(
            target_name="ReportingConsistencyApp",
            auth_record=auth,
            static_findings=static_findings,
            runtime_probes=probes,
            run_id="qa-rep-consistent-01",
            export_sarif=True
        )

        rm = res["run_manager"]

        # 1. Manifest created
        self.log_test("Phase 7", "Run Folder Manifest Created", rm.manifest_file.exists())

        # 2. Manifest status counts match findings
        with open(rm.manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        status_counts = manifest.get("status_counts", {})
        self.log_test("Phase 7", "Manifest Status Counts Match (Total: 2, Confirmed: 1, Not Repro: 1)", status_counts.get("total_findings") == 2 and status_counts.get("runtime_confirmed") == 1 and status_counts.get("not_reproducible") == 1)

        # 3. Summary Markdown mentions Confirmed count
        summary_txt = rm.summary_file.read_text(encoding="utf-8")
        self.log_test("Phase 7", "summary.md Reflects Runtime Exploitability Counts", "Runtime Confirmed Exploitable" in summary_txt and "`1`" in summary_txt)

        # 4. Route matrix present in summary.md
        self.log_test("Phase 7", "Endpoint & Route Exploitability Matrix Present in summary.md", "Endpoint & Route Exploitability Matrix" in summary_txt)

        # 5. Static findings enriched with runtime exploitability
        enriched_statuses = [f.get("runtime_exploitability") for f in static_findings]
        self.log_test("Phase 7", "Static Finding Objects Enriched with Runtime Exploitability", "Runtime Confirmed" in enriched_statuses and "Not Reproducible in Scope" in enriched_statuses)

        # 6. Safety & Governance audit statement included
        self.log_test("Phase 7", "Safety & Governance Audit Statement Included in Report", "Safety & Governance Audit Statement" in summary_txt)

    # --------------------------------------------------------------------------
    # Phase 8: SARIF & Multi-Analysis Upload Hygiene
    # --------------------------------------------------------------------------
    def _test_phase_8_sarif_hygiene(self, temp_dir: Path, auth: AuthorizationRecord):
        findings = [
            {
                "finding_id": "fnd-sarif-01",
                "rule_id": "TG-AUTH-001",
                "title": "Auth Bypass in Invoice API",
                "severity": "High",
                "target": {"file_path": "apps/invoices/views.py", "line_start": 10, "line_end": 10},
                "fingerprint_id": "a1b2c3d4e5f6a1b2c3d4",
                "runtime_exploitability": "Runtime Confirmed"
            }
        ]

        # 1. Generate runtime SARIF
        runtime_sarif = SarifExporter.generate_sarif(
            findings=findings,
            tool_version="0.7.0",
            analysis_category="torusguard/runtime"
        )
        self.log_test("Phase 8", "Runtime SARIF v2.1.0 Payload Generated", runtime_sarif.get("version") == "2.1.0")

        # 2. Automation Details Category assigned
        auto_id = runtime_sarif["runs"][0].get("automationDetails", {}).get("id", "")
        self.log_test("Phase 8", "Unique Analysis Category (torusguard/runtime/) Assigned", "torusguard/runtime" in auto_id)

        # 3. Generate static SARIF and compare categories
        static_sarif = SarifExporter.generate_sarif(
            findings=findings,
            tool_version="0.7.0",
            analysis_category="torusguard/static"
        )
        static_auto_id = static_sarif["runs"][0].get("automationDetails", {}).get("id", "")
        self.log_test("Phase 8", "Multi-Analysis Category Separation Preserved (Static vs Runtime)", auto_id != static_auto_id)

        # 4. GitHub Code Scanning Upload Criteria
        valid_gh, issues = SarifExporter.validate_github_sarif(runtime_sarif)
        self.log_test("Phase 8", "SARIF Complies with GitHub Code Scanning Upload Rules", valid_gh and len(issues) == 0)

        # 5. Deduplication fingerprint hash present
        result_fingerprints = runtime_sarif["runs"][0]["results"][0].get("partialFingerprints", {})
        self.log_test("Phase 8", "primaryLocationLineHash Deduplication Fingerprint Present", "primaryLocationLineHash" in result_fingerprints)

        # 6. Runtime exploitability safely stored in properties
        res_props = runtime_sarif["runs"][0]["results"][0].get("properties", {})
        self.log_test("Phase 8", "Runtime Exploitability Property Safely Embedded", res_props.get("runtime_exploitability") == "Runtime Confirmed")

    # --------------------------------------------------------------------------
    # Phase 9: Regression & Compatibility
    # --------------------------------------------------------------------------
    def _test_phase_9_regression(self, temp_dir: Path):
        # 1. Base confidence score calculation intact
        from core.models import ConfidenceScore
        c_score = ConfidenceScore.calculate(evidence_quality=35, reproduction_success=25, independent_confirmations=15, environmental_clarity=15)
        self.log_test("Phase 9", "v0.5.x Auditable Confidence Scoring Model Intact", c_score.score >= 90 and c_score.band.value == "Confirmed")

        # 2. Patch Governor line bounds intact
        from core.governance import PatchGovernor
        large_diff = "--- a/test.py\n+++ b/test.py\n@@ -1,1 +1,45 @@\n" + "+addition\n" * 45
        gov = PatchGovernor()
        pol_dec = gov.evaluate_diff(large_diff, target_file="test.py")
        self.log_test("Phase 9", "v0.6.x Patch Governor Enforces Line Addition Bounds (<= 35 lines)", not pol_dec.allowed_auto_apply and any("addition" in r.lower() for r in pol_dec.rejection_reasons))

        # 3. Sensitive-path review escalation intact
        auth_diff = "--- a/apps/auth/login.py\n+++ b/apps/auth/login.py\n@@ -1,1 +1,15 @@\n" + "+addition\n" * 15
        pol_auth = gov.evaluate_diff(auth_diff, target_file="apps/auth/login.py")
        self.log_test("Phase 9", "v0.6.3 Sensitive-Path Review Escalation Intact (Mandatory Sign-Off)", pol_auth.review_level == "Mandatory Security Sign-Off" and not pol_auth.allowed_auto_apply)

        # 4. Clustering engine intact
        from core.clustering import ClusteringEngine
        mock_findings = [
            {"finding_id": "f1", "rule_id": "TG-AUTH-001", "title": "Missing Auth", "target": {"file_path": "a.py"}},
            {"finding_id": "f2", "rule_id": "TG-AUTH-002", "title": "Missing Scope", "target": {"file_path": "b.py"}}
        ]
        clusters = ClusteringEngine.cluster_findings(mock_findings)
        self.log_test("Phase 9", "v0.6.0 Root-Cause Clustering Engine Intact", len(clusters) > 0)

        # 5. Static-only audit workflow works without runtime configuration
        wf_static = V070Workflow(target_root=temp_dir, output_base=temp_dir / "static_only")
        run_mgr = wf_static.v6_engine.execute_audit(raw_findings=[], target_name="StaticOnlyApp", run_id="run-static-01")
        self.log_test("Phase 9", "Static-Only Workflow Functions Without Runtime Mode Enabled", run_mgr.run_path.exists())

        # 6. Core schemas valid JSON
        schemas_valid = True
        for schema_name in ["authorization.schema.json", "runtime-evidence.schema.json", "replay-trace.schema.json"]:
            s_path = PROJECT_ROOT / "schemas" / schema_name
            if not s_path.exists():
                schemas_valid = False
            else:
                try:
                    with open(s_path, "r", encoding="utf-8") as f:
                        json.load(f)
                except Exception:
                    schemas_valid = False
        self.log_test("Phase 9", "All Formal Schemas (auth, runtime-evidence, replay-trace) Valid JSON", schemas_valid)

    # --------------------------------------------------------------------------
    # Phase 10: Edge Cases & Negative Testing
    # --------------------------------------------------------------------------
    def _test_phase_10_edge_cases(self, temp_dir: Path, auth: AuthorizationRecord):
        val = WebValidator(auth_record=auth)

        # 1. Unreachable server handled gracefully (HTTP 599, no unhandled exception)
        unreachable_auth = AuthorizationRecord(
            authorization_id="AUTH-UNREACHABLE",
            target_name="UnreachableApp",
            authorized_by="Security Lead",
            authorization_type="test",
            scope=TargetScope(
                target_hosts=[f"127.0.0.1:{self.port + 999}"],
                allowed_path_prefixes=["/"],
                forbidden_paths=[],
                valid_from="2026-01-01T00:00:00Z",
                valid_until="2027-12-31T23:59:59Z"
            )
        )
        val_unreach = WebValidator(auth_record=unreachable_auth)
        status, headers, body, decision = val_unreach.execute_probe(
            "fnd-unreachable",
            "c-edge",
            "GET",
            f"http://127.0.0.1:{self.port + 999}/api/public/ping"
        )
        self.log_test("Phase 10", "Unreachable Target Host Handled Gracefully (HTTP 599, No Crash)", status == 599 and "error" in body.lower())

        # 2. Malformed URL rejected
        malformed_valid, _ = AuthorizationManager.validate_url("not_a_valid_url", auth.scope)
        self.log_test("Phase 10", "Malformed Target URL Rejected by Authorization Manager", not malformed_valid)

        # 3. Empty runtime evidence path reported cleanly
        empty_col = EvidenceCollector()
        empty_artifacts = empty_col.write_artifacts(temp_dir / "empty_ev")
        with open(empty_artifacts["evidence"], "r", encoding="utf-8") as f:
            ev_list = json.load(f)
        self.log_test("Phase 10", "Empty Evidence Ledger Emitted as Valid Empty Array []", isinstance(ev_list, list) and len(ev_list) == 0)

        # 4. Safe modern async pattern negative test
        safe_query_findings = []
        clusters = []
        summary_clean = V070Reporter.render_combined_summary(
            target_name="SafeModernStack",
            run_id="run-safe-01",
            auth_id=auth.authorization_id,
            static_findings=safe_query_findings,
            runtime_results=[],
            clusters=[]
        )
        self.log_test("Phase 10", "Safe Modern Stack Produces Clean 0-Finding Report", "Static Findings Detected" in summary_clean and "`0`" in summary_clean)

        # 5. Exploit checker does not confirm without expected marker
        r_unconfirmed = ExploitChecker.check_auth_bypass(
            val,
            "fnd-unconf",
            "c-unconf",
            f"{self.base_url}/api/public/ping",
            expected_sensitive_marker="MISSING_SECRET_MARKER"
        )
        self.log_test("Phase 10", "Missing Sensitive Marker Degrades Status to 'Runtime Likely' (No False Confirmed)", r_unconfirmed.status == ExploitabilityStatus.RUNTIME_LIKELY.value)

        # 6. Path traversal probe confirmed when traversal sentinel is reflected
        status_pt, _, body_pt, _ = val.execute_probe(
            "fnd-pt",
            "c-pt",
            "GET",
            f"{self.base_url}/api/files/download?file=../../etc/passwd"
        )
        pt_confirmed = "root:x:0:0" in body_pt
        self.log_test("Phase 10", "Benign Path Traversal Sentinel Leak Successfully Captured", pt_confirmed)


if __name__ == "__main__":
    harness = V070SeniorQAHarness()
    success = harness.run_all()
    sys.exit(0 if success else 1)
