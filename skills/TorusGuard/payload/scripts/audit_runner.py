#!/usr/bin/env python3
"""
TorusGuard Autonomous Static Security Audit Engine (v1.3.5)
Multi-language static pattern & AST security scanner.
Evaluates source trees against canonical TorusGuard rule families,
augments confidence via the persistent security memory subsystem,
groups findings into root-cause clusters, and emits isolated run folders.

Pure Python 3.10+ standard library (zero external dependencies).
"""

import sys
import os
import re
import json
import hashlib
import argparse
import datetime
import unicodedata
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, TypedDict, Pattern

# Windows console UTF-8 support
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        getattr(sys.stderr, "reconfigure")(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ─── Timezone Configuration: Indian Standard Time (IST, UTC+05:30) ───────────
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30), name="IST")

def get_ist_now() -> datetime.datetime:
    """Return timezone-aware datetime strictly in Indian Standard Time (IST)."""
    return datetime.datetime.now(IST)

# ─── UI Formatter Bridge ──────────────────────────────────────────────────────
scripts_dir = Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

try:
    import term_ui as tui
    BOLD = tui.BOLD
    DIM = tui.DIM
    RESET = tui.RESET
    CYAN = tui.CYAN
    GREEN = tui.GREEN
    YELLOW = tui.YELLOW
    WHITE = tui.WHITE
    GRAY = tui.GRAY
    RED = tui.RED
    MAGENTA = tui.MAGENTA
    format_box_line = tui.format_box_line
    card_border_top = tui.card_border_top
    card_border_bottom = tui.card_border_bottom
    card_divider = tui.card_divider
    card_header = tui.card_header
    truncate_visual = tui.truncate_visual
    get_visual_width = tui.get_visual_width
except Exception:
    # Standalone fallback
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    ANSI_REGEX = re.compile(r'\x1b\[[0-9;]*m|\033\[[0-9;]*m')
    def strip_ansi(text: str) -> str: return ANSI_REGEX.sub('', text)
    def get_visual_width(text: str) -> int:
        clean = strip_ansi(text)
        w = 0
        for ch in clean:
            cp = ord(ch)
            if (0xFE00 <= cp <= 0xFE0F) or cp in (0x200B, 0x200C, 0x200D, 0x00AD): continue
            ea = unicodedata.east_asian_width(ch)
            w += 2 if (ea in ('W', 'F') or cp >= 0x1F300) else 1
        return w
    def truncate_visual(text: str, max_w: int = 67) -> str:
        if get_visual_width(text) <= max_w: return text
        return text[:max_w-3] + "..."
    def format_box_line(content: str, width: int = 67, border: str = "│", border_color: str = CYAN) -> str:
        trunc = truncate_visual(content, width)
        vis = get_visual_width(trunc)
        pad = " " * max(0, width - vis)
        return f"  {border_color}{border}{RESET}  {trunc}{pad}  {border_color}{border}{RESET}"
    def card_border_top(title: str = "", border_color: str = CYAN, double: bool = False) -> str:
        left = "╔" if double else "┌"
        right = "╗" if double else "┐"
        h = "═" if double else "─"
        if title:
            vis = get_visual_width(title)
            rem = max(0, 68 - vis)
            return f"  {border_color}{left}{h} {BOLD}{WHITE}{title}{RESET}{border_color} {h * rem}{right}{RESET}"
        return f"  {border_color}{left}{h * 71}{right}{RESET}"
    def card_border_bottom(border_color: str = CYAN, double: bool = False) -> str:
        left = "╚" if double else "└"
        right = "╝" if double else "┘"
        h = "═" if double else "─"
        return f"  {border_color}{left}{h * 71}{right}{RESET}"
    def card_divider(title: str = "", border_color: str = CYAN, double: bool = False) -> str:
        left = "╠" if double else "├"
        right = "╣" if double else "┤"
        h = "═" if double else "─"
        if title:
            vis = get_visual_width(title)
            rem = max(0, 68 - vis)
            return f"  {border_color}{left}{h} {BOLD}{WHITE}{title}{RESET}{border_color} {h * rem}{right}{RESET}"
        return f"  {border_color}{left}{h * 71}{right}{RESET}"
    def card_header(title: str, subtitle: str = "", version: str = "v1.3.5", border_color: str = CYAN) -> str:
        top = f"  {border_color}╭{'─' * 71}╮{RESET}"
        bottom = f"  {border_color}╰{'─' * 71}╯{RESET}"
        empty = f"  {border_color}│{' ' * 71}│{RESET}"
        space_count = max(1, 67 - get_visual_width(title) - get_visual_width(version))
        t_str = f"{BOLD}{WHITE}{title}{RESET}{' ' * space_count}{GRAY}{version}{RESET}"
        lines = [top, empty, format_box_line(t_str, 67, '│', border_color)]
        if subtitle: lines.append(format_box_line(f"{DIM}{subtitle}{RESET}", 67, '│', border_color))
        lines.extend([empty, bottom])
        return "\n".join(lines)

# ─── Rule Definitions & Sinks ─────────────────────────────────────────────────
class RulePattern(TypedDict):
    rule_id: str
    title: str
    severity: str
    category: str
    cluster: str
    patterns: List[Tuple[Pattern[str], str]]


