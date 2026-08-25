# TorusGuard Deterministic Replay & Regression Workflow Guide

## 🎯 Purpose

This guide details how to add, replay, and validate security fixtures using the **TorusGuard Validation Engine** (`harness/engine/`).

---

## 🏗️ 1. Adding a New Validation Fixture

To add a test fixture:
1. Create paired directories under `examples/<language>/<name>-vuln` and `examples/<language>/<name>-hardened`.
2. Ensure the vulnerable variant contains the unmitigated flaw with an expected finding count > 0.
3. Ensure the hardened variant applies the prescriptive fix and contains 0 findings.
4. Register the fixture in `harness/engine/fixture_manager.py` using `FixtureDefinition`.

### Example Fixture Definition
```python
FixtureDefinition(
    fixture_id="TG-FIX-django-idor-scoping",
    framework="django",
    scenario="Django ViewSet object-level authorization & settings DEBUG exposure",
    target_rule_id="TG-AUTH-007",
    expected_outcome=ValidationOutcome.VULNERABLE_CONFIRMED,
    vulnerable_variant=FixtureVariant(
        relative_path="examples/python/django-vuln",
        code_pattern="Invoice.objects.all()",
        expected_findings_count=6,
    ),
    hardened_variant=FixtureVariant(
        relative_path="examples/python/django-hardened",
        code_pattern="Invoice.objects.filter(owner=request.user)",
        expected_findings_count=0,
        is_hardened=True,
    ),
    reproduction_command="python manage.py test",
    expected_diff_summary="DEBUG set to False; get_queryset scoped to request.user.",
)
```

---

## 🔁 2. Running Replays & Differential Comparison

Execute the full suite:

```bash
python harness/runner.py
```

### What Happens Behind the Scenes:
1. **Schema Check:** Verifies JSON schema validity for `fixture.schema.json` and `validation-run.schema.json`.
2. **Replay Cycle:** Executes 3 consecutive passes against the target, hashing serialized outputs to confirm byte-for-byte determinism.
3. **Differential Check:** Confirms that the vulnerable target triggers findings while the hardened target remains clean.
4. **Regression Assertion:** Verifies that all historical regression cases remain in the `Clean` state.

---

## 🔍 3. Diagnosing Discrepancies

If a test fails, the `FalsePositiveAnalyzer` surfaces the root cause:
- **`False Positive`:** The hardened variant triggered a finding. Refine the rule regex/AST logic in `rules/` to whitelist the safe framework idiom.
- **`False Negative`:** The vulnerable variant failed to trigger a finding. Broaden the detection pattern in `rules/`.
- **`Regression Detected`:** A previously fixed baseline fixture failed to pass. Investigate recent rule or parser changes.
