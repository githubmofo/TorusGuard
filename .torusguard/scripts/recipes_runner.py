#!/usr/bin/env python3
"""
TorusGuard Golden Fix Recipe Explorer (v1.3.0)
Inspect, list, and export reusable, verified AST remediation code snippets
distilled from passing security patches and persistent memory patterns.

Pure Python 3.10+ standard library (zero external dependencies).
"""

import sys
import json
import argparse
import unicodedata
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

# Windows console UTF-8 support
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
    except Exception:
        pass

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


def list_recipes(target_root: Path, detail_id: Optional[str] = None, json_output: bool = False) -> None:
    patterns_file = target_root / ".torusguard" / "memory" / "patterns.json"
    recipes: List[Dict[str, Any]] = []

    if patterns_file.is_file():
        try:
            patterns = json.loads(patterns_file.read_text(encoding="utf-8"))
            recipes = [p for p in patterns if p.get("pattern_type") == "golden_fix_recipe"]
        except Exception:
            recipes = []

    if json_output:
        print(json.dumps(recipes, indent=2))
        return

    # Header Card
    print(f"\n  {CYAN}╭─────────────────────────────────────────────────────────────────────────╮{RESET}")
    print(f"  {CYAN}│                                                                         │{RESET}")
    print(format_box_line(f"{BOLD}🛡️  TORUSGUARD GOLDEN FIX RECIPES                   v1.3.0{RESET}", border_color=CYAN))
    print(format_box_line(f"{DIM}Distilled Ponytail Fixes (<= 35 add, <= 25 del) in Persistent Memory{RESET}", border_color=CYAN))
    print(f"  {CYAN}│                                                                         │{RESET}")
    print(f"  {CYAN}╰─────────────────────────────────────────────────────────────────────────╯{RESET}\n")

    if not recipes:
        print(f"  {YELLOW}ℹ No golden fix recipes captured yet.{RESET}")
        print(f"  Run {CYAN}npx torusguard harden{RESET} followed by {CYAN}npx torusguard apply{RESET} to distill verified recipes.\n")
        return

    print(f"  {CYAN}┌─ Active Distilled Recipes ({len(recipes)}) ─────────────────────────────────────┐{RESET}")
    for idx, r in enumerate(recipes, 1):
        rule_id = r.get("rule_id", "TG-SEC")
        rec_id = r.get("recipe_id", f"recipe-{idx}")
        desc = r.get("description", "Verified fix")
        rdata = r.get("recipe_data", {})
        metrics = rdata.get("ponytail_metrics", {})
        verified = rdata.get("verified_count", 1)
        adds = metrics.get("additions", 0)
        dels = metrics.get("deletions", 0)

        print(format_box_line(f"{GREEN}[{rule_id}]{RESET} {WHITE}{rec_id}{RESET} (Verified {verified}x · +{adds}/-{dels} Ponytail)"))
        print(format_box_line(f"  └─ {DIM}{desc}{RESET}"))
    print(f"  {CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}\n")

    if detail_id:
        target_rec = next((r for r in recipes if r.get("recipe_id") == detail_id), None)
        if target_rec:
            rdata = target_rec.get("recipe_data", {})
            print(f"  {BOLD}Recipe Details: {detail_id}{RESET}")
            print(f"  {DIM}Rule ID:{RESET} {target_rec.get('rule_id')}")
            print(f"  {DIM}Diff Snippet:{RESET}")
            print("  ```diff")
            for line in rdata.get("diff_snippet", "").splitlines():
                if line.startswith("+"):
                    print(f"    {GREEN}{line}{RESET}")
                elif line.startswith("-"):
                    print(f"    {RED}{line}{RESET}")
                else:
                    print(f"    {DIM}{line}{RESET}")
            print("  ```\n")


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Golden Fix Recipe Explorer")
    parser.add_argument("path", nargs="?", default=".", help="Target project root directory")
    parser.add_argument("--detail", "-d", help="Inspect specific recipe ID")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    target = Path(args.path).resolve()
    list_recipes(target, detail_id=args.detail, json_output=args.json)


if __name__ == "__main__":
    main()
