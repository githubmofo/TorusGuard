# Python Dependencies Verification Matrix (TorusGuard v0.4.0)

| Rule ID | Rule Title | Test Target File | Detection Check | Expected Result | Confidence |
|---|---|---|---|---|:---:|
| `TG-SUPPLY-001` | Missing Lockfile | Repository Root | `requirements.txt` present without lockfile | Flagged as Supply Chain Risk | Confirmed |
| `TG-SUPPLY-002` | Vulnerability Scan | Environment / Lockfile | Manifest lacks `pip-audit` check in CI | Flagged as Missing Vulnerability Review | Confirmed |
| `TG-SUPPLY-004` | Unpinned Actions in CI | `.github/workflows/` | Action uses `@v4` tag instead of commit SHA | Flagged as CI Supply Chain Risk | Confirmed |
