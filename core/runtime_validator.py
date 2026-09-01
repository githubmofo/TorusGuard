"""
TorusGuard v0.7.0 Web Validation Engine
Executes authorized HTTP probes against running applications, captures requests/responses,
maintains session state across endpoints, and strictly abides by scope & safety gates.
"""

import json
import urllib.request
import urllib.error
from urllib.parse import urljoin, urlparse
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field

from core.authorization import AuthorizationRecord, AuthorizationManager, AuthorizationError
from core.safety_gate import SafetyGate, SafetyDecision, SafetyReviewLevel
from core.runtime_evidence import EvidenceCollector, RuntimeEvidenceItem


@dataclass
class SessionState:
    session_id: str
    cookies: Dict[str, str] = field(default_factory=dict)
    custom_headers: Dict[str, str] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)

    def add_cookie(self, name: str, value: str):
        self.cookies[name] = value

    def add_header(self, name: str, value: str):
        self.custom_headers[name] = value

    def log_note(self, note: str):
        self.notes.append(note)

    def get_cookie_header(self) -> Optional[str]:
        if not self.cookies:
            return None
        return "; ".join(f"{k}={v}" for k, v in self.cookies.items())


class WebValidator:
    """
    Executes scoped and authorized HTTP interactions against target applications.
    """

    def __init__(
        self,
        auth_record: AuthorizationRecord,
        evidence_collector: Optional[EvidenceCollector] = None,
        timeout_seconds: int = 5,
        max_requests: int = 100
    ):
        self.auth = auth_record
        self.evidence_collector = evidence_collector or EvidenceCollector()
        self.timeout = timeout_seconds
        self.max_requests = max_requests
        self.request_count = 0
        self.session = SessionState(session_id="session-default")
        self.validation_logs: List[Dict[str, Any]] = []

    def execute_probe(
        self,
        finding_id: str,
        cluster_id: str,
        method: str,
        target_url: str,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
        expected_status: Optional[int] = None,
        pre_approved: bool = False,
        route_context: Optional[str] = None,
    ) -> Tuple[int, Dict[str, str], str, SafetyDecision]:
        """
        Validates scope and safety before dispatching an HTTP probe.
        """
        # 1. Authorization check
        AuthorizationManager.check_authorized_or_raise(target_url, self.auth, method=method)

        # 2. Budget check
        if self.request_count >= self.max_requests:
            raise AuthorizationError(f"Request budget exceeded (max {self.max_requests} requests reached).")
        self.request_count += 1

        # 3. Safety Gate Evaluation
        parsed = urlparse(target_url)
        path = parsed.path or "/"
        action_id = f"ACT-{self.request_count:03d}"
        decision = SafetyGate.evaluate_action(action_id, method, path, context=route_context, pre_approved=pre_approved)

        if not decision.allowed_to_proceed:
            # Action blocked by safety gate
            self.session.log_note(f"Probe to {method} {target_url} blocked by Safety Gate ({decision.review_level}).")
            self.validation_logs.append({
                "action_id": action_id,
                "status": "BLOCKED",
                "review_level": decision.review_level,
                "rationale": decision.rationale,
                "url": target_url,
            })
            return 0, {}, "BLOCKED_BY_SAFETY_GATE", decision

        # 4. Prepare Headers (inject session cookies and custom headers)
        merged_headers = self._prepare_request_headers(headers)

        # 5. Dispatch HTTP Request
        status_code, resp_headers, resp_body = self._dispatch_http(
            method=method,
            target_url=target_url,
            headers=merged_headers,
            body=body
        )

        # 6. Record interaction in Evidence Collector
        exploit_status = "Runtime Confirmed" if (expected_status and status_code == expected_status) else "Runtime Likely"
        self.evidence_collector.record_interaction(
            finding_id=finding_id,
            cluster_id=cluster_id,
            method=method,
            url=target_url,
            path=path,
            status_code=status_code,
            req_headers=merged_headers,
            resp_headers=resp_headers,
            req_body=body,
            resp_body=resp_body,
            exploitability_status=exploit_status,
            route_context=route_context,
            reviewer_notes=f"HTTP {status_code} received from {path}"
        )

        self.validation_logs.append({
            "action_id": action_id,
            "status": "COMPLETED",
            "method": method.upper(),
            "url": target_url,
            "status_code": status_code,
            "review_level": decision.review_level
        })

        return status_code, resp_headers, resp_body, decision

    def _prepare_request_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Merges session headers, cookies, and transparent TorusGuard audit headers."""
        merged_headers = dict(self.session.custom_headers)
        if headers:
            merged_headers.update(headers)

        cookie_str = self.session.get_cookie_header()
        if cookie_str and "Cookie" not in merged_headers:
            merged_headers["Cookie"] = cookie_str

        merged_headers["User-Agent"] = "TorusGuard-RuntimeValidator/0.7.0 (Authorized Audit)"
        merged_headers["X-TorusGuard-AuthID"] = self.auth.authorization_id
        return merged_headers

    def _dispatch_http(
        self, method: str, target_url: str, headers: Dict[str, str], body: Optional[str] = None
    ) -> Tuple[int, Dict[str, str], str]:
        """Executes low-level HTTP interaction and parses response cookies/errors."""
        status_code = 0
        resp_headers: Dict[str, str] = {}
        resp_body = ""

        req_data = body.encode("utf-8") if body else None
        req = urllib.request.Request(target_url, data=req_data, headers=headers, method=method.upper())

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                status_code = resp.getcode()
                resp_headers = dict(resp.headers)
                resp_body = resp.read().decode("utf-8", errors="replace")

                if "Set-Cookie" in resp_headers:
                    self._parse_and_store_cookies(resp_headers["Set-Cookie"])

        except urllib.error.HTTPError as e:
            status_code = e.code
            resp_headers = dict(e.headers)
            resp_body = e.read().decode("utf-8", errors="replace")
        except urllib.error.URLError as e:
            status_code = 599
            resp_body = f"Network connection error: {e.reason}"
        except Exception as e:
            status_code = 599
            resp_body = f"Unexpected runtime error: {str(e)}"

        return status_code, resp_headers, resp_body

    def _parse_and_store_cookies(self, cookie_header: str):
        for part in cookie_header.split(","):
            cookie_pair = part.split(";")[0].strip()
            if "=" in cookie_pair:
                k, v = cookie_pair.split("=", 1)
                self.session.add_cookie(k.strip(), v.strip())

    def write_report_artifacts(self, run_dir: Path) -> Dict[str, Path]:
        """
        Emits web-validation.md, session-notes.md, and evidence logs.
        """
        run_dir.mkdir(parents=True, exist_ok=True)
        ev_artifacts = self.evidence_collector.write_artifacts(run_dir)

        # 1. web-validation.md
        wv_file = run_dir / "web-validation.md"
        lines = [
            "# TorusGuard v0.7.0 Web Validation Summary",
            f"\n**Authorization ID:** `{self.auth.authorization_id}`",
            f"**Target:** `{self.auth.target_name}`",
            f"**Total Requests Dispatched:** `{self.request_count}` / `{self.max_requests}`",
            "\n---",
            "\n## 🌐 Interaction Audit Log\n",
            "| Action ID | Method | Target URL | HTTP Status | Safety Review Level | Execution Status |",
            "|---|---|---|:---:|:---:|:---:|",
        ]
        for log in self.validation_logs:
            lines.append(
                f"| `{log.get('action_id')}` | `{log.get('method', 'N/A')}` | `{log.get('url')}` | `{log.get('status_code', '-')}` | `{log.get('review_level')}` | **{log.get('status')}** |"
            )

        with open(wv_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        # 2. session-notes.md
        session_file = run_dir / "session-notes.md"
        s_lines = [
            "# TorusGuard v0.7.0 Runtime Session Notes",
            f"\n**Session Identifier:** `{self.session.session_id}`",
            f"**Captured Cookies:** `{len(self.session.cookies)}` active cookies",
            f"**Custom Headers Set:** `{list(self.session.custom_headers.keys())}`",
            "\n### Session Event Timeline\n",
        ]
        if self.session.notes:
            for note in self.session.notes:
                s_lines.append(f"- {note}")
        else:
            s_lines.append("- No manual session interventions recorded.")

        with open(session_file, "w", encoding="utf-8") as f:
            f.write("\n".join(s_lines) + "\n")

        return {
            "web_validation": wv_file,
            "session_notes": session_file,
            **ev_artifacts
        }
