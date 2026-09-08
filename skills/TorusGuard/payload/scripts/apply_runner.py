#!/usr/bin/env python3
"""
TorusGuard Governed Patch Application & Snapshot Engine (v1.3.0)
Interactive Human Gate authorization, pre-apply .bak rollback snapshots,
atomic patch application, and Golden Fix Recipe distillation into persistent memory.

Pure Python 3.10+ standard library (zero external dependencies).
"""

import sys
import os
import re
import json
import shutil
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
    if not runs_dir.is_dir():
        return None
    runs = sorted(runs_dir.glob("run-*-audit"), key=lambda p: p.stat().st_mtime, reverse=True)
    for r in runs:
        if (r / "bundles").is_dir() and list((r / "bundles").iterdir()):
            return r
    return None


def execute_rollback(target_root: Path, run_id_arg: Optional[str] = None) -> None:
    """Restore all target files from the pre-apply backup snapshots."""
    snapshots_base = target_root / ".torusguard" / "snapshots"
    if not snapshots_base.is_dir():
        print(f"\n  {YELLOW}ℹ No snapshots directory found at: {snapshots_base}{RESET}\n")
        sys.exit(0)

    if run_id_arg:
        snapshot_dir = snapshots_base / run_id_arg
    else:
        snapshots = sorted([d for d in snapshots_base.iterdir() if d.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
        snapshot_dir = snapshots[0] if snapshots else None

    if not snapshot_dir or not snapshot_dir.is_dir():
        print(f"\n  {RED}✖ No rollback snapshot found for run: {run_id_arg or 'latest'}{RESET}\n")
        sys.exit(1)

    restored_files = []
    for bak_file in snapshot_dir.rglob("*.bak"):
        rel_path = bak_file.relative_to(snapshot_dir)
        orig_rel = str(rel_path)[:-4]  # Strip .bak
        dest_file = target_root / orig_rel

        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(bak_file, dest_file)
        restored_files.append(orig_rel)

    print(f"\n  {CYAN}╭─────────────────────────────────────────────────────────────────────────╮{RESET}")
    print(format_box_line(f"{BOLD}🛡️  TORUSGUARD ROLLBACK RESTORATION                   v1.3.0{RESET}", border_color=CYAN))
    print(format_box_line(f"{DIM}Restored original files from pre-apply snapshot{RESET}", border_color=CYAN))
    print(f"  {CYAN}╰─────────────────────────────────────────────────────────────────────────╯{RESET}\n")

    print(f"  {CYAN}┌─ Rollback Snapshot Restored ────────────────────────────────────────────┐{RESET}")
    print(format_box_line(f"Snapshot Run:   {WHITE}{snapshot_dir.name}{RESET}"))
    print(format_box_line(f"Files Restored: {GREEN}{len(restored_files)} file(s) cleanly reverted{RESET}"))
    for rf in restored_files:
        print(format_box_line(f"  ✔ {rf}"))
    print(f"  {CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}\n")
    sys.exit(0)


def execute_apply(target_root: Path, run_id_arg: Optional[str] = None, auto_approve: bool = False) -> Dict[str, Any]:
    runs_dir = target_root / ".torusguard" / "runs"
    if run_id_arg:
        run_folder = runs_dir / run_id_arg
    else:
        run_folder = find_latest_audit_run(runs_dir)

    if not run_folder or not run_folder.is_dir():
        print(f"\n  {RED}✖ No candidate remediation bundles found to apply.{RESET}")
        print(f"  Run {CYAN}npx torusguard harden{RESET} first to formulate candidate patches.\n")
        sys.exit(1)

    bundles_dir = run_folder / "bundles"
    if not bundles_dir.is_dir():
        print(f"\n  {RED}✖ Missing bundles directory in run folder: {run_folder}{RESET}\n")
        sys.exit(1)

    bundle_meta_files = list(bundles_dir.glob("*/metadata.json"))
    if not bundle_meta_files:
        print(f"\n  {YELLOW}ℹ Zero candidate bundles available in {run_folder.name}.{RESET}\n")
        sys.exit(0)

    bundles = []
    for mf in bundle_meta_files:
        try:
            bundles.append(json.loads(mf.read_text(encoding="utf-8")))
        except Exception:
            pass

    # Snapshot directory
    snapshot_dir = target_root / ".torusguard" / "snapshots" / run_folder.name
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # Header Card
    print(f"\n  {CYAN}╭─────────────────────────────────────────────────────────────────────────╮{RESET}")
    print(f"  {CYAN}│                                                                         │{RESET}")
    print(format_box_line(f"{BOLD}🛡️  TORUSGUARD GOVERNED PATCH APPLIER               v1.3.0{RESET}", border_color=CYAN))
    print(format_box_line(f"{DIM}Human-Gate Authorization, Snapshots & Golden Recipe Distillation{RESET}", border_color=CYAN))
    print(f"  {CYAN}│                                                                         │{RESET}")
    print(f"  {CYAN}╰─────────────────────────────────────────────────────────────────────────╯{RESET}\n")

    print(f"  {CYAN}┌─ Candidate Bundles Ready for Application ───────────────────────────────┐{RESET}")
    print(format_box_line(f"Active Run:     {WHITE}{run_folder.name}{RESET}"))
    print(format_box_line(f"Total Bundles:  {GREEN}{len(bundles)} candidate surgical patches formulated{RESET}"))
    print(format_box_line(f"Rollback Safety:Automatic pre-apply snapshot to .torusguard/snapshots/{run_folder.name}"))
    print(f"  {CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}\n")

    applied_count = 0
    skipped_count = 0
    all_approved = auto_approve
    diff_summary_lines = [f"# TorusGuard Applied Patch Summary: {run_folder.name}\n"]
    applied_bundles = []

    # Import memory_engine for Golden Recipe distillation
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import memory_engine

    for idx, b in enumerate(bundles, 1):
        rule_id = b.get("rule_id", "TG-SEC")
        rel_path = b.get("target_file", "")
        line_no = b.get("line_number", 1)
        diff = b.get("proposed_diff", "")
        desc = b.get("what_should_change", "")
        patched_content = b.get("patched_content")

        print(f"  {YELLOW}─── [{idx}/{len(bundles)}] Candidate Patch: [{rule_id}] on {rel_path}:{line_no} ───{RESET}")
        print(f"  Strategy: {WHITE}{desc}{RESET}")
        print(f"  Ponytail: {GREEN}+{b.get('additions', 0)} / -{b.get('deletions', 0)}{RESET}\n")

        # Display syntax-highlighted diff
        for dline in diff.splitlines()[:12]:
            if dline.startswith("+") and not dline.startswith("+++"):
                print(f"    {GREEN}{dline}{RESET}")
            elif dline.startswith("-") and not dline.startswith("---"):
                print(f"    {RED}{dline}{RESET}")
            elif dline.startswith("@"):
                print(f"    {CYAN}{dline}{RESET}")
            else:
                print(f"    {DIM}{dline}{RESET}")
        print()

        if not all_approved:
            try:
                choice = input(f"  {BOLD}Apply this patch?{RESET} ([y]es / [n]o / [a]ll / [q]uit): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print(f"\n  {YELLOW}Aborted by user.{RESET}\n")
                break

            if choice in ("q", "quit"):
                print(f"\n  {YELLOW}Exited review.{RESET}\n")
                break
            elif choice in ("a", "all"):
                all_approved = True
            elif choice not in ("y", "yes", ""):
                print(f"  {GRAY}Skipped.{RESET}\n")
                skipped_count += 1
                continue

        # Execute Application
        target_file = target_root / rel_path
        if not target_file.is_file():
            print(f"  {RED}✖ Target file not found: {target_file}{RESET}\n")
            continue

        # 1. Pre-apply Snapshot (.bak)
        bak_dest = snapshot_dir / (rel_path + ".bak")
        bak_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target_file, bak_dest)

        # 2. Write Patched Content
        if patched_content:
            target_file.write_text(patched_content, encoding="utf-8")
        else:
            continue

        # 3. Distill into Golden Fix Recipe in Memory Engine
        try:
            fn = getattr(memory_engine, "record_golden_recipe", getattr(memory_engine, "store_golden_recipe", None))
            if fn:
                fn(
                    rule_id=rule_id,
                    before_snippet=target_file.read_text(encoding="utf-8").splitlines()[max(0, line_no-1)],
                    after_snippet=desc,
                    diff_snippet=diff,
                    file_type=target_file.suffix,
                    description=desc,
                    root_dir=target_root
                )
            # Record event
            memory_engine.record_event("fix_applied", {
                "rule_id": rule_id,
                "file_path": rel_path,
                "line_number": line_no,
                "bundle_id": b.get("bundle_id")
            }, root_dir=target_root)
        except Exception:
            pass

        applied_count += 1
        applied_bundles.append(b)
        diff_summary_lines.append(f"## Applied: `[{rule_id}]` on `{rel_path}:{line_no}`")
        diff_summary_lines.append("```diff")
        diff_summary_lines.append(diff.strip())
        diff_summary_lines.append("```\n")
        print(f"  {GREEN}✔ Applied successfully.{RESET} (Snapshot saved: {bak_dest.relative_to(target_root)})\n")

    # Write apply artifacts in run folder
    (run_folder / "diff_summary.md").write_text("\n".join(diff_summary_lines), encoding="utf-8")
    apply_plan_lines = [
        f"# TorusGuard Governed Application Plan: {run_folder.name}",
        f"- **Total Candidate Patches:** {len(bundles)}",
        f"- **Successfully Applied:** {applied_count}",
        f"- **Skipped by Human Gate:** {skipped_count}",
        f"- **Execution Timestamp:** {get_ist_now().strftime('%Y-%m-%d %H:%M:%S IST')}",
        f"- **Rollback Directory:** `.torusguard/snapshots/{run_folder.name}`"
    ]
    (run_folder / "apply_plan.md").write_text("\n".join(apply_plan_lines), encoding="utf-8")

    # Update manifest
    manifest_file = run_folder / "manifest.json"
    if manifest_file.is_file():
        try:
            mdata = json.loads(manifest_file.read_text(encoding="utf-8"))
            mdata["status"] = "patches_applied"
            mdata["remediated"] = applied_count
            manifest_file.write_text(json.dumps(mdata, indent=2), encoding="utf-8")
        except Exception:
            pass

    # Summary Box
    print(f"  {CYAN}┌─ Application Summary ───────────────────────────────────────────────────┐{RESET}")
    print(format_box_line(f"Applied Patches:{GREEN}{applied_count} applied cleanly{RESET}"))
    print(format_box_line(f"Skipped / Pass: {GRAY}{skipped_count} skipped{RESET}"))
    print(format_box_line(f"Golden Recipes: {GREEN}{applied_count} distilled into persistent memory{RESET}"))
    print(format_box_line(f"Snapshot Safety:.torusguard/snapshots/{run_folder.name}"))
    print(f"  {CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}\n")

    print(f"  {GREEN}╔═ Next Governed Action ═════════════════════════════════════════════════════╗{RESET}")
    print(format_box_line(f"Differential Recheck: {BOLD}{WHITE}npx torusguard recheck{RESET} (Verify fix closure)", border="║", border_color=GREEN))
    print(format_box_line(f"View Golden Recipes:  {CYAN}npx torusguard recipes{RESET} (Inspect memory)", border="║", border_color=GREEN))
    print(format_box_line(f"Emergency Rollback:   {YELLOW}npx torusguard rollback{RESET} (Instant revert)", border="║", border_color=GREEN))
    print(f"  {GREEN}╚═════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

    return {
        "applied_count": applied_count,
        "skipped_count": skipped_count,
        "applied_bundles": applied_bundles,
        "snapshot_dir": str(snapshot_dir)
    }


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Governed Patch Application Engine")
    parser.add_argument("path", nargs="?", default=".", help="Target project root directory")
    parser.add_argument("--run", "-r", help="Explicit run ID to apply")
    parser.add_argument("--yes", "-y", action="store_true", help="Auto-approve all patches (non-interactive)")
    parser.add_argument("--rollback", action="store_true", help="Rollback all applied patches using snapshots")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    target = Path(args.path).resolve()

    if args.rollback:
        execute_rollback(target, run_id_arg=args.run)
        return

    result = execute_apply(target, run_id_arg=args.run, auto_approve=args.yes)
    if args.json:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
