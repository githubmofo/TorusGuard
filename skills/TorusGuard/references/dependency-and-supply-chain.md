# Dependency and Supply Chain

- Lockfiles.
- Dependency update policy.
- Vulnerability audit commands by ecosystem.
- Dependabot/Renovate.
- GitHub Actions pinning.
- CI secret exposure.
- Pull-request workflow trust.
- Install scripts.
- Dependency provenance.
- Review of new packages.

## Audit Commands
```bash
npm audit
pip-audit
osv-scanner --lockfile=package-lock.json
dotnet list package --vulnerable
bundle audit
govulncheck ./...
```
