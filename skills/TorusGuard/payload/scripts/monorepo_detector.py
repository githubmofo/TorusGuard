#!/usr/bin/env python3
"""
TorusGuard Monorepo & Multi-Package Workspace Detector (v0.9.3)
Discovers and profiles sub-projects across Turborepo, pnpm, npm, and Python workspaces.
Pure Python 3.10+ standard library (zero external dependencies).
"""

import sys
import os
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional


def detect_package_info(abs_pkg_dir: Path, root: Path) -> Dict[str, Any]:
    """Inspects a single directory to detect language and framework."""
    rel_path = str(abs_pkg_dir.relative_to(root)).replace('\\', '/')
    name = abs_pkg_dir.name
    language = "unknown"
    framework = "generic"

    pkg_dir = abs_pkg_dir

    # Check typescript / javascript
    package_json = pkg_dir / "package.json"
    if package_json.is_file() or list(pkg_dir.glob("*.ts")) or list(pkg_dir.glob("*.js")):
        language = "typescript"
        if package_json.is_file():
            try:
                with open(package_json, "r", encoding="utf-8") as f:
                    pj = json.load(f)
                    name = pj.get("name", name)
                    deps = {**pj.get("dependencies", {}), **pj.get("devDependencies", {})}
                    if "next" in deps:
                        framework = "nextjs"
                    elif "express" in deps:
                        framework = "express"
                    elif "react" in deps:
                        framework = "react"
                    elif "vue" in deps or "nuxt" in deps:
                        framework = "vue"
            except Exception:
                pass
        elif list(pkg_dir.glob("*next*")) or "next" in pkg_dir.name:
            framework = "nextjs"

    # Check python
    pyproject = pkg_dir / "pyproject.toml"
    reqs = pkg_dir / "requirements.txt"
    if pyproject.is_file() or reqs.is_file() or list(pkg_dir.glob("*.py")):
        if language == "unknown":
            language = "python"
        content = ""
        if pyproject.is_file():
            content += pyproject.read_text(encoding="utf-8", errors="replace").lower()
        if reqs.is_file():
            content += reqs.read_text(encoding="utf-8", errors="replace").lower()
        for pyf in pkg_dir.glob("*.py"):
            content += pyf.read_text(encoding="utf-8", errors="replace").lower()
        
        if "fastapi" in content or "fastapi" in pkg_dir.name:
            framework = "fastapi"
        elif "django" in content or "django" in pkg_dir.name:
            framework = "django"
        elif "flask" in content or "flask" in pkg_dir.name:
            framework = "flask"

    return {
        "name": name,
        "path": rel_path,
        "language": language,
        "framework": framework
    }


def scan_workspace(root_dir: str = ".") -> Dict[str, Any]:
    """Scans root directory for monorepo configuration and sub-packages."""
    root = Path(root_dir).resolve()
    monorepo_type = "single-project"
    sub_packages: List[Dict[str, Any]] = []

    # 1. Turborepo
    if (root / "turbo.json").is_file():
        monorepo_type = "turborepo"

    # 2. pnpm workspace
    pnpm_ws = root / "pnpm-workspace.yaml"
    if pnpm_ws.is_file():
        monorepo_type = "pnpm-workspace"

    # 3. npm / yarn workspaces
    root_pj = root / "package.json"
    if root_pj.is_file():
        try:
            with open(root_pj, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "workspaces" in data:
                    monorepo_type = "npm/yarn-workspaces"
        except Exception:
            pass

    # Scan common monorepo container directories and direct project subfolders
    candidate_folders = ["apps", "packages", "services", "libs", "modules"]
    found_dirs = []
    
    for cf in candidate_folders:
        container = root / cf
        if container.is_dir():
            for child in container.iterdir():
                if child.is_dir() and not child.name.startswith(('.', '_')):
                    if any((child / m).exists() for m in ["package.json", "pyproject.toml", "requirements.txt", "setup.py", "Cargo.toml", "main.py"]):
                        found_dirs.append(child)

    # Also scan direct subdirectories if not already captured
    for child in root.iterdir():
        if child.is_dir() and not child.name.startswith(('.', '_')) and child.name not in candidate_folders:
            if any((child / m).exists() for m in ["package.json", "pyproject.toml", "requirements.txt", "setup.py", "Cargo.toml", "main.py", "actions.ts"]):
                if child not in found_dirs:
                    found_dirs.append(child)

    if found_dirs:
        if monorepo_type == "single-project":
            monorepo_type = "multi-package-directory"
        for d in found_dirs:
            sub_packages.append(detect_package_info(d, root))

    # If no monorepo sub-packages found, treat root as primary
    if not sub_packages:
        sub_packages.append(detect_package_info(root, root))

    return {
        "root": str(root).replace('\\', '/'),
        "monorepo_type": monorepo_type,
        "is_monorepo": monorepo_type != "single-project",
        "package_count": len(sub_packages),
        "packages": sub_packages
    }


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Monorepo & Multi-Package Detector")
    parser.add_argument("--scan", default=".", help="Root directory to scan (default: .)")
    parser.add_argument("--write", action="store_true", help="Write to .torusguard/config/workspaces.json")
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout")
    args = parser.parse_args()

    res = scan_workspace(args.scan)

    if args.write:
        config_dir = Path(args.scan) / ".torusguard" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        out_file = config_dir / "workspaces.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2)
        print(f"[SUCCESS] Wrote workspace registry to {out_file}")

    if args.json or not args.write:
        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
