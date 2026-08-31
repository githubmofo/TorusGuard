# Remediation Guide: Disabled Template Autoescaping via mark_safe

## What Should Change
Pass raw invoice model to template and rely on autoescaping.

## Target Files to Modify
- `views.py`
