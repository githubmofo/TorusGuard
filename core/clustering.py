"""
TorusGuard v6 Root-Cause Clustering Engine
Groups individual static-analysis findings into cohesive root-cause clusters
so engineering teams can remediate systemic architectural issues rather than chasing isolated alerts.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import hashlib


# Canonical Cluster Taxonomy Definitions
KNOWN_ROOT_CAUSES = {
    "TG-DB-004": {
        "cluster_id": "cluster-tenant-isolation",
        "title": "Missing Multi-Tenant Query Scoping & Model Isolation",
        "shared_remediation_path": "Implement tenant-aware BaseManager / default queryset filtering or tenancy middleware context.",
        "shared_verification_plan": "Execute tenant cross-boundary query assertions and recheck query builders."
    },
    "TG-INPUT-006": {
        "cluster_id": "cluster-path-traversal",
        "title": "Unsafe File Upload Storage & Path Traversal Boundaries",
        "shared_remediation_path": "Sanitize filenames using secure_filename() and enforce safe directory resolution with Path.resolve().",
        "shared_verification_plan": "Run path traversal payload test suite and verify storage isolation."
    },
    "TG-INPUT-005": {
        "cluster_id": "cluster-template-escaping",
        "title": "Disabled Template Autoescaping & Unsafe HTML Rendering",
        "shared_remediation_path": "Remove explicit mark_safe() / |safe filters and use autoescaped context variables.",
        "shared_verification_plan": "Execute XSS payload injection test against rendered view outputs."
    },
    "TG-AUTH-008": {
        "cluster_id": "cluster-header-trust",
        "title": "Untrusted Client Header Trust & Role/Tenant Injection",
        "shared_remediation_path": "Derive user identity and role scopes exclusively from cryptographically signed session tokens or trusted gateways.",
        "shared_verification_plan": "Send spoofed client headers (X-User-Role, X-Tenant-ID) and assert rejection."
    },
    "TG-AUTH-007": {
        "cluster_id": "cluster-idor-scoping",
        "title": "Insecure Direct Object Reference (IDOR) on Primary Keys",
        "shared_remediation_path": "Scope database queries with user_id or account ownership filters before returning model instances.",
        "shared_verification_plan": "Run IDOR authorization matrix tests across test accounts."
    },
    "TG-RATE-001": {
        "cluster_id": "cluster-rate-limiting",
        "title": "Unbounded Resource Consumption & Missing Endpoint Throttling",
        "shared_remediation_path": "Apply Redis/in-memory rate limiting middleware or DRF Throttling classes.",
        "shared_verification_plan": "Execute burst traffic simulation and verify 429 Too Many Requests response."
    },
    "TG-SSRF-001": {
        "cluster_id": "cluster-ssrf-network",
        "title": "Unvalidated Outbound HTTP Requests & Network Boundary Leakage",
        "shared_remediation_path": "Validate destination URLs against strict allowlists and block internal IP ranges (127.0.0.1, 169.254.169.254).",
        "shared_verification_plan": "Attempt outbound requests to loopback and link-local metadata endpoints."
    },
    "TG-WEBHOOK-001": {
        "cluster_id": "cluster-webhook-auth",
        "title": "Unverified Inbound Webhook Signatures & Replay Vulnerability",
        "shared_remediation_path": "Verify HMAC signatures using timing-safe comparisons and enforce timestamp freshness bounds.",
        "shared_verification_plan": "Send unsigned and replay webhook payloads and confirm 401/403 rejection."
    },
    "TG-SEC-001": {
        "cluster_id": "cluster-secrets",
        "title": "Hardcoded Secrets & Sensitive Environment Configuration Exposure",
        "shared_remediation_path": "Extract secrets into environment variables (.env / secrets manager) and exclude from version control.",
        "shared_verification_plan": "Audit git history and scan source files for credential patterns."
    }
}


@dataclass
class RootCauseCluster:
    cluster_id: str
    title: str
    primary_rule: str
    affected_files: List[str] = field(default_factory=list)
    affected_locations: List[str] = field(default_factory=list)
    finding_ids: List[str] = field(default_factory=list)
    shared_remediation_path: str = ""
    shared_verification_plan: str = ""
    risk_severity: str = "High"

    def add_finding(self, finding_id: str, file_path: str, location_str: str, severity: str = "High"):
        if finding_id not in self.finding_ids:
            self.finding_ids.append(finding_id)
        if file_path not in self.affected_files:
            self.affected_files.append(file_path)
        if location_str not in self.affected_locations:
            self.affected_locations.append(location_str)
        # Escalate cluster severity if higher
        severity_order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1, "Informational": 0}
        if severity_order.get(severity, 0) > severity_order.get(self.risk_severity, 0):
            self.risk_severity = severity

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ClusteringEngine:
    """
    Analyzes findings and groups them into root-cause clusters.
    """

    @staticmethod
    def cluster_findings(findings: List[Dict[str, Any]]) -> List[RootCauseCluster]:
        clusters: Dict[str, RootCauseCluster] = {}

        for f in findings:
            rule_id = f.get("rule_id", "TG-GENERIC")
            finding_id = f.get("finding_id", "unknown")
            target = f.get("target", {})
            file_path = target.get("file_path", "unknown")
            start_line = target.get("line_start", 0)
            end_line = target.get("line_end", 0)
            loc_str = f"{file_path}:{start_line}-{end_line}"
            severity = f.get("severity", "High")

            # Determine cluster mapping
            if rule_id in KNOWN_ROOT_CAUSES:
                meta = KNOWN_ROOT_CAUSES[rule_id]
                cid = meta["cluster_id"]
                title = meta["title"]
                rem_path = meta["shared_remediation_path"]
                ver_plan = meta["shared_verification_plan"]
            else:
                # Generic cluster fallback by category/rule prefix
                category = f.get("category", "general")
                cid = f"cluster-{rule_id.lower().replace('tg-', '')}"
                title = f"Systemic {f.get('title', rule_id)} Issues"
                rem_path = "Apply framework-native security controls as documented in rule reference."
                ver_plan = "Re-audit all affected components with /torusguard recheck."

            if cid not in clusters:
                clusters[cid] = RootCauseCluster(
                    cluster_id=cid,
                    title=title,
                    primary_rule=rule_id,
                    shared_remediation_path=rem_path,
                    shared_verification_plan=ver_plan,
                    risk_severity=severity,
                )

            clusters[cid].add_finding(
                finding_id=finding_id,
                file_path=file_path,
                location_str=loc_str,
                severity=severity,
            )

        return list(clusters.values())
