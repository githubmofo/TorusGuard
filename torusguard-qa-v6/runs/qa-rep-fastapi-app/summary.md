# TorusGuard v6 Execution Summary — `fastapi-app`

- **Run ID:** `qa-rep-fastapi-app`
- **Total Findings:** 2
- **Confirmed:** 2 | **High Confidence:** 0 | **Needs Review:** 0
- **Root-Cause Clusters:** 2

## Root-Cause Clustering Breakdown

| Cluster ID | Root-Cause Title | Primary Rule | Findings | Affected Files | Severity |
|---|---|---|---:|---:|---|
| `cluster-ssrf-network` | Unvalidated Outbound HTTP Requests & Network Boundary Leakage | `TG-SSRF-001` | 1 | 1 | High |
| `cluster-header-trust` | Untrusted Client Header Trust & Role/Tenant Injection | `TG-AUTH-008` | 1 | 1 | High |


## Next Actions

1. Run `/torusguard harden` to inspect structured remediation bundles.
2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.
3. Run `/torusguard recheck` to verify impacted trust boundaries.
