#!/usr/bin/env python3
"""
TorusGuard Visual HTML Report Emitter (v2.3.0)
Compiles a self-contained, zero-external-CDN, interactive dashboard
focused on ACTUAL SECURITY POSTURE & GOVERNED REMEDIATION:
  1. Safe Defenses vs. Harmed Exposure (5-Layer Architectural Invariant Matrix)
  2. Severity Breakdown (Dynamic Circular SVG Gauge with Glow & Count-Up, KPI Cards)
  3. Interactive Findings Drawers (Vulnerable Snippets, Invariant Rules, Fix Commands)
  4. Interactive "What-If" Posture Score Simulator (Live Dynamic Gauge Recalculation)
  5. Interactive Directory Attack Surface Heatmap (Click-to-Filter)
  6. OWASP Top 10 (2021/2026) Compliance Radar
  7. Enterprise Compliance Framework Mapping (SOC 2 Type II, ISO/IEC 27001:2022, HIPAA)
  8. Root-Cause Architectural Clusters & Blast Radius
  9. Golden Recipe Explorer (Distilled Verified Fixes, Diffs & Before/After Views)
 10. Prescriptive "Next Best Defenses" Advisory (Stack-Aware Gaps)
 11. In-Browser Artifact Exporters (Zero-Network SARIF v2.1.0 & CSV Downloaders)
 12. Zero-CDN Executive Dark / Light Mode Switcher with LocalStorage Persistence
 13. High-Contrast Print & PDF Export Styling (@media print)

Pure Python 3.10+ standard library (100% zero external dependencies, zero CDNs).
"""

import sys
import json
import html
import datetime
import argparse
from pathlib import Path
from typing import Any, TypedDict


class ComplianceControl(TypedDict):
    code: str
    families: str
    rules: list[str]


class ComplianceFramework(TypedDict):
    name: str
    subtitle: str
    controls: list[ComplianceControl]