RULE_PATTERNS: List[RulePattern] = [
    # ── TG-SEC ───────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-SEC-001",
        "title": "Hardcoded Secret or API Key in Tracked Source",
        "severity": "Critical",
        "category": "secrets",
        "cluster": "cluster-credentials-exposure",
        "patterns": [
            (re.compile(r'\b(?:sk_live|ak_live)_[0-9a-zA-Z]{20,}\b'), "Live payment or cloud API secret key"),
            (re.compile(r'\bgh[pousr]_[0-9a-zA-Z]{36}\b'), "GitHub personal access token"),
            (re.compile(r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----'), "Hardcoded private key block"),
            (re.compile(r'\b(?:jwt_secret|jwtSecret|JWT_SECRET)\s*[:=]\s*["\'][a-zA-Z0-9_\-]{16,}["\']'), "Hardcoded JWT signing secret"),
            (re.compile(r'(?:password|passwd|api_key|apiKey|secret_key)\s*[:=]\s*["\'][A-Za-z0-9@#$%^&+=_\-]{10,}["\']', re.IGNORECASE), "Hardcoded credential or API secret string"),
            (re.compile(r'\bxox[baprs]-[0-9a-zA-Z]{10,48}\b'), "Slack API or Bot token"),
            (re.compile(r'\bSG\.[0-9a-zA-Z_\-]{22}\.[0-9a-zA-Z_\-]{43}\b'), "SendGrid API token")
        ]
    },
    {
        "rule_id": "TG-SEC-002",
        "title": "Public Client Environment Variable Secret Exposure",
        "severity": "Critical",
        "category": "secrets",
        "cluster": "cluster-credentials-exposure",
        "patterns": [
            (re.compile(r'\b(?:NEXT_PUBLIC_|VITE_|REACT_APP_)[A-Z0-9_]*(?:SECRET|PRIVATE|KEY|PASSWORD|TOKEN)\b'), "Client-exposed environment variable containing secret naming pattern")
        ]
    },
    {
        "rule_id": "TG-SEC-003",
        "title": "Tracked Environment File",
        "severity": "High",
        "category": "secrets",
        "cluster": "cluster-credentials-exposure",
        "patterns": [
            (re.compile(r'(?:DATABASE_URL|POSTGRES_PASSWORD|MYSQL_PWD|AWS_SECRET_ACCESS_KEY)\s*=\s*["\']?[^\s"\'#]+["\']?'), "Sensitive production credentials stored in tracked environment configuration")
        ]
    },
    {
        "rule_id": "TG-SEC-004",
        "title": "Sensitive Information in Logs",
        "severity": "Medium",
        "category": "secrets",
        "cluster": "cluster-credentials-exposure",
        "patterns": [
            (re.compile(r'(?:console\.log|logger\.(?:info|debug|error|warn)|logging\.(?:info|debug|error))\s*\([^)]*(?:password|token|secret|apiKey|api_key)[^)]*\)', re.IGNORECASE), "Plaintext credential or token logged to output sink")
        ]
    },
    {
        "rule_id": "TG-SEC-005",
        "title": "Secret in Git History or Query URL",
        "severity": "Critical",
        "category": "secrets",
        "cluster": "cluster-credentials-exposure",
        "patterns": [
            (re.compile(r'[?&](?:token|access_token|api_key|apiKey|secret|password)=[a-zA-Z0-9_\-\.]{8,}', re.IGNORECASE), "Sensitive credential passed via cleartext URL query parameter")
        ]
    },
    {
        "rule_id": "TG-SEC-006",
        "title": "Secret in Build Artifact or Container Layer",
        "severity": "Critical",
        "category": "secrets",
        "cluster": "cluster-credentials-exposure",
        "patterns": [
            (re.compile(r'(?:ENV|ARG)\s+(?:[A-Z0-9_]*SECRET[A-Z0-9_]*|[A-Z0-9_]*KEY[A-Z0-9_]*|PASSWORD)\s*=\s*["\']?[a-zA-Z0-9_\-]{8,}["\']?', re.IGNORECASE), "Hardcoded build secret baked into Docker or container image layer")
        ]
    },
    {
        "rule_id": "TG-SEC-007",
        "title": "Secret in Test or Example Fixture Without Mock Marker",
        "severity": "Critical",
        "category": "secrets",
        "cluster": "cluster-credentials-exposure",
        "patterns": [
            (re.compile(r'(?:AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16})'), "Live AWS access key ID in source or fixture code")
        ]
    },

    # ── TG-AUTH ──────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-AUTH-001",
        "title": "Weak Password Storage or Deprecated Hashing",
        "severity": "Critical",
        "category": "auth",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'\b(?:hashlib\.md5|hashlib\.sha1|createHash\(["\']md5["\']\)|createHash\(["\']sha1["\']\))\s*\([^)]*password', re.IGNORECASE), "Cryptographically broken hash function (MD5/SHA1) used for password processing")
        ]
    },
    {
        "rule_id": "TG-AUTH-002",
        "title": "Client-Only Authorization Enforcement",
        "severity": "High",
        "category": "auth",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'if\s*\(\s*(?:!user\.isAdmin|user\.role\s*!==\s*["\']admin["\'])\s*\)\s*(?:return|history\.push|navigate)', re.IGNORECASE), "Client-only role authorization without guaranteed backend enforcement")
        ]
    },
    {
        "rule_id": "TG-AUTH-003",
        "title": "Missing Object-Level Authorization (IDOR)",
        "severity": "High",
        "category": "auth",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'jwt\.verify\s*\(\s*[a-zA-Z0-9_$.\s,]+,\s*[a-zA-Z0-9_$.\s,]+\s*\)(?!\s*,\s*\{[^}]*algorithms)', re.IGNORECASE), "JWT verification missing explicit algorithms restriction parameter")
        ]
    },
    {
        "rule_id": "TG-AUTH-004",
        "title": "Insecure Session Cookie Configuration",
        "severity": "High",
        "category": "auth",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'\bSESSION_COOKIE_SECURE\s*=\s*False\b'), "Session cookie secure flag disabled in Django settings"),
            (re.compile(r'\bsecure\s*:\s*false\b', re.IGNORECASE), "Cookie secure attribute set to false"),
            (re.compile(r'\bhttpOnly\s*:\s*false\b', re.IGNORECASE), "Cookie httpOnly attribute set to false (XSS readable)"),
            (re.compile(r'@(?:csrf_exempt|allow_anonymous)\b'), "Decorator disabling route-level authentication or CSRF protection"),
            (re.compile(r'\[(?:AllowAnonymous)\]'), "Attribute disabling ASP.NET authentication"),
            (re.compile(r'\.csrf\(\)\.disable\(\)'), "Spring Security CSRF protection explicitly disabled")
        ]
    },
    {
        "rule_id": "TG-AUTH-005",
        "title": "Unsafe Password Reset Token Generation",
        "severity": "High",
        "category": "auth",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'(?:token|resetCode|resetToken)\s*=\s*(?:Math\.random\(\)|random\.randint\(1000|random\.random\(\))', re.IGNORECASE), "Weak pseudorandom generator used for password reset token or OTP")
        ]
    },
    {
        "rule_id": "TG-AUTH-006",
        "title": "Mass Assignment & Privilege Escalation via Payloads",
        "severity": "Critical",
        "category": "auth",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'(?:User\.create|User\.update|user\.update)\s*\(\s*(?:req\.body|request\.data)\s*\)'), "Direct mass assignment of unverified request body onto user model")
        ]
    },
    {
        "rule_id": "TG-AUTH-007",
        "title": "Missing Object-Level and Property-Level Authorization (IDOR)",
        "severity": "Critical",
        "category": "auth",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'(?:db\.[a-zA-Z]+\.find(?:One)?|Model\.find(?:One)?)\s*\(\s*\{\s*_?id\s*:\s*(?:req\.params|req\.query)\.id\s*\}\s*\)'), "Direct database lookup by user-controlled ID without tenant or ownership check")
        ]
    },
    {
        "rule_id": "TG-AUTH-008",
        "title": "Untrusted Role or Tenant Header Injection",
        "severity": "Critical",
        "category": "auth",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'(?:req\.headers|request\.headers)\s*\[?\s*["\']x-(?:user-role|role|is-admin|tenant-id)["\']\s*\]?', re.IGNORECASE), "Directly trusting unverified client HTTP header for role or tenant assignment")
        ]
    },

    # ── TG-DB ────────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-DB-001",
        "title": "Frontend Database Query Logic",
        "severity": "High",
        "category": "database",
        "cluster": "cluster-client-leak",
        "patterns": [
            (re.compile(r'\b(?:createClient|supabase)\.from\([^)]+\)\.delete\(\)'), "Dangerous direct database mutation in client component"),
            (re.compile(r'\bimport\s+.*(?:pg|mysql2|prisma|typeorm).*\s+from'), "Server database driver imported in client file")
        ]
    },
    {
        "rule_id": "TG-DB-002",
        "title": "Privileged Database Credential in Browser Context",
        "severity": "Critical",
        "category": "database",
        "cluster": "cluster-client-leak",
        "patterns": [
            (re.compile(r'\b(?:SUPABASE_SERVICE_ROLE_KEY|DATABASE_URL)\b'), "Service role key or raw database connection string reference in frontend code")
        ]
    },
    {
        "rule_id": "TG-DB-003",
        "title": "Frontend Use of Admin or Server-Only Database SDKs",
        "severity": "Critical",
        "category": "database",
        "cluster": "cluster-client-leak",
        "patterns": [
            (re.compile(r'import\s+.*(?:firebase-admin|@prisma/client|mongoose).*from\s+["\']', re.IGNORECASE), "Server-only database ORM/SDK imported in client code")
        ]
    },
    {
        "rule_id": "TG-DB-004",
        "title": "Missing Tenant Query Isolation in Multi-Tenant Models",
        "severity": "Critical",
        "category": "database",
        "cluster": "cluster-tenant-isolation",
        "patterns": [
            (re.compile(r'\.objects\.get\s*\(\s*id\s*=\s*[^,\)]+\)'), "Django ORM .get(id=...) query lacking explicit tenant scope filter"),
            (re.compile(r'\.findById\s*\(\s*(?:req\.params|id)[^\)]*\)'), "Direct findById query lacking organization/tenant boundaries"),
            (re.compile(r'prisma\.[a-zA-Z]+\.findUnique\s*\(\s*\{\s*where:\s*\{\s*id\b'), "Prisma findUnique query lacking tenantId boundary filter")
        ]
    },

    # ── TG-INPUT ─────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-INPUT-001",
        "title": "Missing Server-Side Request Validation",
        "severity": "High",
        "category": "injection",
        "cluster": "cluster-injection",
        "patterns": [
            (re.compile(r'(?:const|let|var)\s+\{[^}]+\}\s*=\s*req\.body\s*;?\s*(?!\s*(?:const|let|var|[a-zA-Z0-9_]+\.parse|\.validate))'), "Destructuring unvalidated req.body without schema validation")
        ]
    },
    {
        "rule_id": "TG-INPUT-002",
        "title": "Raw SQL Concatenation",
        "severity": "Critical",
        "category": "injection",
        "cluster": "cluster-injection",
        "patterns": [
            (re.compile(r'(?:query|execute|raw)\s*\(\s*f["\'].*SELECT.*\{', re.IGNORECASE), "Python f-string interpolation in raw SQL query"),
            (re.compile(r'(?:query|execute|raw)\s*\(\s*[`"\'].*SELECT.*\$\{', re.IGNORECASE), "JavaScript template literal interpolation in SQL query"),
            (re.compile(r'(?:query|execute|raw)\s*\(\s*["\'].*SELECT.*\+\s*(?:req|input|params)', re.IGNORECASE), "String concatenation in raw SQL query")
        ]
    },
    {
        "rule_id": "TG-INPUT-003",
        "title": "Unsafe Dynamic Code or HTML Execution",
        "severity": "High",
        "category": "injection",
        "cluster": "cluster-injection",
        "patterns": [
            (re.compile(r'\beval\s*\('), "Direct eval() execution on untrusted input"),
            (re.compile(r'\bexec\s*\('), "Direct exec() execution on untrusted input"),
            (re.compile(r'\bdangerouslySetInnerHTML\s*='), "React dangerouslySetInnerHTML rendering raw unescaped HTML"),
            (re.compile(r'\.innerHTML\s*='), "Direct DOM innerHTML assignment vulnerable to XSS")
        ]
    },
    {
        "rule_id": "TG-INPUT-004",
        "title": "Command Injection via Shell Execution",
        "severity": "High",
        "category": "injection",
        "cluster": "cluster-injection",
        "patterns": [
            (re.compile(r'(?:child_process\.exec|execSync|subprocess\.Popen|os\.system)\s*\([^)]*\+\s*(?:req|params|cmd|input)'), "Untrusted user parameter concatenated into shell execution command")
        ]
    },
    {
        "rule_id": "TG-INPUT-005",
        "title": "Unsafe Template Rendering & Disabled Autoescaping",
        "severity": "High",
        "category": "injection",
        "cluster": "cluster-injection",
        "patterns": [
            (re.compile(r'render_template_string\s*\('), "Flask render_template_string rendering untrusted input"),
            (re.compile(r'autoescape\s*=\s*False\b'), "Template engine autoescape explicitly disabled")
        ]
    },
    {
        "rule_id": "TG-INPUT-006",
        "title": "Path Traversal and Unsafe Upload Storage",
        "severity": "Critical",
        "category": "filesystem",
        "cluster": "cluster-injection",
        "patterns": [
            (re.compile(r'(?:open|readFile|readFileSync)\s*\([^)]*\+\s*(?:req|params|query)'), "File read operation using unsanitized user request path"),
            (re.compile(r'path\.join\s*\([^)]*(?:req\.params|req\.query)\.[a-zA-Z0-9_]+\)'), "Path traversal sink in path.join without basename sanitization")
        ]
    },

    # ── TG-RATE ──────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-RATE-001",
        "title": "Unlimited Authentication Endpoint",
        "severity": "High",
        "category": "rate",
        "cluster": "cluster-rate-limiting",
        "patterns": [
            (re.compile(r'(?:app|router)\.post\s*\(\s*["\']/(?:api/)?(?:auth/)?(?:login|signin|register|reset-password)["\'],\s*(?:async\s*)?\('), "Authentication POST endpoint defined without rate-limiting middleware")
        ]
    },
    {
        "rule_id": "TG-RATE-002",
        "title": "Unlimited Public Write Endpoint",
        "severity": "Medium",
        "category": "rate",
        "cluster": "cluster-rate-limiting",
        "patterns": [
            (re.compile(r'(?:app|router)\.post\s*\(\s*["\']/(?:api/)?(?:contact|feedback|comments|messages)["\'],\s*(?:async\s*)?\('), "Public submission endpoint defined without rate-limiting or captcha defense")
        ]
    },
    {
        "rule_id": "TG-RATE-003",
        "title": "Unbounded Resource Consumption",
        "severity": "High",
        "category": "rate",
        "cluster": "cluster-rate-limiting",
        "patterns": [
            (re.compile(r'(?:findMany|find)\s*\(\s*\{\s*\}\s*\)'), "Database query returning all records without pagination take/limit"),
            (re.compile(r'SELECT\s+\*\s+FROM\s+[a-zA-Z0-9_]+\s*;', re.IGNORECASE), "Raw unbounded SELECT * query lacking LIMIT clause")
        ]
    },

    # ── TG-AGENT ─────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-AGENT-001",
        "title": "Prompt Injection in System Context Files",
        "severity": "Critical",
        "category": "agent",
        "cluster": "cluster-agent-security",
        "patterns": [
            (re.compile(r'\{[^{}]*role\s*:\s*["\']system["\'][^{}]*content\s*:[^{}]*\$\{'), "User-controlled template string concatenated into LLM system prompt"),
            (re.compile(r'\[\s*\{\s*["\']role["\']\s*:\s*["\']system["\']\s*,\s*["\']content["\']\s*:\s*f["\']'), "Python f-string interpolation inside LLM system prompt message")
        ]
    },
    {
        "rule_id": "TG-AGENT-002",
        "title": "Unsafe Tool Dispatch & Shell Execution without Sandboxing",
        "severity": "Critical",
        "category": "agent",
        "cluster": "cluster-agent-security",
        "patterns": [
            (re.compile(r'(?:exec|spawnSync|run_command|os\.system)\s*\([^)]*tool_call\.(?:arguments|args)'), "AI agent tool call executing unsandboxed shell command")
        ]
    },
    {
        "rule_id": "TG-AGENT-003",
        "title": "Overly Broad MCP Tool Scoping & Credential Access",
        "severity": "High",
        "category": "agent",
        "cluster": "cluster-agent-security",
        "patterns": [
            (re.compile(r'env\s*:\s*process\.env\b'), "Exposing entire host process.env to sub-agent or MCP tool environment")
        ]
    },
    {
        "rule_id": "TG-AGENT-004",
        "title": "Persistent Memory & Cross-Session Information Leakage",
        "severity": "High",
        "category": "agent",
        "cluster": "cluster-agent-security",
        "patterns": [
            (re.compile(r'globalMemory\s*\[\s*["\'][a-zA-Z0-9_]+["\']\s*\]\s*='), "Global shared memory variable persisting cross-session user conversations")
        ]
    },

    # ── TG-SSRF ──────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-SSRF-001",
        "title": "User-Controlled Server-Side URL Fetch",
        "severity": "Critical",
        "category": "ssrf",
        "cluster": "cluster-ssrf",
        "patterns": [
            (re.compile(r'(?:fetch|axios\.get|requests\.get|urllib\.request\.urlopen)\s*\(\s*(?:req\.query|req\.body|request\.GET)\.[a-zA-Z0-9_]+'), "Outbound HTTP request directly invoking user-supplied URL parameter")
        ]
    },
    {
        "rule_id": "TG-SSRF-002",
        "title": "Missing Internal Network Protection",
        "severity": "Critical",
        "category": "ssrf",
        "cluster": "cluster-ssrf",
        "patterns": [
            (re.compile(r'(?:fetch|axios(?:\.get|\.post)?|requests\.(?:get|post)|urllib\.request\.urlopen|http\.get)\s*\(\s*["\']https?://(?:localhost|127\.0\.0\.1|169\.254\.169\.254|metadata\.google)'), "Server-side HTTP request targeting internal loopback or cloud metadata endpoint"),
            (re.compile(r'(?:target_url|dest_url|request_url|backend_url|url)\s*=\s*["\']https?://(?:169\.254\.169\.254|metadata\.google)'), "Target URL assigned to internal cloud metadata endpoint")
        ]
    },
    {
        "rule_id": "TG-SSRF-003",
        "title": "Unsafe Redirect Following",
        "severity": "Critical",
        "category": "ssrf",
        "cluster": "cluster-ssrf",
        "patterns": [
            (re.compile(r'(?:maxRedirects\s*:\s*(?:[5-9]|[1-9][0-9])|allow_redirects\s*=\s*True)'), "HTTP client configured to follow redirects without domain revalidation")
        ]
    },
    {
        "rule_id": "TG-SSRF-004",
        "title": "Unbounded Outbound Request Without Timeout",
        "severity": "Critical",
        "category": "ssrf",
        "cluster": "cluster-ssrf",
        "patterns": [
            (re.compile(r'requests\.(?:get|post|put)\s*\((?![^)]*\btimeout\s*=)[^)]*\)'), "Python requests call without explicit timeout parameter")
        ]
    },

    # ── TG-WEBHOOK ───────────────────────────────────────────────────────────
    {
        "rule_id": "TG-WEBHOOK-001",
        "title": "Missing Webhook Signature Verification",
        "severity": "Critical",
        "category": "webhook",
        "cluster": "cluster-webhook",
        "patterns": [
            (re.compile(r'(?:app|router)\.post\s*\(\s*["\']/(?:api/)?(?:stripe|github|webhooks?)(?:/[a-zA-Z0-9_]+)?["\'],\s*(?:async\s*)?\(\s*(?:req|request)'), "Webhook endpoint handler defined without cryptographic signature verification middleware")
        ]
    },
    {
        "rule_id": "TG-WEBHOOK-002",
        "title": "Replayable Webhook Without Timestamp Validation",
        "severity": "Critical",
        "category": "webhook",
        "cluster": "cluster-webhook",
        "patterns": [
            (re.compile(r'verifyWebhook\s*\([^)]*\)(?!.*timestamp)'), "Webhook signature check without tolerance or timestamp replay defense")
        ]
    },
    {
        "rule_id": "TG-WEBHOOK-003",
        "title": "Missing Webhook Idempotency",
        "severity": "Critical",
        "category": "webhook",
        "cluster": "cluster-webhook",
        "patterns": [
            (re.compile(r'(?:handleWebhook|processWebhookEvent)\s*\(\s*event\s*\)\s*\{(?!.*(?:hasProcessed|processedEvents|idempotency))'), "Webhook processing function without event ID deduplication record")
        ]
    },
    {
        "rule_id": "TG-WEBHOOK-004",
        "title": "Unvalidated Webhook Event Type",
        "severity": "Critical",
        "category": "webhook",
        "cluster": "cluster-webhook",
        "patterns": [
            (re.compile(r'handlers\s*\[\s*event\.type\s*\]\s*\('), "Dynamic invocation of webhook handler via unverified event.type index")
        ]
    },

    # ── TG-WS ────────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-WS-001",
        "title": "Unauthenticated WebSocket Handshake",
        "severity": "High",
        "category": "ws",
        "cluster": "cluster-websocket",
        "patterns": [
            (re.compile(r'wss?\.on\s*\(\s*["\']connection["\'],\s*\(\s*ws\s*,\s*req\s*\)\s*=>\s*\{(?!.*(?:token|auth|verify|session))'), "WebSocket server accepting connections without token verification in handshake")
        ]
    },
    {
        "rule_id": "TG-WS-002",
        "title": "Missing Channel-Level Authorization",
        "severity": "Critical",
        "category": "ws",
        "cluster": "cluster-websocket",
        "patterns": [
            (re.compile(r'socket\.join\s*\(\s*data\.channel\s*\)(?!.*(?:canAccess|hasPermission|isMember))'), "Socket joining room or channel without user permission verification")
        ]
    },
    {
        "rule_id": "TG-WS-003",
        "title": "Unvalidated WebSocket Message",
        "severity": "Critical",
        "category": "ws",
        "cluster": "cluster-websocket",
        "patterns": [
            (re.compile(r'ws\.on\s*\(\s*["\']message["\'],\s*(?:async\s*)?\(\s*data\s*\)\s*=>\s*\{\s*const\s+[a-zA-Z0-9_]+\s*=\s*JSON\.parse'), "Parsing WebSocket message payload without schema validation")
        ]
    },
    {
        "rule_id": "TG-WS-004",
        "title": "Unbounded WebSocket Connections",
        "severity": "Critical",
        "category": "ws",
        "cluster": "cluster-websocket",
        "patterns": [
            (re.compile(r'new\s+WebSocketServer\s*\(\s*\{\s*server\s*\}\s*\)'), "WebSocketServer instantiated without maxPayload or client connection bounds")
        ]
    },

    # ── TG-CSRF ──────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-CSRF-001",
        "title": "Missing CSRF Protection",
        "severity": "Critical",
        "category": "csrf",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'<form\s+[^>]*method=["\']POST["\'][^>]*>(?![\s\S]*name=["\'](?:csrf_token|csrfToken|_csrf)["\'])'), "HTML POST form without hidden CSRF token input field")
        ]
    },
    {
        "rule_id": "TG-CSRF-002",
        "title": "Unsafe Credentialed Cross-Origin Request",
        "severity": "Critical",
        "category": "csrf",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'res\.setHeader\s*\(\s*["\']Access-Control-Allow-Origin["\']\s*,\s*["\']\*["\']\s*\);\s*res\.setHeader\s*\(\s*["\']Access-Control-Allow-Credentials["\']\s*,\s*["\']true["\']'), "Wildcard CORS origin paired with credentials flag")
        ]
    },

    # ── TG-GQL ───────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-GQL-001",
        "title": "Missing Query Depth or Complexity Limits",
        "severity": "High",
        "category": "gql",
        "cluster": "cluster-graphql",
        "patterns": [
            (re.compile(r'new\s+ApolloServer\s*\(\s*\{\s*typeDefs\s*,\s*resolvers\s*\}\s*\)'), "ApolloServer initialized without query depth or complexity limits")
        ]
    },
    {
        "rule_id": "TG-GQL-002",
        "title": "Resolver Missing Authorization",
        "severity": "Critical",
        "category": "gql",
        "cluster": "cluster-graphql",
        "patterns": [
            (re.compile(r'Mutation\s*:\s*\{[\s\S]*?(?:delete|update|mutate)[a-zA-Z0-9_]*\s*:\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{(?!.*(?:context\.user|context\.auth))'), "GraphQL mutation resolver executing without user authorization check")
        ]
    },
    {
        "rule_id": "TG-GQL-003",
        "title": "Unbounded GraphQL Pagination or Batching",
        "severity": "Critical",
        "category": "gql",
        "cluster": "cluster-graphql",
        "patterns": [
            (re.compile(r'resolve\s*\(\s*parent\s*,\s*args\s*\)\s*\{\s*return\s+db\.[a-zA-Z]+\.find\(\)'), "GraphQL field resolver returning unpaginated database collection")
        ]
    },
    {
        "rule_id": "TG-GQL-004",
        "title": "Unnecessary Production Introspection",
        "severity": "Critical",
        "category": "gql",
        "cluster": "cluster-graphql",
        "patterns": [
            (re.compile(r'\bintrospection\s*:\s*true\b', re.IGNORECASE), "GraphQL schema introspection enabled in configuration")
        ]
    },

    # ── TG-SUPPLY ────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-SUPPLY-001",
        "title": "Missing or Ignored Dependency Lockfile",
        "severity": "Critical",
        "category": "supply",
        "cluster": "cluster-supply-chain",
        "patterns": [
            (re.compile(r'^\s*package-lock\.json\s*$', re.MULTILINE), "Lockfile package-lock.json explicitly ignored in .gitignore")
        ]
    },
    {
        "rule_id": "TG-SUPPLY-002",
        "title": "Vulnerable Dependency Review Missing",
        "severity": "Critical",
        "category": "supply",
        "cluster": "cluster-supply-chain",
        "patterns": [
            (re.compile(r'(?:npm|yarn|pnpm)\s+(?:install|ci)\s+.*--(?:no-audit|audit=false)'), "Dependency installation command skipping security audit checks")
        ]
    },
    {
        "rule_id": "TG-SUPPLY-003",
        "title": "Unsafe CI/CD Secret Exposure",
        "severity": "Critical",
        "category": "supply",
        "cluster": "cluster-supply-chain",
        "patterns": [
            (re.compile(r'run\s*:\s*echo\s+["\']?\$\{\{\s*secrets\.[A-Z0-9_]+\s*\}\}'), "CI workflow step echoing secret into pipeline logs")
        ]
    },
    {
        "rule_id": "TG-SUPPLY-004",
        "title": "Unpinned CI Action",
        "severity": "Critical",
        "category": "supply",
        "cluster": "cluster-supply-chain",
        "patterns": [
            (re.compile(r'uses\s*:\s*actions\/[a-zA-Z0-9_\-]+@(?!main)[a-zA-Z0-9_\.]+(?<![a-f0-9]{40})$'), "GitHub Action referenced by mutable tag instead of immutable commit SHA")
        ]
    },
    {
        "rule_id": "TG-SUPPLY-005",
        "title": "Unsafe Dependency Install Script",
        "severity": "Critical",
        "category": "supply",
        "cluster": "cluster-supply-chain",
        "patterns": [
            (re.compile(r'curl\s+-[a-zA-Z]*s[a-zA-Z]*\s+https?:\/\/[^\s|]+\s*\|\s*(?:bash|sh)'), "Remote installation script piped directly to bash without checksum verification")
        ]
    },
    {
        "rule_id": "TG-SUPPLY-006",
        "title": "Container Build Secret Persistence",
        "severity": "High",
        "category": "supply",
        "cluster": "cluster-supply-chain",
        "patterns": [
            (re.compile(r'COPY\s+\.env\s+'), "Production Dockerfile copying local .env into container filesystem")
        ]
    },

    # ── TG-BIZ ───────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-BIZ-001",
        "title": "Client-Controlled Sensitive Business Value",
        "severity": "Critical",
        "category": "biz",
        "cluster": "cluster-biz-logic",
        "patterns": [
            (re.compile(r'(?:amount|price|discount|total)\s*:\s*(?:req\.body|request\.data)\.(?:amount|price|discount)'), "Sensitive pricing or discount amount accepted directly from client payload")
        ]
    },
    {
        "rule_id": "TG-BIZ-002",
        "title": "Replayable One-Time Operation",
        "severity": "Critical",
        "category": "biz",
        "cluster": "cluster-biz-logic",
        "patterns": [
            (re.compile(r'(?:chargeCard|processPayment|transferFunds)\s*\([^)]*\)(?!.*idempotency)'), "Financial transaction execution without idempotency key parameter")
        ]
    },
    {
        "rule_id": "TG-BIZ-003",
        "title": "Missing Workflow-State Validation",
        "severity": "Critical",
        "category": "biz",
        "cluster": "cluster-biz-logic",
        "patterns": [
            (re.compile(r'(?:order|invoice)\.status\s*=\s*(?:req\.body|request\.data)\.status'), "Direct client modification of order workflow status")
        ]
    },
    {
        "rule_id": "TG-BIZ-004",
        "title": "Unrestricted Sensitive Business Flow",
        "severity": "Critical",
        "category": "biz",
        "cluster": "cluster-biz-logic",
        "patterns": [
            (re.compile(r'(?:deleteMany|updateMany)\s*\(\s*\{\s*\}\s*\)'), "Bulk destructive mutation executing without filter criteria or threshold guard")
        ]
    },

    # ── TG-CACHE ─────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-CACHE-001",
        "title": "Sensitive Response Publicly Cacheable",
        "severity": "Critical",
        "category": "cache",
        "cluster": "cluster-cache",
        "patterns": [
            (re.compile(r'Cache-Control["\']?\s*,\s*["\']public,\s*max-age=\d+["\']', re.IGNORECASE), "Public caching header configured on potentially sensitive response")
        ]
    },
    {
        "rule_id": "TG-CACHE-002",
        "title": "Missing User Cache Isolation",
        "severity": "Critical",
        "category": "cache",
        "cluster": "cluster-cache",
        "patterns": [
            (re.compile(r'cache\.set\s*\(\s*["\']user_profile_["\']\s*\+\s*id\s*,\s*data\s*\)(?!.*tenant)'), "Cache key lacking tenant isolation prefix")
        ]
    },
    {
        "rule_id": "TG-CACHE-003",
        "title": "Sensitive Data in URL",
        "severity": "Critical",
        "category": "cache",
        "cluster": "cluster-cache",
        "patterns": [
            (re.compile(r'(?:router|app)\.get\s*\(\s*["\'][^"\']*(?:password|ssn|credit_card)[^"\']*["\']'), "Sensitive PII or password transmitted in GET URL query path")
        ]
    },

    # ── TG-CLIENT ────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-CLIENT-001",
        "title": "Public Production Source Maps",
        "severity": "Medium",
        "category": "client",
        "cluster": "cluster-client-leak",
        "patterns": [
            (re.compile(r'\bproductionSourceMap\s*:\s*true\b', re.IGNORECASE), "Webpack/Vite productionSourceMap enabled in build configuration"),
            (re.compile(r'\bsourcemap\s*:\s*true\b', re.IGNORECASE), "Build config emitting unminified source maps in production output")
        ]
    },
    {
        "rule_id": "TG-CLIENT-002",
        "title": "Sensitive Client Bundle Content",
        "severity": "High",
        "category": "client",
        "cluster": "cluster-client-leak",
        "patterns": [
            (re.compile(r'["\']use client["\'];[\s\S]*?import\s+.*(?:nodemailer|bcrypt|jsonwebtoken|aws-sdk).*from'), "Server-only private dependency imported into React Client Component")
        ]
    },

    # ── TG-PLATFORM ──────────────────────────────────────────────────────────
    {
        "rule_id": "TG-PLATFORM-001",
        "title": "Wildcard CORS With Credentials",
        "severity": "High",
        "category": "platform",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'\bCORS_ALLOW_ALL_ORIGINS\s*=\s*True\b'), "Wildcard CORS origin enabled across entire application"),
            (re.compile(r'@CrossOrigin\s*\(\s*["\']\*["\']\s*\)'), "Wildcard CORS origin annotation in Java/Spring"),
            (re.compile(r'cors\(\s*\{\s*origin\s*:\s*["\']\*["\']'), "Wildcard CORS origin configured in Express middleware")
        ]
    },
    {
        "rule_id": "TG-PLATFORM-002",
        "title": "Missing Security Headers",
        "severity": "Medium",
        "category": "platform",
        "cluster": "cluster-platform",
        "patterns": [
            (re.compile(r'const\s+app\s*=\s*express\(\);(?![\s\S]*app\.use\s*\(\s*helmet)'), "Express application initialized without helmet security headers middleware")
        ]
    },
    {
        "rule_id": "TG-PLATFORM-003",
        "title": "Production Stack Trace Exposure",
        "severity": "Medium",
        "category": "platform",
        "cluster": "cluster-platform",
        "patterns": [
            (re.compile(r'res\.status\(500\)\.(?:send|json)\s*\(\s*(?:err\.stack|error\.stack)\s*\)'), "Uncaught internal error stack trace sent directly to client response"),
            (re.compile(r'\bDEBUG\s*=\s*True\b'), "Django DEBUG mode enabled in configuration")
        ]
    },
    {
        "rule_id": "TG-PLATFORM-004",
        "title": "Missing Request Size Limits",
        "severity": "Medium",
        "category": "platform",
        "cluster": "cluster-platform",
        "patterns": [
            (re.compile(r'express\.(?:json|urlencoded)\s*\(\s*\{\s*limit\s*:\s*["\'](?:[5-9][0-9]|[1-9][0-9]{2,})mb["\']', re.IGNORECASE), "Excessively permissive request body size limit (>50MB) risking denial of service")
        ]
    },

    # ── TG-DIFF ──────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-DIFF-001",
        "title": "Accidental Security Check Bypass in Patch Additions",
        "severity": "Critical",
        "category": "transport",
        "cluster": "cluster-transport-security",
        "patterns": [
            (re.compile(r'\bverify\s*=\s*False\b'), "Disabled TLS certificate verification (verify=False)"),
            (re.compile(r'\bInsecureSkipVerify\s*:\s*true\b'), "Disabled Go TLS certificate verification (InsecureSkipVerify: true)"),
            (re.compile(r'\bNODE_TLS_REJECT_UNAUTHORIZED\s*=\s*[\'"]?0[\'"]?'), "Disabled Node.js TLS verification (NODE_TLS_REJECT_UNAUTHORIZED=0)"),
            (re.compile(r'\brejectUnauthorized\s*:\s*false\b'), "Disabled Node.js TLS rejectUnauthorized"),
            (re.compile(r'\bCURLOPT_SSL_VERIFYPEER\s*(?:=>|,)\s*(?:false|0)\b', re.IGNORECASE), "Disabled PHP curl SSL verification")
        ]
    },
    {
        "rule_id": "TG-DIFF-002",
        "title": "Secret and Token Ingestion in Patch Additions",
        "severity": "Critical",
        "category": "diff",
        "cluster": "cluster-credentials-exposure",
        "patterns": [
            (re.compile(r'^\+[^+].*(?:eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}|ghp_[a-zA-Z0-9]{36})'), "Hardcoded secret or auth token introduced in patch addition")
        ]
    },
    {
        "rule_id": "TG-DIFF-003",
        "title": "Unintentional Removal of Tenant Filter in Patch Deletions",
        "severity": "High",
        "category": "diff",
        "cluster": "cluster-tenant-isolation",
        "patterns": [
            (re.compile(r'^\-[^-].*(?:tenantId|organization_id|account_id)'), "Removal of tenant isolation boundary in patch deletion")
        ]
    },

    # ── TG-EDGE ──────────────────────────────────────────────────────────────
    {
        "rule_id": "TG-EDGE-001",
        "title": "Serverless & Edge Global State Memory Leakage",
        "severity": "High",
        "category": "edge",
        "cluster": "cluster-edge",
        "patterns": [
            (re.compile(r'^(?:let|var)\s+(?:userCache|sessionData|requestState)\s*=\s*\{', re.MULTILINE), "Mutable global state variable declared outside serverless handler function")
        ]
    },
    {
        "rule_id": "TG-EDGE-003",
        "title": "AWS Lambda Ephemeral Execution & Cold Start Security",
        "severity": "High",
        "category": "edge",
        "cluster": "cluster-edge",
        "patterns": [
            (re.compile(r'export\s+const\s+handler\s*=\s*async\s*\([^)]*\)\s*=>\s*\{[\s\S]*?secretsmanager\.getSecretValue'), "Fetching cloud secrets inside request handler loop instead of cold-start cache")
        ]
    }
]

