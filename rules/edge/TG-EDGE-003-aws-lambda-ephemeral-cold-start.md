# TG-EDGE-003: AWS Lambda Ephemeral Execution & Cold Start Security

## Severity
Medium by default. Escalate to High if IAM credentials or temporary execution tokens are leaked or indefinitely reused across invocations.

## Applies To
- AWS Lambda (Python, Node.js)
- Serverless Framework / AWS SAM / AWS CDK

## Why It Matters
AWS Lambda execution environments are frequently reused across invocations. While initializing heavy clients (such as AWS SDK or database pools) outside the handler improves cold start latency:
1. **Stale Credentials & Leaked Tokens:** Temporary STS session tokens or database auth credentials initialized during cold start can expire or persist between distinct tenants.
2. **Ephemeral Disk Residue (`/tmp`):** The `/tmp` storage directory is preserved across warm invocations of the same execution environment. Writing unencrypted sensitive files, tokens, or customer exports to `/tmp` can expose data to subsequent requests.
3. **Execution Timeouts:** Unbounded subrequests without client-side timeouts can consume maximum execution seconds, triggering Denial-of-Wallet.

## What TorusGuard Looks For
1. Writing unencrypted sensitive data or credentials directly to `/tmp` without explicit deletion in a `finally` block.
2. Global caching of dynamic, tenant-specific STS or database credentials outside the handler.
3. Outbound network calls inside Lambda handlers lacking explicit connection and read timeouts.

## Unsafe Example
```python
# UNSAFE: Writing sensitive customer export to /tmp without cleanup
import os
import boto3

def lambda_handler(event, context):
    user_id = event["userId"]
    temp_path = f"/tmp/export_{user_id}.json"
    
    # Writes sensitive data to /tmp; persists across warm invocations!
    with open(temp_path, "w") as f:
        f.write(event["sensitiveUserData"])
        
    upload_to_s3(temp_path)
    # Missing cleanup: subsequent invocations can access this file!
    return {"status": "ok"}
```

## Safe Example
```python
# SAFE: Ephemeral cleanup guaranteed via try/finally and unique temp storage
import os
import tempfile
import boto3

def lambda_handler(event, context):
    user_id = event.get("userId")
    if not user_id:
        return {"statusCode": 400, "body": "Missing userId"}

    # Use secure tempfile with guaranteed cleanup
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        try:
            temp_file.write(event["sensitiveUserData"])
            temp_file.flush()
            upload_to_s3(temp_file.name)
        finally:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)

    return {"statusCode": 200, "body": "Export completed safely"}
```

## Remediation
1. **Always clean up `/tmp` files:** Use `tempfile.NamedTemporaryFile` with a `finally` block or context manager that guarantees file removal.
2. **Avoid Global Caching of Tenant Context:** Initialize IAM STS assume-role credentials per request within the handler.
3. **Configure Timeouts:** Set client connection and read timeouts on all outbound HTTP and AWS SDK clients.

## Verification
- Assert that all `/tmp` file writes are wrapped in cleanup blocks.
- Test that consecutive invocations with different tenant payloads do not find pre-existing files in `/tmp`.

## Related Rules
- `TG-EDGE-001`: Serverless & Edge Global State Memory Leakage
- `TG-SEC-001`: Hardcoded Secrets
