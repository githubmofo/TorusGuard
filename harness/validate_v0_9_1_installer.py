#!/usr/bin/env python3
"""
TorusGuard v0.9.1 Installation & Autonomy Validation Harness
Simulates external project installation via both:
1. npx skills add + /torusguard init (bootstrap.py)
2. Standalone CLI installer (install.py)
Verifies full workspace scaffolding, manifest verification, and zero regressions.
"""

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path


def test_bootstrap_simulation():
    """Simulates npx skills add in an external project followed by bootstrap.py."""
    print("=== Test 1: Simulating 'npx skills add' + /torusguard init ===")
    repo_root = Path(__file__).resolve().parent.parent

    with tempfile.TemporaryDirectory() as tmpdir:
        test_project = Path(tmpdir) / "sample-django-app"
        test_project.mkdir()

        # Simulate existing project files
        (test_project / "manage.py").write_text("# Django entry point", encoding="utf-8")
        (test_project / "requirements.txt").write_text("django>=5.0\npsycopg2-binary\n", encoding="utf-8")

        # Simulate agent directory where npx skills add puts the skill
        agent_skills_dir = test_project / ".agent" / "skills" / "torusguard"
        shutil.copytree(
            repo_root / "skills" / "torusguard",
            agent_skills_dir,
            ignore=shutil.ignore_patterns("*.pyc", "__pycache__")
        )
        print("  [PASS] Simulated 'npx skills add': skill copied into .agent/skills/torusguard/")

        # Execute bootstrap.py as an agent would on /torusguard init
        bootstrap_script = agent_skills_dir / "bootstrap.py"
        res = subprocess.run(
            [sys.executable, str(bootstrap_script), "--target", str(test_project)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15
        )
        assert res.returncode == 0, f"bootstrap.py failed: {res.stderr}\n{res.stdout}"
        print("  [PASS] bootstrap.py executed with exit code 0")

        # Verify .torusguard directory structure
        tg_dir = test_project / ".torusguard"
        assert tg_dir.is_dir(), "Missing .torusguard directory in project root"

        subdirs = [
            "config", "agents", "workflows", "scripts", "templates",
            "schemas", "references", "rules", "skills", "runs"
        ]
        for s in subdirs:
            assert (tg_dir / s).is_dir(), f"Missing subdirectory in .torusguard: {s}"
        print(f"  [PASS] All {len(subdirs)} subdirectories verified in .torusguard/")

        # Verify core master files
        assert (tg_dir / "TORUSGUARD.md").is_file(), "Missing TORUSGUARD.md"
        assert (tg_dir / "ARCHITECTURE.md").is_file(), "Missing ARCHITECTURE.md"
        assert (tg_dir / ".manifest.json").is_file(), "Missing .manifest.json"
        assert (tg_dir / "rules" / "TORUSGUARD.md").is_file(), "Missing dual-path rules/TORUSGUARD.md"
        print("  [PASS] Core documents verified (TORUSGUARD.md, ARCHITECTURE.md, .manifest.json, dual-path rule)")

        # Verify manifest integrity inside provisioned project
        manifest_script = tg_dir / "scripts" / "manifest_builder.py"
        assert manifest_script.is_file(), "Missing manifest_builder.py"
        res_manifest = subprocess.run(
            [sys.executable, str(manifest_script), "--dir", str(tg_dir), "--check"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15
        )
        assert res_manifest.returncode == 0, f"Manifest check failed in provisioned workspace: {res_manifest.stderr}"
        print("  [PASS] Manifest check verified: 100% hash integrity match")

        # Verify stack detection picked up Django
        cfg_file = tg_dir / "config" / "torusguard.json"
        assert cfg_file.is_file(), "Missing torusguard.json"
        content = cfg_file.read_text(encoding="utf-8")
        assert "django" in content.lower(), f"Expected django in detected stack config: {content}"
        print("  [PASS] Stack detection correctly auto-configured Django stack")

    print("\n>>> TEST 1 PASSED (100%) <<<\n")


def test_standalone_installer():
    """Simulates direct installation via root install.py."""
    print("=== Test 2: Simulating Standalone 'python install.py' ===")
    repo_root = Path(__file__).resolve().parent.parent

    with tempfile.TemporaryDirectory() as tmpdir:
        test_project = Path(tmpdir) / "sample-fastapi-app"
        test_project.mkdir()

        # Simulate FastAPI app files
        (test_project / "main.py").write_text("from fastapi import FastAPI\napp = FastAPI()", encoding="utf-8")
        (test_project / "requirements.txt").write_text("fastapi>=0.110\nuvicorn\nsqlalchemy\n", encoding="utf-8")

        # Run root install.py targeting test_project
        install_script = repo_root / "install.py"
        res = subprocess.run(
            [sys.executable, str(install_script), "--target", str(test_project)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15
        )
        assert res.returncode == 0, f"install.py failed: {res.stderr}\n{res.stdout}"
        print("  [PASS] install.py executed with exit code 0")

        # Verify workspace
        tg_dir = test_project / ".torusguard"
        assert tg_dir.is_dir(), "Missing .torusguard directory in project root"
        assert (tg_dir / "TORUSGUARD.md").is_file(), "Missing TORUSGUARD.md"
        assert (tg_dir / "ARCHITECTURE.md").is_file(), "Missing ARCHITECTURE.md"
        assert (tg_dir / ".manifest.json").is_file(), "Missing .manifest.json"
        print("  [PASS] Standalone installer provisioned complete workspace cleanly")

    print("\n>>> TEST 2 PASSED (100%) <<<\n")


if __name__ == "__main__":
    try:
        test_bootstrap_simulation()
        test_standalone_installer()
        print("================================================================================")
        print("ALL v0.9.1 INSTALLER & WORKSPACE AUTONOMY TESTS PASSED (100%)")
        print("================================================================================")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected exception: {e}")
        sys.exit(2)
