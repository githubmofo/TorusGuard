# /torusguard-redos — Regular Expression Complexity Scanner

$ARGUMENTS

---

## Objective
Detect and remediate catastrophic exponential ($O(2^n)$) and polynomial backtracking regular expressions in web applications to prevent availability and thread starvation DoS attacks.

---

## Tri-Mode Parity
- **Mode A (Terminal CLI):** `torusguard redos [target]`
- **Mode B (AI Chat Slash Command):** `/torusguard redos [target]`
- **Mode C (Native MCP Tool):** `torusguard_redos`

---

## Execution Steps

1. **Locate Regex Definitions:** Walk source tree to find regex literals and constructor calls (`RegExp`, `re.compile`, `regexp.MustCompile`).
2. **Analyze Backtracking Complexity:**
   - Detect nested quantifiers (`(x+)+`, `(x*)*`) causing $O(2^n)$ exponential blowup (`TG-REDOS-001`).
   - Detect overlapping alternations with outer repetition causing polynomial blowup (`TG-REDOS-002`).
3. **Audit Input Length Guardrails:** Check if untrusted inputs evaluated against regexes are bounded in character length.
4. **Formulate Safe Remediation:** Refactor vulnerable regexes into linear deterministic expressions, anchor tokens, or parser logic.
5. **Synchronize Report:** Log all ReDoS findings in `security_report.md`.