# File extensions to scan
SOURCE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".go", ".java", ".cs", ".php", ".rb", ".json", ".yaml", ".yml"
}

# Directories to skip
SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", "__pycache__",
    "dist", "build", ".next", ".nuxt", "coverage", ".torusguard",
    ".idea", ".vscode", "target", "bin", "obj", "payload"
}

def is_test_file(path_str: str) -> bool:
    """Check if file belongs to tests, fixtures, or test harnesses."""
    clean = path_str.replace("\\", "/").lower()
    markers = ["/test/", "/tests/", "/spec/", "/specs/", "/fixtures/", "/mock/", "/mocks/",
               "/harness/", "__tests__", "test_", "_test.", ".test.", ".spec."]
    return any(m in clean for m in markers)


def find_files_to_scan(target_root: Path, include_tests: bool = False) -> List[Path]:
    """Recursively collect source files eligible for static security audit."""
    files = []
    for root, dirs, filenames in os.walk(target_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in SOURCE_EXTENSIONS:
                if f in ("audit_runner.py", "diff_guard.py", "finding_scorer.py", "harden_runner.py", "apply_runner.py", "recheck_runner.py", "report_sync.py", "term_ui.py", "sarif_exporter.py", "safety_gate.py", "stack_detect.py", "recipes_runner.py", "html_reporter.py", "run_manager.py", "rules_sync.py", "bootstrap.py", "scope.json", "rules_catalog.json"):
                    continue
                full_path = Path(root) / f
                if not include_tests and is_test_file(str(full_path)):
                    continue
                files.append(full_path)
    return sorted(files)


def scan_file(file_path: Path, target_root: Path) -> List[Dict[str, Any]]:
    """Scan a single source file against the TorusGuard rule families."""
    findings = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = content.splitlines()
    rel_path = str(file_path.relative_to(target_root)).replace("\\", "/")
    is_test = is_test_file(rel_path)

    for rule in RULE_PATTERNS:
        rule_id = rule["rule_id"]
        if rule_id == "TG-PLATFORM-002" and "helmet" in content and "app.use(helmet" in content:
            continue
        patterns: List[Tuple[Pattern[str], str]] = rule["patterns"]
        for regex, desc in patterns:
            for idx, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith(("#", "//", "/*", "*")):
                    if "bypass" not in stripped.lower() and "todo" not in stripped.lower():
                        continue

                match = regex.search(line)
                if match:
                    line_num = idx + 1
                    seed = f"{rule_id}:{rel_path}:{line_num}:{stripped}"
                    fp = f"{rule_id}-{hashlib.sha256(seed.encode('utf-8')).hexdigest()[:8]}"

                    start_ctx = max(0, idx - 2)
                    end_ctx = min(len(lines), idx + 3)
                    snippet = "\n".join(lines[start_ctx:end_ctx])

                    findings.append({
                        "finding_id": fp,
                        "rule_id": rule_id,
                        "title": rule["title"],
                        "description": desc,
                        "severity": "Low" if is_test else rule["severity"],
                        "category": rule["category"],
                        "cluster": rule["cluster"],
                        "file_path": rel_path,
                        "line_number": line_num,
                        "matched_text": match.group(0)[:80],
                        "snippet": snippet,
                        "is_test": is_test,
                        "target": {
                            "file_path": rel_path,
                            "start_line": line_num,
                            "end_line": line_num
                        }
                    })
                    break
    return findings


def score_and_cluster_findings(findings: List[Dict[str, Any]], target_root: Path) -> Tuple[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]]:
    """
    Score each finding using finding_scorer.py and persistent memory patterns.
    Returns (scored_findings, clusters_map).
    """
    try:
        import finding_scorer
    except Exception:
        finding_scorer = None

    scored = []
    clusters: Dict[str, List[Dict[str, Any]]] = {}

    for f in findings:
        score = 70
        band = "High Confidence"
        factors = {}

        if finding_scorer:
            try:
                eq = 35
                rs = 0
                ic = 5
                ec = 15
                mr = 0
                s, b, facts = finding_scorer.compute_confidence_score(
                    evidence_quality=eq,
                    reproduction_success=rs,
                    independent_confirmations=ic,
                    environmental_clarity=ec,
                    manual_review_status=mr,
                    rule_id=f["rule_id"],
                    file_path=f["file_path"],
                    root_dir=target_root
                )
                score = s
                band = b
                factors = facts
            except Exception:
                pass

        f["confidence_score"] = score
        f["confidence_band"] = band
        f["confidence_factors"] = factors
        scored.append(f)

        c_id = f["cluster"]
        if c_id not in clusters:
            clusters[c_id] = []
        clusters[c_id].append(f)

    # Sort descending by severity (Critical -> High -> Medium -> Low), then score
    sev_rank = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
    scored.sort(key=lambda x: (sev_rank.get(x["severity"], 0), x["confidence_score"]), reverse=True)
    return scored, clusters


