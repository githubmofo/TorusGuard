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
        language = "TypeScript" if (list(pkg_dir.glob("*.ts")) or list(pkg_dir.glob("**/*.ts"))) else "JavaScript"
        if package_json.is_file():
            try:
                with open(package_json, "r", encoding="utf-8") as f:
                    pj = json.load(f)
                    name = pj.get("name", name)
                    deps = {**pj.get("dependencies", {}), **pj.get("devDependencies", {})}
                    if "next" in deps:
                        framework = "nextjs"
                    elif "@nestjs/core" in deps:
                        framework = "nestjs"
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
            language = "Python"
        content = ""
        if pyproject.is_file():
            content += pyproject.read_text(encoding="utf-8", errors="replace").lower()
        if reqs.is_file():
            content += reqs.read_text(encoding="utf-8", errors="replace").lower()
        for pyf in pkg_dir.glob("*.py"):
            content += pyf.read_text(encoding="utf-8", errors="replace").lower()
        
        if "fastapi" in content or "fastapi" in pkg_dir.name:
            framework = "FastAPI"
        elif "django" in content or "django" in pkg_dir.name:
            framework = "Django"
        elif "flask" in content or "flask" in pkg_dir.name:
            framework = "Flask"

    # Check Go
    go_mod = pkg_dir / "go.mod"
    if go_mod.is_file() or list(pkg_dir.glob("*.go")):
        if language == "unknown":
            language = "Go"
        if go_mod.is_file():
            try:
                gc = go_mod.read_text(encoding="utf-8", errors="replace")
                if "gin-gonic/gin" in gc:
                    framework = "Gin"
                elif "gofiber/fiber" in gc:
                    framework = "Fiber"
                elif "go-chi/chi" in gc:
                    framework = "Chi"
            except Exception:
                pass

    # Check Rust
    cargo_toml = pkg_dir / "Cargo.toml"
    if cargo_toml.is_file() or list(pkg_dir.glob("*.rs")):
        if language == "unknown":
            language = "Rust"
        if cargo_toml.is_file():
            try:
                cc = cargo_toml.read_text(encoding="utf-8", errors="replace")
                if "actix-web" in cc:
                    framework = "Actix-web"
                elif "axum" in cc:
                    framework = "Axum"
                elif "rocket" in cc:
                    framework = "Rocket"
            except Exception:
                pass

    # Check Java / Kotlin
    pom_xml = pkg_dir / "pom.xml"
    b_gradle = pkg_dir / "build.gradle"
    b_gradle_kts = pkg_dir / "build.gradle.kts"
    if pom_xml.is_file() or b_gradle.is_file() or b_gradle_kts.is_file() or list(pkg_dir.glob("**/*.java")) or list(pkg_dir.glob("**/*.kt")):
        if language == "unknown":
            language = "Kotlin" if (b_gradle_kts.is_file() or list(pkg_dir.glob("**/*.kt"))) else "Java"
        jc = ""
        for jf in [pom_xml, b_gradle, b_gradle_kts]:
            if jf.is_file():
                try:
                    jc += jf.read_text(encoding="utf-8", errors="replace") + "\n"
                except Exception:
                    pass
        if "spring-boot" in jc or "springframework" in jc:
            framework = "Spring Boot"
        elif "quarkus" in jc:
            framework = "Quarkus"
        elif "ktor" in jc:
            framework = "Ktor"

    # Check C#
    csprojs = list(pkg_dir.glob("*.csproj")) + list(pkg_dir.glob("**/*.csproj"))
    if csprojs or list(pkg_dir.glob("*.sln")) or list(pkg_dir.glob("*.cs")):
        if language == "unknown":
            language = "C#"
        csc = ""
        for cf in csprojs[:5]:
            try:
                csc += cf.read_text(encoding="utf-8", errors="replace") + "\n"
            except Exception:
                pass
        if "Microsoft.NET.Sdk.Web" in csc or "Microsoft.AspNetCore" in csc or "Swashbuckle" in csc:
            framework = "ASP.NET Core"

    # Check PHP
    composer_json = pkg_dir / "composer.json"
    if composer_json.is_file() or list(pkg_dir.glob("*.php")):
        if language == "unknown":
            language = "PHP"
        if composer_json.is_file():
            try:
                with open(composer_json, "r", encoding="utf-8") as f:
                    c_data = json.load(f)
                reqs = {**c_data.get("require", {}), **c_data.get("require-dev", {})}
                if "laravel/framework" in reqs:
                    framework = "Laravel"
                elif any("symfony" in k for k in reqs):
                    framework = "Symfony"
            except Exception:
                pass

    # Check Ruby
    gemfile = pkg_dir / "Gemfile"
    if gemfile.is_file() or list(pkg_dir.glob("*.rb")):
        if language == "unknown":
            language = "Ruby"
        if gemfile.is_file():
            try:
                gc = gemfile.read_text(encoding="utf-8", errors="replace")
                if "rails" in gc:
                    framework = "Ruby on Rails"
            except Exception:
                pass

    return {
        "name": name,
        "path": rel_path,
        "language": language.lower(),
        "framework": framework.lower()
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
    candidate_folders = ["apps", "packages", "services", "src", "libs", "modules"]
    manifest_names = [
        "package.json", "pyproject.toml", "requirements.txt", "setup.py", "Cargo.toml",
        "go.mod", "pom.xml", "build.gradle", "build.gradle.kts", "composer.json",
        "Gemfile", "mix.exs", "pubspec.yaml", "CMakeLists.txt", "main.py", "main.go", "actions.ts"
    ]
    found_dirs = []
    
    def has_manifest(d: Path) -> bool:
        if any((d / m).exists() for m in manifest_names):
            return True
        if list(d.glob("*.csproj")) or list(d.glob("*/*.csproj")):
            return True
        return False

    for cf in candidate_folders:
        container = root / cf
        if container.is_dir():
            for child in container.iterdir():
                if child.is_dir() and not child.name.startswith(('.', '_')):
                    if has_manifest(child):
                        found_dirs.append(child)

    # Also scan direct subdirectories if not already captured
    for child in root.iterdir():
        if child.is_dir() and not child.name.startswith(('.', '_')) and child.name not in candidate_folders:
            if has_manifest(child):
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
