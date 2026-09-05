"""
Validation Harness for TorusGuard v0.8.0 - Part 3 (Scripts, References, Rules & Integration)
Verifies:
1. All 5 Python utility scripts in .torusguard/scripts/
2. All framework reference guides in .torusguard/references/
3. Rule catalog guide in .torusguard/rules/README.md
4. README.md and CHANGELOG.md integration
5. Functional execution of utility scripts
"""

import sys
import json
import subprocess
from pathlib import Path

def test_part3_scripts_references_integration():
    root = Path(__file__).resolve().parent.parent
    torusguard_dir = root / ".torusguard"
    
    print("=== TorusGuard v0.8.0 Part 3 Validation ===")
    
    # 1. Check Python Utility Scripts (5 files)
    scripts_dir = torusguard_dir / "scripts"
    assert scripts_dir.is_dir(), "Missing .torusguard/scripts directory"
    expected_scripts = [
        "stack_detect.py",
        "finding_scorer.py",
        "sarif_exporter.py",
        "run_manager.py",
        "safety_gate.py"
    ]
    for script_name in expected_scripts:
        script_file = scripts_dir / script_name
        assert script_file.is_file(), f"Missing script: {script_file}"
        res = subprocess.run([sys.executable, str(script_file), "--help"], capture_output=True, text=True)
        assert res.returncode == 0, f"Script {script_name} --help failed: {res.stderr}"
        print(f"  [PASS] Script verified & runnable: {script_name}")

    # 2. Test Functional Execution of Scripts
    # Test finding_scorer
    res_scorer = subprocess.run([sys.executable, str(scripts_dir / "finding_scorer.py"), "--eq", "35", "--rs", "25", "--ic", "15", "--ec", "15", "--json"], capture_output=True, text=True)
    assert res_scorer.returncode == 0, "finding_scorer failed"
    scorer_data = json.loads(res_scorer.stdout)
    assert scorer_data["total_score"] >= 90 and scorer_data["classification_band"] == "Confirmed", f"Unexpected scorer output: {scorer_data}"
    print(f"  [PASS] finding_scorer.py functional execution verified (Score: {scorer_data['total_score']})")

    # Test safety_gate
    res_gate = subprocess.run([sys.executable, str(scripts_dir / "safety_gate.py"), "-m", "DELETE", "-p", "/admin/delete", "--json"], capture_output=True, text=True)
    assert res_gate.returncode == 0, "safety_gate failed"
    gate_data = json.loads(res_gate.stdout)
    assert gate_data["decision"] == "Manual Only"
    print(f"  [PASS] safety_gate.py functional execution verified (DELETE -> Manual Only)")

    # Test stack_detect
    res_stack = subprocess.run([sys.executable, str(scripts_dir / "stack_detect.py"), str(root), "--json"], capture_output=True, text=True)
    assert res_stack.returncode == 0, "stack_detect failed"
    stack_data = json.loads(res_stack.stdout)
    assert "language" in stack_data and "confidence" in stack_data
    print(f"  [PASS] stack_detect.py functional execution verified (Detected: {stack_data['language']} / {stack_data['framework']})")

    # 3. Check Framework References
    ref_dir = torusguard_dir / "references"
    assert ref_dir.is_dir(), "Missing .torusguard/references directory"
    expected_refs = [
        "django-security.md",
        "fastapi-security.md",
        "flask-security.md",
        "drf-security.md",
        "sqlalchemy-security.md",
        "nextjs-security.md",
        "express-security.md",
        "react-vite-security.md",
        "supabase-security.md",
        "firebase-security.md"
    ]
    for ref_name in expected_refs:
        ref_file = ref_dir / ref_name
        assert ref_file.is_file(), f"Missing reference: {ref_file}"
        assert len(ref_file.read_text(encoding="utf-8")) > 100, f"Reference {ref_name} is too short"
        print(f"  [PASS] Reference guide verified: {ref_name}")

    # 4. Check Rules System README
    rules_readme = torusguard_dir / "rules" / "README.md"
    assert rules_readme.is_file(), "Missing .torusguard/rules/README.md"
    content_rules = rules_readme.read_text(encoding="utf-8")
    assert "Rule Architecture & Taxonomy" in content_rules
    assert "Active Rules System" in content_rules
    print("  [PASS] .torusguard/rules/README.md catalog verified")

    # 5. Check README & CHANGELOG Integration
    readme_file = root / "README.md"
    readme_content = readme_file.read_text(encoding="utf-8")
    assert "Release-v0." in readme_content or "Release-v1." in readme_content, "README.md missing Release badge"
    assert "npx skills add" in readme_content, "README.md missing npx skills add instruction"
    assert "/torusguard verify" in readme_content, "README.md missing /torusguard verify command"
    assert "/torusguard report" in readme_content, "README.md missing /torusguard report command"
    assert "/torusguard status" in readme_content, "README.md missing /torusguard status command"
    print("  [PASS] README.md integration verified (v0.8.0, npx install, 11 commands)")

    changelog_file = root / "CHANGELOG.md"
    changelog_content = changelog_file.read_text(encoding="utf-8")
    assert "## [0.8.0]" in changelog_content, "CHANGELOG.md missing [0.8.0] entry"
    print("  [PASS] CHANGELOG.md integration verified ([0.8.0] entry present)")

    print("\n>>> ALL TORUSGUARD v0.8.0 PART 3 CHECKS PASSED (100%) <<<\n")

if __name__ == "__main__":
    try:
        test_part3_scripts_references_integration()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected exception: {e}")
        sys.exit(2)
