#!/usr/bin/env python3
"""
TorusGuard Golden Fix Recipe Explorer (v1.3.3)
Inspect, list, and export reusable, verified AST remediation code snippets
distilled from passing security patches and persistent memory patterns.
Standardized 75-column terminal UI formatting.

Pure Python 3.10+ standard library (zero external dependencies).
"""

import sys
import json
import argparse
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

# ─── Formatting Helpers ────────────────────────────────────────────────────────
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
    print()
    print(box_header("🛡️  TORUSGUARD GOLDEN FIX RECIPES", "Distilled Ponytail Fixes (<= 35 add, <= 25 del) in Persistent Memory", "v1.3.3"))
    print()

    if not recipes:
        print(f"  {YELLOW}ℹ No golden fix recipes captured yet.{RESET}")
        print(f"  Run {CYAN}npx torusguard harden{RESET} followed by {CYAN}npx torusguard apply{RESET} to distill verified recipes.\n")
        return

    print(border_top(f"Active Distilled Recipes ({len(recipes)})"))
    for idx, r in enumerate(recipes, 1):
        rule_id = r.get("rule_id", "TG-SEC")
        rec_id = r.get("recipe_id", f"recipe-{idx}")
        desc = r.get("description", "Verified fix")
        rdata = r.get("recipe_data", {})
        metrics = rdata.get("ponytail_metrics", {})
        verified = rdata.get("verified_count", 1)
        adds = metrics.get("additions", 0)
        dels = metrics.get("deletions", 0)

        print(box_line(f"{GREEN}[{rule_id}]{RESET} {WHITE}{rec_id}{RESET} (Verified {verified}x · +{adds}/-{dels} Ponytail)"))
        print(box_line(f"  └─ {DIM}{desc}{RESET}"))
    print(border_bottom())
    print()

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
