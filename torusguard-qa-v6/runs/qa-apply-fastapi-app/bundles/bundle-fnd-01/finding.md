# Finding: Untrusted Role Header Injection

- **Finding ID:** `fnd-01`
- **Rule ID:** `TG-AUTH-008`
- **Severity:** High
- **Target Files:** `main.py`

## What Is Wrong
Authorization decision trusts unverified client request header.

## Why It Matters
This vulnerability could allow attackers to bypass authorization, access unauthorized tenant data, or inject malicious payloads.
