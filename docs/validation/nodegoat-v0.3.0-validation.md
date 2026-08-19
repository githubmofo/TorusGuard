# TorusGuard v0.3.0 External Repository Validation Report
Target: OWASP NodeGoat
Test type: Local, authorized repository review
Status: Validation completed with follow-up actions

## Scope
- Repository: OWASP NodeGoat
- Purpose: Local validation of TorusGuard v0.3.0 rules
- Application type: Intentionally vulnerable Node.js web application
- Database: MongoDB
- Test mode: Simulated /torusguard audit
- Network scope: Local source review only
- No external systems were scanned

## Environment
- Operating system: Windows 10
- Node.js version: 18.x
- Package-manager version: npm 9.x
- Commit hash tested: Latest default branch as of 2026-08-19
- Dependencies installed: Yes
- Application executed: No (MongoDB connection required)
- Audit method: Source analysis and simulated reasoning
- Date of test: 2026-08-19

## Finding Classification
- **Confirmed** — directly verified in source or configuration
- **Likely** — strong evidence exists but needs a runtime/manual check
- **Manual review** — TorusGuard cannot safely determine the result automatically
- **Informational** — useful context without a confirmed vulnerability

## Verified Findings

### TG-CSRF-001
Status: Confirmed configuration finding
Evidence: CSRF middleware configuration is commented out in server.js, and state-changing session-authenticated routes remain active.
Impact: An attacker may be able to induce authenticated browser requests from another origin if no equivalent defense exists.
Remediation: Use a maintained CSRF protection strategy appropriate to the application, or migrate to an architecture with a documented alternative defense.

### TG-CACHE-001
Status: Confirmed or likely, depending on runtime headers
Impact: Sensitive user-specific responses may be stored by browser or intermediate caches if cache-control directives are absent.
Remediation: Use private/no-store cache directives for sensitive responses and verify that CDN and reverse-proxy behavior does not override them.

### TG-SUPPLY-*
| Package | Version | Direct/Transitive | Advisory/CVE | Runtime Impact | Recommended Action |
|---|---:|---|---|---|---|
| request | 2.88.0 | Transitive | Deprecated | High | Run ecosystem-specific audit tools (npm audit) |
| express | outdated | Direct | Multiple | Critical | Update to secure version |
| csurf | outdated | Direct | Deprecated | Medium | Migrate away from deprecated package |

## Manual Verification Required
### TG-BIZ-*
- File or route to inspect: `app/routes/allocations.js`
- Expected input: POST data altering allocations
- Safe test environment: Local development server
- What the reviewer must verify: Rate limits and ability to repeat actions across users
- Evidence required to upgrade to Confirmed: Reproducible PoC script showing business logic manipulation
- Evidence required to close the finding: Confirmed server-side validation rejecting manipulated business inputs

### TG-SSRF-*
- File or route to inspect: `app/routes/research.js`
- Expected input: User-supplied URL for fetching
- Safe test environment: Isolated container with no internal network access
- What the reviewer must verify: Whether local/private IPs and link-local metadata addresses are blocked
- Evidence required to upgrade to Confirmed: Successful fetch of a restricted local IP (e.g., 127.0.0.1)
- Evidence required to close the finding: Explicit allowlisting or strict URL parser usage

## NodeGoat Dependency Experiment
`npm audit fix --force` was tested separately on the NodeGoat workspace. It resolved some dependency findings but introduced or exposed major version migrations involving core packages such as Express and MongoDB. These changes are not included in the TorusGuard v0.3.0 release and are not treated as a validated NodeGoat remediation. They require a separate compatibility and refactoring project.
