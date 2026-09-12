# TG-SUPPLY-003: Unsafe CI/CD Secret Exposure in Workflow Logs

## Severity
Critical. Echoing or printing pipeline secrets in CI/CD step commands (`echo ${{ secrets.API_KEY }}`) or passing secrets directly in command line arguments persists plaintext credentials in build logs.

## Applies To
- GitHub Actions, GitLab CI, CircleCI, Bitbucket Pipelines
- YAML Workflows

## Why It Matters
CI/CD logs are often accessible to broad team members, external contributors, or public viewers on open-source repositories. Even when CI providers attempt log masking, modified or base64-encoded strings bypass masking and remain permanently visible in build logs.

## What TorusGuard Looks For
- CI steps running `echo` or `print` on `${{ secrets.* }}` or `$SECRET_*`.
- Passing secrets as command-line arguments instead of masked environment variables.

## Unsafe Example
```yaml
# UNSAFE: Echoing secrets directly into execution step logs
- name: Deploy to Cloud
  run: |
    echo "Using token ${{ secrets.DEPLOY_TOKEN }}"
    deploy-tool --token ${{ secrets.DEPLOY_TOKEN }}
```

## Safe Example
```yaml
# SAFE: Injecting secrets strictly via environment variables without logging
- name: Deploy to Cloud
  env:
    DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
  run: |
    deploy-tool
```

## Ponytail Remediation Budget
- Additions: <= 5 lines
- Deletions: <= 3 lines

## Remediation
1. Never print or echo secret variables in workflow step commands.
2. Pass secrets into steps strictly via the `env:` block.
3. Avoid command-line arguments for secrets; configure tools to read credentials from environment variables or secure files.

## Related Rules
- `TG-SEC-001`: Hardcoded Secret or API Key in Tracked Source
- `TG-SUPPLY-004`: Unpinned CI Action
