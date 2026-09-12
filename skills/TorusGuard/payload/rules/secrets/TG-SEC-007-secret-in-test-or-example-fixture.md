# TG-SEC-007: Secret in Test or Example Fixture

## Severity
Medium. Committing real production or staging credentials into test fixtures, mocks, or example configuration files leaks secrets under the assumption that test directories are unmonitored.

## Applies To
- Test Suites, Mock Fixtures, Example Configs
- All Languages & Frameworks

## Why It Matters
Developers often copy live payload captures from production to create integration tests or seed fixtures. If these fixtures contain real API keys or customer JWT tokens, they are exposed in source control.

## What TorusGuard Looks For
- High-entropy tokens, Stripe live keys (`sk_live_`), or valid JWT signatures present in `tests/`, `fixtures/`, or `examples/` directories.

## Unsafe Example
```javascript
// UNSAFE: Real active production API key used in test fixture
const mockAuth = {
  apiKey: "sk_live_51M0...REAL_STRIPE_LIVE_KEY_12345"
};
```

## Safe Example
```javascript
// SAFE: Explicit synthetic mock sentinel string
const mockAuth = {
  apiKey: "sk_test_fake_mock_token_for_unit_tests_only"
};
```

## Ponytail Remediation Budget
- Additions: <= 2 lines
- Deletions: <= 2 lines

## Remediation
1. Replace all real credentials in test directories with synthetic, inert mock sentinels (`test_token_dummy`).
2. Rotate any credentials that were copied from production to test files.

## Related Rules
- `TG-SEC-001`: Hardcoded Secret or API Key in Tracked Source
- `TG-SEC-004`: Sensitive Information in Logs
