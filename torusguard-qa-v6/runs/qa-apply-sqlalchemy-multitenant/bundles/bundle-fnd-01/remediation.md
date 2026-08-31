# Remediation Guide: Missing Tenant Query Isolation in SQLAlchemy

## What Should Change
Add tenant_id predicate to query filter.

## Target Files to Modify
- `queries.py`
