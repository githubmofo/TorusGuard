#!/usr/bin/env python3
"""
TorusGuard Autonomous Remediation Engine (v1.3.5)
Evaluates audit findings against canonical patch templates, enforces Ponytail bounds
(<= 35 additions, <= 25 deletions), packages structured candidate remediation bundles,
and renders unified patch diffs with standardized 75-column terminal UI.

Pure Python 3.10+ standard library (zero external dependencies).
"""

import sys
import os
import re
import json
import difflib
import hashlib
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Ensure scripts dir is in sys.path for term_ui import
scripts_dir = Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

try:
    import term_ui
except ImportError:
    term_ui = None

# Windows console UTF-8 support
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ─── Timezone Configuration: Indian Standard Time (IST, UTC+05:30) ───────────
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30), name="IST")

def get_ist_now() -> datetime.datetime:
    return datetime.datetime.now(IST)

# ─── Fallback Formatters (if term_ui missing) ──────────────────────────────────
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
WHITE = "\033[97m"
GRAY = "\033[90m"
RED = "\033[31m"

def box_line(content: str, width: int = 67, border: str = "│", border_color: str = CYAN) -> str:
    if term_ui:
        return term_ui.format_box_line(content, width=width, border=border, border_color=border_color)
    return f"  {border_color}{border}{RESET}  {content}"

def box_header(title: str, subtitle: str = "", version: str = "v1.3.5", border_color: str = CYAN) -> str:
    if term_ui:
        return term_ui.card_header(title, subtitle, version, border_color)
    return f"=== {title} ({version}) ==="

def border_top(title: str = "", border_color: str = CYAN, double: bool = False) -> str:
    if term_ui:
        return term_ui.card_border_top(title, border_color=border_color, double=double)
    return "┌" + "─" * 71 + "┐"

def border_bottom(border_color: str = CYAN, double: bool = False) -> str:
    if term_ui:
        return term_ui.card_border_bottom(border_color=border_color, double=double)
    return "└" + "─" * 71 + "┘"


def find_latest_audit_run(runs_dir: Path) -> Optional[Path]:
    """Locate the most recent audit run folder containing findings.json."""
    if not runs_dir.is_dir():
        return None
    runs = sorted(runs_dir.glob("run-*-audit"), key=lambda p: p.stat().st_mtime, reverse=True)
    for r in runs:
        if (r / "findings.json").is_file():
            return r
    return None


