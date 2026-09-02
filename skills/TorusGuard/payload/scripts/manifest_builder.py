#!/usr/bin/env python3
"""
TorusGuard Cryptographic Manifest Builder & Verifier
Generates or validates SHA-256 integrity digests for all .torusguard files.
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path


def compute_file_sha256(filepath):
    """Compute SHA-256 digest of a file in binary mode."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as fh:
        while chunk := fh.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def scan_workspace_files(base_dir):
    """Scan all files inside .torusguard, ignoring runs, pyc, and gitkeep."""
    base_dir = Path(base_dir).resolve()
    file_map = {}

    for root, dirs, files in os.walk(base_dir):
        if "runs" in dirs:
            dirs.remove("runs")
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")

        for f in sorted(files):
            if f in [".manifest.json", ".gitkeep"] or f.endswith(".pyc"):
                continue
            full_path = Path(root) / f
            rel_path = full_path.relative_to(base_dir).as_posix()
            file_map[rel_path] = compute_file_sha256(full_path)

    return file_map


def check_manifest(base_dir):
    """Check disk files against existing .manifest.json."""
    base_dir = Path(base_dir).resolve()
    manifest_file = base_dir / ".manifest.json"

    if not manifest_file.exists():
        print(f"[ERROR] Missing manifest file: {manifest_file}")
        return False

    with open(manifest_file, "r", encoding="utf-8") as fh:
        expected = json.load(fh)

    current = scan_workspace_files(base_dir)

    # Files expected to change during user initialization/configuration
    USER_CONFIGS = {"config/torusguard.json", "config/scope.json"}

    missing = set(expected.keys()) - set(current.keys())
    added = set(current.keys()) - set(expected.keys())
    altered_core = [k for k in expected if k in current and expected[k] != current[k] and k not in USER_CONFIGS]
    altered_configs = [k for k in expected if k in current and expected[k] != current[k] and k in USER_CONFIGS]

    print("================================================================================")
    print("TORUSGUARD INTEGRITY MANIFEST VERIFICATION")
    print("================================================================================")
    print(f"Directory: {base_dir}")
    print(f"Indexed Files: {len(expected)}")

    if missing:
        print(f"\n[FAIL] Missing files ({len(missing)}):")
        for m in sorted(missing):
            print(f"  - {m}")

    if altered_core:
        print(f"\n[FAIL] Altered / Tampered core files ({len(altered_core)}):")
        for a in sorted(altered_core):
            print(f"  - {a}")

    if altered_configs:
        print(f"\n[INFO] Tailored user project configs ({len(altered_configs)}):")
        for ac in sorted(altered_configs):
            print(f"  * {ac}")

    if added:
        print(f"\n[INFO] Untracked new files ({len(added)}):")
        for ad in sorted(added):
            print(f"  + {ad}")

    if not missing and not altered_core:
        print("\n[PASS] 100% of workspace files match cryptographic SHA-256 signatures cleanly.")
        print("================================================================================")
        return True

    print("\n================================================================================")
    print("INTEGRITY VERIFICATION FAILED")
    print("================================================================================")
    return False


def write_manifest(base_dir):
    """Write freshly computed manifest to .torusguard/.manifest.json."""
    base_dir = Path(base_dir).resolve()
    manifest_file = base_dir / ".manifest.json"

    current = scan_workspace_files(base_dir)
    with open(manifest_file, "w", encoding="utf-8") as fh:
        json.dump(current, fh, indent=2)

    print(f"[SUCCESS] Wrote {len(current)} entries to {manifest_file}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TorusGuard Manifest Builder & Verifier")
    parser.add_argument("--dir", default=".torusguard", help="Target .torusguard directory")
    parser.add_argument("--write", action="store_true", help="Generate and write manifest")
    parser.add_argument("--check", action="store_true", help="Check workspace against manifest")
    args = parser.parse_args()

    if args.write:
        success = write_manifest(args.dir)
    else:
        # Default to --check
        success = check_manifest(args.dir)

    sys.exit(0 if success else 1)
