# Finding: Disabled Template Autoescaping via mark_safe

- **Finding ID:** `fnd-01`
- **Rule ID:** `TG-INPUT-005`
- **Severity:** High
- **Target Files:** `views.py`

## What Is Wrong
mark_safe bypasses HTML autoescaping on user input.

## Why It Matters
This vulnerability could allow attackers to bypass authorization, access unauthorized tenant data, or inject malicious payloads.
