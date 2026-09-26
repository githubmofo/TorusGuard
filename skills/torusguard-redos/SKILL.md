---
name: torusguard-redos
description: Analyzes regular expressions across JavaScript, TypeScript, Python, and Go for catastrophic exponential backtracking and ReDoS vulnerabilities via CLI, Chat, or MCP.
version: 2.0.0
workflow: .torusguard/workflows/redos.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - internal/scanner/redos.go
  - cmd/torusguard/main.go
  - cmd/torusguard/mcp.go
---

# TorusGuard ReDoS Complexity Scanner

## Objective
Detect and remediate catastrophic exponential ($O(2^n)$) and polynomial ($O(n^k)$) backtracking regular expressions in web applications. Prevents thread starvation, CPU exhaustion, and availability denial of service attacks caused by untrusted user input matching evil regex patterns.

---

## Tri-Mode Execution

### Mode A: Automated CLI Execution
Run ReDoS scanning against source code files:
```bash
# Scan current workspace for catastrophic regex backtracking
torusguard redos

# Scan specific directory or source tree
torusguard redos --target ./src
```

### Mode B: In-Session AI Chat Slash Command
Run `/torusguard redos` in chat.
The agent executes the compiled Go ReDoS analyzer or MCP tool to locate dangerous nested quantifiers, overlapping alternations, and unanchored expressions.

### Mode C: Native MCP Tool Call
MCP-enabled coding agents (Antigravity, Cursor, Windsurf, Claude Code) call:
```json
{
  "tool": "torusguard_redos",
  "arguments": {
    "target": "."
  }
}
```

---

## Supported Patterns & Invariants
- **TG-REDOS-001 (Nested Quantifier Catastrophic Backtracking):** Detects nested repetitions such as `(a+)+`, `([a-zA-Z0-9]+)*`, or `((foo)*)+` that cause exponential evaluation time $O(2^n)$ when matching non-matching suffixes (e.g. `aaaaaaaaaaaaaaaa!`).
- **TG-REDOS-002 (Overlapping Alternation with Outer Repetition):** Detects patterns like `(a|ab)+` or `(user|username)*` where multiple branches match identical prefixes, causing exponential branch exploration.

---

## 🏛️ OpenCodeReview Hybrid Architecture Integration
- **First-Principles NFA/DFA Complexity Analysis:** Scans regex literals and constructor invocations across JS, TS, Python, and Go.
- **Engine-Aware Triage:** Flags backtracking engines (V8, Node.js, Python `re`, PCRE) as high risk while noting linear-time DFA engines (Go `regexp`/RE2, Rust `regex`).
- **Surgical Patching:** Replaces evil regexes with bounded, non-overlapping expressions or length pre-checks (≤35 additions, ≤25 deletions).

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Nested Quantifiers** | Writes `([a-zA-Z0-9_]+)*` or `(https?://.+)*`, causing $O(2^n)$ catastrophic backtracking on malicious input. | Flatten expressions: `[a-zA-Z0-9_]*` or use non-overlapping delimiters like `[^/\s]+`. |
| **Overlapping Alternation** | Combines overlapping options inside repetition: `(a\|aa)+` or `(\w+\|\d+)+`. | Disjoint branch design: ensure alternatives cannot consume the same character prefix. |
| **Missing Input Length Guards** | Evaluates complex regexes against arbitrarily long input strings from untrusted HTTP bodies. | Impose input bounds (`if (input.length > 256) return false`) before regex evaluation. |
| **Unanchored Wildcards** | Writes `.*foo.*` without anchors, leading to quadratic scan across long documents. | Anchor patterns with `^` and `$` whenever full string matching is intended. |
| **Engine Indifference** | Assumes all regex engines backtrack identically; doesn't know Go RE2 is linear $O(n)$ while Node V8 is vulnerable. | Tailor remediation to target runtime: use atomic groups/lookahead in V8/Python or switch to parser combinators. |

---

## ✅ Pre-Flight Self-Audit

Before concluding a ReDoS complexity audit, verify:
- [ ] Were all regex literals and `RegExp` / `re.compile` declarations inspected?
- [ ] Are any nested quantifiers (`(x+)+`, `(x*)*`) present in the codebase?
- [ ] Are alternatives in grouped alternations strictly mutually exclusive?
- [ ] Is untrusted input strictly bounded in length before regex execution?
- [ ] Are remediations validated within Ponytail diff bounds?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY: Identify regex patterns evaluated on untrusted user inputs.
BUILD:  Execute torusguard redos or torusguard_redos to detect exponential backtracking structures.
CONFIRM: Refactor pattern into deterministic, non-overlapping tokens, adding length guards and testing with evil payloads.
```
