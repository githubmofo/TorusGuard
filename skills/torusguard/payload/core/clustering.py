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
    },
    "TG-AGENT-001": {
        "cluster_id": "cluster-prompt-injection",
        "title": "AI Agent User Prompt Concatenation & System Prompt Override",
        "shared_remediation_path": "Isolate untrusted user input within explicit inert XML delimiters or structured user-role message arrays.",
        "shared_verification_plan": "Execute prompt injection canary payloads and verify refusal to override system directives."
    },
    "TG-CSRF-001": {
        "cluster_id": "cluster-csrf-missing",
        "title": "Cross-Site Request Forgery (CSRF) & Missing SameSite Cookie Protection",
        "shared_remediation_path": "Enforce SameSite=Lax/Strict on session cookies and validate cryptographic anti-CSRF tokens on state mutations.",
        "shared_verification_plan": "Attempt cross-origin state-changing POST requests without CSRF token."
    },
    "TG-GQL-001": {
        "cluster_id": "cluster-graphql-abuse",
        "title": "Unbounded GraphQL Query Depth & Production Introspection Exposure",
        "shared_remediation_path": "Configure GraphQL query depth limiting (max depth 6) and disable schema introspection in production.",
        "shared_verification_plan": "Send deeply nested recursive query and introspection requests to production endpoint."
    },
    "TG-SUPPLY-001": {
        "cluster_id": "cluster-supply-chain",
        "title": "Supply Chain Vulnerability & Unpinned CI/CD Action Hashes",
        "shared_remediation_path": "Pin GitHub Actions to full immutable commit SHAs and enforce lockfile integrity verification in CI.",
        "shared_verification_plan": "Scan workflow files for mutable tag references and verify lockfile checksums."
    },
    "TG-BIZ-001": {
        "cluster_id": "cluster-business-logic",
        "title": "Business Logic Invariant Violation & Negative Quantity/Discount Bypass",
        "shared_remediation_path": "Assert non-negative amount invariants, enforce transactional locks, and cap discounts server-side.",
        "shared_verification_plan": "Submit negative amount and coupon boundary payloads in transactional API endpoints."
    },
    "TG-CACHE-001": {
        "cluster_id": "cluster-cache-poisoning",
        "title": "Web Cache Poisoning & Missing Cache-Control on Sensitive Responses",
        "shared_remediation_path": "Sanitize unkeyed HTTP request headers and apply 'Cache-Control: no-store' on private or authenticated responses.",
        "shared_verification_plan": "Send unkeyed headers (X-Forwarded-Host) and inspect cached responses."
    },
    "TG-WS-001": {
        "cluster_id": "cluster-websocket-auth",
        "title": "Missing WebSocket Handshake Authentication & Origin Verification",
        "shared_remediation_path": "Authenticate client credentials during WebSocket upgrade and reject connections with unwhitelisted Origin headers.",
        "shared_verification_plan": "Connect from untrusted origin and assert handshake rejection with 403 Forbidden."
    },
    "TG-EDGE-001": {
        "cluster_id": "cluster-edge-abuse",
        "title": "Serverless Subrequest Fan-Out Explosion & Missing Timeout Bounds",
        "shared_remediation_path": "Enforce concurrency caps on edge subrequests and configure strict execution timeouts (<= 15s).",
        "shared_verification_plan": "Simulate high subrequest fan-out and assert bounded concurrency."
    },
    "TG-CONT-001": {
        "cluster_id": "cluster-container-hardening",
        "title": "Container Security Misconfiguration & Root User Execution",
        "shared_remediation_path": "Define non-root USER in Dockerfile, avoid mounting /var/run/docker.sock, and disallow privileged mode.",
        "shared_verification_plan": "Inspect container image metadata and assert non-root UID."
    },
    "TG-GIT-001": {
        "cluster_id": "cluster-git-secret-mining",
        "title": "Committed Credentials & Leaked Tokens in Git Commit History",
        "shared_remediation_path": "Rotate exposed keys immediately, purge secret commits using git-filter-repo, and install pre-commit secret hooks.",
        "shared_verification_plan": "Mine git commit logs for high-entropy tokens and regex matches."
    },
    "TG-REDOS-001": {
        "cluster_id": "cluster-regex-backtracking",
        "title": "Regular Expression Denial of Service (ReDoS) via Nested Quantifiers",
        "shared_remediation_path": "Refactor regex patterns to eliminate nested quantifiers (e.g. (a+)+) or enforce execution timeouts.",
        "shared_verification_plan": "Execute polynomial/exponential adversarial string payloads against regex engine."
    },
    "TG-RAG-001": {
        "cluster_id": "cluster-rag-tenant-leak",
        "title": "RAG Pipeline Vector Database Multi-Tenant Isolation Leakage",
        "shared_remediation_path": "Always include tenant_id or user_id in vector similarity filter metadata (e.g. filter={'tenant_id': tid}).",
        "shared_verification_plan": "Query vector database with tenant A context requesting tenant B documents."
    },
    "TG-INPUT-007": {
        "cluster_id": "cluster-open-redirect",
        "title": "Unvalidated URL Redirection (Open Redirect)",
        "shared_remediation_path": "Validate destination URLs against an allowlist of trusted domains and restrict to relative paths.",
        "shared_verification_plan": "Test redirect endpoints with external and protocol-relative URLs."
    },
    "TG-INPUT-008": {
        "cluster_id": "cluster-deserialization",
        "title": "Insecure Object Deserialization via Untrusted Streams",
        "shared_remediation_path": "Avoid pickle/yaml.load with untrusted input; use safe serialization formats (JSON) or SafeLoader.",
        "shared_verification_plan": "Submit serialized gadget payload and confirm safe parser rejection."
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
    hotspot_module: str = ""
    is_high_density: bool = False

    def add_finding(self, finding_id: str, file_path: str, location_str: str, severity: str = "High"):
        if finding_id not in self.finding_ids:
            self.finding_ids.append(finding_id)
        if file_path not in self.affected_files:
            self.affected_files.append(file_path)
        if location_str not in self.affected_locations:
            self.affected_locations.append(location_str)

        # Update hotspot module (top directory)
        parts = file_path.replace("\\", "/").split("/")
        if len(parts) > 1:
            self.hotspot_module = "/".join(parts[:2])
        else:
            self.hotspot_module = parts[0]

        # Density threshold (> 5 findings in one cluster is high density)
        if len(self.finding_ids) >= 5:
            self.is_high_density = True

        # Escalate cluster severity if higher
        severity_order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1, "Informational": 0}
        if severity_order.get(severity, 0) > severity_order.get(self.risk_severity, 0):
            self.risk_severity = severity

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Generated / Vendor File Exclusion Patterns
IGNORED_PATTERNS = [
    "migrations/", "node_modules/", "dist/", "build/", "vendor/",
    ".venv/", "venv/", ".min.js", ".min.css", ".pb.go", "_pb2.py",
    "bundle.js", ".map"
]


def is_generated_file(file_path: str) -> bool:
    norm = file_path.replace("\\", "/").lower()
    return any(p in norm for p in IGNORED_PATTERNS)


class ClusteringEngine:
    """
    Analyzes findings and groups them into root-cause clusters with scale and density metrics.
    """

    @staticmethod
    def cluster_findings(
        findings: List[Dict[str, Any]],
        filter_generated: bool = False
    ) -> List[RootCauseCluster]:
        clusters: Dict[str, RootCauseCluster] = {}

        for f in findings:
            target = f.get("target", {})
            file_path = target.get("file_path", "unknown")

            if filter_generated and is_generated_file(file_path):
                continue

            rule_id = f.get("rule_id", "TG-GENERIC")
            finding_id = f.get("finding_id", "unknown")
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

        # Sort clusters by severity and finding count
        severity_order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1, "Informational": 0}
        sorted_clusters = sorted(
            clusters.values(),
            key=lambda c: (severity_order.get(c.risk_severity, 0), len(c.finding_ids)),
            reverse=True
        )

        return sorted_clusters
