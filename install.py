#!/usr/bin/env python3
"""
TorusGuard Standalone Zero-Dependency Installer
Allows direct terminal setup via:
    python install.py [--target /path/to/project]
or:
    curl -sSL https://raw.githubusercontent.com/githubmofo/TorusGuard/main/install.py | python
"""

import os
import sys
import shutil
import json
import argparse
import urllib.request
import tempfile
import zipfile
from pathlib import Path

REPO_URL = "https://github.com/githubmofo/TorusGuard"
ARCHIVE_URL = "https://github.com/githubmofo/TorusGuard/archive/refs/heads/main.zip"


def install_torusguard(target_dir=None, force=False):
    target_root = Path(target_dir or os.getcwd()).resolve()
    torusguard_target = target_root / ".torusguard"
    here = Path(__file__).resolve().parent

    print("================================================================================")
    print("TORUSGUARD ZERO-DEPENDENCY INSTALLER")
    print("================================================================================")
    print(f"Target Directory: {target_root}")
    print(f"Destination:      {torusguard_target}")

    if torusguard_target.exists() and not force:
        print(f"\n[INFO] .torusguard workspace already exists at {torusguard_target}")
        print("Use --force to re-scaffold.")
        return True

    # Check if we are running inside the TorusGuard repository clone
    local_source = here / ".torusguard"
    bundled_payload = here / "skills" / "torusguard" / "payload"
    bootstrap_script = here / "skills" / "torusguard" / "bootstrap.py"

    if bootstrap_script.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("bootstrap", str(bootstrap_script))
        bootstrap_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bootstrap_mod)
        return bootstrap_mod.scaffold_workspace(target_root=target_root, force=force)

    # Standalone execution (download archive from GitHub)
    print("\nDownloading TorusGuard workspace archive from GitHub...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_zip = Path(tmpdir) / "torusguard.zip"
        try:
            req = urllib.request.Request(ARCHIVE_URL, headers={"User-Agent": "TorusGuard-Installer/0.9.1"})
            with urllib.request.urlopen(req) as resp, open(tmp_zip, "wb") as out_f:
                shutil.copyfileobj(resp, out_f)
            print("  [SUCCESS] Archive downloaded successfully.")

            with zipfile.ZipFile(tmp_zip, "r") as zip_ref:
                zip_ref.extractall(tmpdir)

            extracted_root = Path(tmpdir) / "TorusGuard-main"
            remote_source = extracted_root / ".torusguard"

            if remote_source.is_dir():
                if torusguard_target.exists() and force:
                    shutil.rmtree(torusguard_target)
                shutil.copytree(remote_source, torusguard_target, ignore=shutil.ignore_patterns("runs", "*.pyc", "__pycache__"))
                print(f"  [SUCCESS] Scaffolding copied into {torusguard_target}")
            else:
                print("  [ERROR] .torusguard folder not found in extracted archive.")
                return False

        except Exception as e:
            print(f"  [ERROR] Installation failed: {e}")
            return False

    print("\n================================================================================")
    print("[SUCCESS] TORUSGUARD INSTALLED SUCCESSFULLY!")
    print("================================================================================")
    print("Next steps:")
    print("  1. Open your AI IDE (Antigravity, Cursor, Claude Code, Cline).")
    print("  2. Run `/torusguard audit` to scan your project.")
    print("================================================================================")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TorusGuard Standalone Installer")
    parser.add_argument("--target", type=str, help="Target project root directory")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing workspace")
    args = parser.parse_args()

    success = install_torusguard(target_dir=args.target, force=args.force)
    sys.exit(0 if success else 1)
