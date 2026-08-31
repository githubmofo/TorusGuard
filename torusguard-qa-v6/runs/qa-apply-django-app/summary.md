# TorusGuard v6 Execution Summary — `django-app`

- **Run ID:** `qa-apply-django-app`
- **Total Findings Modeled:** 2
- **Confirmed:** 2 | **High Confidence:** 0 | **Needs Review:** 0
- **Root-Cause Clusters:** 2

## Root-Cause Clustering Breakdown

| Cluster ID | Root-Cause Title | Primary Rule | Findings | Files | Hotspot Module | Severity |
|---|---|---|---:|---:|---|---|
| `cluster-tenant-isolation` | Missing Multi-Tenant Query Scoping & Model Isolation | `TG-DB-004` | 1 | 1 | `views.py` | High |
| `cluster-template-escaping` | Disabled Template Autoescaping & Unsafe HTML Rendering | `TG-INPUT-005` | 1 | 1 | `views.py` | High |


## Next Actions

1. Run `/torusguard harden` to inspect structured remediation bundles.
2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.
3. Run `/torusguard recheck` to verify impacted trust boundaries.
