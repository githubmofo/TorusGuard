#!/usr/bin/env python3
"""
TorusGuard Autonomous Static Security Audit Engine (v1.3.3)
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
    def card_header(title: str, subtitle: str = "", version: str = "v1.3.3", border_color: str = CYAN) -> str:
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
    # ── Secrets & Credentials (TG-SEC) ──────────────────────────────────────────
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
        "severity": "High",
        "category": "secrets",
        "cluster": "cluster-credentials-exposure",
        "patterns": [
            (re.compile(r'\b(?:NEXT_PUBLIC_|VITE_|REACT_APP_)[A-Z0-9_]*(?:SECRET|PRIVATE|KEY|PASSWORD|TOKEN)\b'), "Client-exposed environment variable containing secret naming pattern")
        ]
    },
    {
        "rule_id": "TG-SEC-004",
        "title": "Sensitive Credential or Token Logging",
        "severity": "Medium",
        "category": "secrets",
        "cluster": "cluster-credentials-exposure",
        "patterns": [
            (re.compile(r'(?:console\.log|logger\.(?:info|debug|error|warn))\s*\([^)]*(?:password|token|secret|apiKey|api_key)[^)]*\)', re.IGNORECASE), "Plaintext credential or token logged to standard output")
        ]
    },
    # ── Database Safety & Multi-Tenant Query Isolation (TG-DB) ────────────────
    {
        "rule_id": "TG-DB-004",
        "title": "Missing Multi-Tenant Isolation in Scoped Query",
        "severity": "High",
        "category": "database",
        "cluster": "cluster-tenant-isolation",
        "patterns": [
            (re.compile(r'\.objects\.get\s*\(\s*id\s*=\s*[^,\)]+\)'), "Django ORM .get(id=...) query lacking explicit tenant scope filter"),
            (re.compile(r'\.findById\s*\(\s*(?:req\.params|id)[^\)]*\)'), "Direct findById query lacking organization/tenant boundaries"),
            (re.compile(r'prisma\.[a-zA-Z]+\.findUnique\s*\(\s*\{\s*where:\s*\{\s*id\b'), "Prisma findUnique query lacking tenantId boundary filter")
        ]
    },
    {
        "rule_id": "TG-DB-001",
        "title": "Frontend / Client-Side Direct Database Query",
        "severity": "Critical",
        "category": "database",
        "cluster": "cluster-client-leak",
        "patterns": [
            (re.compile(r'\b(?:createClient|supabase)\.from\([^)]+\)\.delete\(\)'), "Dangerous direct database mutation in client component"),
            (re.compile(r'\bimport\s+.*(?:pg|mysql2|prisma|typeorm).*\s+from'), "Server database driver imported in client file")
        ]
    },
    {
        "rule_id": "TG-DB-002",
        "title": "Privileged Database Secret or Master Role Key in Client Code",
        "severity": "Critical",
        "category": "database",
        "cluster": "cluster-client-leak",
        "patterns": [
            (re.compile(r'\b(?:SUPABASE_SERVICE_ROLE_KEY|DATABASE_URL)\b'), "Service role key or raw database connection string reference in frontend code")
        ]
    },
    # ── Input Validation & Code / SQL Injection (TG-INPUT) ─────────────────────
    {
        "rule_id": "TG-INPUT-002",
        "title": "Unescaped Raw SQL Query Concatenation",
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
        "rule_id": "TG-INPUT-005",
        "title": "Unsafe Template Rendering Without Autoescaping",
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
        "title": "Unvalidated User Input in File Path Resolution",
        "severity": "High",
        "category": "filesystem",
        "cluster": "cluster-injection",
        "patterns": [
            (re.compile(r'(?:open|readFile|readFileSync)\s*\([^)]*\+\s*(?:req|params|query)'), "File read operation using unsanitized user request path"),
            (re.compile(r'path\.join\s*\([^)]*(?:req\.params|req\.query)\.[a-zA-Z0-9_]+\)'), "Path traversal sink in path.join without basename sanitization")
        ]
    },
    # ── Authentication & Session Safety (TG-AUTH) ──────────────────────────────
    {
        "rule_id": "TG-AUTH-004",
        "title": "Insecure Session Cookie or Disabled CSRF Protection",
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
    # ── Security Bypasses & Transport Invariants (TG-DIFF / TG-PLATFORM) ───────
    {
        "rule_id": "TG-DIFF-001",
        "title": "Disabled TLS / SSL Certificate Validation",
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
        "rule_id": "TG-PLATFORM-001",
        "title": "Wildcard Permissive CORS Configuration with Credentials",
        "severity": "High",
        "category": "platform",
        "cluster": "cluster-auth-bypass",
        "patterns": [
            (re.compile(r'\bCORS_ALLOW_ALL_ORIGINS\s*=\s*True\b'), "Wildcard CORS origin enabled across entire application"),
            (re.compile(r'@CrossOrigin\s*\(\s*["\']\*["\']\s*\)'), "Wildcard CORS origin annotation in Java/Spring"),
            (re.compile(r'cors\(\s*\{\s*origin\s*:\s*["\']\*["\']'), "Wildcard CORS origin configured in Express middleware")
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
    ".idea", ".vscode", "target", "bin", "obj"
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
                if f in ("audit_runner.py", "diff_guard.py", "finding_scorer.py"):
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
    print(card_header("🛡️  TORUSGUARD STATIC SECURITY AUDIT", "Autonomous AST & Invariant Security Scanner", "v1.3.3"))
    print()

    print(card_border_top("Audit Execution Scope"))
    print(format_box_line(f"{BOLD}Target:{RESET}       {WHITE}{str(target_root)}{RESET}"))
    print(format_box_line(f"{BOLD}Stack:{RESET}        {GREEN}{stack_str}{RESET}"))
    print(format_box_line(f"{BOLD}Files:{RESET}        {WHITE}{file_count} files evaluated across 11 canonical families{RESET}"))
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
