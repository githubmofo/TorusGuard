# TorusGuard v6 Execution Summary — `tiny-repo`

- **Run ID:** `qa-apply-tiny-repo`
- **Total Findings Modeled:** 2
- **Confirmed:** 2 | **High Confidence:** 0 | **Needs Review:** 0
- **Root-Cause Clusters:** 2

## Root-Cause Clustering Breakdown

| Cluster ID | Root-Cause Title | Primary Rule | Findings | Files | Hotspot Module | Severity |
|---|---|---|---:|---:|---|---|
| `cluster-secrets` | Hardcoded Secrets & Sensitive Environment Configuration Exposure | `TG-SEC-001` | 1 | 1 | `app.py` | Critical |
| `cluster-platform-003` | Systemic Production Debug Mode Enabled Issues | `TG-PLATFORM-003` | 1 | 1 | `app.py` | Medium |


## Next Actions

1. Run `/torusguard harden` to inspect structured remediation bundles.
2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.
3. Run `/torusguard recheck` to verify impacted trust boundaries.
