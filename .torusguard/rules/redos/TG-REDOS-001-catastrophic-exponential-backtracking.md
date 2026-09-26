# TG-REDOS-001: Catastrophic Exponential Backtracking in Regular Expression

## Severity
High. Regular expressions with catastrophic backtracking trigger exponential time complexity ($O(2^n)$) when evaluating non-matching input strings, freezing CPU cores and causing Denial of Service.

## Applies To
- JavaScript / TypeScript (`RegExp`, `pattern.test()`), Python (`re.match`, `re.search`), Go, Java, Ruby
- Input validation patterns, email validators, URL extractors

## Why It Matters
Traditional regex engines using NFA backtracking (e.g. JavaScript V8, Python `re`, Java `java.util.regex`, PCRE) explore all possible match paths on failure. When a pattern contains overlapping nested repetitions like `(a+)+$`, an input of 30 characters like `aaaaaaaaaaaaaaaaaaaaaaaaaaaaab` can require over 1 billion comparison operations, freezing the Node.js event loop or Python GIL.

## What TorusGuard Looks For
1. Nested repetitions: `([a-zA-Z0-9]+)+`, `(a+)+`, `(\d+)*`.
2. Overlapping alternations with outer quantifiers: `(a|aa)+`, `(x|x)*`.
3. Greedy repetition with overlapping prefix and suffix.

## Unsafe Example
```javascript
// UNSAFE: Catastrophic backtracking on non-matching strings
const EMAIL_REGEX = /^([a-zA-Z0-9_\.\-])+@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

// Freezes server:
EMAIL_REGEX.test("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!");
```

## Safe Example
```javascript
// SAFE: Linear time validation using atomic checks, character class bounds, or validator libraries
const validator = require('validator');
if (!validator.isEmail(input)) {
  throw new Error("Invalid email");
}

// Or constrained regex without nested quantifiers:
const SAFE_EMAIL = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
```

## Remediation
1. Eliminate nested quantifiers (`(x+)+` -> `x+`).
2. Disallow overlapping tokens in alternations.
3. In Node.js, wrap untrusted input validation with `safe-regex` or strict input length bounds (e.g. `if (input.length > 256) return false;`).

## Related Rules
- `TG-REDOS-002`: Unbounded Nested Quantifier
- `TG-RATE-003`: Unbounded Resource Consumption
