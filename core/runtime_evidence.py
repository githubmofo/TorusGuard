"""
TorusGuard v0.7.0 Runtime Evidence Model & Secret Redaction Engine
Captures reproducible HTTP & browser validation evidence while automatically
redacting credentials, JWTs, API keys, and sensitive payload parameters.
"""

import re
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


class RedactionEngine:
    """
    Sanitizes authorization headers, cookies, tokens, and secret parameters.
    """

    PATTERNS = [
        (re.compile(r"Bearer\s+([A-Za-z0-9_\-\.]+)", re.IGNORECASE), "Bearer [REDACTED_TOKEN]"),
        (re.compile(r"Basic\s+([A-Za-z0-9+/=]+)", re.IGNORECASE), "Basic [REDACTED_CREDS]"),
        (re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+"), "[REDACTED_JWT]"),
        (re.compile(r"sk_live_[0-9a-zA-Z]{24,}"), "sk_live_[REDACTED_KEY]"),
        (re.compile(r"AKIA[0-9A-Z]{16}"), "AKIA[REDACTED_AWS_KEY]"),
        (re.compile(r"([\"']?password[\"']?\s*[:=]\s*[\"'])([^\"']+)([\"'])", re.IGNORECASE), r"\1[REDACTED_PASSWORD]\3"),
        (re.compile(r"([\"']?secret[\"']?\s*[:=]\s*[\"'])([^\"']+)([\"'])", re.IGNORECASE), r"\1[REDACTED_SECRET]\3"),
    ]

    @classmethod
    def redact_text(cls, text: Optional[str]) -> str:
        if not text:
            return ""
        redacted = text
        for pattern, repl in cls.PATTERNS:
            redacted = pattern.sub(repl, redacted)
        return redacted

    @classmethod
    def redact_headers(cls, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        if not headers:
            return {}
        sanitized = {}
        sensitive_headers = {"authorization", "cookie", "set-cookie", "x-api-key", "proxy-authorization"}
        for k, v in headers.items():
            if k.lower() in sensitive_headers:
                sanitized[k] = cls.redact_text(str(v))
            else:
                sanitized[k] = str(v)
        return sanitized


@dataclass
class RuntimeEvidenceItem:
    evidence_id: str
    finding_id: str
    cluster_id: str
    timestamp: str
    method: str
    url: str
    path: str
    status_code: int
    request_headers: Dict[str, str]
    response_headers: Dict[str, str]
    request_body_redacted: Optional[str]
    response_body_snippet: str
    exploitability_status: str
    reproducible: bool = True
    route_context: Optional[str] = None
    reviewer_notes: Optional[str] = None
    screenshot_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EvidenceCollector:
    """
    Collects runtime HTTP request/response evidence and writes sanitized artifacts.
    """

    def __init__(self):
        self.evidence_items: List[RuntimeEvidenceItem] = []
        self.requests_log: List[Dict[str, Any]] = []
        self.responses_log: List[Dict[str, Any]] = []

    def record_interaction(
        self,
        finding_id: str,
        cluster_id: str,
        method: str,
        url: str,
        path: str,
        status_code: int,
        req_headers: Dict[str, str],
        resp_headers: Dict[str, str],
        req_body: Optional[str],
        resp_body: Optional[str],
        exploitability_status: str,
        route_context: Optional[str] = None,
        reviewer_notes: Optional[str] = None,
        screenshot_path: Optional[str] = None,
    ) -> RuntimeEvidenceItem:
        now = datetime.now(timezone.utc).isoformat()
        ev_id = f"EV-RT-{len(self.evidence_items) + 1:04d}"

        sanitized_req_headers = RedactionEngine.redact_headers(req_headers)
        sanitized_resp_headers = RedactionEngine.redact_headers(resp_headers)
        sanitized_req_body = RedactionEngine.redact_text(req_body) if req_body else None
        snippet = RedactionEngine.redact_text((resp_body or "")[:500])

        item = RuntimeEvidenceItem(
            evidence_id=ev_id,
            finding_id=finding_id,
            cluster_id=cluster_id,
            timestamp=now,
            method=method.upper(),
            url=url,
            path=path,
            status_code=status_code,
            request_headers=sanitized_req_headers,
            response_headers=sanitized_resp_headers,
            request_body_redacted=sanitized_req_body,
            response_body_snippet=snippet,
            exploitability_status=exploitability_status,
            reproducible=True,
            route_context=route_context,
            reviewer_notes=reviewer_notes,
            screenshot_path=screenshot_path,
        )

        self.evidence_items.append(item)

        # Append to logs
        self.requests_log.append({
            "evidence_id": ev_id,
            "timestamp": now,
            "method": method.upper(),
            "url": url,
            "headers": sanitized_req_headers,
            "body": sanitized_req_body,
        })
        self.responses_log.append({
            "evidence_id": ev_id,
            "timestamp": now,
            "status_code": status_code,
            "headers": sanitized_resp_headers,
            "body_snippet": snippet,
        })

        return item

    def write_artifacts(self, run_dir: Path) -> Dict[str, Path]:
        """
        Emits requests.json, responses.json, and runtime-evidence.json.
        """
        run_dir.mkdir(parents=True, exist_ok=True)
        req_file = run_dir / "requests.json"
        resp_file = run_dir / "responses.json"
        ev_file = run_dir / "runtime-evidence.json"

        with open(req_file, "w", encoding="utf-8") as f:
            json.dump(self.requests_log, f, indent=2)

        with open(resp_file, "w", encoding="utf-8") as f:
            json.dump(self.responses_log, f, indent=2)

        with open(ev_file, "w", encoding="utf-8") as f:
            json.dump([item.to_dict() for item in self.evidence_items], f, indent=2)

        return {
            "requests": req_file,
            "responses": resp_file,
            "evidence": ev_file,
        }
