#!/usr/bin/env python3
"""
TorusGuard Autonomous Remediation Engine (v1.3.3)
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

def box_header(title: str, subtitle: str = "", version: str = "v1.3.3", border_color: str = CYAN) -> str:
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
    print(box_header("🛡️  TORUSGUARD GOVERNED REMEDIATION ENGINE", "Autonomous Minimal Patch Formulation & Ponytail Packaging", "v1.3.3"))
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