def generate_patch_for_finding(finding: Dict[str, Any], target_root: Path) -> Optional[Dict[str, Any]]:
    """
    Formulate a minimal, surgical fix for a finding adhering to Ponytail bounds
    (<= 35 additions, <= 25 deletions).
    """
    rule_id = finding.get("rule_id", "")
    file_path = finding.get("file_path", "")
    line_number = finding.get("line_number", 1)
    description = finding.get("description", "")

    full_target = target_root / file_path
    if not full_target.is_file():
        return None

    try:
        content = full_target.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    lines = content.splitlines()
    if not (1 <= line_number <= len(lines)):
        return None

    target_line = lines[line_number - 1]
    indent = re.match(r'^\s*', target_line).group(0)  # type: ignore
    new_lines = list(lines)
    applied_rule = False
    fix_explanation = ""

    # Strategy 1: Hardcoded Secrets (TG-SEC-001 / TG-SEC-002)
    if rule_id in ("TG-SEC-001", "TG-SEC-002"):
        if file_path.endswith((".js", ".jsx", ".ts", ".tsx", ".mjs")):
            if re.search(r'(jwt_secret|jwtSecret|JWT_SECRET)', target_line, re.IGNORECASE):
                var_match = re.search(r'(const|let|var)\s+([A-Za-z0-9_]+)\s*=', target_line)
                var_name = var_match.group(2) if var_match else "JWT_SECRET"
                replacement = f'{indent}const {var_name} = process.env.JWT_SECRET || "";'
                new_lines[line_number - 1] = replacement
                applied_rule = True
                fix_explanation = f"Migrated hardcoded JWT secret to environment variable process.env.JWT_SECRET"
            elif re.search(r'(:=|=)\s*["\'][A-Za-z0-9_\-]{8,}["\']', target_line):
                var_match = re.search(r'(const|let|var)?\s*([A-Za-z0-9_]+)\s*[:=]', target_line)
                var_name = var_match.group(2) if var_match else "API_KEY"
                env_key = re.sub(r'(?<!^)(?=[A-Z])', '_', var_name).upper()
                replacement = f'{indent}const {var_name} = process.env.{env_key} || "";'
                new_lines[line_number - 1] = replacement
                applied_rule = True
                fix_explanation = f"Replaced hardcoded credential with process.env.{env_key}"
            elif "password:" in target_line or "password :" in target_line:
                fixed_line = re.sub(r'password:\s*["\'][^"\']+["\']', 'password: process.env.DEMO_USER_PASSWORD || "REDACTED_PASSWORD"', target_line)
                if fixed_line != target_line:
                    new_lines[line_number - 1] = fixed_line
                    applied_rule = True
                    fix_explanation = "Replaced hardcoded password with environment variable process.env.DEMO_USER_PASSWORD"
        elif file_path.endswith(".py"):
            if re.search(r'(:=|=)\s*["\'][A-Za-z0-9_\-]{8,}["\']', target_line):
                var_match = re.search(r'([A-Za-z0-9_]+)\s*=', target_line)
                var_name = var_match.group(1) if var_match else "SECRET_KEY"
                env_key = var_name.upper()
                replacement = f'{indent}{var_name} = os.environ.get("{env_key}", "")'
                new_lines[line_number - 1] = replacement
                applied_rule = True
                fix_explanation = f"Replaced hardcoded credential with os.environ.get('{env_key}')"

    # Strategy 2: Dangerous React HTML rendering & DOM innerHTML (TG-INPUT-003)
    elif rule_id == "TG-INPUT-003":
        if "dangerouslySetInnerHTML" in target_line:
            var_match = re.search(r'__html\s*:\s*([A-Za-z0-9_$.]+)', target_line)
            var_name = var_match.group(1) if var_match else "content"
            replacement = f'{indent}<div>{{{var_name}}}</div>'
            new_lines[line_number - 1] = replacement
            applied_rule = True
            fix_explanation = "Replaced raw dangerouslySetInnerHTML injection with safe React text interpolation"
        elif ".innerHTML" in target_line:
            if re.search(r'\.innerHTML\s*=\s*["\']["\']', target_line):
                fixed_line = re.sub(r'([a-zA-Z0-9_$]+)\.innerHTML\s*=\s*["\']["\']', r'\1.textContent = ""', target_line)
                if fixed_line != target_line:
                    new_lines[line_number - 1] = fixed_line
                    applied_rule = True
                    fix_explanation = "Replaced unsafe innerHTML DOM reset with safe textContent assignment"
            elif re.search(r'([a-zA-Z0-9_$]+)\.innerHTML\s*=\s*([a-zA-Z0-9_$.]+)\s*;?$', target_line):
                fixed_line = re.sub(r'([a-zA-Z0-9_$]+)\.innerHTML\s*=\s*([a-zA-Z0-9_$.]+)', r'\1.textContent = \2', target_line)
                if fixed_line != target_line:
                    new_lines[line_number - 1] = fixed_line
                    applied_rule = True
                    fix_explanation = "Replaced raw DOM innerHTML assignment with XSS-safe textContent"

    # Strategy 3: Raw SQL Concatenation (TG-INPUT-002)
    elif rule_id == "TG-INPUT-002":
        if file_path.endswith(".py") and ("f\"SELECT" in target_line or "f'SELECT" in target_line):
            fixed_line = re.sub(r'f(["\']SELECT.*?WHERE.*?)(\{[^}]+\})', r'\1%s', target_line)
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Replaced unsafe Python SQL f-string interpolation with parameterized SQL query placeholder"
        elif file_path.endswith((".js", ".jsx", ".ts", ".tsx", ".mjs")):
            # Template string SQL injection: `SELECT ... ${var}` -> parameterized placeholder
            if "`SELECT" in target_line or "`select" in target_line:
                fixed_line = re.sub(r'\$\{[^}]+\}', '?', target_line)
                if fixed_line != target_line:
                    new_lines[line_number - 1] = fixed_line
                    applied_rule = True
                    fix_explanation = "Replaced template literal SQL string interpolation with parameterized SQL placeholder (?)"

    # Strategy 4: Multi-Tenant Query Scoping (TG-DB-004)
    elif rule_id == "TG-DB-004":
        if ".objects.get(" in target_line and "tenant" not in target_line.lower() and "org" not in target_line.lower():
            fixed_line = target_line.replace(".objects.get(", ".objects.get(organization_id=request.user.organization_id, ")
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Added explicit organization_id tenant boundary filter to ORM query"
        elif "findUnique(" in target_line and "tenant" not in target_line.lower():
            fixed_line = target_line.replace("findUnique({ where: {", "findFirst({ where: { tenantId: req.tenantId,")
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Enforced tenantId multi-tenant isolation in Prisma lookup"

    # Strategy 5: Permissive CORS with Credentials (TG-PLATFORM-001)
    elif rule_id == "TG-PLATFORM-001":
        if "CORS_ALLOW_ALL_ORIGINS = True" in target_line:
            replacement = f'{indent}CORS_ALLOWED_ORIGINS = [os.environ.get("ALLOWED_ORIGIN", "https://app.example.com")]'
            new_lines[line_number - 1] = replacement
            applied_rule = True
            fix_explanation = "Replaced wildcard CORS configuration with strict origin whitelist environment variable"
        elif "cors(" in target_line and ("origin: '*'" in target_line or 'origin: "*"' in target_line):
            fixed_line = target_line.replace("origin: '*'", "origin: process.env.ALLOWED_ORIGIN || 'http://localhost:5173'")
            fixed_line = fixed_line.replace('origin: "*"', "origin: process.env.ALLOWED_ORIGIN || 'http://localhost:5173'")
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Constrained wildcard CORS origin to process.env.ALLOWED_ORIGIN with secure fallback"

    # Strategy 6: Cookie Missing Security Flags (TG-AUTH-004)
    elif rule_id == "TG-AUTH-004":
        if "res.cookie(" in target_line and "httpOnly" not in target_line:
            # res.cookie('token', token) -> res.cookie('token', token, { httpOnly: true, secure: process.env.NODE_ENV === 'production', sameSite: 'lax' })
            fixed_line = re.sub(
                r'res\.cookie\(\s*([a-zA-Z0-9_\'\"]+)\s*,\s*([a-zA-Z0-9_]+)\s*\)',
                r"res.cookie(\1, \2, { httpOnly: true, secure: process.env.NODE_ENV === 'production', sameSite: 'lax' })",
                target_line
            )
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Injected mandatory security flags (httpOnly, secure, sameSite) to cookie definition"

    # Strategy 7: Path Traversal (TG-INPUT-006)
    elif rule_id == "TG-INPUT-006":
        if "path.join(" in target_line and "path.basename" not in target_line:
            fixed_line = re.sub(r'path\.join\((.*?),\s*([a-zA-Z0-9_$.]+)\)', r'path.join(\1, path.basename(\2))', target_line)
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Wrapped dynamic path segment in path.basename to neutralize path traversal sequences"
        elif "os.path.join(" in target_line and "os.path.basename" not in target_line:
            fixed_line = re.sub(r'os\.path\.join\((.*?),\s*([a-zA-Z0-9_$.]+)\)', r'os.path.join(\1, os.path.basename(\2))', target_line)
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Wrapped dynamic path segment in os.path.basename to neutralize path traversal sequences"

    # Strategy 8: TLS Verification Bypass (TG-DIFF-001)
    elif rule_id == "TG-DIFF-001":
        if "verify=False" in target_line:
            fixed_line = target_line.replace("verify=False", "verify=True")
            new_lines[line_number - 1] = fixed_line
            applied_rule = True
            fix_explanation = "Restored mandatory TLS certificate verification (verify=True)"
        elif "rejectUnauthorized: false" in target_line:
            fixed_line = target_line.replace("rejectUnauthorized: false", "rejectUnauthorized: true")
            new_lines[line_number - 1] = fixed_line
            applied_rule = True
            fix_explanation = "Restored TLS certificate authority validation (rejectUnauthorized: true)"
        elif "InsecureSkipVerify: true" in target_line:
            fixed_line = target_line.replace("InsecureSkipVerify: true", "InsecureSkipVerify: false")
            new_lines[line_number - 1] = fixed_line
            applied_rule = True
            fix_explanation = "Restored mandatory TLS certificate validation (InsecureSkipVerify: false)"


    # Strategy 9: Hardcoded Database / Service Credential in Config (TG-SEC-003)
    elif rule_id == "TG-SEC-003":
        if "=" in target_line:
            var_match = re.match(r'^\s*([A-Za-z0-9_]+)\s*=', target_line)
            if var_match:
                vname = var_match.group(1)
                fixed_line = f'{indent}{vname} = os.environ.get("{vname}", "")' if file_path.endswith('.py') else f'{indent}const {vname} = process.env.{vname} || "";'
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = f"Extracted sensitive config variable {vname} to environment variable"

    # Strategy 10: Weak Password Hashing (TG-AUTH-001)
    elif rule_id == "TG-AUTH-001":
        if "hashlib.md5" in target_line:
            fixed_line = target_line.replace("hashlib.md5(", "hashlib.sha256(")
            new_lines[line_number - 1] = fixed_line
            applied_rule = True
            fix_explanation = "Replaced broken MD5 hashing with SHA-256 (or bcrypt/argon2)"
        elif "createHash('md5')" in target_line:
            fixed_line = target_line.replace("createHash('md5')", "createHash('sha256')")
            new_lines[line_number - 1] = fixed_line
            applied_rule = True
            fix_explanation = "Replaced broken MD5 hashing with SHA-256"

    # Strategy 11: JWT Missing Algorithm Restriction (TG-AUTH-003)
    elif rule_id == "TG-AUTH-003":
        if "jwt.verify(" in target_line and "algorithms" not in target_line:
            fixed_line = re.sub(r'jwt\.verify\(\s*([^,\)]+)\s*,\s*([^,\)]+)\s*\)', r"jwt.verify(\1, \2, { algorithms: ['HS256'] })", target_line)
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Restricted JWT verification to explicit algorithm list ['HS256']"

    # Strategy 12: Untrusted Role/Tenant Header Injection (TG-AUTH-008)
    elif rule_id == "TG-AUTH-008":
        if "req.headers[" in target_line or "request.headers.get(" in target_line:
            if file_path.endswith((".js", ".ts")):
                fixed_line = f'{indent}const role = req.user ? req.user.role : "user"; // Derived securely from authenticated session'
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Replaced unverified client HTTP header with verified session-derived identity"
            elif file_path.endswith(".py"):
                fixed_line = f'{indent}role = getattr(request.user, "role", "user") # Derived securely from authenticated session'
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Replaced unverified client HTTP header with verified session-derived identity"

    # Strategy 13: Rate Limiting Injection (TG-RATE-001)
    elif rule_id == "TG-RATE-001":
        if re.search(r'\.(?:post|all)\s*\(\s*[\'"][^\'"]+[\'"]\s*,\s*(?:async\s*)?\(', target_line):
            fixed_line = re.sub(
                r'(\.(?:post|all)\s*\(\s*[\'"][^\'"]+[\'"]\s*),\s*((?:async\s*)?\()',
                r'\1, authLimiter, \2',
                target_line
            )
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Injected authLimiter rate-limiting middleware to protect authentication endpoint from brute force"

    # Strategy 14: Prompt Injection System Context Isolation (TG-AGENT-001)
    elif rule_id == "TG-AGENT-001":
        if 'role": "system"' in target_line or "role': 'system'" in target_line:
            fixed_line = target_line.replace('"role": "system"', '"role": "user"')
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Demoted untrusted user input from system prompt into role: 'user' message container"

    # Strategy 15: Outbound URL Fetch Validation (TG-SSRF-001)
    elif rule_id == "TG-SSRF-001":
        if "fetch(" in target_line and "validateUrl(" not in target_line:
            fixed_line = re.sub(r'fetch\(\s*([^,\)]+)', r'fetch(validateSafeUrl(\1)', target_line)
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Wrapped outbound URL in validateSafeUrl domain whitelist guard"
        elif "requests.get(" in target_line and "validate_url(" not in target_line:
            fixed_line = re.sub(r'requests\.get\(\s*([^,\)]+)', r'requests.get(validate_safe_url(\1)', target_line)
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Wrapped outbound URL in validate_safe_url domain whitelist guard"

    # Strategy 16: Outbound Request Timeout (TG-SSRF-004)
    elif rule_id == "TG-SSRF-004":
        if "requests.get(" in target_line and "timeout=" not in target_line:
            fixed_line = target_line.replace(")", ", timeout=10)")
            new_lines[line_number - 1] = fixed_line
            applied_rule = True
            fix_explanation = "Injected explicit 10-second request timeout to prevent resource exhaustion"

    # Strategy 17: Production Debug Mode Disablement (TG-PLATFORM-003)
    elif rule_id == "TG-PLATFORM-003":
        if "DEBUG = True" in target_line:
            fixed_line = f'{indent}DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ("true", "1")'
            new_lines[line_number - 1] = fixed_line
            applied_rule = True
            fix_explanation = "Guard DEBUG mode behind DJANGO_DEBUG environment variable"

    # Strategy 18: Production Introspection Disablement (TG-GQL-004)
    elif rule_id == "TG-GQL-004":
        if "introspection: true" in target_line or "introspection: True" in target_line:
            fixed_line = re.sub(r'introspection\s*:\s*(?:true|True)', 'introspection: process.env.NODE_ENV !== "production"', target_line)
            new_lines[line_number - 1] = fixed_line
    # Strategy 19: Privileged Database Credential in Frontend (TG-DB-002)
    elif rule_id == "TG-DB-002":
        if "SUPABASE_SERVICE_ROLE_KEY" in target_line:
            var_match = re.search(r'(export\s+const|const)\s+([A-Za-z0-9_]+)\s*=', target_line)
            var_name = var_match.group(2) if var_match else "SUPABASE_SERVICE_ROLE_KEY"
            replacement = f'{indent}export const {var_name} = process.env.{var_name} || "";'
            new_lines[line_number - 1] = replacement
            applied_rule = True
            fix_explanation = f"Replaced hardcoded privileged database credential with process.env.{var_name}"

    # Strategy 20: Public Source Maps in Production (TG-CLIENT-001)
    elif rule_id == "TG-CLIENT-001":
        if "sourcemap: true" in target_line:
            fixed_line = target_line.replace("sourcemap: true", "sourcemap: false")
            new_lines[line_number - 1] = fixed_line
            applied_rule = True
            fix_explanation = "Disabled public production source map emission"

    # Strategy 21: Sensitive Information in Logs (TG-SEC-004)
    elif rule_id == "TG-SEC-004":
        if "console.log" in target_line:
            fixed_line = f"{indent}// Security: Sensitive credential log removed per TG-SEC-004"
            new_lines[line_number - 1] = fixed_line
            applied_rule = True
            fix_explanation = "Redacted console logging of sensitive token or credential"

    # Strategy 22: Unlimited Public Write Endpoint (TG-RATE-002)
    elif rule_id == "TG-RATE-002":
        if re.search(r'\.(?:post|put|patch)\s*\(\s*[\'"][^\'"]+[\'"]\s*,\s*(?:async\s*)?\(', target_line):
            fixed_line = re.sub(
                r'(\.(?:post|put|patch)\s*\(\s*[\'"][^\'"]+[\'"]\s*),\s*((?:async\s*)?\()',
                r'\1, writeLimiter, \2',
                target_line
            )
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Injected writeLimiter rate-limiting middleware to public write endpoint"

    # Strategy 23: Missing Security Headers (TG-PLATFORM-002)
    elif rule_id == "TG-PLATFORM-002":
        if "const app = express();" in target_line:
            replacement = f'{indent}const helmet = require("helmet");\n{indent}const app = express();\n{indent}app.use(helmet());'
            new_lines[line_number - 1] = replacement
            applied_rule = True
            fix_explanation = "Injected helmet security headers middleware into Express application"

    # Strategy 24: Missing Request Body Validation (TG-INPUT-001)
    elif rule_id == "TG-INPUT-001":
        if "req.body" in target_line and ("const {" in target_line or "let {" in target_line):
            replacement = f'{indent}if (!req.body || typeof req.body !== "object") return res.status(400).json({{ error: "Invalid payload" }});\n{target_line}'
            new_lines[line_number - 1] = replacement
            applied_rule = True
            fix_explanation = "Added defensive request body payload validation before destructuring"

    if not applied_rule:
        return None

    # Calculate unified diff
    orig_lines = [l + "\n" for l in lines]
    patched_lines = [l + "\n" for l in new_lines]
    diff = "".join(difflib.unified_diff(
        orig_lines, patched_lines,
        fromfile=f"a/{file_path}", tofile=f"b/{file_path}",
        n=2
    ))

    additions = sum(1 for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
    deletions = sum(1 for l in diff.splitlines() if l.startswith("-") and not l.startswith("---"))

    # Ponytail bounds validation: <= 35 additions, <= 25 deletions
    if additions > 35 or deletions > 25:
        return None

    bundle_id = f"bnd-{rule_id.lower()}-{line_number}-{hashlib.sha256(diff.encode('utf-8')).hexdigest()[:6]}"

    return {
        "bundle_id": bundle_id,
        "finding_id": finding.get("finding_id", f"{rule_id}-{line_number}"),
        "rule_id": rule_id,
        "title": finding.get("title", rule_id),
        "target_file": file_path,
        "line_number": line_number,
        "target_line": target_line,
        "replacement_line": new_lines[line_number - 1],
        "what_is_wrong": description,
        "why_it_matters": "Security vulnerability violating TorusGuard strict production safety invariant.",
        "what_should_change": fix_explanation,
        "proposed_diff": diff,
        "additions": additions,
        "deletions": deletions,
        "patched_content": "\n".join(new_lines)
    }


def execute_harden(target_root: Path, run_id_arg: Optional[str] = None) -> Dict[str, Any]:
    """Execute autonomous remediation formulation and package candidate bundles."""
    runs_dir = target_root / ".torusguard" / "runs"
    if run_id_arg:
        run_folder = runs_dir / run_id_arg
    else:
        run_folder = find_latest_audit_run(runs_dir)

    if not run_folder or not run_folder.is_dir():
        print(f"\n  {RED}✖ No audit runs found to harden.{RESET}")
        print(f"  Run {CYAN}npx torusguard audit{RESET} first to discover actionable findings.\n")
        sys.exit(1)

    findings_file = run_folder / "findings.json"
    if not findings_file.is_file():
        print(f"\n  {RED}✖ Missing findings.json in run folder:{RESET} {run_folder}\n")
        sys.exit(1)

    try:
        findings = json.loads(findings_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"\n  {RED}✖ Failed to parse findings.json:{RESET} {e}\n")
        sys.exit(1)

    bundles_dir = run_folder / "bundles"
    bundles_dir.mkdir(parents=True, exist_ok=True)

    bundles = []
    seen_file_lines = set()
    for f in findings:
        target_key = (f.get("file_path"), f.get("line_number"))
        if target_key in seen_file_lines:
            continue
        candidate = generate_patch_for_finding(f, target_root)
        if candidate:
            seen_file_lines.add(target_key)
            bundles.append(candidate)
            b_dir = bundles_dir / candidate["bundle_id"]
            b_dir.mkdir(parents=True, exist_ok=True)

            # 1. patch.diff
            (b_dir / "patch.diff").write_text(candidate["proposed_diff"], encoding="utf-8")

            # 2. minimal_patch_plan.md
            plan_content = [
                f"# Remediation Plan: {candidate['bundle_id']}",
                f"- **Rule ID:** `{candidate['rule_id']}`",
                f"- **Target File:** `{candidate['target_file']}:{candidate['line_number']}`",
                f"- **Ponytail Churn:** `+{candidate['additions']} / -{candidate['deletions']}` (Compliant <=35/<=25)",
                f"\n## Proposed Change\n{candidate['what_should_change']}\n",
                "## Unified Diff Preview\n```diff",
                candidate["proposed_diff"],
                "```"
            ]
            (b_dir / "minimal_patch_plan.md").write_text("\n".join(plan_content), encoding="utf-8")

            # 3. metadata.json
            with open(b_dir / "metadata.json", "w", encoding="utf-8") as mf:
                json.dump(candidate, mf, indent=2)

    # Render run-level remediation.md
    remediation_lines = [
        f"# TorusGuard Governed Remediation Catalog",
        f"**Run ID:** `{run_folder.name}`  ",
        f"**Generated:** `{get_ist_now().strftime('%Y-%m-%d %H:%M:%S IST')}`  ",
        f"**Candidate Bundles Formulated:** `{len(bundles)}`  \n",
        "---",
        "## Formulated Candidate Patches\n"
    ]

    for b in bundles:
        remediation_lines.append(f"### [{b['rule_id']}] {b['title']}")
        remediation_lines.append(f"- **Target:** `{b['target_file']}:{b['line_number']}` | **Bundle ID:** `{b['bundle_id']}`")
        remediation_lines.append(f"- **Strategy:** {b['what_should_change']}")
        remediation_lines.append(f"- **Ponytail Churn:** `+{b['additions']} / -{b['deletions']}`")
        remediation_lines.append("```diff")
        remediation_lines.append(b["proposed_diff"].strip())
        remediation_lines.append("```\n")

    (run_folder / "remediation.md").write_text("\n".join(remediation_lines), encoding="utf-8")
    try:
        import report_sync
        report_sync.record_harden_bundles(target_root, bundles, run_folder.name)
    except Exception:
        pass

    # Update manifest
    manifest_file = run_folder / "manifest.json"
    if manifest_file.is_file():
        try:
            mdata = json.loads(manifest_file.read_text(encoding="utf-8"))
            mdata["remediation_bundles_count"] = len(bundles)
            manifest_file.write_text(json.dumps(mdata, indent=2), encoding="utf-8")
        except Exception:
            pass

    # Print 75-column Terminal Cards
    print()
    print(box_header("🛡️  TORUSGUARD GOVERNED REMEDIATION ENGINE", "Autonomous Minimal Patch Formulation & Ponytail Packaging", "v1.3.5"))
    print()

    print(border_top("Remediation Scope"))
    print(box_line(f"Active Run:     {WHITE}{run_folder.name}{RESET}"))
    print(box_line(f"Target Scope:   {WHITE}{target_root}{RESET}"))
    print(box_line(f"Total Findings: {len(findings)} evaluated | {GREEN}{len(bundles)} surgical patches formulated{RESET}"))
    print(box_line(f"Ponytail Guard: {GREEN}All patches strictly <= 35 additions, <= 25 deletions{RESET}"))
    print(border_bottom())
    print()

    if bundles:
        print(border_top(f"Formulated Candidate Patches ({len(bundles)})"))
        for b in bundles[:5]:
            print(box_line(f"{YELLOW}[{b['rule_id']}]{RESET} {WHITE}{b['target_file']}:{b['line_number']}{RESET} (+{b['additions']}/-{b['deletions']})"))
            print(box_line(f"  └─ {DIM}{b['what_should_change']}{RESET}"))
        if len(bundles) > 5:
            print(box_line(f"  ... and {len(bundles) - 5} more patches cataloged in remediation.md"))
        print(border_bottom())
        print()

        print(border_top("Next Governed Action", border_color=GREEN, double=True))
        print(box_line(f"Living Report:    {CYAN}security_report.md (patch previews attached){RESET}", border="║", border_color=GREEN))
        print(box_line(f"Review & Apply:   {BOLD}{WHITE}npx torusguard apply{RESET}  (CLI Human Gate)", border="║", border_color=GREEN))
        print(box_line(f"Auto-Apply Flag:  {CYAN}npx torusguard apply --yes{RESET} (Automated mode)", border="║", border_color=GREEN))
        print(box_line(f"AI IDE Chat:      Run {CYAN}/torusguard-apply{RESET} in your AI chat", border="║", border_color=GREEN))
        print(border_bottom(border_color=GREEN, double=True))
        print()
    else:
        print(f"  {YELLOW}ℹ No automatic patch templates matched current findings.{RESET}")
        print(f"  {GRAY}Findings require architectural refactoring or AI-assisted guidance.{RESET}\n")
        print(border_top("Recommended Next Steps"))
        print(box_line("1. In AI Chat: Run /torusguard-harden to synthesize custom fixes"))
        print(box_line("2. View visual posture report: npx torusguard report --html"))
        print(box_line(f"3. Inspect findings: .torusguard/runs/{run_folder.name}/findings.md"))
        print(border_bottom())
        print()

    return {
        "status": "success",
        "run_folder": str(run_folder),
        "bundles_count": len(bundles),
        "bundles": bundles
    }


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Autonomous Governed Remediation Engine")
    parser.add_argument("path", nargs="?", default=".", help="Target project root directory")
    parser.add_argument("--run", "-r", help="Explicit run ID to harden (default: latest audit run)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    target = Path(args.path).resolve()
    result = execute_harden(target, run_id_arg=args.run)

    if args.json:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
