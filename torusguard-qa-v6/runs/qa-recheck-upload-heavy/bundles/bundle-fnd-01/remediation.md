# Remediation Guide: Path Traversal in Storage Handler

## What Should Change
Sanitize filename and assert resolved path resides within UPLOAD_DIR.

## Target Files to Modify
- `storage.py`
