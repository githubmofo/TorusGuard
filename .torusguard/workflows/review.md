# TorusGuard Review Workflow (`/torusguard review`)

## Purpose
Executes differential incremental Git diff security review against a reference branch or commit (default: `HEAD~1`).
Inspects changed lines for new security regressions, evaluates net security score deltas, and outputs pull request review comments.

## Steps
1. Determine reference branch or commit (e.g. `HEAD~1` or `origin/main`).
2. Run differential scan via `torusguard review [--diff <ref>]` or native MCP tool `torusguard_review`.
3. Check PR Gate Decision (`PASSED` or `BLOCKED`).
4. If blocked, review newly introduced violations and formulate surgical Ponytail fixes via `/torusguard harden`.
