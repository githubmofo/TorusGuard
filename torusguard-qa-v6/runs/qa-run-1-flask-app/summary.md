# TorusGuard v6 Execution Summary — `flask-app`

- **Run ID:** `qa-run-1-flask-app`
- **Total Findings Modeled:** 2
- **Confirmed:** 2 | **High Confidence:** 0 | **Needs Review:** 0
- **Root-Cause Clusters:** 2

## Root-Cause Clustering Breakdown

| Cluster ID | Root-Cause Title | Primary Rule | Findings | Files | Hotspot Module | Severity |
|---|---|---|---:|---:|---|---|
| `cluster-template-escaping` | Disabled Template Autoescaping & Unsafe HTML Rendering | `TG-INPUT-005` | 1 | 1 | `app.py` | Critical |
| `cluster-path-traversal` | Unsafe File Upload Storage & Path Traversal Boundaries | `TG-INPUT-006` | 1 | 1 | `app.py` | High |


## Next Actions

1. Run `/torusguard harden` to inspect structured remediation bundles.
2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.
3. Run `/torusguard recheck` to verify impacted trust boundaries.
