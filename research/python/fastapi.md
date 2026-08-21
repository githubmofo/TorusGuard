# FastAPI Security Research Notes (TorusGuard v0.4.0)

## Research Findings
- **Pydantic Validation Boundaries:** Pydantic v2 validates types, but by default ignores unexpected fields unless `extra = "forbid"` is set. Unfiltered model dumps (`model.dict()`) unpacked into database entities reintroduce mass-assignment vectors.
- **Dependency Hierarchy:** Route dependencies (`Depends`) must separate identity validation (`get_current_user`) from authorization/ownership enforcement.
- **SSRF Bounding:** Outbound requests using `httpx` or `requests` must resolve hostnames to IP addresses and block private subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`).
