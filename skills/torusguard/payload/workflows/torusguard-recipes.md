---
description: Explore, search, export, and project distilled Golden Fix Recipes in persistent security memory.
tools: Read, Grep, Glob, Bash, Write
version: 1.4.0
agent: remediator
lifecycle-phase: Phase 6 (Memory & Recipes)
required-skills:
  - torusguard-recipes
scripts-binding:
  - .torusguard/scripts/recipes_runner.py
  - .torusguard/scripts/memory_engine.py
---

# /torusguard recipes — Golden Fix Recipe Explorer & Memory Distillation

$ARGUMENTS

---

## Objective
Inspect, search, export, and project reusable, verified Ponytail remediation code snippets distilled from passing security patches and persistent memory patterns.

---

## Command Flags & Arguments

| Mode | Command Syntax | Description |
| :--- | :--- | :--- |
| **List Recipes** | `npx torusguard recipes` | List all distilled golden fix recipes with verification counts and churn |
| **Search Filter** | `npx torusguard recipes --search <query>` | Filter recipes by keyword, rule family (e.g. `TG-SEC`), or language |
| **Inspect Detail** | `npx torusguard recipes --detail <id>` | View complete unified diff snippet for a specific recipe |
| **Export Catalog** | `npx torusguard recipes --export <file>` | Export recipes to `.json` or `.md` catalog format |
| **Apply Preview** | `npx torusguard recipes --apply <id>` | Project recipe diff onto codebase for manual review |
| **Target Directory** | `npx torusguard recipes --target <dir>` | Specify custom project root directory |

---

## Execution Steps

1. **Query Memory Patterns:** Read `.torusguard/memory/patterns.json` for verified `golden_fix_recipe` entries.
2. **Apply Filter / Search:** Match `--search` query against rule IDs, titles, diffs, and target file types.
3. **Render 75-Column Cards:** Format recipe cards showing verified counts, rule family, and Ponytail additions/deletions.
4. **Export / Apply:** If requested, write export file or render projected patch snippet.

---

## Output Card Format

```markdown
### 🛡️ TorusGuard Golden Fix Recipes
- **Total Distilled:** [Count] verified recipes
- **Filter:** [Query or None]
- **Ponytail Bounds:** All recipes strictly <= 35 additions, <= 25 deletions
- **Storage:** `.torusguard/memory/patterns.json`
```
