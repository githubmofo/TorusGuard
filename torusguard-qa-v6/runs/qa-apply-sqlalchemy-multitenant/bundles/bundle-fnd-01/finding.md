# Finding: Missing Tenant Query Isolation in SQLAlchemy

- **Finding ID:** `fnd-01`
- **Rule ID:** `TG-DB-004`
- **Severity:** High
- **Target Files:** `queries.py`

## What Is Wrong
Query filters by ID without tenant boundary enforcement.

## Why It Matters
This vulnerability could allow attackers to bypass authorization, access unauthorized tenant data, or inject malicious payloads.