# Windows console UTF-8 support
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        getattr(sys.stderr, "reconfigure")(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass


FAMILY_METADATA: dict[str, dict[str, str]] = {
    "TG-AGENT": {
        "layer_id": "layer-app",
        "layer_name": "Application & LLM Defense",
        "domain": "AI Agent & LLM Injection Defense",
        "guarantee": "Structural user prompt isolation, inert delimiters, and tool call schema validation. Prevents direct and indirect prompt injection attacks.",
        "owasp": "OWASP LLM01: Prompt Injection",
        "compliance": "ISO 27001 A.8.28 (Secure Coding)"
    },
    "TG-INPUT": {
        "layer_id": "layer-app",
        "layer_name": "Application & LLM Defense",
        "domain": "Input Sanitization & Traversal",
        "guarantee": "Strict path normalization, command argument escaping, and safe DOM assignment. Prevents path traversal, OS command injection, and Reflected/DOM XSS.",
        "owasp": "OWASP A03:2021 - Injection",
        "compliance": "SOC 2 CC6.6 / ISO 27001 A.8.28"
    },
    "TG-AUTH": {
        "layer_id": "layer-auth",
        "layer_name": "Identity, Auth & Real-Time",
        "domain": "Authentication & Session Integrity",
        "guarantee": "Timing-safe secret compares, strong argon2id/bcrypt password hashing, explicit JWT algorithm pinning, and secure cookie session attributes.",
        "owasp": "OWASP A07:2021 - Identification & Authentication Failures",
        "compliance": "SOC 2 CC6.1 / ISO 27001 A.8.24 / HIPAA § 164.312(a)(1)"
    },
    "TG-CSRF": {
        "layer_id": "layer-auth",
        "layer_name": "Identity, Auth & Real-Time",
        "domain": "Cross-Site Request Forgery",
        "guarantee": "Cryptographic anti-CSRF token verification on state-changing requests and SameSite=Lax/Strict cookie isolation.",
        "owasp": "OWASP A01:2021 - Broken Access Control",
        "compliance": "SOC 2 CC6.1 / ISO 27001 A.8.28"
    },
    "TG-WS": {
        "layer_id": "layer-auth",
        "layer_name": "Identity, Auth & Real-Time",
        "domain": "WebSocket & Real-Time Security",
        "guarantee": "Handshake origin validation, connection ticket verification, and inbound frame size bounds to eliminate CSWSH and socket exhaustion.",
        "owasp": "OWASP A01:2021 - Broken Access Control / A05: Misconfiguration",
        "compliance": "SOC 2 CC6.6 / ISO 27001 A.8.20"
    },
    "TG-BIZ": {
        "layer_id": "layer-auth",
        "layer_name": "Identity, Auth & Real-Time",
        "domain": "Business Logic & Workflow Limits",
        "guarantee": "Strict positive financial amount constraints, atomic database transaction locks, and coupon stacking bounds to prevent race conditions.",
        "owasp": "OWASP A04:2021 - Insecure Design",
        "compliance": "HIPAA § 164.312(c)(1) Data Integrity / SOC 2 CC7.1"
    },
    "TG-DB": {
        "layer_id": "layer-db",
        "layer_name": "Database, GraphQL & Cache",
        "domain": "Database Isolation & Injection",
        "guarantee": "Zero unparameterized SQL concatenation. Enforces prepared statements with bound parameters and mandatory tenant partition scoping.",
        "owasp": "OWASP A03:2021 - Injection / A01: Broken Access Control",
        "compliance": "SOC 2 CC6.1 / ISO 27001 A.8.28 / HIPAA § 164.312(a)(1)"
    },
    "TG-GQL": {
        "layer_id": "layer-db",
        "layer_name": "Database, GraphQL & Cache",
        "domain": "GraphQL Safety & Introspection",
        "guarantee": "Query depth limiting (max depth <= 7), circular reference blocking, field complexity cost analysis, and production schema introspection suppression.",
        "owasp": "OWASP A05:2021 - Security Misconfiguration",
        "compliance": "SOC 2 CC6.6 / ISO 27001 A.8.28"
    },
    "TG-CACHE": {
        "layer_id": "layer-db",
        "layer_name": "Database, GraphQL & Cache",
        "domain": "Cache Poisoning & Cache Timing",
        "guarantee": "Mandatory Cache-Control: no-store on authenticated sensitive responses and unkeyed HTTP header sanitization to prevent web cache poisoning.",
        "owasp": "OWASP A05:2021 - Security Misconfiguration",
        "compliance": "SOC 2 CC6.7 / ISO 27001 A.8.20"
    },
    "TG-SSRF": {
        "layer_id": "layer-net",
        "layer_name": "Network, SSRF & Webhooks",
        "domain": "Server-Side Request Forgery",
        "guarantee": "Outbound URL hostname whitelisting, RFC1918 private IP range blocking (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.1) and cloud metadata blocking (169.254.169.254).",
        "owasp": "OWASP A10:2021 - Server-Side Request Forgery (SSRF)",
        "compliance": "SOC 2 CC6.6 / ISO 27001 A.8.20"
    },
    "TG-WEBHOOK": {
        "layer_id": "layer-net",
        "layer_name": "Network, SSRF & Webhooks",
        "domain": "Inbound Webhook Verification",
        "guarantee": "Mandatory cryptographic HMAC-SHA256 signature verification over raw request buffers and replay attack protection with <= 300s timestamp limits.",
        "owasp": "OWASP A08:2021 - Software and Data Integrity Failures",
        "compliance": "SOC 2 CC6.6 / ISO 27001 A.8.20 / HIPAA § 164.312(c)(1)"
    },
    "TG-RATE": {
        "layer_id": "layer-net",
        "layer_name": "Network, SSRF & Webhooks",
        "domain": "Rate Limiting & Resource Protection",
        "guarantee": "Sliding-window IP rate limiting on auth and write endpoints, bounded JSON payload parsers (<= 1MB), and slowloris connection timeouts.",
        "owasp": "OWASP A04:2021 - Insecure Design / A07: Auth Failures",
        "compliance": "SOC 2 CC6.6 / ISO 27001 A.8.20"
    },
    "TG-PLATFORM": {
        "layer_id": "layer-platform",
        "layer_name": "Platform, Supply Chain & Secrets",
        "domain": "Server Hardening & Security Headers",
        "guarantee": "Mandatory production security headers (CSP, HSTS max-age>=31536000, X-Content-Type-Options: nosniff, X-Frame-Options: DENY) and debug mode suppression.",
        "owasp": "OWASP A05:2021 - Security Misconfiguration",
        "compliance": "SOC 2 CC6.7 / ISO 27001 A.8.20 / HIPAA § 164.312(e)(1)"
    },
    "TG-SUPPLY": {
        "layer_id": "layer-platform",
        "layer_name": "Platform, Supply Chain & Secrets",
        "domain": "Supply Chain & Dependency Health",
        "guarantee": "Lockfile cryptographic integrity checks, known high/critical CVE build gates, verified registry origins, and build script execution bounds.",
        "owasp": "OWASP A06:2021 - Vulnerable and Outdated Components",
        "compliance": "SOC 2 CC7.1 / ISO 27001 A.8.28"
    },
    "TG-CLIENT": {
        "layer_id": "layer-platform",
        "layer_name": "Platform, Supply Chain & Secrets",
        "domain": "Client Bundle & Frontend Secrets",
        "guarantee": "Zero server role keys, database master credentials, or private API secrets leaked into frontend bundles or public environment variables.",
        "owasp": "OWASP A01:2021 - Broken Access Control / A05: Misconfiguration",
        "compliance": "SOC 2 CC6.1 / ISO 27001 A.8.24 / HIPAA § 164.312(e)(1)"
    },
    "TG-EDGE": {
        "layer_id": "layer-platform",
        "layer_name": "Platform, Supply Chain & Secrets",
        "domain": "Edge Computing & Serverless Limits",
        "guarantee": "Subrequest fan-out limits (<= 50 per invocation), serverless wall-clock execution timeouts (<= 30s), and memory bounds for edge functions.",
        "owasp": "OWASP A04:2021 - Insecure Design",
        "compliance": "SOC 2 CC6.6 / ISO 27001 A.8.20"
    },
    "TG-DIFF": {
        "layer_id": "layer-platform",
        "layer_name": "Platform, Supply Chain & Secrets",
        "domain": "Polyglot Bypass & Churn Bounds",
        "guarantee": "Strict Ponytail Protocol enforcement (<= 35 additions, <= 25 deletions per patch) and zero security suppression pragmas (nosec pragmas, InsecureSkipVerify).",
        "owasp": "OWASP A08:2021 - Software Integrity",
        "compliance": "SOC 2 CC7.1 / ISO 27001 A.8.28 / HIPAA § 164.312(c)(1)"
    },
    "TG-SEC": {
        "layer_id": "layer-platform",
        "layer_name": "Platform, Supply Chain & Secrets",
        "domain": "Core Secrets & API Tokens",
        "guarantee": "Zero hardcoded API keys, private certificates, AWS/GCP/Stripe tokens, or JWT secrets in tracked source code. Mandatory externalized environment configuration.",
        "owasp": "OWASP A02:2021 - Cryptographic Failures",
        "compliance": "SOC 2 CC6.7 / ISO 27001 A.8.24 / HIPAA § 164.312(e)(1)"
    }
}

ARCHITECTURAL_LAYERS: list[dict[str, Any]] = [
    {
        "id": "layer-app",
        "name": "Application & LLM Defense",
        "icon": "🛡️",
        "families": ["TG-AGENT", "TG-INPUT"],
        "description": "User prompt isolation, inert delimiters, traversal defense, and input escaping."
    },
    {
        "id": "layer-auth",
        "name": "Identity, Auth & Real-Time",
        "icon": "🔑",
        "families": ["TG-AUTH", "TG-CSRF", "TG-WS", "TG-BIZ"],
        "description": "Constant-time comparisons, password hashing, algorithm pinning, SameSite cookies, and business flow bounds."
    },
    {
        "id": "layer-db",
        "name": "Database, GraphQL & Cache",
        "icon": "💾",
        "families": ["TG-DB", "TG-GQL", "TG-CACHE"],
        "description": "Parameterized SQL queries, multi-tenant row partitioning, GraphQL query depth limits, and cache timing guards."
    },
    {
        "id": "layer-net",
        "name": "Network, SSRF & Webhooks",
        "icon": "🌐",
        "families": ["TG-SSRF", "TG-WEBHOOK", "TG-RATE"],
        "description": "Private IP / metadata blocking, cryptographic HMAC webhook authentication, and sliding-window rate limiters."
    },
    {
        "id": "layer-platform",
        "name": "Platform, Supply Chain & Secrets",
        "icon": "🏗️",
        "families": ["TG-PLATFORM", "TG-SUPPLY", "TG-CLIENT", "TG-EDGE", "TG-DIFF", "TG-SEC"],
        "description": "Security headers, dependency lockfile integrity, zero client bundle secrets, serverless limits, and Ponytail bounds."
    }
]


def find_project_root(start_dir: str | Path | None = None) -> Path:
    """Detect project root directory."""
    current = Path(start_dir or Path.cwd()).resolve()
    markers = [".git", "package.json", "pyproject.toml", ".torusguard"]
    for m in markers:
        if (current / m).exists():
            return current
    for parent in current.parents:
        for m in markers:
            if (parent / m).exists():
                return parent
    return current


def load_all_rule_catalog() -> list[dict[str, Any]]:
    """Load complete 74-rule catalog from audit_runner."""
    try:
        scripts_dir = Path(__file__).resolve().parent
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        import audit_runner  # type: ignore
        catalog = []
        for r in getattr(audit_runner, "RULE_PATTERNS", []):
            rid = r.get("rule_id", "TG-GEN")
            fam = rid.rsplit("-", 1)[0]
            meta = FAMILY_METADATA.get(fam, {})
            catalog.append({
                "rule_id": rid,
                "title": r.get("title", "Security Invariant"),
                "severity": r.get("severity", "Medium"),
                "category": r.get("category", "general"),
                "cluster": r.get("cluster", "cluster-general"),
                "layer_id": meta.get("layer_id", "layer-platform"),
                "layer_name": meta.get("layer_name", "Platform & Security"),
                "guarantee": meta.get("guarantee", "Enforces security guardrails without bypasses."),
                "owasp": meta.get("owasp", "OWASP Security Standard"),
                "compliance": meta.get("compliance", "Enterprise Security Baseline")
            })
        if catalog:
            return catalog
    except Exception:
        pass

    # Fallback built-in catalog if audit_runner cannot be loaded
    return [
        {"rule_id": "TG-SEC-001", "title": "Hardcoded Secret or API Key", "severity": "Critical", "category": "secrets", "layer_id": "layer-platform", "layer_name": "Platform, Supply Chain & Secrets", "guarantee": "Zero hardcoded secrets in source.", "owasp": "OWASP A02:2021", "compliance": "SOC 2 CC6.7"},
        {"rule_id": "TG-SEC-002", "title": "Public Client Environment Secret", "severity": "Critical", "category": "secrets", "layer_id": "layer-platform", "layer_name": "Platform, Supply Chain & Secrets", "guarantee": "Zero private keys in frontend bundles.", "owasp": "OWASP A01:2021", "compliance": "SOC 2 CC6.1"},
        {"rule_id": "TG-AUTH-001", "title": "Weak Password Storage", "severity": "Critical", "category": "auth", "layer_id": "layer-auth", "layer_name": "Identity, Auth & Real-Time", "guarantee": "Enforces strong password hashing.", "owasp": "OWASP A07:2021", "compliance": "SOC 2 CC6.1"},
        {"rule_id": "TG-DB-001", "title": "Raw SQL Concatenation", "severity": "Critical", "category": "database", "layer_id": "layer-db", "layer_name": "Database, GraphQL & Cache", "guarantee": "Enforces parameterized queries.", "owasp": "OWASP A03:2021", "compliance": "SOC 2 CC6.1"},
        {"rule_id": "TG-INPUT-001", "title": "Missing Server Input Validation", "severity": "High", "category": "input", "layer_id": "layer-app", "layer_name": "Application & LLM Defense", "guarantee": "Enforces boundary schema validation.", "owasp": "OWASP A03:2021", "compliance": "ISO 27001 A.8.28"},
        {"rule_id": "TG-RATE-001", "title": "Unlimited Auth Endpoint", "severity": "High", "category": "rate", "layer_id": "layer-net", "layer_name": "Network, SSRF & Webhooks", "guarantee": "Enforces auth rate limiting.", "owasp": "OWASP A04:2021", "compliance": "SOC 2 CC6.6"},
        {"rule_id": "TG-SSRF-001", "title": "Unvalidated Outbound HTTP Request", "severity": "High", "category": "ssrf", "layer_id": "layer-net", "layer_name": "Network, SSRF & Webhooks", "guarantee": "Blocks private VPC and metadata IPs.", "owasp": "OWASP A10:2021", "compliance": "SOC 2 CC6.6"},
        {"rule_id": "TG-PLATFORM-001", "title": "Missing Security Headers", "severity": "Medium", "category": "platform", "layer_id": "layer-platform", "layer_name": "Platform, Supply Chain & Secrets", "guarantee": "Enforces HTTP hardening headers.", "owasp": "OWASP A05:2021", "compliance": "SOC 2 CC6.7"}
    ]


def load_report_telemetry(root_dir: Path) -> dict[str, Any]:
    """Gather all project telemetry, findings, rules catalog, and memory state."""
    tg_dir = root_dir / ".torusguard"
    memory_dir = tg_dir / "memory"
    config_file = tg_dir / "config" / "torusguard.json"

    cfg: dict[str, Any] = {}
    if config_file.exists():
        try:
            cfg = json.loads(config_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            cfg = {}

    profile_file = memory_dir / "profile.json"
    patterns_file = memory_dir / "patterns.json"
    context_file = memory_dir / "context.json"

    profile: dict[str, Any] = {}
    patterns: list[dict[str, Any]] = []
    context: dict[str, Any] = {}

    if profile_file.exists():
        try:
            profile = json.loads(profile_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            profile = {}

    if patterns_file.exists():
        try:
            patterns = json.loads(patterns_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            patterns = []

    if context_file.exists():
        try:
            context = json.loads(context_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            context = {}

    stack_info = cfg.get("detected_stack", {})
    if not stack_info:
        try:
            import stack_detect  # type: ignore
            stack_info = stack_detect.detect_stack(root_dir)
        except Exception:
            stack_info = {"language": "Universal", "framework": "None", "data_layer": "None"}

    # Load actual findings from latest audit run
    runs_dir = tg_dir / "runs"
    latest_findings: list[dict[str, Any]] = []
    latest_run_name = "none"
    if runs_dir.is_dir():
        run_folders = sorted(
            [d for d in runs_dir.iterdir() if d.is_dir() and (d / "findings.json").is_file()],
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        if run_folders:
            findings_file = run_folders[0] / "findings.json"
            latest_run_name = run_folders[0].name
            try:
                latest_findings = json.loads(findings_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                latest_findings = []

    # Rule catalog & Safe vs. Harmed computation
    all_rules = load_all_rule_catalog()
    violated_ids = {f.get("rule_id") for f in latest_findings if not f.get("is_canary", False)}
    safe_rules = [r for r in all_rules if r["rule_id"] not in violated_ids]
    violated_rules = [r for r in all_rules if r["rule_id"] in violated_ids]

    ist_tz = datetime.timezone(datetime.timedelta(hours=5, minutes=30), name="IST")
    now_ist = datetime.datetime.now(ist_tz)
    return {
        "project_name": root_dir.name or "Project",
        "root_dir": str(root_dir),
        "generated_at": now_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
        "config": cfg,
        "profile": profile,
        "patterns": patterns,
        "context": context,
        "detected_stack": stack_info,
        "findings": latest_findings,
        "latest_run": latest_run_name,
        "all_rules": all_rules,
        "safe_rules": safe_rules,
        "violated_rules": violated_rules,
    }


def compute_posture_score(telemetry: dict[str, Any]) -> int:
    """Calculate posture score from actual findings, aligned with report_sync.py."""
    findings = telemetry.get("findings", [])
    if not findings:
        return 100

    # Only non-canary findings count toward production penalty
    critical = sum(1 for f in findings if f.get("severity") == "Critical" and not f.get("is_canary", False))
    high = sum(1 for f in findings if f.get("severity") == "High" and not f.get("is_canary", False))
    medium = sum(1 for f in findings if f.get("severity") == "Medium" and not f.get("is_canary", False))
    low = sum(1 for f in findings if f.get("severity") == "Low" and not f.get("is_canary", False))

    penalty = (critical * 25) + (high * 15) + (medium * 5) + (low * 2)
    return max(0, min(100, 100 - penalty))


def get_recommended_defenses(detected_stack: dict[str, Any], violated_rule_ids: set[str]) -> list[dict[str, Any]]:
    """Generate prescriptive next best defense recommendations tailored to the stack."""
    recs = []
    lang = (detected_stack.get("language") or "Universal")
    fw = (detected_stack.get("framework") or "Universal")
    stack_tag = f"{lang}" + (f" / {fw}" if fw != "None" else "")

    # Platform headers recommendation
    if "TG-PLATFORM-002" not in violated_rule_ids and "TG-PLATFORM-001" not in violated_rule_ids:
        recs.append({
            "rule_id": "TG-PLATFORM-002",
            "priority": "P0 Critical",
            "title": "Enforce HTTP Security Headers (CSP, HSTS, X-Frame-Options)",
            "mitigates": "OWASP A05: Security Misconfiguration",
            "stack_tag": stack_tag,
            "rationale": "Protects against clickjacking, MIME-confusion, and cross-site scripting attacks.",
            "invariant_guarantee": "Zero unhardened HTTP endpoints. Requires HSTS max-age >= 31536000 and CSP nonce isolation.",
            "command": "npx torusguard harden --rule TG-PLATFORM-002"
        })

    # Rate limiting on auth
    recs.append({
        "rule_id": "TG-RATE-001",
        "priority": "P0 Critical",
        "title": "Auth Endpoint Rate Limiting & Resource Throttling",
        "mitigates": "OWASP A07: Identification and Authentication Failures",
        "stack_tag": stack_tag,
        "rationale": "Prevents brute-force credential stuffing, password spraying, and resource exhaustion.",
        "invariant_guarantee": "Max 5 failed attempts per IP window on auth routes with exponential backoff.",
        "command": "npx torusguard harden --rule TG-RATE-001"
    })

    # Timing-safe auth compare
    recs.append({
        "rule_id": "TG-AUTH-002",
        "priority": "P1 Recommended",
        "title": "Timing-Safe Secret & Signature Verification",
        "mitigates": "OWASP A02: Cryptographic Failures",
        "stack_tag": stack_tag,
        "rationale": "Eliminates side-channel timing attacks on API keys, HMAC signatures, and tokens.",
        "invariant_guarantee": "Constant-time evaluation across all cryptographic comparison call-sites.",
        "command": "npx torusguard harden --rule TG-AUTH-002"
    })

    # Tenant database isolation
    if "TG-DB-004" not in violated_rule_ids:
        recs.append({
            "rule_id": "TG-DB-004",
            "priority": "P0 Critical",
            "title": "Enforce Multi-Tenant Database Query Partition Scoping",
            "mitigates": "OWASP A01: Broken Access Control",
            "stack_tag": stack_tag,
            "rationale": "Guarantees cross-tenant data isolation and eliminates BOLA/IDOR vulnerabilities.",
            "invariant_guarantee": "All database queries MUST be explicitly scoped by authenticated tenant ID.",
            "command": "npx torusguard harden --rule TG-DB-004"
        })

    # SSRF Private IP protection
    recs.append({
        "rule_id": "TG-SSRF-002",
        "priority": "P1 Recommended",
        "title": "Block Outbound Requests to Cloud Metadata (169.254.169.254)",
        "mitigates": "OWASP A10: Server-Side Request Forgery",
        "stack_tag": stack_tag,
        "rationale": "Stops attackers from querying internal cloud metadata instances or private VPC ranges.",
        "invariant_guarantee": "Strict hostname resolution with CIDR blocking for 169.254.169.254 and RFC1918 subnets.",
        "command": "npx torusguard harden --rule TG-SSRF-002"
    })

    # AI Agent structural defense
    if "TG-AGENT-001" not in violated_rule_ids:
        recs.append({
            "rule_id": "TG-AGENT-001",
            "priority": "P2 Hardening",
            "title": "Structural AI Prompt Sandboxing & Inert Delimiters",
            "mitigates": "OWASP LLM01: Prompt Injection",
            "stack_tag": "AI / LLM Stack",
            "rationale": "Enforces user prompt boundary isolation to stop direct and indirect jailbreaks.",
            "invariant_guarantee": "User input MUST be wrapped in inert XML tags and never directly concatenated into system prompt.",
            "command": "npx torusguard harden --rule TG-AGENT-001"
        })

    return recs[:5]


def format_diff_html(diff_text: str) -> str:
    """Format unified diff with colorized line styling."""
    if not diff_text:
        return '<span class="diff-line-ctx">// No diff representation recorded</span>'
    formatted_lines = []
    for line in diff_text.splitlines():
        esc = html.escape(line)
        if line.startswith("+++") or line.startswith("---"):
            formatted_lines.append(f'<span class="diff-line-header">{esc}</span>')
        elif line.startswith("@@"):
            formatted_lines.append(f'<span class="diff-line-hunk">{esc}</span>')
        elif line.startswith("+"):
            formatted_lines.append(f'<span class="diff-line-add">{esc}</span>')
        elif line.startswith("-"):
            formatted_lines.append(f'<span class="diff-line-del">{esc}</span>')
        else:
            formatted_lines.append(f'<span class="diff-line-ctx">{esc}</span>')
    return "\n".join(formatted_lines)


def get_curated_golden_recipes(patterns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return memory recipes unpacked with rich diffs, Before/After snippets, and Ponytail metrics."""
    memory_recipes = [p for p in patterns if p.get("pattern_type") == "golden_fix_recipe"]
    unpacked: list[dict[str, Any]] = []

    for idx, r in enumerate(memory_recipes):
        rd = r.get("recipe_data") or {}
        rule_id = rd.get("rule_id") or r.get("rule_id") or "TG-GEN"
        desc = rd.get("description") or r.get("description") or "Verified fix pattern"
        diff = rd.get("diff_snippet") or ""
        before = rd.get("before_snippet") or ""
        after = rd.get("after_snippet") or ""
        metrics = rd.get("ponytail_metrics") or {"additions": 1, "deletions": 1}
        ftype = rd.get("file_type") or r.get("file_type") or ".ts"
        verified = rd.get("verified_count") or 1
        rec_id = rd.get("recipe_id") or r.get("recipe_id") or f"recipe-{rule_id}-{idx}"

        # Determine human category
        if "SEC" in rule_id:
            cat = "Secrets"
        elif "CLIENT" in rule_id:
            cat = "Client"
        elif "DB" in rule_id or "GQL" in rule_id:
            cat = "Database"
        elif "INPUT" in rule_id or "AGENT" in rule_id:
            cat = "Input"
        elif "PLATFORM" in rule_id or "SUPPLY" in rule_id or "EDGE" in rule_id or "DIFF" in rule_id:
            cat = "Platform"
        elif "RATE" in rule_id:
            cat = "Rate Limiting"
        elif "SSRF" in rule_id or "WEBHOOK" in rule_id:
            cat = "SSRF"
        else:
            cat = "General"

        unpacked.append({
            "recipe_id": rec_id,
            "rule_id": rule_id,
            "title": desc,
            "description": desc,
            "diff_snippet": diff,
            "before_snippet": before,
            "after_snippet": after,
            "solution_pattern": after or diff,
            "code_pattern": diff,
            "ponytail_metrics": metrics,
            "file_type": ftype,
            "verified_count": verified,
            "category": cat
        })

    if unpacked:
        return unpacked

    # Fallback built-in reference Golden Recipes if patterns is empty
    return [
        {
            "recipe_id": "recipe-TG-DB-001-default",
            "rule_id": "TG-DB-001",
            "title": "Parameterized SQL Query Pattern",
            "description": "Replaces vulnerable raw string interpolation with parameterized bound parameters.",
            "diff_snippet": "--- a/db/queries.py\n+++ b/db/queries.py\n@@ -10,3 +10,3 @@\n-db.execute(f'SELECT * FROM users WHERE id = {user_id}')\n+db.execute('SELECT * FROM users WHERE id = :id', {'id': user_id})",
            "before_snippet": "db.execute(f'SELECT * FROM users WHERE id = {user_id}')",
            "after_snippet": "db.execute('SELECT * FROM users WHERE id = :id', {'id': user_id})",
            "solution_pattern": "db.execute('SELECT * FROM users WHERE id = :id', {'id': user_id})",
            "code_pattern": "- db.execute(f'SELECT * FROM users WHERE id = {user_id}')\n+ db.execute('SELECT * FROM users WHERE id = :id', {'id': user_id})",
            "ponytail_metrics": {"additions": 1, "deletions": 1},
            "file_type": ".py",
            "verified_count": 1,
            "category": "Database"
        },
        {
            "recipe_id": "recipe-TG-AUTH-002-default",
            "rule_id": "TG-AUTH-002",
            "title": "Timing-Safe Cryptographic Comparison",
            "description": "Replaces standard equality (===) with timing-safe constant-time evaluation.",
            "diff_snippet": "--- a/auth/verify.ts\n+++ b/auth/verify.ts\n@@ -22,3 +22,3 @@\n-if (token === expectedSecret) {\n+if (crypto.timingSafeEqual(Buffer.from(token), Buffer.from(expectedSecret))) {",
            "before_snippet": "if (token === expectedSecret) { ... }",
            "after_snippet": "if (crypto.timingSafeEqual(Buffer.from(token), Buffer.from(expectedSecret))) { ... }",
            "solution_pattern": "if (crypto.timingSafeEqual(Buffer.from(token), Buffer.from(expectedSecret))) { ... }",
            "code_pattern": "- if (token === expectedSecret) { ... }\n+ if (crypto.timingSafeEqual(Buffer.from(token), Buffer.from(expectedSecret))) { ... }",
            "ponytail_metrics": {"additions": 1, "deletions": 1},
            "file_type": ".ts",
            "verified_count": 1,
            "category": "Auth"
        },
        {
            "recipe_id": "recipe-TG-SSRF-002-default",
            "rule_id": "TG-SSRF-002",
            "title": "Outbound Private IP Range Filtering",
            "description": "Validates outbound target IP against private VPC ranges and cloud metadata IPs.",
            "diff_snippet": "--- a/net/proxy.py\n+++ b/net/proxy.py\n@@ -15,4 +15,6 @@\n-response = requests.get(target_url)\n+ip = socket.gethostbyname(urlparse(target_url).hostname)\n+if ipaddress.ip_address(ip).is_private: raise SecurityError('SSRF blocked')\n+response = requests.get(target_url)",
            "before_snippet": "response = requests.get(target_url)",
            "after_snippet": "ip = socket.gethostbyname(urlparse(target_url).hostname)\nif ipaddress.ip_address(ip).is_private: raise SecurityError('SSRF blocked')\nresponse = requests.get(target_url)",
            "solution_pattern": "ip = socket.gethostbyname(urlparse(target_url).hostname)\nif ipaddress.ip_address(ip).is_private: raise SecurityError('SSRF blocked')\nresponse = requests.get(target_url)",
            "code_pattern": "- response = requests.get(target_url)\n+ ip = socket.gethostbyname(urlparse(target_url).hostname)\n+ if ipaddress.ip_address(ip).is_private: raise SecurityError('SSRF blocked')",
            "ponytail_metrics": {"additions": 3, "deletions": 1},
            "file_type": ".py",
            "verified_count": 1,
            "category": "SSRF"
        }
    ]


def generate_html_dashboard(telemetry: dict[str, Any]) -> str:
    """Build a complete, standalone, single-file interactive HTML security dashboard."""
    score = compute_posture_score(telemetry)
    findings = telemetry.get("findings", [])
    patterns = telemetry.get("patterns", [])
    cfg = telemetry.get("config", {})
    detected = cfg.get("detected_stack", {})
    profile = telemetry.get("profile", {})
    all_rules = telemetry.get("all_rules", [])
    safe_rules = telemetry.get("safe_rules", [])
    violated_rules = telemetry.get("violated_rules", [])

    # Polyglot stack information
    primary_lang = detected.get("language") or "Universal"
    primary_fw = detected.get("framework") or "None"
    primary_db = detected.get("data_layer") or "None"

    stack = profile.get("stack", [])
    if not stack and primary_lang != "Unknown":
        stack = [primary_lang]
        if primary_fw != "None":
            stack.append(primary_fw)
        if primary_db != "None":
            stack.append(primary_db)
    stack_label = ", ".join(stack) if stack else "Polyglot Project"

    # Severity counts
    crit_count = sum(1 for f in findings if f.get("severity") == "Critical")
    high_count = sum(1 for f in findings if f.get("severity") == "High")
    med_count = sum(1 for f in findings if f.get("severity") in ("Medium", "Low"))
    total_count = len(findings)
    total_rules = len(all_rules) if all_rules else 74
    defended_count = len(safe_rules) if safe_rules else (total_rules - len(violated_rules))
    coverage_pct = int((defended_count / total_rules) * 100) if total_rules > 0 else 100

    # Recipes
    recipes = get_curated_golden_recipes(patterns)

    # Recommendations
    violated_ids = {f.get("rule_id") for f in findings if not f.get("is_canary", False)}
    recommendations = get_recommended_defenses(detected, violated_ids)

    # Open vs resolved counts
    open_count = sum(1 for f in findings if f.get("status", "open") not in ("fixed", "resolved", "confirmed_fixed"))
    resolved_count = total_count - open_count

    # Gauge values & Dynamic Theme Accents
    circumference = 251.2
    dash_offset = circumference - (circumference * (score / 100.0))
    if score >= 90:
        grad_start = "#3fb950"
        grad_end = "#2ea043"
        glow_color = "#3fb950"
        status_label = "🟢 HARDENED & SECURE"
        status_badge_class = "status-clean"
    elif score >= 75:
        grad_start = "#58a6ff"
        grad_end = "#1f6feb"
        glow_color = "#58a6ff"
        status_label = "🔵 ELEVATED RESILIENCE"
        status_badge_class = "status-elevated"
    elif score >= 50:
        grad_start = "#d29922"
        grad_end = "#bb8009"
        glow_color = "#d29922"
        status_label = "🟡 WARNINGS DETECTED"
        status_badge_class = "status-warn"
    else:
        grad_start = "#f85149"
        grad_end = "#da3633"
        glow_color = "#f85149"
        status_label = "🔴 CRITICAL RISK"
        status_badge_class = "status-critical"

    # ── Findings Table HTML (with Expandable Drawers & Simulator Checkboxes) ──
    findings_rows = ""
    sev_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    sorted_f = sorted(findings, key=lambda x: (sev_order.get(x.get("severity", "Low"), 9), -x.get("confidence_score", 0)))

    if sorted_f:
        for idx, f in enumerate(sorted_f[:50]):
            fid = html.escape(f.get("finding_id", f"fid-{idx}"))
            drawer_id = f"drawer-{idx}"
            sev = f.get("severity", "Medium")
            sev_class = "badge-critical" if sev == "Critical" else ("badge-high" if sev == "High" else "badge-medium")
            rule = html.escape(f.get("rule_id", "TG-GEN"))
            title = html.escape(f.get("title", "Finding"))
            fpath = html.escape(f.get("file_path", "unknown"))
            line = f.get("line_number", 0)
            conf = f.get("confidence_score", 70)
            desc = html.escape(f.get("description", "Security invariant check failed."))
            snippet = html.escape(f.get("snippet", f.get("matched_text", "// No preview snippet available")))
            is_canary = f.get("is_canary", False)
            canary_badge = ' <span class="badge badge-canary">Canary Test</span>' if is_canary else ''
            f_status = "resolved" if f.get("status") in ("fixed", "resolved", "confirmed_fixed") else "open"
            status_badge = ' <span class="badge badge-success">&#10004; Resolved</span>' if f_status == "resolved" else ""

            search_blob = html.escape(f"{rule} {title} {fpath} {sev} {f_status}".lower())

            findings_rows += f"""
            <tr class="finding-row" data-severity="{sev.lower()}" data-status="{f_status}" data-search="{search_blob}" data-path="{fpath}" data-drawer-id="{drawer_id}" onclick="toggleDrawer(this)">
              <td style="text-align: center;" onclick="event.stopPropagation()">
                <label class="sim-checkbox-label" title="Simulate fixing this finding in What-If Posture Simulator">
                  <input type="checkbox" class="sim-fix-chk" data-finding-id="{fid}" data-severity="{sev}" onchange="updateSimulatedScore()">
                </label>
              </td>
              <td><span class="badge {sev_class}">{sev}</span>{canary_badge}{status_badge}</td>
              <td><code class="rule-id">{rule}</code></td>
              <td class="finding-title">{title}</td>
              <td><code>{fpath}:{line}</code></td>
              <td><span class="conf-score">{conf}%</span></td>
              <td style="text-align: right;"><span class="drawer-chevron">&#9656;</span></td>
            </tr>
            <tr id="{drawer_id}" class="drawer-row" style="display: none;">
              <td colspan="7">
                <div class="drawer-content">
                  <div class="drawer-header">
                    <div>
                      <strong>Finding ID:</strong> <code>{fid}</code> &middot; 
                      <strong>File:</strong> <code>{fpath}:{line}</code> &middot; 
                      <strong>Confidence:</strong> {conf}/100
                    </div>
                  </div>
                  <div class="drawer-desc">{desc}</div>
                  <div class="code-preview">
                    <pre><code>{snippet}</code></pre>
                  </div>
                  <div class="drawer-actions">
                    <div class="cmd-box">
                      <code>npx torusguard harden --finding {fid}</code>
                      <button class="btn-copy" onclick="copyText('npx torusguard harden --finding {fid}', this); event.stopPropagation();">&#128203; Copy Command</button>
                    </div>
                  </div>
                </div>
              </td>
            </tr>"""
        if len(sorted_f) > 50:
            findings_rows += f'<tr><td colspan="7" class="overflow-row">... and {len(sorted_f) - 50} more findings cataloged in run artifacts</td></tr>'
    else:
        findings_rows = '<tr><td colspan="7" class="empty-cell">&#10004; Zero security invariant violations detected. Posture is 100% clean and defended.</td></tr>'

    # ── 5-Layer Architectural Invariant Matrix ──
    # Group all rules by architectural layer
    layers_html = ""
    for layer in ARCHITECTURAL_LAYERS:
        lid = layer["id"]
        lname = layer["name"]
        licon = layer["icon"]
        ldesc = layer["description"]
        lfams = layer["families"]

        layer_rules = [r for r in all_rules if any(r.get("rule_id", "").startswith(fam) for fam in lfams)]
        l_total = len(layer_rules)
        l_defended = sum(1 for r in layer_rules if r["rule_id"] not in violated_ids)
        l_status_class = "status-clean" if l_defended == l_total else ("status-warn" if l_defended >= l_total * 0.75 else "status-critical")

        chips_html = ""
        for r in layer_rules:
            rid = r["rule_id"]
            rtitle = r["title"]
            rsev = r.get("severity", "Medium")
            is_defended = rid not in violated_ids
            chip_cls = "inv-chip-safe" if is_defended else "inv-chip-violated"
            dot_color = "var(--accent-green)" if is_defended else "var(--accent-red)"
            status_text = "Defended" if is_defended else "Violated"
            search_data = f"{rid} {rtitle} {rsev} {status_text} {lname}".lower()

            chips_html += f"""
            <div class="inv-chip {chip_cls}" data-rule="{rid}" data-layer="{lid}" data-search="{html.escape(search_data)}" onclick="inspectInvariant('{rid}')" title="Click to inspect security invariant guarantee for {rid}">
              <span class="inv-dot" style="background: {dot_color};"></span>
              <code class="inv-code">{rid}</code>
              <span class="inv-title">{html.escape(rtitle)}</span>
            </div>"""

        layers_html += f"""
        <div class="layer-card" data-layer-id="{lid}">
          <div class="layer-header">
            <div class="layer-title-group">
              <span class="layer-icon">{licon}</span>
              <div>
                <div class="layer-name">{lname}</div>
                <div class="layer-desc">{ldesc}</div>
              </div>
            </div>
            <div class="layer-badge {l_status_class}">{l_defended}/{l_total} Enforced</div>
          </div>
          <div class="layer-chips-grid">
            {chips_html}
          </div>
        </div>"""

    # ── OWASP Top 10 Compliance Radar ──
    owasp_defs = [
        ("A01: Broken Access Control", ["TG-DB-001", "TG-DB-004", "TG-AUTH-006", "TG-WS-002", "TG-BIZ-001", "TG-BIZ-002"]),
        ("A02: Cryptographic Failures", ["TG-SEC-001", "TG-SEC-002", "TG-SEC-003", "TG-SEC-004", "TG-SEC-005", "TG-AUTH-002"]),
        ("A03: Injection Defense", ["TG-INPUT-001", "TG-INPUT-002", "TG-INPUT-003", "TG-INPUT-004", "TG-DB-002", "TG-DB-003", "TG-GQL-001"]),
        ("A05: Security Configuration", ["TG-PLATFORM-001", "TG-PLATFORM-002", "TG-PLATFORM-003", "TG-PLATFORM-004", "TG-CLIENT-001", "TG-CLIENT-002"]),
        ("A06: Supply Chain Health", ["TG-SUPPLY-001", "TG-SUPPLY-002", "TG-SUPPLY-003", "TG-SUPPLY-004", "TG-SUPPLY-005"]),
        ("A07: Identity & Auth", ["TG-AUTH-001", "TG-AUTH-003", "TG-AUTH-004", "TG-AUTH-005", "TG-AUTH-007", "TG-CSRF-001", "TG-CSRF-002"]),
        ("A08: Software Integrity", ["TG-WEBHOOK-001", "TG-WEBHOOK-002", "TG-WEBHOOK-003", "TG-DIFF-001", "TG-DIFF-002"]),
        ("A10: SSRF Defense", ["TG-SSRF-001", "TG-SSRF-002", "TG-SSRF-003", "TG-SSRF-004"])
    ]

    owasp_cards_html = ""
    for category_name, rule_codes in owasp_defs:
        matched = [f for f in findings if f.get("rule_id") in rule_codes and not f.get("is_canary", False)]
        cat_count = len(matched)
        if cat_count == 0:
            c_score = 100
            c_color = "var(--accent-green)"
            c_badge = "100% Compliant"
        elif cat_count == 1:
            c_score = 80
            c_color = "var(--accent-yellow)"
            c_badge = "1 Issue"
        else:
            c_score = max(20, 100 - (cat_count * 20))
            c_color = "var(--accent-red)"
            c_badge = f"{cat_count} Issues"

        owasp_cards_html += f"""
        <div class="owasp-card">
          <div class="owasp-top">
            <span class="owasp-title">{category_name}</span>
            <span class="owasp-badge" style="color: {c_color}; border-color: {c_color};">{c_badge}</span>
          </div>
          <div class="owasp-bar-bg">
            <div class="owasp-bar" style="width: {c_score}%; background: {c_color};"></div>
          </div>
        </div>"""

    # ── Enterprise Compliance Framework Matrix ──
    compliance_frameworks: list[ComplianceFramework] = [
        {
            "name": "SOC 2 Type II",
            "subtitle": "AICPA Trust Services Criteria (Security & Boundary)",
            "controls": [
                {"code": "CC6.1 Logical Access", "families": "TG-AUTH, TG-CLIENT", "rules": ["TG-AUTH-001", "TG-AUTH-002", "TG-AUTH-003", "TG-AUTH-004", "TG-CLIENT-001"]},
                {"code": "CC6.6 Network Boundary", "families": "TG-SSRF, TG-RATE, TG-WS", "rules": ["TG-SSRF-001", "TG-SSRF-002", "TG-RATE-001", "TG-WS-001"]},
                {"code": "CC6.7 Transmission Security", "families": "TG-PLATFORM, TG-SEC", "rules": ["TG-PLATFORM-001", "TG-PLATFORM-002", "TG-SEC-001", "TG-SEC-002"]},
                {"code": "CC7.1 Vulnerability & Churn", "families": "TG-DIFF, TG-SUPPLY", "rules": ["TG-DIFF-001", "TG-DIFF-002", "TG-SUPPLY-001", "TG-SUPPLY-002"]}
            ]
        },
        {
            "name": "ISO/IEC 27001:2022",
            "subtitle": "Annex A Controls for Technological & Application Security",
            "controls": [
                {"code": "A.8.20 Network Security", "families": "TG-SSRF, TG-WEBHOOK, TG-RATE", "rules": ["TG-SSRF-001", "TG-WEBHOOK-001", "TG-RATE-001"]},
                {"code": "A.8.24 Cryptography Usage", "families": "TG-SEC, TG-AUTH", "rules": ["TG-SEC-001", "TG-SEC-003", "TG-AUTH-002"]},
                {"code": "A.8.28 Secure Coding", "families": "TG-INPUT, TG-DB, TG-GQL, TG-AGENT", "rules": ["TG-INPUT-001", "TG-DB-001", "TG-GQL-001", "TG-AGENT-001"]}
            ]
        },
        {
            "name": "HIPAA Security Rule",
            "subtitle": "45 CFR Part 164 Technical Safeguards for ePHI",
            "controls": [
                {"code": "§ 164.312(a)(1) Access Control", "families": "TG-AUTH, TG-DB (Tenant Isolation)", "rules": ["TG-AUTH-001", "TG-DB-004", "TG-AUTH-006"]},
                {"code": "§ 164.312(c)(1) ePHI Integrity", "families": "TG-WEBHOOK, TG-BIZ, TG-DIFF", "rules": ["TG-WEBHOOK-001", "TG-BIZ-001", "TG-DIFF-001"]},
                {"code": "§ 164.312(e)(1) Transmission Security", "families": "TG-PLATFORM, TG-SEC, TG-CLIENT", "rules": ["TG-PLATFORM-001", "TG-SEC-001", "TG-CLIENT-001"]}
            ]
        }
    ]

    compliance_cards_html = ""
    for fw in compliance_frameworks:
        fw_name = fw["name"]
        fw_sub = fw["subtitle"]
        controls = fw["controls"]
        all_fw_rules = [rid for c in controls for rid in c["rules"]]
        fw_violated = [rid for rid in all_fw_rules if rid in violated_ids]
        fw_pct = int(((len(all_fw_rules) - len(fw_violated)) / len(all_fw_rules)) * 100) if all_fw_rules else 100
        badge_cls = "badge-success" if fw_pct == 100 else ("badge-medium" if fw_pct >= 80 else "badge-critical")

        ctrl_rows_html = ""
        for ctrl in controls:
            c_code = ctrl["code"]
            c_fams = ctrl["families"]
            c_rules = ctrl["rules"]
            c_viol = [r for r in c_rules if r in violated_ids]
            c_status = '<span class="badge badge-success">&#10004; Passing</span>' if not c_viol else f'<span class="badge badge-critical">{len(c_viol)} Violated</span>'

            ctrl_rows_html += f"""
            <div class="comp-ctrl-row">
              <div>
                <div class="comp-ctrl-code">{c_code}</div>
                <div class="comp-ctrl-fams">{c_fams}</div>
              </div>
              <div>{c_status}</div>
            </div>"""

        compliance_cards_html += f"""
        <div class="card comp-card">
          <div class="comp-card-header">
            <div>
              <div class="comp-title">{fw_name}</div>
              <div class="comp-sub">{fw_sub}</div>
            </div>
            <span class="badge {badge_cls}">{fw_pct}% Met</span>
          </div>
          <div class="comp-ctrl-list">
            {ctrl_rows_html}
          </div>
        </div>"""

    # ── Root-Cause Architectural Clusters ──
    cluster_groups: dict[str, list[dict[str, Any]]] = {}
    for f in findings:
        c_key = f.get("cluster") or f.get("category") or "General Invariants"
        if c_key not in cluster_groups:
            cluster_groups[c_key] = []
        cluster_groups[c_key].append(f)

    sorted_clusters = sorted(cluster_groups.items(), key=lambda x: len(x[1]), reverse=True)
    clusters_html = ""
    if sorted_clusters:
        for c_name, c_list in sorted_clusters[:5]:
            c_count = len(c_list)
            unique_files = len(set(item.get("file_path", "") for item in c_list))
            clusters_html += f"""
            <div class="cluster-item">
              <div class="cluster-header">
                <strong>{html.escape(c_name.replace('-', ' ').title())}</strong>
                <span class="badge badge-high">{c_count} findings</span>
              </div>
              <div class="cluster-sub">Blast Radius: {unique_files} file(s) affected</div>
            </div>"""
    else:
        clusters_html = '<div class="empty-state">&#10004; No architectural vulnerability clusters identified. Systemic invariants enforced.</div>'

    # ── Interactive Attack Surface Heatmap by Directory ──
    dir_counts: dict[str, int] = {}
    for f in findings:
        fp = f.get("file_path", "")
        parts = fp.replace("\\", "/").split("/")
        d_name = f"{parts[0]}/" if len(parts) > 1 else "root"
        dir_counts[d_name] = dir_counts.get(d_name, 0) + 1

    sorted_dirs = sorted(dir_counts.items(), key=lambda x: x[1], reverse=True)
    max_dir_count = sorted_dirs[0][1] if sorted_dirs else 1
    heatmap_rows_html = ""
    if sorted_dirs:
        for d_name, count in sorted_dirs[:6]:
            pct = int((count / max_dir_count) * 100)
            bar_color = "#f85149" if count > 5 else ("#d29922" if count > 2 else "#58a6ff")
            heatmap_rows_html += f"""
            <div class="heatmap-row" onclick="filterByDirectory('{html.escape(d_name)}')" title="Click to filter findings in {html.escape(d_name)}">
              <span class="heatmap-label">{html.escape(d_name)}</span>
              <div class="heatmap-bar-bg">
                <div class="heatmap-bar" style="width: {pct}%; background: {bar_color};"></div>
              </div>
              <span class="heatmap-count">{count}</span>
            </div>"""
    else:
        heatmap_rows_html = '<div class="empty-state">&#10004; Zero directory surface exposure detected across repository modules.</div>'

    # ── Golden Fix Recipes (Dual-View Diff / Split, Churn Metrics, Category Filter) ──
    # Category counts for filter pills
    recipe_cats: dict[str, int] = {}
    for r in recipes:
        c = r.get("category", "General")
        recipe_cats[c] = recipe_cats.get(c, 0) + 1

    recipe_cat_pills_html = f'<span class="pill active" data-recipe-cat-filter="all" onclick="filterRecipeCategory(\'all\')">All ({len(recipes)})</span>'
    for c_name, c_cnt in sorted(recipe_cats.items()):
        c_slug = c_name.lower().replace(" ", "-")
        recipe_cat_pills_html += f'<span class="pill" data-recipe-cat-filter="{c_slug}" onclick="filterRecipeCategory(\'{c_slug}\')">{c_name} ({c_cnt})</span>'

    recipes_html = ""
    for r in recipes:
        rid = html.escape(r.get("rule_id", "TG-FIX"))
        rtitle = html.escape(r.get("title", "Verified fix pattern"))
        rcat = html.escape(r.get("category", "General").lower().replace(" ", "-"))
        rec_key = html.escape(r.get("recipe_id", f"recipe-{rid}").replace(" ", "-"))
        metrics = r.get("ponytail_metrics") or {"additions": 1, "deletions": 1}
        adds = metrics.get("additions", 1)
        dels = metrics.get("deletions", 1)
        ftype = html.escape(r.get("file_type", ".ts"))
        vcount = r.get("verified_count", 1)

        diff_str = r.get("diff_snippet") or ""
        before_str = r.get("before_snippet") or "// Vulnerable snippet"
        after_str = r.get("after_snippet") or r.get("solution_pattern") or "// Hardened pattern"

        formatted_diff = format_diff_html(diff_str)
        escaped_before = html.escape(before_str)
        escaped_after = html.escape(after_str)
        copy_payload = html.escape((after_str or diff_str).replace("\n", " ").replace('"', '&quot;'))

        recipes_html += f"""
        <div class="recipe-card" data-category="{rcat}">
          <div class="recipe-header">
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
              <span class="badge badge-success">{rid}</span>
              <strong>{rtitle}</strong>
            </div>
            <div class="recipe-meta-badges">
              <span class="chip chip-filetype">{ftype}</span>
              <span class="ponytail-badge" title="Ponytail line churn budget (&le; 35 additions, &le; 25 deletions)">⚡ +{adds} / -{dels} lines</span>
              <span class="verified-badge">&#10004; Verified {vcount}x</span>
            </div>
          </div>
          <div class="recipe-view-switcher">
            <button class="recipe-tab-btn active" id="btn-view-diff-{rec_key}" onclick="setRecipeView('{rec_key}', 'diff')">Unified Diff</button>
            <button class="recipe-tab-btn" id="btn-view-split-{rec_key}" onclick="setRecipeView('{rec_key}', 'split')">Before / After</button>
          </div>
          <div id="recipe-view-diff-{rec_key}" class="code-preview recipe-diff-container">
            <pre><code>{formatted_diff}</code></pre>
          </div>
          <div id="recipe-view-split-{rec_key}" class="recipe-split-container" style="display: none;">
            <div class="split-pane">
              <div class="split-label split-del">&#10008; Before (Vulnerable)</div>
              <div class="code-preview"><pre><code>{escaped_before}</code></pre></div>
            </div>
            <div class="split-pane">
              <div class="split-label split-add">&#10004; After (Hardened)</div>
              <div class="code-preview"><pre><code>{escaped_after}</code></pre></div>
            </div>
          </div>
          <div class="recipe-actions">
            <div class="cmd-box">
              <code>npx torusguard harden --rule {rid}</code>
              <button class="btn-copy" onclick="copyText('npx torusguard harden --rule {rid}', this); event.stopPropagation();">&#128203; Copy Command</button>
            </div>
            <button class="btn btn-sm" onclick="copyText('{copy_payload}', this); event.stopPropagation();">&#128203; Copy Pattern</button>
          </div>
        </div>"""

    # ── Prescriptive "Next Best Defenses" Advisory ──
    advisory_html = ""
    for adv in recommendations:
        arid = html.escape(adv["rule_id"])
        aprio = html.escape(adv.get("priority", "P1 Recommended"))
        atitle = html.escape(adv["title"])
        amitig = html.escape(adv.get("mitigates", "OWASP Invariant"))
        astack = html.escape(adv.get("stack_tag", "Polyglot"))
        arationale = html.escape(adv["rationale"])
        aguarantee = html.escape(adv.get("invariant_guarantee", "Guarantees zero architectural bypasses."))
        acmd = html.escape(adv["command"])

        prio_cls = "badge-critical" if "P0" in aprio else ("badge-high" if "P1" in aprio else "badge-canary")

        advisory_html += f"""
        <div class="advisory-item">
          <div class="advisory-top">
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
              <span class="badge {prio_cls}">{aprio}</span>
              <span class="badge badge-primary">{arid}</span>
              <strong>{atitle}</strong>
            </div>
            <span class="chip chip-filetype">{astack}</span>
          </div>
          <div class="advisory-mitigates"><strong>Mitigates:</strong> {amitig}</div>
          <div class="advisory-desc">{arationale}</div>
          <div class="advisory-guarantee"><strong>Invariant Guarantee:</strong> {aguarantee}</div>
          <div class="cmd-box" style="margin-top: 8px;">
            <code>{acmd}</code>
            <button class="btn-copy" onclick="copyText('{acmd}', this); event.stopPropagation();">&#128203; Copy</button>
          </div>
        </div>"""

    # ── Client-side JSON Payloads ──
    findings_json_str = json.dumps(findings).replace("</script>", "<\\/script>")
    sarif_rules_json_str = json.dumps([{"id": r["rule_id"], "shortDescription": {"text": r["title"]}} for r in all_rules[:74]])
    rule_catalog_json_str = json.dumps({r["rule_id"]: r for r in all_rules}).replace("</script>", "<\\/script>")
    violated_ids_json_str = json.dumps(list(violated_ids))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TorusGuard Security Report &middot; {html.escape(telemetry.get('project_name', 'Project'))}</title>
  <style>
    :root {{
      --bg-dark: #0d1117;
      --bg-surface: #161b22;
      --bg-card: #21262d;
      --border-subtle: #30363d;
      --text-main: #f0f6fc;
      --text-muted: #8b949e;
      --accent-blue: #58a6ff;
      --accent-green: #3fb950;
      --accent-yellow: #d29922;
      --accent-red: #f85149;
      --accent-orange: #db6d28;
      --accent-purple: #bc8cff;
      --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    body.light-theme {{
      --bg-dark: #f6f8fa;
      --bg-surface: #ffffff;
      --bg-card: #f0f3f6;
      --border-subtle: #d0d7de;
      --text-main: #1f2328;
      --text-muted: #656d76;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-stack);
      line-height: 1.5;
      padding: 24px;
      transition: background 0.2s ease, color 0.2s ease;
    }}
    .container {{ max-width: 1240px; margin: 0 auto; }}

    /* Header */
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border-subtle);
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .logo-group h1 {{
      font-size: 22px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .shield-icon {{ font-size: 24px; }}
    .project-meta {{ color: var(--text-muted); font-size: 13px; margin-top: 4px; }}
    .header-actions {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
    .status-badge {{
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
    }}
    .status-clean {{ background: rgba(63, 185, 80, 0.15); border: 1px solid var(--accent-green); color: var(--accent-green); }}
    .status-elevated {{ background: rgba(88, 166, 255, 0.15); border: 1px solid var(--accent-blue); color: var(--accent-blue); }}
    .status-warn {{ background: rgba(210, 153, 34, 0.15); border: 1px solid var(--accent-yellow); color: var(--accent-yellow); }}
    .status-critical {{ background: rgba(248, 81, 73, 0.15); border: 1px solid var(--accent-red); color: var(--accent-red); }}

    .btn {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: background 0.2s, border-color 0.2s;
    }}
    .btn:hover {{ background: #30363d; border-color: var(--text-muted); }}
    body.light-theme .btn:hover {{ background: #e1e4e8; }}
    .btn-sm {{ padding: 3px 8px; font-size: 11px; }}

    /* KPI Grid */
    .grid-kpi {{
      display: grid;
      grid-template-columns: 220px repeat(4, 1fr);
      gap: 14px;
      margin-bottom: 24px;
    }}
    @media (max-width: 950px) {{ .grid-kpi {{ grid-template-columns: 1fr 1fr; }} }}
    @media (max-width: 600px) {{ .grid-kpi {{ grid-template-columns: 1fr; }} }}

    .card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 18px;
    }}
    .gauge-card {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }}
    .gauge-svg {{ width: 110px; height: 110px; transform: rotate(-90deg); filter: drop-shadow(0 0 6px rgba(0, 0, 0, 0.3)); }}
    .gauge-bg {{ fill: none; stroke: var(--bg-card); stroke-width: 8; }}
    .gauge-fill {{
      fill: none;
      stroke-width: 8;
      stroke-linecap: round;
      stroke-dasharray: 251.2;
      stroke-dashoffset: 251.2;
      transition: stroke-dashoffset 0.9s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .gauge-value {{
      position: absolute;
      font-size: 30px;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.5px;
    }}
    .sev-card {{ text-align: center; cursor: pointer; transition: transform 0.15s, border-color 0.2s; }}
    .sev-card:hover {{ transform: translateY(-2px); border-color: var(--accent-blue); }}
    .sev-card .sev-count {{ font-size: 34px; font-weight: 800; }}
    .sev-card .sev-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); margin-top: 4px; }}

    /* What-If Posture Simulator Card */
    .simulator-card {{
      margin-bottom: 24px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-left: 4px solid var(--accent-blue);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      padding: 14px 18px;
    }}
    .simulator-clean {{ border-left-color: var(--accent-green); }}
    .sim-stats {{ display: flex; align-items: center; gap: 10px; font-size: 13px; }}
    .sim-actions {{ display: flex; gap: 6px; flex-wrap: wrap; }}
    .sim-checkbox-label {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      cursor: pointer;
      font-size: 11px;
      color: var(--text-muted);
    }}
    .sim-fix-chk {{ cursor: pointer; accent-color: var(--accent-blue); }}

    /* Invariant Matrix */
    .defended-section {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 18px;
      margin-bottom: 24px;
    }}
    .defended-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      cursor: pointer;
    }}
    .coverage-bar-container {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 10px 14px;
      margin-bottom: 16px;
    }}
    .coverage-stats {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}
    .coverage-progress-bg {{
      height: 8px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 4px;
      overflow: hidden;
    }}
    .coverage-progress-fill {{
      height: 100%;
      background: var(--accent-green);
      border-radius: 4px;
      transition: width 0.6s ease;
    }}
    .inv-search-bar {{
      margin-bottom: 16px;
      display: flex;
      gap: 10px;
      align-items: center;
    }}
    .layers-container {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .layer-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 12px 14px;
    }}
    .layer-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}
    .layer-title-group {{ display: flex; align-items: center; gap: 8px; }}
    .layer-icon {{ font-size: 16px; }}
    .layer-name {{ font-size: 13px; font-weight: 700; color: var(--text-main); }}
    .layer-desc {{ font-size: 11px; color: var(--text-muted); }}
    .layer-badge {{
      font-size: 11px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 10px;
    }}
    .layer-chips-grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .inv-chip {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 4px 8px;
      font-size: 11px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .inv-chip:hover {{
      border-color: var(--accent-blue);
      transform: translateY(-1px);
    }}
    .inv-chip-safe {{ border-left: 2px solid var(--accent-green); }}
    .inv-chip-violated {{ border-left: 2px solid var(--accent-red); background: rgba(248, 81, 73, 0.08); }}
    .inv-dot {{ width: 6px; height: 6px; border-radius: 50%; }}
    .inv-code {{ font-family: monospace; font-weight: 600; color: var(--accent-blue); font-size: 11px; }}
    .inv-title {{ color: var(--text-main); max-width: 140px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

    /* Modal / Drawer for Invariant Inspection */
    .modal-backdrop {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(2px);
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}
    .modal-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      max-width: 600px;
      width: 100%;
      padding: 22px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }}
    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 14px;
    }}
    .modal-close-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 18px;
      cursor: pointer;
    }}
    .modal-close-btn:hover {{ color: var(--text-main); }}
    .modal-body {{ font-size: 13px; color: var(--text-main); display: flex; flex-direction: column; gap: 12px; }}

    /* Filter & Search Bar */
    .filter-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .filter-pills {{ display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }}
    .pill-group-label {{
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-right: 2px;
    }}
    .pill {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 4px 10px;
      border-radius: 14px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.15s ease;
      user-select: none;
    }}
    .pill:hover {{ color: var(--text-main); border-color: var(--text-muted); }}
    .pill.active {{
      background: var(--accent-blue);
      border-color: var(--accent-blue);
      color: #fff;
    }}
    .dir-filter-chip {{
      display: none;
      background: rgba(88, 166, 255, 0.15);
      border: 1px solid var(--accent-blue);
      color: var(--accent-blue);
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 12px;
      cursor: pointer;
    }}
    .btn-reset-filters {{
      display: none;
      background: rgba(248, 81, 73, 0.12);
      border: 1px solid rgba(248, 81, 73, 0.35);
      color: var(--accent-red);
      font-size: 11px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 12px;
      cursor: pointer;
      margin-left: 4px;
      transition: all 0.15s;
    }}
    .btn-reset-filters:hover {{ background: rgba(248, 81, 73, 0.25); }}
    .search-wrapper {{
      position: relative;
      display: inline-flex;
      align-items: center;
    }}
    .search-input {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 7px 28px 7px 12px;
      border-radius: 6px;
      font-size: 13px;
      width: 280px;
      outline: none;
      transition: border-color 0.15s;
    }}
    .search-input:focus {{ border-color: var(--accent-blue); }}
    .search-clear-btn {{
      position: absolute;
      right: 8px;
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 14px;
      line-height: 1;
      padding: 2px 4px;
      display: none;
    }}
    .search-clear-btn:hover {{ color: var(--text-main); }}
    .filter-stats-bar {{
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 14px;
      padding-left: 2px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    /* Table & Drawers */
    .table-container {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      overflow: hidden;
      margin-bottom: 24px;
    }}
    table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }}
    th {{
      background: var(--bg-card);
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-subtle);
      font-weight: 600;
      color: var(--text-muted);
    }}
    td {{ padding: 12px 14px; border-bottom: 1px solid var(--border-subtle); vertical-align: middle; }}
    tr.finding-row {{ cursor: pointer; transition: background 0.1s; }}
    tr.finding-row:hover {{ background: rgba(255, 255, 255, 0.02); }}
    body.light-theme tr.finding-row:hover {{ background: rgba(0, 0, 0, 0.02); }}
    tr.finding-row.expanded {{ background: rgba(88, 166, 255, 0.05); }}
    .drawer-chevron {{ display: inline-block; transition: transform 0.2s; font-size: 14px; color: var(--text-muted); }}
    tr.finding-row.expanded .drawer-chevron {{ transform: rotate(90deg); color: var(--accent-blue); }}

    /* Badges */
    .badge {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}
    .badge-critical {{ background: rgba(248, 81, 73, 0.2); color: var(--accent-red); border: 1px solid var(--accent-red); }}
    .badge-high {{ background: rgba(219, 109, 40, 0.2); color: var(--accent-orange); border: 1px solid var(--accent-orange); }}
    .badge-medium {{ background: rgba(210, 153, 34, 0.2); color: var(--accent-yellow); border: 1px solid var(--accent-yellow); }}
    .badge-success {{ background: rgba(63, 185, 80, 0.2); color: var(--accent-green); border: 1px solid var(--accent-green); }}
    .badge-primary {{ background: rgba(88, 166, 255, 0.2); color: var(--accent-blue); border: 1px solid var(--accent-blue); }}
    .badge-canary {{ background: rgba(188, 140, 255, 0.2); color: var(--accent-purple); border: 1px solid var(--accent-purple); }}

    .rule-id {{ color: var(--accent-blue); font-family: monospace; font-weight: 600; }}
    .conf-score {{ color: var(--text-muted); font-size: 12px; }}

    /* Drawer Content */
    .drawer-content {{
      padding: 16px;
      background: var(--bg-dark);
      border-left: 3px solid var(--accent-blue);
      margin: 8px 12px;
      border-radius: 4px;
    }}
    body.light-theme .drawer-content {{ background: var(--bg-card); }}
    .drawer-header {{
      display: flex;
      justify-content: space-between;
      color: var(--text-muted);
      font-size: 12px;
      margin-bottom: 8px;
    }}
    .drawer-desc {{ font-size: 13px; color: var(--text-main); margin-bottom: 12px; }}
    .code-preview {{
      background: #000;
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 10px;
      font-family: monospace;
      font-size: 12px;
      overflow-x: auto;
      margin-bottom: 12px;
    }}
    body.light-theme .code-preview {{ background: #f6f8fa; border-color: var(--border-subtle); }}
    .code-preview code {{ color: #7ee787; font-family: monospace; }}
    body.light-theme .code-preview code {{ color: #1f2328; }}
    .drawer-actions {{ display: flex; justify-content: flex-end; gap: 8px; }}
    .cmd-box {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      padding: 4px 8px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      font-family: monospace;
    }}
    .btn-copy {{
      background: transparent;
      border: none;
      color: var(--accent-blue);
      cursor: pointer;
      font-size: 11px;
    }}
    .btn-copy:hover {{ text-decoration: underline; }}
    .btn-copy.copied {{ color: var(--accent-green) !important; }}

    /* Section Titles */
    .section-title {{
      font-size: 14px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    /* OWASP Grid */
    .grid-owasp {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 24px;
    }}
    @media (max-width: 950px) {{ .grid-owasp {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 550px) {{ .grid-owasp {{ grid-template-columns: 1fr; }} }}
    .owasp-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 12px;
    }}
    .owasp-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
    .owasp-title {{ font-size: 11px; font-weight: 600; color: var(--text-main); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .owasp-badge {{ font-size: 10px; font-weight: 700; border: 1px solid; border-radius: 8px; padding: 1px 6px; }}
    .owasp-bar-bg {{ width: 100%; height: 6px; background: var(--bg-card); border-radius: 3px; overflow: hidden; }}
    .owasp-bar {{ height: 100%; border-radius: 3px; }}

    /* Compliance Framework Grid */
    .grid-compliance {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin-bottom: 24px;
    }}
    @media (max-width: 900px) {{ .grid-compliance {{ grid-template-columns: 1fr; }} }}
    .comp-card {{ padding: 14px; }}
    .comp-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 10px;
    }}
    .comp-title {{ font-size: 13px; font-weight: 700; color: var(--text-main); }}
    .comp-sub {{ font-size: 11px; color: var(--text-muted); margin-top: 2px; }}
    .comp-ctrl-list {{ display: flex; flex-direction: column; gap: 8px; }}
    .comp-ctrl-row {{ display: flex; justify-content: space-between; align-items: center; font-size: 11px; }}
    .comp-ctrl-code {{ font-weight: 600; color: var(--text-main); }}
    .comp-ctrl-fams {{ color: var(--text-muted); font-size: 10px; }}

    /* Dual Grids */
    .grid-bottom {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }}
    @media (max-width: 850px) {{ .grid-bottom {{ grid-template-columns: 1fr; }} }}

    .cluster-item {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 10px 12px;
      margin-bottom: 8px;
    }}
    .cluster-header {{ display: flex; justify-content: space-between; align-items: center; font-size: 13px; }}
    .cluster-sub {{ font-size: 11px; color: var(--text-muted); margin-top: 4px; }}

    /* Heatmap */
    .heatmap-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; cursor: pointer; padding: 4px 6px; border-radius: 4px; }}
    .heatmap-row:hover {{ background: rgba(255, 255, 255, 0.03); }}
    body.light-theme .heatmap-row:hover {{ background: rgba(0, 0, 0, 0.03); }}
    .heatmap-label {{ font-size: 12px; font-family: monospace; color: var(--text-main); min-width: 110px; text-align: right; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .heatmap-bar-bg {{ flex: 1; height: 16px; background: var(--bg-card); border-radius: 4px; overflow: hidden; }}
    .heatmap-bar {{ height: 100%; border-radius: 4px; }}
    .heatmap-count {{ font-size: 12px; font-weight: 600; color: var(--text-muted); min-width: 25px; }}

    /* Golden Recipes & Diff Engine */
    .recipe-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 14px;
      margin-bottom: 12px;
    }}
    .recipe-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      flex-wrap: wrap;
      gap: 8px;
      font-size: 13px;
    }}
    .recipe-meta-badges {{ display: flex; align-items: center; gap: 6px; }}
    .chip-filetype {{ background: rgba(88, 166, 255, 0.1); border: 1px solid var(--accent-blue); color: var(--accent-blue); font-size: 10px; font-family: monospace; padding: 2px 6px; border-radius: 4px; }}
    .ponytail-badge {{ background: rgba(210, 153, 34, 0.15); border: 1px solid var(--accent-yellow); color: var(--accent-yellow); font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px; }}
    .verified-badge {{ background: rgba(63, 185, 80, 0.15); border: 1px solid var(--accent-green); color: var(--accent-green); font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px; }}
    .recipe-view-switcher {{
      display: flex;
      gap: 4px;
      margin-bottom: 8px;
    }}
    .recipe-tab-btn {{
      background: transparent;
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 11px;
      cursor: pointer;
    }}
    .recipe-tab-btn.active {{
      background: var(--accent-blue);
      border-color: var(--accent-blue);
      color: #fff;
    }}
    .diff-line-header {{ color: var(--text-muted); font-weight: 600; display: block; }}
    .diff-line-hunk {{ color: var(--accent-blue); background: rgba(88, 166, 255, 0.1); display: block; padding: 1px 4px; border-radius: 2px; }}
    .diff-line-add {{ color: #7ee787; background: rgba(46, 160, 67, 0.18); display: block; padding: 1px 4px; border-radius: 2px; }}
    .diff-line-del {{ color: #ffa198; background: rgba(248, 81, 73, 0.18); display: block; padding: 1px 4px; border-radius: 2px; }}
    .diff-line-ctx {{ color: var(--text-muted); display: block; padding: 1px 4px; }}
    body.light-theme .diff-line-add {{ color: #1a7f37; background: rgba(46, 160, 67, 0.15); }}
    body.light-theme .diff-line-del {{ color: #cf222e; background: rgba(207, 34, 46, 0.15); }}
    body.light-theme .diff-line-hunk {{ color: #0969da; background: rgba(9, 105, 218, 0.1); }}

    .recipe-split-container {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 12px;
    }}
    @media (max-width: 650px) {{ .recipe-split-container {{ grid-template-columns: 1fr; }} }}
    .split-pane .code-preview {{ margin-bottom: 0; min-height: 70px; }}
    .split-label {{ font-size: 11px; font-weight: 600; margin-bottom: 4px; }}
    .split-del {{ color: var(--accent-red); }}
    .split-add {{ color: var(--accent-green); }}
    .recipe-actions {{ display: flex; justify-content: space-between; align-items: center; margin-top: 8px; }}

    /* Advisory Items */
    .advisory-item {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 12px;
      margin-bottom: 10px;
    }}
    .advisory-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }}
    .advisory-mitigates {{ font-size: 11px; color: var(--accent-blue); margin-bottom: 4px; }}
    .advisory-desc {{ font-size: 12px; color: var(--text-main); margin-bottom: 4px; }}
    .advisory-guarantee {{ font-size: 11px; color: var(--text-muted); margin-bottom: 6px; }}

    .empty-state {{ text-align: center; padding: 20px; color: var(--text-muted); font-size: 13px; }}
    .empty-cell {{ text-align: center; color: var(--accent-green); padding: 24px; font-weight: 600; }}

    footer {{
      margin-top: 36px;
      text-align: center;
      color: var(--text-muted);
      font-size: 12px;
      border-top: 1px solid var(--border-subtle);
      padding-top: 18px;
    }}

    /* Print & PDF styling */
    @media print {{
      body {{ background: #fff !important; color: #000 !important; padding: 10px; }}
      .card, .owasp-card, .cluster-item, .defended-section, .table-container, .recipe-card, .advisory-item, .comp-card {{
        border: 1px solid #ccc !important;
        background: #fff !important;
        color: #000 !important;
        box-shadow: none !important;
      }}
      .header-actions, .filter-bar, .btn-copy, footer, .drawer-actions, .simulator-card, .recipe-view-switcher, .recipe-actions {{ display: none !important; }}
      .finding-row {{ background: #fff !important; color: #000 !important; }}
      .finding-title, .rule-id {{ color: #000 !important; }}
      .drawer-row {{ display: table-row !important; }}
      .drawer-content {{ background: #f6f8fa !important; border-left: 3px solid #000 !important; }}
      .code-preview {{ background: #eee !important; color: #000 !important; }}
      .code-preview code {{ color: #000 !important; }}
      .gauge-card {{ display: none !important; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="logo-group">
        <h1><span class="shield-icon">&#128737;</span> TorusGuard Security Report</h1>
        <div class="project-meta">
          <strong>{html.escape(telemetry.get('project_name', 'Project'))}</strong> &middot;
          {html.escape(stack_label)} &middot;
          {html.escape(telemetry.get('generated_at', ''))}
        </div>
      </div>
      <div class="header-actions">
        <button class="btn" id="themeToggleBtn" onclick="toggleTheme()">☀️ Light Mode</button>
        <button class="btn" onclick="downloadSarif()">&#128229; Export SARIF</button>
        <button class="btn" onclick="downloadCsv()">&#128202; Export CSV</button>
        <button class="btn" onclick="window.print()">&#128438; Print / PDF</button>
        <div class="status-badge {status_badge_class}">{status_label}</div>
      </div>
    </header>

    <!-- KPI Cards -->
    <div class="grid-kpi">
      <div class="card gauge-card">
        <div style="position: relative; display: flex; align-items: center; justify-content: center;">
          <svg class="gauge-svg" viewBox="0 0 100 100">
            <defs>
              <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{grad_start}" />
                <stop offset="100%" stop-color="{grad_end}" />
              </linearGradient>
              <filter id="gaugeGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="{glow_color}" flood-opacity="0.5"/>
              </filter>
            </defs>
            <circle class="gauge-bg" cx="50" cy="50" r="40" />
            <circle class="gauge-fill" id="gaugeCircleFill" cx="50" cy="50" r="40" stroke="url(#gaugeGradient)" filter="url(#gaugeGlow)" />
          </svg>
          <div class="gauge-value" id="postureScoreText">0</div>
        </div>
        <div class="stat-label" style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; margin-top: 10px;">Posture Score</div>
      </div>

      <div class="card sev-card" onclick="filterBySeverity('critical')">
        <div class="sev-count" style="color: var(--accent-red);">{crit_count}</div>
        <div class="sev-label">Critical Exposure</div>
      </div>

      <div class="card sev-card" onclick="filterBySeverity('high')">
        <div class="sev-count" style="color: var(--accent-orange);">{high_count}</div>
        <div class="sev-label">High Exposure</div>
      </div>

      <div class="card sev-card" onclick="filterBySeverity('medium')">
        <div class="sev-count" style="color: var(--accent-yellow);">{med_count}</div>
        <div class="sev-label">Medium / Low</div>
      </div>

      <div class="card sev-card" onclick="toggleDefendedSection()">
        <div class="sev-count" style="color: var(--accent-green);">{defended_count}<span style="font-size: 16px; color: var(--text-muted);">/{total_rules}</span></div>
        <div class="sev-label">Guards Defended</div>
      </div>
    </div>

    <!-- What-If Posture Score Simulator -->
    <div class="card simulator-card {'simulator-clean' if len(sorted_f) == 0 else ''}">
      <div>
        <div style="display: flex; align-items: center; gap: 8px;">
          <strong style="font-size: 13px;">⚡ Interactive "What-If" Posture Score Simulator</strong>
          <span class="badge badge-primary">Dynamic Recalculation</span>
        </div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">
          {'All 74 security invariants are currently defended. Simulator is ready for live remediation modeling during audit cycles.' if len(sorted_f) == 0 else 'Simulate applying governed patches to preview projected posture improvement in real time:'}
        </div>
      </div>
      <div class="sim-stats">
        <div>Current: <strong id="simCurrentVal">{score}</strong>/100</div>
        <div>&rarr;</div>
        <div>Projected: <strong id="simProjectedVal" style="color: var(--accent-blue);">{score}</strong>/100 <span id="simDeltaBadge" class="badge badge-success">+0 pts</span></div>
      </div>
      <div class="sim-actions">
        <button class="btn btn-sm" onclick="simulateFixAll('Critical')">&#9889; Simulate Criticals</button>
        <button class="btn btn-sm" onclick="simulateFixAll('all')">&#9889; Simulate All Fixes</button>
        <button class="btn btn-sm" onclick="resetSimulatedFixes()">Reset Simulator</button>
      </div>
    </div>

    <!-- Active Defenses & Protected Invariants (5-Layer Architectural Invariant Matrix) -->
    <div class="defended-section" id="defendedSection">
      <div class="defended-header" onclick="toggleDefendedVisibility()">
        <div class="section-title" style="margin-bottom: 0;">
          &#128737; Active Defenses &amp; Protected Invariants ({defended_count} Passing)
        </div>
        <span id="defendedToggleIcon" style="color: var(--text-muted); font-size: 12px;">&#9660; Collapse Matrix</span>
      </div>
      <div id="defendedMatrixBody">
        <div class="coverage-bar-container">
          <div class="coverage-stats">
            <span><strong>{defended_count} of {total_rules} Invariants Enforced</strong> ({coverage_pct}% Defense Coverage)</span>
            <span class="badge {'badge-success' if coverage_pct >= 90 else 'badge-high'}">{coverage_pct}% Enforced</span>
          </div>
          <div class="coverage-progress-bg">
            <div class="coverage-progress-fill" style="width: {coverage_pct}%;"></div>
          </div>
        </div>
        <div class="inv-search-bar">
          <div class="search-wrapper" style="width: 100%;">
            <input type="text" id="invSearchInput" class="search-input" style="width: 100%;" placeholder="Search 74 invariants by ID, title, layer, or keyword..." oninput="filterInvariants()">
            <button class="search-clear-btn" id="invSearchClearBtn" onclick="clearInvSearch()">&times;</button>
          </div>
          <div id="invMatchCount" style="font-size: 11px; color: var(--accent-blue); white-space: nowrap;"></div>
        </div>
        <div class="layers-container" id="layersList">
          {layers_html}
        </div>
      </div>
    </div>

    <!-- Filter & Search Bar for Findings -->
    <div class="filter-bar">
      <div class="filter-pills">
        <span class="pill-group-label">Severity:</span>
        <span class="pill active" data-sev-filter="all" onclick="filterBySeverity('all')">All</span>
        <span class="pill" data-sev-filter="critical" onclick="filterBySeverity('critical')">&#128308; Critical ({crit_count})</span>
        <span class="pill" data-sev-filter="high" onclick="filterBySeverity('high')">&#128992; High ({high_count})</span>
        <span class="pill" data-sev-filter="medium" onclick="filterBySeverity('medium')">&#128993; Med/Low ({med_count})</span>

        <span class="pill-group-label" style="margin-left: 8px;">Status:</span>
        <span class="pill active" data-status-filter="all" onclick="filterByStatus('all')">All</span>
        <span class="pill" data-status-filter="open" onclick="filterByStatus('open')">&#9888; Open ({open_count})</span>
        <span class="pill" data-status-filter="resolved" onclick="filterByStatus('resolved')">&#10004; Resolved ({resolved_count})</span>

        <span class="dir-filter-chip" id="dirFilterChip" onclick="clearDirectoryFilter()">
          Folder: <strong id="dirFilterName"></strong> &times;
        </span>
        <button class="btn-reset-filters" id="btnResetFilters" onclick="resetAllFilters()">&times; Reset Filters</button>
      </div>
      <div class="search-wrapper">
        <input type="text" id="searchInput" class="search-input" placeholder="Search rules, titles, files..." oninput="searchFindings()">
        <button class="search-clear-btn" id="searchClearBtn" onclick="clearSearch()">&times;</button>
      </div>
    </div>
    <div class="filter-stats-bar">
      <div>Showing <span id="visibleCount" style="font-weight: 700; color: var(--text-main);">{min(len(sorted_f), 50)}</span> of <span id="totalCount" style="font-weight: 700; color: var(--text-main);">{len(sorted_f)}</span> cataloged findings</div>
      <div id="activeFilterSummary" style="font-size: 11px; color: var(--accent-blue);"></div>
    </div>

    <!-- Findings Table -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th style="width: 70px; text-align: center;">Simulate</th>
            <th style="width: 110px;">Severity</th>
            <th style="width: 130px;">Rule ID</th>
            <th>Finding Title</th>
            <th style="width: 250px;">File &amp; Location</th>
            <th style="width: 90px;">Confidence</th>
            <th style="width: 30px;"></th>
          </tr>
        </thead>
        <tbody id="findingsTableBody">
          {findings_rows}
        </tbody>
      </table>
    </div>

    <!-- OWASP Top 10 Compliance Radar -->
    <div class="section-title">&#128737; OWASP Top 10 (2021/2026) Compliance Matrix</div>
    <div class="grid-owasp">
      {owasp_cards_html}
    </div>

    <!-- Enterprise Compliance Framework Mapping -->
    <div class="section-title">&#127963; Enterprise Compliance Framework Mapping (SOC 2 &middot; ISO 27001 &middot; HIPAA)</div>
    <div class="grid-compliance">
      {compliance_cards_html}
    </div>

    <!-- Middle Grid: Heatmap + Clusters -->
    <div class="grid-bottom">
      <div class="card">
        <div class="section-title">&#128293; Directory Attack Surface Heatmap</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">Click a folder to filter findings for that directory:</div>
        {heatmap_rows_html}
      </div>

      <div class="card">
        <div class="section-title">&#128736; Root-Cause Architectural Clusters</div>
        {clusters_html}
      </div>
    </div>

    <!-- Bottom Grid: Golden Recipes + Next Best Defenses -->
    <div class="grid-bottom">
      <div class="card">
        <div class="section-title">&#10024; Golden Fix Recipes ({len(recipes)})</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Verified remediation patterns distilled from applied patches:</div>
        <div class="filter-pills" style="margin-bottom: 12px;">
          {recipe_cat_pills_html}
        </div>
        <div id="recipeContainer">
          {recipes_html}
        </div>
      </div>

      <div class="card">
        <div class="section-title">&#128161; Next Best Defenses Advisory</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">Stack-tailored recommendations to achieve hardened posture:</div>
        {advisory_html}
      </div>
    </div>

    <footer>
      TorusGuard v1.3.6 &middot; Autonomous Security Engine for AI-Built Applications &middot; 100% Local-First &middot; Zero Cloud Telemetry
    </footer>
  </div>

  <!-- Invariant Inspection Modal -->
  <div id="invariantModal" class="modal-backdrop" style="display: none;" onclick="closeInvariantModal(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <div class="modal-header">
        <div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span id="modalInvSev" class="badge badge-medium">Medium</span>
            <code id="modalInvRule" class="rule-id" style="font-size: 14px;">TG-GEN</code>
            <span id="modalInvStatus" class="badge badge-success">Defended</span>
          </div>
          <h3 id="modalInvTitle" style="font-size: 16px; margin-top: 6px; color: var(--text-main);">Security Invariant</h3>
        </div>
        <button class="modal-close-btn" onclick="closeInvariantModal(event)">&times;</button>
      </div>
      <div class="modal-body">
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Architectural Layer &amp; Category</div>
          <div id="modalInvLayer" style="margin-top: 2px; font-weight: 500;">Application &amp; LLM Defense</div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Invariant Guarantee</div>
          <div id="modalInvGuarantee" style="margin-top: 4px; line-height: 1.4; color: var(--text-main);">
            Enforces deterministic verification without bypasses.
          </div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Ponytail Churn Invariant</div>
          <div style="margin-top: 2px; color: var(--accent-yellow); font-size: 12px;">
            &le; 35 additions, &le; 25 deletions per surgical patch bundle.
          </div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600; margin-bottom: 4px;">Governed CLI Command</div>
          <div class="cmd-box" id="modalInvCmd">
            <code>npx torusguard harden --rule TG-GEN</code>
            <button class="btn-copy" onclick="copyText('npx torusguard harden --rule TG-GEN', this)">&#128203; Copy</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const RAW_FINDINGS = {findings_json_str};
    const SARIF_RULES = {sarif_rules_json_str};
    const INVARIANT_CATALOG = {rule_catalog_json_str};
    const VIOLATED_RULE_IDS = {violated_ids_json_str};

    let currentSeverity = 'all';
    let currentStatus = 'all';
    let currentDirectory = '';
    let currentRecipeCategory = 'all';
    let BASE_POSTURE_SCORE = {score};

    // ── Theme Switcher ──
    function initTheme() {{
      const saved = localStorage.getItem('tg_theme');
      const btn = document.getElementById('themeToggleBtn');
      if (saved === 'light') {{
        document.body.classList.add('light-theme');
        if (btn) btn.innerHTML = '&#127769; Dark Mode';
      }} else {{
        document.body.classList.remove('light-theme');
        if (btn) btn.innerHTML = '&#9728;&#65039; Light Mode';
      }}
    }}

    function toggleTheme() {{
      const isLight = document.body.classList.toggle('light-theme');
      localStorage.setItem('tg_theme', isLight ? 'light' : 'dark');
      const btn = document.getElementById('themeToggleBtn');
      if (btn) btn.innerHTML = isLight ? '&#127769; Dark Mode' : '&#9728;&#65039; Light Mode';
    }}

    document.addEventListener('DOMContentLoaded', initTheme);
    if (document.readyState === 'complete' || document.readyState === 'interactive') {{
      initTheme();
    }}

    // ── What-If Posture Score Simulator ──
    function updateSimulatedScore() {{
      const checkboxes = document.querySelectorAll('.sim-fix-chk');
      const fixedIds = new Set();
      checkboxes.forEach(cb => {{
        if (cb.checked) {{
          fixedIds.add(cb.getAttribute('data-finding-id'));
        }}
      }});

      let remCrit = 0, remHigh = 0, remMed = 0, remLow = 0;
      RAW_FINDINGS.forEach(f => {{
        if (f.is_canary) return;
        if (fixedIds.has(f.finding_id)) return; // Simulated as fixed
        const s = f.severity;
        if (s === 'Critical') remCrit++;
        else if (s === 'High') remHigh++;
        else if (s === 'Medium') remMed++;
        else if (s === 'Low') remLow++;
      }});

      const penalty = (remCrit * 25) + (remHigh * 15) + (remMed * 5) + (remLow * 2);
      const newScore = Math.max(0, Math.min(100, 100 - penalty));

      // Update projected UI labels
      const projEl = document.getElementById('simProjectedVal');
      const deltaEl = document.getElementById('simDeltaBadge');
      if (projEl) projEl.textContent = newScore;
      const delta = newScore - BASE_POSTURE_SCORE;
      if (deltaEl) {{
        deltaEl.textContent = (delta >= 0 ? '+' : '') + delta + ' pts';
        deltaEl.className = 'badge ' + (delta > 0 ? 'badge-success' : 'badge-primary');
      }}

      // Animate SVG gauge to simulated score
      animateGaugeTo(newScore);
    }}

    function simulateFixAll(sev) {{
      const checkboxes = document.querySelectorAll('.sim-fix-chk');
      checkboxes.forEach(cb => {{
        const cbSev = cb.getAttribute('data-severity');
        if (sev === 'all' || cbSev === sev) {{
          cb.checked = true;
        }}
      }});
      updateSimulatedScore();
    }}

    function resetSimulatedFixes() {{
      const checkboxes = document.querySelectorAll('.sim-fix-chk');
      checkboxes.forEach(cb => {{ cb.checked = false; }});
      updateSimulatedScore();
    }}

    function animateGaugeTo(targetScore) {{
      const circumference = 251.2;
      const targetOffset = circumference - (circumference * (targetScore / 100.0));
      const gaugeEl = document.getElementById('gaugeCircleFill');
      const textEl = document.getElementById('postureScoreText');

      if (gaugeEl) {{
        gaugeEl.style.strokeDashoffset = targetOffset;
      }}
      if (textEl) {{
        textEl.textContent = targetScore;
      }}
    }}

    // ── Invariant Matrix Filters & Inspection ──
    function filterInvariants() {{
      const input = document.getElementById('invSearchInput');
      const clearBtn = document.getElementById('invSearchClearBtn');
      const q = (input ? input.value : '').toLowerCase().trim();
      if (clearBtn) clearBtn.style.display = q ? 'block' : 'none';

      const chips = document.querySelectorAll('.inv-chip');
      let matchCount = 0;
      chips.forEach(chip => {{
        const s = chip.getAttribute('data-search') || '';
        const visible = !q || s.includes(q);
        chip.style.display = visible ? 'inline-flex' : 'none';
        if (visible) matchCount++;
      }});

      const countEl = document.getElementById('invMatchCount');
      if (countEl) {{
        countEl.textContent = q ? '(' + matchCount + ' matching)' : '';
      }}
    }}

    function clearInvSearch() {{
      const input = document.getElementById('invSearchInput');
      if (input) input.value = '';
      filterInvariants();
    }}

    function inspectInvariant(ruleId) {{
      const item = INVARIANT_CATALOG[ruleId];
      if (!item) return;
      const modal = document.getElementById('invariantModal');
      const isViolated = VIOLATED_RULE_IDS.includes(ruleId);

      document.getElementById('modalInvRule').textContent = item.rule_id;
      document.getElementById('modalInvTitle').textContent = item.title;
      document.getElementById('modalInvLayer').textContent = item.layer_name + ' &middot; ' + item.category;
      document.getElementById('modalInvGuarantee').textContent = item.guarantee;

      const sevEl = document.getElementById('modalInvSev');
      sevEl.textContent = item.severity;
      sevEl.className = 'badge ' + (item.severity === 'Critical' ? 'badge-critical' : (item.severity === 'High' ? 'badge-high' : 'badge-medium'));

      const statusEl = document.getElementById('modalInvStatus');
      statusEl.innerHTML = isViolated ? '&#9888; Violated' : '&#10004; Defended';
      statusEl.className = 'badge ' + (isViolated ? 'badge-critical' : 'badge-success');

      const cmdBox = document.getElementById('modalInvCmd');
      cmdBox.innerHTML = `<code>npx torusguard harden --rule ${{item.rule_id}}</code>
        <button class="btn-copy" onclick="copyText('npx torusguard harden --rule ${{item.rule_id}}', this); event.stopPropagation();">&#128203; Copy</button>`;

      if (modal) modal.style.display = 'flex';
    }}

    function closeInvariantModal(e) {{
      const modal = document.getElementById('invariantModal');
      if (modal) modal.style.display = 'none';
    }}

    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') closeInvariantModal();
    }});

    // ── Golden Recipes View Switcher & Category Filter ──
    function setRecipeView(recipeId, viewMode) {{
      const diffView = document.getElementById('recipe-view-diff-' + recipeId);
      const splitView = document.getElementById('recipe-view-split-' + recipeId);
      const btnDiff = document.getElementById('btn-view-diff-' + recipeId);
      const btnSplit = document.getElementById('btn-view-split-' + recipeId);

      if (viewMode === 'diff') {{
        if (diffView) diffView.style.display = 'block';
        if (splitView) splitView.style.display = 'none';
        if (btnDiff) btnDiff.classList.add('active');
        if (btnSplit) btnSplit.classList.remove('active');
      }} else {{
        if (diffView) diffView.style.display = 'none';
        if (splitView) splitView.style.display = 'grid';
        if (btnDiff) btnDiff.classList.remove('active');
        if (btnSplit) btnSplit.classList.add('active');
      }}
    }}

    function filterRecipeCategory(cat) {{
      currentRecipeCategory = cat;
      document.querySelectorAll('[data-recipe-cat-filter]').forEach(p => {{
        if (p.getAttribute('data-recipe-cat-filter') === cat) p.classList.add('active');
        else p.classList.remove('active');
      }});

      document.querySelectorAll('.recipe-card').forEach(card => {{
        const cardCat = card.getAttribute('data-category') || '';
        if (cat === 'all' || cardCat === cat) {{
          card.style.display = '';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    // ── Findings Filtering & Drawer Lifecycle ──
    function filterBySeverity(sev) {{
      currentSeverity = sev;
      document.querySelectorAll('[data-sev-filter]').forEach(p => {{
        if (p.getAttribute('data-sev-filter') === sev) p.classList.add('active');
        else p.classList.remove('active');
      }});
      searchFindings();
    }}

    function filterByStatus(status) {{
      currentStatus = status;
      document.querySelectorAll('[data-status-filter]').forEach(p => {{
        if (p.getAttribute('data-status-filter') === status) p.classList.add('active');
        else p.classList.remove('active');
      }});
      searchFindings();
    }}

    function filterFindings(sev) {{
      filterBySeverity(sev);
    }}

    function filterByDirectory(dir) {{
      currentDirectory = dir.replace(/\\/$/, '');
      const chip = document.getElementById('dirFilterChip');
      const chipName = document.getElementById('dirFilterName');
      if (chip && chipName) {{
        chipName.textContent = currentDirectory;
        chip.style.display = 'inline-flex';
      }}
      searchFindings();
    }}

    function clearDirectoryFilter() {{
      currentDirectory = '';
      const chip = document.getElementById('dirFilterChip');
      if (chip) chip.style.display = 'none';
      searchFindings();
    }}

    function clearSearch() {{
      const searchInput = document.getElementById('searchInput');
      if (searchInput) searchInput.value = '';
      searchFindings();
    }}

    function resetAllFilters() {{
      currentSeverity = 'all';
      currentStatus = 'all';
      currentDirectory = '';
      const searchInput = document.getElementById('searchInput');
      if (searchInput) searchInput.value = '';

      document.querySelectorAll('[data-sev-filter]').forEach(p => {{
        if (p.getAttribute('data-sev-filter') === 'all') p.classList.add('active');
        else p.classList.remove('active');
      }});
      document.querySelectorAll('[data-status-filter]').forEach(p => {{
        if (p.getAttribute('data-status-filter') === 'all') p.classList.add('active');
        else p.classList.remove('active');
      }});
      const chip = document.getElementById('dirFilterChip');
      if (chip) chip.style.display = 'none';

      searchFindings();
    }}

    function toggleDefendedVisibility() {{
      const body = document.getElementById('defendedMatrixBody');
      const icon = document.getElementById('defendedToggleIcon');
      if (!body) return;
      if (body.style.display === 'none') {{
        body.style.display = 'block';
        icon.innerHTML = '&#9660; Collapse Matrix';
      }} else {{
        body.style.display = 'none';
        icon.innerHTML = '&#9654; Expand Matrix';
      }}
    }}

    function toggleDefendedSection() {{
      const sec = document.getElementById('defendedSection');
      if (sec) sec.scrollIntoView({{ behavior: 'smooth' }});
    }}

    function searchFindings() {{
      const searchInput = document.getElementById('searchInput');
      const clearBtn = document.getElementById('searchClearBtn');
      const query = (searchInput ? searchInput.value : '').toLowerCase().trim();

      if (clearBtn) clearBtn.style.display = query ? 'block' : 'none';

      const rows = document.querySelectorAll('.finding-row');
      let visibleCount = 0;

      rows.forEach(r => {{
        const rSev = r.getAttribute('data-severity') || '';
        const rStatus = r.getAttribute('data-status') || 'open';
        const rSearch = r.getAttribute('data-search') || '';
        const rPath = r.getAttribute('data-path') || '';
        const drawerId = r.getAttribute('data-drawer-id');
        const drawer = document.getElementById(drawerId);

        let matchSev = (currentSeverity === 'all') || (rSev === currentSeverity);
        if (currentSeverity === 'medium') {{
          matchSev = (rSev === 'medium' || rSev === 'low');
        }}

        let matchStatus = (currentStatus === 'all') || (rStatus === currentStatus);

        let matchDir = true;
        if (currentDirectory) {{
          matchDir = rPath.toLowerCase().startsWith(currentDirectory.toLowerCase());
        }}

        const matchQuery = !query || rSearch.includes(query);
        const visible = matchSev && matchStatus && matchDir && matchQuery;

        if (visible) visibleCount++;
        r.style.display = visible ? '' : 'none';
        if (drawer && !visible) {{
          drawer.style.display = 'none';
          r.classList.remove('expanded');
        }}
      }});

      const countEl = document.getElementById('visibleCount');
      if (countEl) countEl.textContent = visibleCount;

      const resetBtn = document.getElementById('btnResetFilters');
      const hasActiveFilters = currentSeverity !== 'all' || currentStatus !== 'all' || currentDirectory !== '' || query !== '';
      if (resetBtn) {{
        resetBtn.style.display = hasActiveFilters ? 'inline-block' : 'none';
      }}

      const summaryEl = document.getElementById('activeFilterSummary');
      if (summaryEl) {{
        const parts = [];
        if (currentSeverity !== 'all') parts.push(`Sev: ${{currentSeverity}}`);
        if (currentStatus !== 'all') parts.push(`Status: ${{currentStatus}}`);
        if (currentDirectory) parts.push(`Dir: ${{currentDirectory}}`);
        if (query) parts.push(`Query: "${{query}}"`);
        summaryEl.textContent = parts.length ? `(${{parts.join(', ')}})` : '';
      }}
    }}

    function initPostureGauge() {{
      const targetScore = {score};
      const circumference = 251.2;
      const targetOffset = circumference - (circumference * (targetScore / 100.0));
      const gaugeEl = document.getElementById('gaugeCircleFill');
      const textEl = document.getElementById('postureScoreText');

      setTimeout(() => {{
        if (gaugeEl) {{
          gaugeEl.style.strokeDashoffset = targetOffset;
        }}
      }}, 50);

      if (textEl) {{
        const duration = 800;
        const startTime = performance.now();
        function updateCount(now) {{
          const elapsed = now - startTime;
          const progress = Math.min(elapsed / duration, 1.0);
          const eased = 1 - Math.pow(1 - progress, 3);
          const val = Math.round(eased * targetScore);
          textEl.textContent = val;
          if (progress < 1.0) {{
            requestAnimationFrame(updateCount);
          }} else {{
            textEl.textContent = targetScore;
          }}
        }}
        requestAnimationFrame(updateCount);
      }}
    }}
    document.addEventListener('DOMContentLoaded', initPostureGauge);
    if (document.readyState === 'complete' || document.readyState === 'interactive') {{
      initPostureGauge();
    }}

    function toggleDrawer(row) {{
      const drawerId = row.getAttribute('data-drawer-id');
      const drawer = document.getElementById(drawerId);
      if (!drawer) return;

      const isExpanded = row.classList.contains('expanded');
      if (isExpanded) {{
        row.classList.remove('expanded');
        drawer.style.display = 'none';
      }} else {{
        row.classList.add('expanded');
        drawer.style.display = '';
      }}
    }}

    function copyText(text, btn) {{
      const cleanText = text.replace(/\\\\n/g, '\\n');
      if (navigator.clipboard && window.isSecureContext) {{
        navigator.clipboard.writeText(cleanText).then(() => {{
          showCopied(btn);
        }}).catch(() => {{
          fallbackCopy(cleanText, btn);
        }});
      }} else {{
        fallbackCopy(cleanText, btn);
      }}
    }}

    function fallbackCopy(text, btn) {{
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try {{
        document.execCommand('copy');
        showCopied(btn);
      }} catch (e) {{}}
      document.body.removeChild(ta);
    }}

    function showCopied(btn) {{
      const orig = btn.innerHTML;
      btn.innerHTML = '&#10004; Copied!';
      btn.classList.add('copied');
      setTimeout(() => {{
        btn.innerHTML = orig;
        btn.classList.remove('copied');
      }}, 2000);
    }}

    function downloadSarif() {{
      const sarifData = {{
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{{
          "tool": {{
            "driver": {{
              "name": "TorusGuard",
              "semanticVersion": "1.3.6",
              "informationUri": "https://github.com/githubmofo/TorusGuard",
              "rules": SARIF_RULES
            }}
          }},
          "results": RAW_FINDINGS.map(f => ({{
            "ruleId": f.rule_id || "TG-GEN",
            "message": {{ "text": f.description || f.title || "Violation" }},
            "level": f.severity === "Critical" ? "error" : (f.severity === "High" ? "error" : "warning"),
            "locations": [{{
              "physicalLocation": {{
                "artifactLocation": {{ "uri": f.file_path || "unknown" }},
                "region": {{ "startLine": f.line_number || 1 }}
              }}
            }}]
          }}))
        }}]
      }};

      const blob = new Blob([JSON.stringify(sarifData, null, 2)], {{ type: "application/json" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "torusguard-report.sarif";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}

    function downloadCsv() {{
      let csv = "Finding ID,Rule ID,Severity,Title,File Path,Line Number,Confidence\\n";
      RAW_FINDINGS.forEach(f => {{
        const row = [
          `"${{(f.finding_id || '').replace(/"/g, '""')}}"`,
          `"${{(f.rule_id || '').replace(/"/g, '""')}}"`,
          `"${{(f.severity || '').replace(/"/g, '""')}}"`,
          `"${{(f.title || '').replace(/"/g, '""')}}"`,
          `"${{(f.file_path || '').replace(/"/g, '""')}}"`,
          f.line_number || 0,
          f.confidence_score || 70
        ];
        csv += row.join(",") + "\\n";
      }});

      const blob = new Blob([csv], {{ type: "text/csv;charset=utf-8;" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "torusguard-report.csv";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}
  </script>
</body>
</html>
"""


def emit_html_report(
    target_path: str | Path | None = None,
    root_dir: str | Path | None = None
) -> dict[str, Any]:
    """Emit the standalone HTML report to disk using atomic swapping with retry."""
    root = Path(root_dir or find_project_root()).resolve()
    telemetry = load_report_telemetry(root)
    html_content = generate_html_dashboard(telemetry)
    if target_path:
        out_file = Path(target_path)
        if not out_file.is_absolute():
            out_file = (root / out_file).resolve()
    else:
        out_file = root / "report.html"

    out_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        from report_sync import atomic_write_text
        atomic_write_text(out_file, html_content)
    except Exception:
        out_file.write_text(html_content, encoding="utf-8")

    # Always mirror to .torusguard/runs/report-latest.html
    latest_run_html = root / ".torusguard" / "runs" / "report-latest.html"
    if out_file.resolve() != latest_run_html.resolve():
        try:
            latest_run_html.parent.mkdir(parents=True, exist_ok=True)
            from report_sync import atomic_write_text
            atomic_write_text(latest_run_html, html_content)
        except Exception:
            try:
                latest_run_html.write_text(html_content, encoding="utf-8")
            except Exception:
                pass

    # If writing to a non-standard path and a root report.html exists, also keep it synchronized
    root_report = root / "report.html"
    if out_file.resolve() != root_report.resolve() and root_report.is_file():
        try:
            from report_sync import atomic_write_text
            atomic_write_text(root_report, html_content)
        except Exception:
            try:
                root_report.write_text(html_content, encoding="utf-8")
            except Exception:
                pass

    all_rules = telemetry.get("all_rules", [])
    safe_rules = telemetry.get("safe_rules", [])
    violated_rules = telemetry.get("violated_rules", [])
    findings = telemetry.get("findings", [])

    return {
        "status": "success",
        "report_path": str(out_file),
        "latest_mirror_path": str(latest_run_html),
        "file_size_bytes": len(html_content.encode("utf-8")),
        "posture_score": compute_posture_score(telemetry),
        "total_rules": len(all_rules),
        "defended_count": len(safe_rules),
        "harmed_count": len(violated_rules),
        "critical_count": sum(1 for f in findings if f.get("severity") == "Critical" and not f.get("is_canary")),
        "high_count": sum(1 for f in findings if f.get("severity") == "High" and not f.get("is_canary")),
        "medium_count": sum(1 for f in findings if f.get("severity") in ("Medium", "Low") and not f.get("is_canary")),
    }


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Visual HTML Report Emitter")
    parser.add_argument("--out", help="Output HTML file path (default: report.html at project root)")
    parser.add_argument("--root", help="Project root override")
    parser.add_argument("--json", action="store_true", help="Output raw JSON summary")

    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else None

    res = emit_html_report(target_path=args.out, root_dir=root)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        rep_path = Path(res["report_path"]).resolve()
        file_url = rep_path.as_uri()
        score = res["posture_score"]
        score_label = "Optimal Defense" if score >= 90 else ("Hardened" if score >= 75 else ("Degraded" if score >= 50 else "Critical Exposure"))
        score_color = "\033[32m" if score >= 90 else ("\033[36m" if score >= 75 else ("\033[33m" if score >= 50 else "\033[31m"))
        reset = "\033[0m"
        bold = "\033[1m"
        white = "\033[97m"
        cyan = "\033[36m"
        dim = "\033[2m"
        green = "\033[32m"
        red = "\033[31m"
        yellow = "\033[33m"

        try:
            import term_ui as tui
            print()
            print(tui.card_header("🛡️  TORUSGUARD VISUAL SECURITY REPORT", "Single-File Offline Dashboard", "v2.3.0"))
            print(f"\n  {bold}▸ Report URL:{reset}       {cyan}{file_url}{reset}")
            print(f"  {bold}▸ Output File:{reset}      {white}{rep_path.name}{reset}")
            print(f"  {bold}▸ Living Ledger:{reset}    {green}security_report.md{reset}\n")

            print(tui.card_border_top("Executive Posture"))
            print(tui.format_box_line(f"Posture Score:     {bold}{score_color}{score}/100{reset} ({score_label})"))
            harmed = res.get("harmed_count", 0)
            defended = res.get("defended_count", 74)
            total = res.get("total_rules", 74)
            harmed_color = red if harmed > 0 else green
            print(tui.format_box_line(f"Invariants:        {green}{defended} Defended{reset} · {harmed_color}{harmed} Harmed{reset} ({total} Rules)"))
            findings_str = f"{red}{res.get('critical_count', 0)} Critical{reset} · {yellow}{res.get('high_count', 0)} High{reset} · {cyan}{res.get('medium_count', 0)} Medium{reset}"
            print(tui.format_box_line(f"Exposure Status:   {findings_str}"))
            print(tui.format_box_line(f"Dashboard Size:    {white}{res['file_size_bytes']} bytes{reset} (Zero CDN, 100% Offline)"))
            print(tui.card_divider("Interactive Capabilities"))
            print(tui.format_box_line("• 5-Layer Architectural Invariant Matrix with modal inspection"))
            print(tui.format_box_line("• Interactive What-If Posture Simulator with live gauge updates"))
            print(tui.format_box_line("• Enterprise Compliance Framework Mapping (SOC 2, ISO, HIPAA)"))
            print(tui.format_box_line("• Golden Recipe Explorer with Unified Diff & Before/After views"))
            print(tui.format_box_line("• Zero-CDN Executive Dark / Light Mode Theme Switcher"))
            print(tui.card_border_bottom())
            print(f"\n  {dim}Tip: Open {cyan}{file_url}{dim} directly in any browser to inspect.{reset}\n")
        except Exception:
            print(f"[SUCCESS] Emitted TorusGuard visual dashboard: {res['report_path']}")
            print(f"Posture Score: {res['posture_score']}/100 · Size: {res['file_size_bytes']} bytes")


if __name__ == "__main__":
    main()
