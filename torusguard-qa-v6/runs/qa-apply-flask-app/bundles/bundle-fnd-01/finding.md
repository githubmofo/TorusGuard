# Finding: Unsafe File Path Traversal

- **Finding ID:** `fnd-01`
- **Rule ID:** `TG-INPUT-006`
- **Severity:** High
- **Target Files:** `app.py`

## What Is Wrong
Filename passed directly from client without sanitization.

## Why It Matters
This vulnerability could allow attackers to bypass authorization, access unauthorized tenant data, or inject malicious payloads.