def emit_run_artifacts(run_folder: Path, scored_findings: List[Dict[str, Any]], clusters: Dict[str, List[Dict[str, Any]]], target_root: Path) -> None:
    """Generate findings.json, findings.md, and summary.md into run folder."""
    now_ist = get_ist_now()

    # 1. findings.json
    (run_folder / "findings.json").write_text(json.dumps(scored_findings, indent=2), encoding="utf-8")

    # 2. findings.md
    md_lines = [
        f"# TorusGuard Security Audit Findings: {run_folder.name}",
        f"- Target Root: `{target_root}`",
        f"- Total Scored Findings: `{len(scored_findings)}`",
        f"- Identified Clusters: `{len(clusters)}`",
        f"- Generated At: `{now_ist.strftime('%Y-%m-%d %H:%M:%S IST')}`\n",
        "---",
        "## Summary of Findings\n"
    ]

    for f in scored_findings:
        md_lines.append(f"### [{f['severity']}] {f['rule_id']} - {f['title']}")
        md_lines.append(f"- **Finding ID:** `{f['finding_id']}`")
        md_lines.append(f"- **Location:** `{f['file_path']}:{f['line_number']}`")
        md_lines.append(f"- **Confidence Score:** `{f['confidence_score']}/100` ({f['confidence_band']})")
        md_lines.append(f"- **Cluster:** `{f['cluster']}`")
        md_lines.append(f"- **Description:** {f['description']}")
        md_lines.append("```")
        md_lines.append(f['snippet'])
        md_lines.append("```\n")

    (run_folder / "findings.md").write_text("\n".join(md_lines), encoding="utf-8")

    # 3. summary.md
    summary_lines = [
        f"# TorusGuard Audit Summary: {run_folder.name}",
        f"- Scanned Scope: {target_root}",
        f"- Total Findings: {len(scored_findings)}",
        f"- Root-Cause Clusters: {len(clusters)}",
        f"- Generated: {now_ist.strftime('%Y-%m-%d %H:%M:%S IST')}"
    ]
    (run_folder / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")

    # 4. Update manifest.json status
    manifest_file = run_folder / "manifest.json"
    if manifest_file.exists():
        try:
            with open(manifest_file, "r", encoding="utf-8") as mf:
                mdata = json.load(mf)
            mdata["status"] = "completed"
            mdata["findings_count"] = len(scored_findings)
            with open(manifest_file, "w", encoding="utf-8") as mf:
                json.dump(mdata, mf, indent=2)
        except Exception:
            pass


def print_audit_dashboard(target_root: Path, file_count: int, scored_findings: List[Dict[str, Any]], clusters: Dict[str, List[Dict[str, Any]]], run_folder: Path, detected_stack: Optional[Dict[str, Any]] = None) -> None:
    """Print the unified 75-column TorusGuard Static Audit results card."""
    crit_count = sum(1 for f in scored_findings if f["severity"] == "Critical")
    high_count = sum(1 for f in scored_findings if f["severity"] == "High")
    med_count = sum(1 for f in scored_findings if f["severity"] in ("Medium", "Low"))

    stack_str = "Auto-detected"
    if detected_stack and detected_stack.get("framework") and detected_stack.get("framework") != "None":
        stack_str = f"{detected_stack.get('framework')} ({detected_stack.get('language')})"

    print()
    print(card_header("🛡️  TORUSGUARD STATIC SECURITY AUDIT", "Autonomous AST & Invariant Security Scanner", "v1.3.5"))
    print()

    print(card_border_top("Audit Execution Scope"))
    print(format_box_line(f"{BOLD}Target:{RESET}       {WHITE}{str(target_root)}{RESET}"))
    print(format_box_line(f"{BOLD}Stack:{RESET}        {GREEN}{stack_str}{RESET}"))
    print(format_box_line(f"{BOLD}Files:{RESET}        {WHITE}{file_count} files evaluated across 18 rule families (74 rules){RESET}"))
    print(card_border_bottom())
    print()

    # Findings Box
    status_icon = f"{RED}✖ CRITICAL FINDINGS DETECTED{RESET}" if crit_count > 0 else (f"{YELLOW}⚠ HIGH VULNERABILITIES DETECTED{RESET}" if high_count > 0 else f"{GREEN}✔ SECURITY POSTURE CLEAN{RESET}")
    print(card_border_top("Findings & Confidence Scores"))
    print(format_box_line(f"Status:      {status_icon}"))
    print(format_box_line(f"Findings:    {RED}{crit_count} Critical{RESET}  {YELLOW}{high_count} High{RESET}  {CYAN}{med_count} Medium/Low{RESET}  ({len(scored_findings)} total)"))
    print(format_box_line(f"Clusters:    {WHITE}{len(clusters)} architectural root causes identified{RESET}"))
    print(card_divider())

    if not scored_findings:
        print(format_box_line(f"{GREEN}✔ Zero security invariant violations detected.{RESET}"))
    else:
        for idx, f in enumerate(scored_findings[:5]):
            sev_color = RED if f["severity"] == "Critical" else (YELLOW if f["severity"] == "High" else CYAN)
            line_str = f"[{sev_color}{f['severity']}{RESET}] {BOLD}{f['rule_id']}{RESET} at {f['file_path']}:{f['line_number']}"
            print(format_box_line(line_str))
            desc_str = f"  └─ {DIM}{f['description'][:58]}{RESET} ({CYAN}{f['confidence_score']}/100{RESET})"
            print(format_box_line(desc_str))
        if len(scored_findings) > 5:
            print(format_box_line(f"{DIM}... and {len(scored_findings) - 5} more findings in report file{RESET}"))

    print(card_border_bottom())
    print()

    # Run Artifacts & Next Steps Box
    rel_run = str(run_folder.relative_to(target_root)).replace("\\", "/") if str(run_folder).startswith(str(target_root)) else str(run_folder).replace("\\", "/")
    findings_artifact = f"{rel_run}/findings.md"
    print(card_border_top("Artifacts & Next Actions", border_color=GREEN, double=True))
    print(format_box_line(f"{BOLD}Run Artifact:{RESET}  {WHITE}{findings_artifact}{RESET}", border="║", border_color=GREEN))
    print(format_box_line(f"{BOLD}Living Ledger:{RESET} {CYAN}security_report.md (updated){RESET}", border="║", border_color=GREEN))
    print(format_box_line(f"{BOLD}Visual Dash:{RESET}   {CYAN}npx torusguard report --html{RESET}", border="║", border_color=GREEN))
    print(format_box_line(f"{BOLD}Surgical Fix:{RESET}  In AI Chat, run {CYAN}/torusguard-harden{RESET}", border="║", border_color=GREEN))
    print(card_border_bottom(border_color=GREEN, double=True))
    print()


def execute_audit(target_root: Path, severity_floor: str = "medium", json_output: bool = False, include_tests: bool = False) -> Dict[str, Any]:
    """Execute the full TorusGuard static security audit."""
    target_root = target_root.resolve()
    s_dir = Path(__file__).resolve().parent

    # 1. Stack detection
    detected_stack = None
    stack_script = s_dir / "stack_detect.py"
    if stack_script.is_file():
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("stack_detect", str(stack_script))
            if spec and spec.loader:
                sd = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(sd)
                if hasattr(sd, "detect_stack"):
                    detected_stack = sd.detect_stack(target_root)
        except Exception:
            pass

    # 2. Collect files & scan
    files = find_files_to_scan(target_root, include_tests=include_tests)
    all_findings = []
    for f in files:
        all_findings.extend(scan_file(f, target_root))

    # 3. Score & Cluster
    scored_findings, clusters = score_and_cluster_findings(all_findings, target_root)

    # 4. Allocate run folder
    runs_dir = target_root / ".torusguard" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    if str(s_dir) not in sys.path:
        sys.path.insert(0, str(s_dir))
    try:
        import run_manager
        run_folder = run_manager.create_run(runs_dir, "audit", target_root.name)
    except Exception:
        timestamp = get_ist_now().strftime("%Y%m%d-%H%M%S")
        run_folder = runs_dir / f"run-{timestamp}-audit"
        run_folder.mkdir(parents=True, exist_ok=True)

    # 5. Emit artifacts & sync memory
    emit_run_artifacts(run_folder, scored_findings, clusters, target_root)
    try:
        import report_sync
        report_sync.record_audit_findings(target_root, scored_findings, run_folder.name)
    except Exception:
        pass
    try:
        if "run_manager" in sys.modules:
            sys.modules["run_manager"].sync_run_to_memory(run_folder, scored_findings)
    except Exception:
        pass

    result = {
        "status": "completed",
        "target_root": str(target_root),
        "files_scanned": len(files),
        "total_findings": len(scored_findings),
        "critical_count": sum(1 for f in scored_findings if f["severity"] == "Critical"),
        "high_count": sum(1 for f in scored_findings if f["severity"] == "High"),
        "medium_count": sum(1 for f in scored_findings if f["severity"] in ("Medium", "Low")),
        "clusters_count": len(clusters),
        "run_folder": str(run_folder),
        "findings": scored_findings
    }

    if json_output:
        print(json.dumps(result, indent=2))
    else:
        print_audit_dashboard(target_root, len(files), scored_findings, clusters, run_folder, detected_stack)

    return result


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Static Security Audit Engine")
    parser.add_argument("path", nargs="?", default=".", help="Target project root directory to audit")
    parser.add_argument("--scope", "-s", help="Alternative path to target project")
    parser.add_argument("--severity", choices=["critical", "high", "medium", "low"], default="medium", help="Severity floor")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--include-tests", action="store_true", help="Include test files and harness fixtures in scan")
    args = parser.parse_args()

    target = Path(args.scope or args.path).resolve()
    res = execute_audit(target, severity_floor=args.severity, json_output=args.json, include_tests=args.include_tests)
    sys.exit(0 if res["critical_count"] == 0 else 1)


if __name__ == "__main__":
    main()
