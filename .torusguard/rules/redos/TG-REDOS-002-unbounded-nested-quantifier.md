# TG-REDOS-002: Unbounded Nested Quantifier in Input Validation

## Severity
Medium. Unbounded repeated capture groups without boundary anchors cause polynomial ($O(n^2)$) or exponential degradation on large payloads.

## Applies To
- Input validation filters, route path matchers, sanitizer regexes
- Polyglot web backends and client-side form validators

## Why It Matters
When regexes use repeated capture groups like `(\w+\s*)+` without anchoring, trailing spaces or punctuation force the engine into deep recursive state branches. While not always pure exponential, large payloads (e.g. 50KB JSON strings) will peg CPU at 100% for minutes.

## What TorusGuard Looks For
1. Nested groups where both inner and outer components have greedy repetition (`+` or `*`).
2. Regexes evaluated on user-supplied strings without a preceding string length check.

## Unsafe Example
```python
# UNSAFE: Unbounded nested quantifier on user input
import re

TAG_REGEX = re.compile(r"^(<[a-z]+(\s+[a-z]+=[^>]+)*>)+$")
match = TAG_REGEX.match(user_payload)
```

## Safe Example
```python
# SAFE: Bounded input length check + non-nested linear pattern
import re

if len(user_payload) > 512:
    return False

# Use a dedicated HTML parser (BeautifulSoup / html5lib) instead of regex
```

## Remediation
1. Bound user input length *before* regex execution.
2. Replace complex nested regexes with dedicated, parser-based validation libraries (e.g., standard parsers for HTML, URLs, and emails).

## Related Rules
- `TG-REDOS-001`: Catastrophic Exponential Backtracking
- `TG-INPUT-001`: Missing Server Validation
