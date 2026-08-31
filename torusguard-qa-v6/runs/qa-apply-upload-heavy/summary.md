# TorusGuard v6 Execution Summary — `upload-heavy`

- **Run ID:** `qa-apply-upload-heavy`
- **Total Findings:** 1
- **Confirmed:** 1 | **High Confidence:** 0 | **Needs Review:** 0
- **Root-Cause Clusters:** 1

## Root-Cause Clustering Breakdown

| Cluster ID | Root-Cause Title | Primary Rule | Findings | Affected Files | Severity |
|---|---|---|---:|---:|---|
| `cluster-path-traversal` | Unsafe File Upload Storage & Path Traversal Boundaries | `TG-INPUT-006` | 1 | 1 | High |


## Next Actions

1. Run `/torusguard harden` to inspect structured remediation bundles.
2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.
3. Run `/torusguard recheck` to verify impacted trust boundaries.
