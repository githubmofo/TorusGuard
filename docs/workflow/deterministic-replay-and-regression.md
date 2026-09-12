# TorusGuard Deterministic Replay & Regression Workflow Guide (v1.3.5)

## 🎯 Purpose

This guide details how to add, replay, and validate security fixtures and assert regression invariance across the 74-rule polyglot catalog using the **TorusGuard Validation Engine** (`harness/runner.py` and `harness/engine/`) under the **v1.3.5** release line.

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

Execute the full validation battery across all 81 harness test suites:

```bash
# Recommended NPM command
npm test

# Direct Python test runner
python harness/runner.py
```

### What Happens Behind the Scenes:
1. **Schema Check:** Verifies JSON schema validity for all 10 schemas including `fixture.schema.json`, `golden-recipe.schema.json`, and `validation-run.schema.json`.
2. **Rule Integrity:** Validates all 74 AST rule specifications across all 18 families.
3. **Replay Cycle:** Executes 3 consecutive passes against each target, hashing serialized outputs to confirm byte-for-byte determinism.
4. **Differential Check:** Confirms that the vulnerable target triggers findings while the hardened target remains clean.
5. **Regression Assertion:** Verifies that all historical regression cases remain in the `Clean` state.
6. **Living Ledger Sync:** Verifies that differential fixes properly transition findings to `RESOLVED 🟢` in `security_report.md`.

---

## 🔍 3. Diagnosing Discrepancies

If a test fails, the `FalsePositiveAnalyzer` surfaces the root cause:
- **`False Positive`:** The hardened variant triggered a finding. Refine the rule regex/AST logic in `.torusguard/scripts/audit_runner.py` to recognise the safe framework idiom.
- **`False Negative`:** The vulnerable variant failed to trigger a finding. Broaden the detection pattern in `audit_runner.py`.
- **`Regression Detected`:** A previously fixed baseline fixture failed to pass. Investigate recent rule or parser changes.
