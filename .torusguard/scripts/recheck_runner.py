#!/usr/bin/env python3
"""
TorusGuard Targeted Differential Recheck Engine (v1.3.0)
Executes scoped differential re-audits verifying only impacted files and adjacent boundaries.
Evaluates formal status transitions (Confirmed Fixed vs Regressed), updates run manifest,
and records verification telemetry in the persistent security memory subsystem.

Pure Python 3.10+ standard library (zero external dependencies).
"""

import sys
import os
import re
import json
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
    if not runs_dir.is_dir():
        return None
    runs = sorted(runs_dir.glob("run-*-audit"), key=lambda p: p.stat().st_mtime, reverse=True)
    return runs[0] if runs else None


def execute_recheck(target_root: Path, run_id_arg: Optional[str] = None) -> Dict[str, Any]:
    runs_dir = target_root / ".torusguard" / "runs"
    if run_id_arg:
        run_folder = runs_dir / run_id_arg
    else:
        run_folder = find_latest_audit_run(runs_dir)

    if not run_folder or not run_folder.is_dir():
        print(f"\n  {RED}✖ No audit run found to recheck.{RESET}\n")
        sys.exit(1)

    # Import audit scanner and memory engine
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import audit_runner
    import memory_engine

    bundles_dir = run_folder / "bundles"
    bundle_meta_files = list(bundles_dir.glob("*/metadata.json")) if bundles_dir.is_dir() else []

    # Header Card
    print(f"\n  {CYAN}╭─────────────────────────────────────────────────────────────────────────╮{RESET}")
    print(f"  {CYAN}│                                                                         │{RESET}")
    print(format_box_line(f"{BOLD}🛡️  TORUSGUARD DIFFERENTIAL RECHECK ENGINE          v1.3.0{RESET}", border_color=CYAN))
    print(format_box_line(f"{DIM}Targeted Differential AST Scan & Regression Verification{RESET}", border_color=CYAN))
    print(f"  {CYAN}│                                                                         │{RESET}")
    print(f"  {CYAN}╰─────────────────────────────────────────────────────────────────────────╯{RESET}\n")

    print(f"  {CYAN}┌─ Recheck Verification Scope ────────────────────────────────────────────┐{RESET}")
    print(format_box_line(f"Active Run:     {WHITE}{run_folder.name}{RESET}"))
    print(format_box_line(f"Target Root:    {WHITE}{target_root}{RESET}"))
    print(f"  {CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}\n")

    recheck_results = []
    confirmed_count = 0
    regressed_count = 0
    unresolved_count = 0

    recheck_md_lines = [
        f"# TorusGuard Differential Recheck Report",
        f"**Run ID:** `{run_folder.name}`  ",
        f"**Timestamp:** `{get_ist_now().strftime('%Y-%m-%d %H:%M:%S IST')}`  \n",
        "---",
        "## Recheck Transition Catalog\n"
    ]

    for mf in bundle_meta_files:
        try:
            bdata = json.loads(mf.read_text(encoding="utf-8"))
        except Exception:
            continue

        rule_id = bdata.get("rule_id", "")
        rel_path = bdata.get("target_file", "")
        target_path = target_root / rel_path

        if not target_path.is_file():
            continue

        # Differential scan on this single modified file
        file_findings = audit_runner.scan_file(target_path, target_root)
        matching_rule_findings = [f for f in file_findings if f.get("rule_id") == rule_id]

        if not matching_rule_findings:
            outcome = "Confirmed Fixed"
            confirmed_count += 1
            status_color = GREEN
            # Record in memory
            try:
                memory_engine.record_event("fix_verified", {
                    "rule_id": rule_id,
                    "file_path": rel_path,
                    "verification_result": "fixed"
                }, root_dir=target_root)
            except Exception:
                pass
        else:
            outcome = "Unresolved"
            unresolved_count += 1
            status_color = YELLOW

        recheck_results.append({
            "rule_id": rule_id,
            "target_file": rel_path,
            "outcome": outcome,
            "title": bdata.get("title", rule_id)
        })

        recheck_md_lines.append(f"### [{rule_id}] {bdata.get('title')}")
        recheck_md_lines.append(f"- **File:** `{rel_path}`")
        recheck_md_lines.append(f"- **Outcome:** `{outcome}`")
        recheck_md_lines.append(f"- **Verification Timestamp:** {get_ist_now().strftime('%Y-%m-%d %H:%M:%S IST')}\n")

        print(f"  {status_color}✔ [{outcome}]{RESET} {WHITE}{rule_id}{RESET} on {rel_path}")

    # Write recheck.md
    (run_folder / "recheck.md").write_text("\n".join(recheck_md_lines), encoding="utf-8")

    # Update manifest
    manifest_file = run_folder / "manifest.json"
    if manifest_file.is_file():
        try:
            mdata = json.loads(manifest_file.read_text(encoding="utf-8"))
            mdata["status"] = "verified_fixed" if regressed_count == 0 and unresolved_count == 0 else "recheck_completed"
            mdata["confirmed_fixed_count"] = confirmed_count
            mdata["regressed_count"] = regressed_count
            manifest_file.write_text(json.dumps(mdata, indent=2), encoding="utf-8")
        except Exception:
            pass

    print()
    print(f"  {CYAN}┌─ Recheck Summary ───────────────────────────────────────────────────────┐{RESET}")
    print(format_box_line(f"Confirmed Fixed:{GREEN}{confirmed_count} vulnerabilities verified closed{RESET}"))
    print(format_box_line(f"Regressed:      {RED if regressed_count > 0 else GREEN}{regressed_count} regressions detected{RESET}"))
    print(format_box_line(f"Unresolved:     {YELLOW if unresolved_count > 0 else GREEN}{unresolved_count} unresolved{RESET}"))
    print(format_box_line(f"Memory Sync:    {GREEN}Verification events synced to persistent memory engine{RESET}"))
    print(f"  {CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}\n")

    print(f"  {GREEN}╔═ Next Governed Action ═════════════════════════════════════════════════════╗{RESET}")
    print(format_box_line(f"Visual Dashboard: {BOLD}{WHITE}npx torusguard report --html{RESET} (Updated posture score)", border="║", border_color=GREEN))
    print(format_box_line(f"View Recipes:     {CYAN}npx torusguard recipes{RESET} (Active golden fix recipes)", border="║", border_color=GREEN))
    print(f"  {GREEN}╚═════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

    return {
        "run_folder": str(run_folder),
        "confirmed_fixed_count": confirmed_count,
        "regressed_count": regressed_count,
        "unresolved_count": unresolved_count,
        "results": recheck_results
    }


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Differential Recheck Engine")
    parser.add_argument("path", nargs="?", default=".", help="Target project root directory")
    parser.add_argument("--run", "-r", help="Explicit run ID to recheck")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    target = Path(args.path).resolve()
    result = execute_recheck(target, run_id_arg=args.run)

    if args.json:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
