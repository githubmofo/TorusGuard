# Deployment Security Pre-flight - [PROJECT_NAME]

## Release metadata
- **Project:** [PROJECT_NAME]
- **Release version:** [RELEASE_VERSION]
- **Environment:** [TARGET_ENVIRONMENT]
- **Release date:** [RELEASE_DATE]
- **Release owner:** [RELEASE_OWNER]

## Pre-flight checks

### Secrets/config
- [ ] Secrets are loaded from approved secret manager (`[SECRETS_MANAGER_NAME]`)
- [ ] No secrets are hardcoded in code, config, or client bundle
- [ ] Environment variables are complete and validated for `[TARGET_ENVIRONMENT]`
- [ ] Secret rotation status is current for `[CRITICAL_SECRET_LIST]`

### Database exposure
- [ ] Database is not publicly reachable from the internet
- [ ] Network ACL/security group rules allow only approved sources
- [ ] Database credentials use least privilege roles
- [ ] TLS is enforced for database connections

### Input validation
- [ ] Server-side validation is enforced for all external inputs
- [ ] File upload validation (type/size/content) is enforced
- [ ] Dangerous deserialization and command execution paths are blocked
- [ ] Validation failures return safe error responses

### Auth/authorization
- [ ] Authentication is required for protected routes
- [ ] Authorization checks enforce role/resource ownership
- [ ] Privileged actions require elevated permissions and audit trail
- [ ] Session/token configuration matches security baseline

### Rate limits/resource controls
- [ ] Rate limiting is enabled for public and auth endpoints
- [ ] Abuse controls exist for brute-force and scraping scenarios
- [ ] Request concurrency/timeouts are configured
- [ ] Resource quotas are enforced for expensive operations

### Client bundle/source maps
- [ ] Client bundle excludes secrets and internal-only config values
- [ ] Source maps are disabled for production or access-restricted
- [ ] Debug endpoints and development flags are disabled
- [ ] Dependency metadata leakage has been reviewed

### CORS/headers/errors
- [ ] CORS allows only approved origins/methods/headers
- [ ] Security headers (CSP, HSTS, X-Content-Type-Options, etc.) are set
- [ ] Error responses avoid stack traces and internal details
- [ ] Cookie flags (`Secure`, `HttpOnly`, `SameSite`) are correctly configured

### HTTPS/deployment
- [ ] HTTPS is enforced end-to-end with valid certificates
- [ ] Redirects from HTTP to HTTPS are enabled
- [ ] Deployment uses immutable artifacts and verified provenance
- [ ] Rollback and health-check gates are confirmed

### Dependency review
- [ ] Dependency scan completed with no unapproved critical/high CVEs
- [ ] Lockfiles are committed and reproducible builds are enabled
- [ ] New dependencies have ownership and maintenance review
- [ ] Runtime base images/packages are patched to current baseline

### Backups/logging/monitoring
- [ ] Backup jobs and restore tests are current
- [ ] Security/audit logging is enabled and retained per policy
- [ ] Monitoring and alerts cover auth failures, error spikes, and latency
- [ ] Incident escalation contacts and runbooks are current

## Final decision
- [ ] **PASS**
- [ ] **PASS WITH WARNINGS**
- [ ] **FAIL**

- **Decision notes:** [FINAL_DECISION_NOTES]
- **Approver:** [APPROVER_NAME]
- **Approval date:** [APPROVAL_DATE]
