# Remediation Guide: Unsafe File Path Traversal

## What Should Change
Sanitize with werkzeug secure_filename.

## Target Files to Modify
- `app.py`
