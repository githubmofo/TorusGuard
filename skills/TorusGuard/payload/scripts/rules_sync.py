#!/usr/bin/env python3
"""
TorusGuard AI IDE Rules Auto-Sync Engine (v1.2.0)
Compiles project security memory, golden fix recipes, and active guardrails
into prompt-optimized rule files for Cursor, Claude Code, Antigravity, and Windsurf.
Non-destructive: preserves existing user rules via demarcated comment fences.
Zero external dependencies (Python 3.10+ stdlib).
"""

import sys
import json
import re
import argparse
from pathlib import Path
from typing import Any

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

START_MARKER = "<!-- TORUSGUARD-SECURITY-GUARDRAILS:START -->"
END_MARKER = "<!-- TORUSGUARD-SECURITY-GUARDRAILS:END -->"
MAX_PROMPT_TOKENS = 400


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


def load_security_context(root_dir: Path) -> dict[str, Any]:
    """Load security profile and patterns from memory subsystem."""
    tg_dir = root_dir / ".torusguard"
    memory_dir = tg_dir / "memory"

    context_file = memory_dir / "context.json"
    patterns_file = memory_dir / "patterns.json"
    profile_file = memory_dir / "profile.json"

    context_data: dict[str, Any] = {}
    patterns: list[dict[str, Any]] = []
    profile: dict[str, Any] = {}

    if context_file.exists():
        try:
            context_data = json.loads(context_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            context_data = {}

    if patterns_file.exists():
        try:
            patterns = json.loads(patterns_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            patterns = []

    if profile_file.exists():
        try:
            profile = json.loads(profile_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            profile = {}

    cfg_file = tg_dir / "config" / "torusguard.json"
    if cfg_file.exists():
        try:
            cfg = json.loads(cfg_file.read_text(encoding="utf-8"))
            det = cfg.get("detected_stack", {})
            if not profile.get("stack"):
                lang = det.get("language")
                fw = det.get("framework")
                if lang and lang != "Unknown":
                    stk = [lang]
                    if fw and fw != "None":
                        stk.append(fw)
                    profile["stack"] = stk
        except (json.JSONDecodeError, OSError):
            pass

    # Dynamic fallback to stack_detect if stack is still unknown
    if not profile.get("stack"):
        try:
            import stack_detect  # type: ignore
            det_stk = stack_detect.detect_stack(root_dir)
            lang = det_stk.get("language")
            fw = det_stk.get("framework")
            if lang and lang != "Unknown":
                stk = [lang]
                if fw and fw != "None":
                    stk.append(fw)
                profile["stack"] = stk
        except Exception:
            pass

    return {
        "context": context_data,
        "patterns": patterns,
        "profile": profile
    }


def format_dense_security_rules(sec_data: dict[str, Any]) -> str:
    """
    Format active security memory into a dense, token-budgeted markdown block (<=400 tokens),
    dynamically tailored to the detected language and framework family.
    """
    patterns = sec_data.get("patterns", [])
    profile = sec_data.get("profile", {})
    stack = profile.get("stack", [])

    golden_recipes: list[dict[str, Any]] = []
    regressions: list[dict[str, Any]] = []
    common_vulns: list[dict[str, Any]] = []

    for p in patterns:
        ptype = p.get("pattern_type")
        if ptype == "golden_fix_recipe":
            golden_recipes.append(p)
        elif ptype == "regression_watch":
            regressions.append(p)
        elif ptype in ("common_vulnerability", "recurring_fix"):
            common_vulns.append(p)

    lines: list[str] = [
        START_MARKER,
        "## 🛡️ TorusGuard Active Project Security Invariants",
        "> Auto-synced from `.torusguard/memory/`. Adhere to these guardrails in all generated code.",
        ""
    ]

    if stack:
        lines.append(f"**Detected Stack:** {', '.join(stack)}")
        lines.append("")

    # Core Behavioral Invariants (Stack-Adaptive & Token-Optimized)
    stack_lower = " ".join(stack).lower()
    sql_guards = []
    bypass_guards = []

    if "go" in stack_lower:
        sql_guards.append("`db.Query(..., args)` / GORM")
        bypass_guards.append("`InsecureSkipVerify: true`")
    if "rust" in stack_lower:
        sql_guards.append("`sqlx::query!` / Diesel")
        bypass_guards.append("`unsafe { ... }`")
    if "java" in stack_lower or "kotlin" in stack_lower:
        sql_guards.append("JPA / PreparedStatement")
        bypass_guards.append("`csrf().disable()`")
    if "c#" in stack_lower or "dotnet" in stack_lower:
        sql_guards.append("EF Core LINQ / `FromSqlInterpolated`")
        bypass_guards.append("`[AllowAnonymous]`")
    if "php" in stack_lower:
        sql_guards.append("PDO prepared statements / Eloquent")
        bypass_guards.append("`CURLOPT_SSL_VERIFYPEER => false`")
    if "typescript" in stack_lower or "javascript" in stack_lower or "next" in stack_lower or "express" in stack_lower:
        sql_guards.append("Prisma / Drizzle binders")
        bypass_guards.append("`rejectUnauthorized: false`")

    if not sql_guards:
        sql_rule = "1. **Zero Raw SQL / String Formats:** Always use parameterized queries (e.g. `%s`, `?`, or ORM bound params)."
    else:
        sql_rule = f"1. **Zero Raw SQL:** Always use parameterized queries ({' / '.join(sql_guards[:2])})."

    if not bypass_guards:
        bypass_rule = "4. **No Security Bypasses:** Never insert `# nosec`, `verify=False`, `@csrf_exempt`, or `bypass_auth=True`."
    else:
        bypass_rule = f"4. **No Security Bypasses:** Never insert `# nosec`, `verify=False`, or {', '.join(bypass_guards[:2])}."

    lines.extend([
        "### Universal Guardrails",
        sql_rule,
        "2. **Tenant Isolation:** Enforce tenant/owner filtering on every database lookup (never query without `tenant_id` or owner scope).",
        "3. **Ponytail Bound Rule:** Remediation patches must be minimal (<= 35 additions, <= 25 deletions).",
        bypass_rule,
        ""
    ])

    # Golden Fix Recipes (Top 2 to preserve tokens)
    if golden_recipes:
        lines.append("### Verified Golden Fix Patterns")
        for rec in golden_recipes[:2]:
            rule = rec.get("rule_id", "TG-SEC")
            desc = rec.get("description", "Verified AST fix")
            r_data = rec.get("recipe_data", {})
            before = r_data.get("before_snippet", "")
            after = r_data.get("after_snippet", "")
            lines.append(f"- **{rule}** ({desc}):")
            if before and after:
                lines.append(f"  - ❌ Avoid: `{before[:70]}`")
                lines.append(f"  - ✅ Prefer: `{after[:70]}`")
        lines.append("")

    # High-Risk Regression Watches
    if regressions:
        lines.append("### Active Regression Watches (Do Not Re-Introduce)")
        for reg in regressions[:3]:
            rule = reg.get("rule_id", "TG-REG")
            files = ", ".join(reg.get("affected_files", [])[:2]) or "tracked files"
            lines.append(f"- **{rule}**: Recurrence risk in `{files}`.")
        lines.append("")

    lines.append(END_MARKER)
    return "\n".join(lines)


def inject_rules_into_file(file_path: Path, rules_block: str) -> bool:
    """
    Non-destructively inject or replace the TorusGuard block in a target rules file.
    Creates parent directories if necessary.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    existing_content = ""

    if file_path.exists():
        try:
            existing_content = file_path.read_text(encoding="utf-8")
        except OSError:
            existing_content = ""

    pattern = re.compile(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
        re.DOTALL
    )

    if pattern.search(existing_content):
        updated_content = pattern.sub(rules_block, existing_content)
    else:
        if existing_content.strip():
            updated_content = existing_content.rstrip() + "\n\n" + rules_block + "\n"
        else:
            updated_content = rules_block + "\n"

    try:
        file_path.write_text(updated_content, encoding="utf-8")
        return True
    except OSError as err:
        print(f"Error writing rules to {file_path}: {err}", file=sys.stderr)
        return False


def sync_rules(
    target_format: str = "all",
    root_dir: str | Path | None = None
) -> dict[str, Any]:
    """
    Synchronize project security invariants into target IDE rules files.
    Supported targets: 'cursor', 'claude', 'agent', 'windsurf', 'all'.
    """
    root = Path(root_dir or find_project_root()).resolve()
    sec_data = load_security_context(root)
    rules_block = format_dense_security_rules(sec_data)

    target_files: dict[str, Path] = {
        "cursor": root / ".cursorrules",
        "claude": root / "CLAUDE.md",
        "agent": root / ".agent" / "rules" / "torusguard.md",
        "windsurf": root / ".windsurfrules"
    }

    synced_targets: list[str] = []
    formats_to_sync = list(target_files.keys()) if target_format == "all" else [target_format]

    for fmt in formats_to_sync:
        if fmt in target_files:
            target_path = target_files[fmt]
            success = inject_rules_into_file(target_path, rules_block)
            if success:
                synced_targets.append(str(target_path.relative_to(root)))

    # Estimate token overhead (approx 4 chars/token)
    token_est = max(1, len(rules_block) // 4)

    return {
        "status": "success" if synced_targets else "skipped",
        "synced_files": synced_targets,
        "token_estimate": token_est,
        "within_budget": token_est <= MAX_PROMPT_TOKENS
    }


def main():
    parser = argparse.ArgumentParser(description="TorusGuard AI IDE Rules Auto-Sync Engine")
    parser.add_argument(
        "--format",
        choices=["all", "cursor", "claude", "agent", "windsurf"],
        default="all",
        help="Target AI IDE rules format to sync"
    )
    parser.add_argument("--root", help="Project root override")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else None

    result = sync_rules(target_format=args.format, root_dir=root)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"[SUCCESS] Synced TorusGuard security invariants to {len(result['synced_files'])} file(s):")
        for f in result["synced_files"]:
            print(f"  - {f}")
        print(f"Token estimate: ~{result['token_estimate']} tokens (budget <= {MAX_PROMPT_TOKENS})")


if __name__ == "__main__":
    main()
