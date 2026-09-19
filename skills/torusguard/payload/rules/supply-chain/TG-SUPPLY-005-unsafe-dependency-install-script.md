# TG-SUPPLY-005: Unsafe Dependency Install Script

## Severity
Critical. Piping remote scripts directly from `curl` or `wget` into `bash` or `sh` without checksum verification or cryptographic signature checking creates an immediate Remote Code Execution (RCE) vulnerability.

## Applies To
- CI/CD Workflows, Setup Scripts, Dockerfiles, Provisioning Scripts
- Shell, Bash, Dockerfile

## Why It Matters
If the remote server is compromised, the DNS hijacked, or a CDN man-in-the-middle occurs, arbitrary malicious code is executed directly in your environment. Furthermore, partial network downloads can cause truncated execution of dangerous shell commands.

## What TorusGuard Looks For
- Shell patterns piping `curl -s ... | bash` or `wget -O- ... | sh`.

## Unsafe Example
```bash
# UNSAFE: Piping remote URL directly into shell execution
curl -sSL https://install.vendor.com/setup.sh | bash
```

## Safe Example
```bash
# SAFE: Downloading script, verifying SHA-256 checksum, and executing
EXPECTED_SHA="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
curl -sSL -o install.sh https://install.vendor.com/setup.sh
echo "${EXPECTED_SHA}  install.sh" | sha256sum --check -
bash install.sh
```

## Ponytail Remediation Budget
- Additions: <= 5 lines
- Deletions: <= 2 lines

## Remediation
1. Avoid piping remote URLs directly into shell execution.
2. Download the installation script to a file and verify its SHA-256 checksum before execution.
3. Package dependencies through verified package managers (npm, pip, cargo, apt) rather than curl scripts.

## Related Rules
- `TG-INPUT-004`: Command Injection via Shell Execution
- `TG-SUPPLY-004`: Unpinned CI Action
