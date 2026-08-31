# Finding: Path Traversal in Storage Handler

- **Finding ID:** `fnd-01`
- **Rule ID:** `TG-INPUT-006`
- **Severity:** High
- **Target Files:** `storage.py`

## What Is Wrong
raw_filename joined to destination path without canonicalization.

## Why It Matters
This vulnerability could allow attackers to bypass authorization, access unauthorized tenant data, or inject malicious payloads.
