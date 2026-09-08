#!/usr/bin/env python3
"""
TorusGuard Autonomous Remediation Engine (v1.3.0)
Evaluates audit findings against canonical patch templates, enforces Ponytail bounds
(<= 35 additions, <= 25 deletions), packages structured candidate remediation bundles,
and renders unified patch diffs.

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
import unicodedata
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

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

# ─── ANSI Colors & Formatter ───────────────────────────────────────────────────
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
WHITE = "\033[97m"
GRAY = "\033[90m"
RED = "\033[31m"

ANSI_REGEX = re.compile(r'\033\[[0-9;]*m')

def get_visual_width(text: str) -> int:
    clean = ANSI_REGEX.sub('', text)
    width = 0
    for ch in clean:
        ea = unicodedata.east_asian_width(ch)
        if ea in ('W', 'F'):
            width += 2
        elif ord(ch) >= 0x1F300:
            width += 2
        else:
            width += 1
    return width

def format_box_line(content: str, width: int = 71, border: str = "│", border_color: str = CYAN) -> str:
    vis = get_visual_width(content)
    pad = " " * max(0, width - vis)
    return f"  {border_color}{border}{RESET}  {content}{pad}{border_color}{border}{RESET}"


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
    indent = re.match(r'^\s*', target_line).group(0) # type: ignore
    new_lines = list(lines)
    applied_rule = False
    fix_explanation = ""

    # Strategy 1: Hardcoded Secrets (TG-SEC-001 / TG-SEC-002)
    if rule_id in ("TG-SEC-001", "TG-SEC-002"):
        if file_path.endswith((".js", ".jsx", ".ts", ".tsx", ".mjs")):
            # const secret = "..." -> const secret = process.env.JWT_SECRET || "...";
            if re.search(r'(jwt_secret|jwtSecret|JWT_SECRET)', target_line, re.IGNORECASE):
                replacement = f'{indent}const secret = process.env.JWT_SECRET || "";'
                new_lines[line_number - 1] = replacement
                applied_rule = True
                fix_explanation = "Migrated hardcoded JWT secret to environment variable process.env.JWT_SECRET"
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

    # Strategy 2: Dangerous React HTML rendering (TG-INPUT-003)
    elif rule_id == "TG-INPUT-003":
        if "dangerouslySetInnerHTML" in target_line:
            # <div dangerouslySetInnerHTML={{ __html: bio }} /> -> <div>{bio}</div>
            var_match = re.search(r'__html\s*:\s*([A-Za-z0-9_]+)', target_line)
            var_name = var_match.group(1) if var_match else "content"
            replacement = f'{indent}<div>{{{var_name}}}</div>'
            new_lines[line_number - 1] = replacement
            applied_rule = True
            fix_explanation = "Replaced raw dangerouslySetInnerHTML injection with safe React text interpolation"

    # Strategy 3: Raw SQL Concatenation (TG-INPUT-002)
    elif rule_id == "TG-INPUT-002":
        if file_path.endswith(".py") and ("f\"SELECT" in target_line or "f'SELECT" in target_line):
            # Replace f-string injection with parameterized query
            fixed_line = re.sub(r'f(["\']SELECT.*?WHERE.*?)(\{[^}]+\})', r'\1%s', target_line)
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Replaced unsafe Python SQL f-string interpolation with parameterized SQL query placeholder"

    # Strategy 4: Multi-Tenant Query Scoping (TG-DB-004)
    elif rule_id == "TG-DB-004":
        if ".objects.get(" in target_line and "tenant" not in target_line.lower() and "org" not in target_line.lower():
            # .objects.get(id=...) -> .objects.get(id=..., organization_id=request.user.organization_id)
            fixed_line = target_line.replace(".objects.get(", ".objects.get(organization_id=request.user.organization_id, ")
            if fixed_line != target_line:
                new_lines[line_number - 1] = fixed_line
                applied_rule = True
                fix_explanation = "Added explicit organization_id tenant boundary filter to ORM query"

    # Strategy 5: Permissive CORS with Credentials (TG-PLATFORM-001)
    elif rule_id == "TG-PLATFORM-001":
        if "CORS_ALLOW_ALL_ORIGINS = True" in target_line:
            replacement = f'{indent}CORS_ALLOWED_ORIGINS = [os.environ.get("ALLOWED_ORIGIN", "https://app.example.com")]'
            new_lines[line_number - 1] = replacement
            applied_rule = True
            fix_explanation = "Replaced wildcard CORS configuration with strict origin whitelist environment variable"

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

    # Ponytail bounds validation
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
    for f in findings:
        candidate = generate_patch_for_finding(f, target_root)
        if candidate:
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

    # Print 75-column Terminal Card
    print(f"\n  {CYAN}╭─────────────────────────────────────────────────────────────────────────╮{RESET}")
    print(f"  {CYAN}│                                                                         │{RESET}")
    print(format_box_line(f"{BOLD}🛡️  TORUSGUARD GOVERNED REMEDIATION ENGINE         v1.3.0{RESET}", border_color=CYAN))
    print(format_box_line(f"{DIM}Autonomous Minimal Patch Formulation & Ponytail Packaging{RESET}", border_color=CYAN))
    print(f"  {CYAN}│                                                                         │{RESET}")
    print(f"  {CYAN}╰─────────────────────────────────────────────────────────────────────────╯{RESET}\n")

    print(f"  {CYAN}┌─ Remediation Scope ─────────────────────────────────────────────────────┐{RESET}")
    print(format_box_line(f"Active Run:     {WHITE}{run_folder.name}{RESET}"))
    print(format_box_line(f"Target Scope:   {WHITE}{target_root}{RESET}"))
    print(format_box_line(f"Total Findings: {len(findings)} evaluated | {GREEN}{len(bundles)} surgical patches formulated{RESET}"))
    print(format_box_line(f"Ponytail Guard: {GREEN}All patches strictly <= 35 additions, <= 25 deletions{RESET}"))
    print(f"  {CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}\n")

    if bundles:
        print(f"  {CYAN}┌─ Formulated Candidate Patches ({len(bundles)}) ───────────────────────────────────┐{RESET}")
        for b in bundles[:5]:
            print(format_box_line(f"{YELLOW}[{b['rule_id']}]{RESET} {WHITE}{b['target_file']}:{b['line_number']}{RESET} (+{b['additions']}/-{b['deletions']})"))
            print(format_box_line(f"  └─ {DIM}{b['what_should_change']}{RESET}"))
        if len(bundles) > 5:
            print(format_box_line(f"  ... and {len(bundles) - 5} more patches cataloged in remediation.md"))
        print(f"  {CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}\n")
    else:
        print(f"  {YELLOW}ℹ No automatic patch templates matched current findings.{RESET}\n")

    print(f"  {GREEN}╔═ Next Governed Action ═════════════════════════════════════════════════════╗{RESET}")
    print(format_box_line(f"Review & Apply:   {BOLD}{WHITE}npx torusguard apply{RESET}  (CLI Human Gate)", border="║", border_color=GREEN))
    print(format_box_line(f"Auto-Apply Flag:  {CYAN}npx torusguard apply --yes{RESET} (Automated mode)", border="║", border_color=GREEN))
    print(format_box_line(f"AI IDE Chat:      Run {CYAN}/torusguard-apply{RESET} in your AI chat", border="║", border_color=GREEN))
    print(f"  {GREEN}╚═════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

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
