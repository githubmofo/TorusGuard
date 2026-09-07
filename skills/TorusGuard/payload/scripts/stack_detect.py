#!/usr/bin/env python3
"""
TorusGuard Universal Polyglot Stack Detector (v1.3.0)
Inspects project directory to detect programming language, framework, ORM/data layer,
and dependency manifests across 16+ languages, 30+ frameworks, and 20+ data layers.
Zero external dependencies (100% Python 3.10+ standard library).
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Any

# Windows console UTF-8 support
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        getattr(sys.stderr, "reconfigure")(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

# Comprehensive Manifest Catalog across 16+ Language Ecosystems
MANIFEST_CATALOG: dict[str, str] = {
    # Python
    "pyproject.toml": "Python",
    "requirements.txt": "Python",
    "Pipfile": "Python",
    "poetry.lock": "Python",
    "manage.py": "Python",
    "setup.py": "Python",
    # JavaScript / TypeScript
    "package.json": "JavaScript / TypeScript",
    "pnpm-lock.yaml": "JavaScript / TypeScript",
    "yarn.lock": "JavaScript / TypeScript",
    "bun.lockb": "JavaScript / TypeScript",
    "deno.json": "JavaScript / TypeScript",
    # Go
    "go.mod": "Go",
    "go.sum": "Go",
    # Rust
    "Cargo.toml": "Rust",
    "Cargo.lock": "Rust",
    # Java / Kotlin
    "pom.xml": "Java",
    "build.gradle": "Java / Kotlin",
    "build.gradle.kts": "Kotlin",
    "gradlew": "Java / Kotlin",
    # C# / .NET
    "global.json": "C# / .NET",
    # PHP
    "composer.json": "PHP",
    "composer.lock": "PHP",
    # Ruby
    "Gemfile": "Ruby",
    "Gemfile.lock": "Ruby",
    # Elixir
    "mix.exs": "Elixir",
    "mix.lock": "Elixir",
    # Dart / Flutter
    "pubspec.yaml": "Dart / Flutter",
    "pubspec.lock": "Dart / Flutter",
    # C / C++
    "CMakeLists.txt": "C / C++",
    "Makefile": "C / C++",
    "meson.build": "C / C++",
    # Scala
    "build.sbt": "Scala",
    # Swift
    "Package.swift": "Swift"
}

# Extension mappings for fallback file census
EXTENSION_MAP: dict[str, str] = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".cs": "C#",
    ".php": "PHP",
    ".rb": "Ruby",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".swift": "Swift",
    ".dart": "Dart",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".scala": "Scala",
    ".c": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".h": "C / C++",
    ".hpp": "C++",
    ".sh": "Shell / Bash",
    ".sql": "SQL"
}


def census_file_extensions(project_root: Path) -> dict[str, int]:
    """Tally source file extensions to infer primary languages when no manifest is present."""
    census: dict[str, int] = {}
    ignored_dirs = {".git", "node_modules", "vendor", ".venv", "venv", "dist", "build", ".torusguard", "target"}

    for p in project_root.rglob("*"):
        if p.is_file() and not any(part in ignored_dirs for part in p.parts):
            ext = p.suffix.lower()
            if ext in EXTENSION_MAP:
                lang = EXTENSION_MAP[ext]
                census[lang] = census.get(lang, 0) + 1
    return census


def detect_stack(project_root: Path) -> dict[str, Any]:
    """
    Universally detect programming language, framework, ORM, and dependency manifests.
    """
    profile: dict[str, Any] = {
        "language": "Unknown",
        "framework": "None",
        "data_layer": "None",
        "ecosystem_family": "universal",
        "dependency_files": [],
        "detection_evidence": [],
        "confidence": "Needs Review",
        "recommended_rules": [
            "TG-SEC-*",
            "TG-INPUT-*",
            "TG-AUTH-*"
        ],
        "recommended_references": [
            "polyglot-security-matrix.md"
        ]
    }

    # 1. Discover all dependency manifest files present
    for manifest_name, lang in MANIFEST_CATALOG.items():
        if (project_root / manifest_name).is_file():
            profile["dependency_files"].append(manifest_name)

    # Check for C# csproj/sln files (recursive)
    csproj_files = list(project_root.glob("**/*.csproj"))
    sln_files = list(project_root.glob("**/*.sln"))
    for f in (csproj_files + sln_files)[:10]:
        rel = str(f.relative_to(project_root))
        if rel not in profile["dependency_files"]:
            profile["dependency_files"].append(rel)

    # 2. Inspect Ecosystems in order of specificity

    # -------------------------------------------------------------------------
    # A. Python Ecosystem
    # -------------------------------------------------------------------------
    manage_py = project_root / "manage.py"
    settings_py = list(project_root.glob("**/settings.py"))
    has_py_manifest = any(f in profile["dependency_files"] for f in ["pyproject.toml", "requirements.txt", "Pipfile", "poetry.lock"])

    if manage_py.is_file() or settings_py:
        profile["language"] = "Python"
        profile["ecosystem_family"] = "python"
        profile["framework"] = "Django"
        profile["data_layer"] = "Django ORM"
        profile["confidence"] = "Confirmed"
        evidence_file = "manage.py" if manage_py.is_file() else str(settings_py[0].relative_to(project_root))
        profile["detection_evidence"].append({
            "file": evidence_file,
            "indicator": "Django management or settings configuration"
        })
        profile["recommended_rules"].extend(["TG-DB-004", "TG-RATE-001", "TG-PLATFORM-*"])
        profile["recommended_references"].extend(["django-security.md", "python-security-overview.md"])

        # Check for DRF
        for py_file in project_root.glob("**/*.py"):
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                if "rest_framework" in content:
                    profile["framework"] = "Django / DRF"
                    profile["recommended_references"].append("drf-security.md")
                    break
            except Exception:
                continue

    elif has_py_manifest or list(project_root.glob("*.py")):
        # Check FastAPI / Flask / SQLAlchemy
        py_search_files = list(project_root.glob("*.py")) + list(project_root.glob("app/**/*.py")) + list(project_root.glob("src/**/*.py"))
        for py_file in py_search_files[:25]:
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                if "FastAPI(" in content or "from fastapi" in content:
                    profile["language"] = "Python"
                    profile["ecosystem_family"] = "python"
                    profile["framework"] = "FastAPI"
                    profile["confidence"] = "Confirmed"
                    profile["detection_evidence"].append({
                        "file": str(py_file.relative_to(project_root)),
                        "indicator": "FastAPI application instantiation"
                    })
                    profile["recommended_references"].append("fastapi-security.md")
                elif "Flask(__name__)" in content or "from flask" in content:
                    profile["language"] = "Python"
                    profile["ecosystem_family"] = "python"
                    profile["framework"] = "Flask"
                    profile["confidence"] = "Confirmed"
                    profile["detection_evidence"].append({
                        "file": str(py_file.relative_to(project_root)),
                        "indicator": "Flask application instantiation"
                    })
                    profile["recommended_references"].append("flask-security.md")

                if "sqlalchemy" in content:
                    profile["data_layer"] = "SQLAlchemy"
                    profile["recommended_references"].append("sqlalchemy-security.md")
                elif "tortoise" in content:
                    profile["data_layer"] = "Tortoise ORM"
            except Exception:
                continue

        if profile["language"] == "Unknown" and has_py_manifest:
            profile["language"] = "Python"
            profile["ecosystem_family"] = "python"
            profile["confidence"] = "High Confidence"
            profile["detection_evidence"].append({
                "file": profile["dependency_files"][0],
                "indicator": "Python dependency manifest"
            })
            profile["recommended_references"].append("python-security-overview.md")

    # -------------------------------------------------------------------------
    # B. JavaScript / TypeScript Ecosystem
    # -------------------------------------------------------------------------
    pkg_json_path = project_root / "package.json"
    has_backend_manifest = any((project_root / m).is_file() for m in [
        "composer.json", "mix.exs", "Gemfile", "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "build.gradle.kts"
    ]) or bool(csproj_files) or bool(sln_files)

    if pkg_json_path.is_file() and profile["language"] == "Unknown" and not has_backend_manifest:
        is_ts = bool(list(project_root.glob("**/*.ts*")))
        profile["language"] = "TypeScript" if is_ts else "JavaScript"
        profile["ecosystem_family"] = "javascript"
        try:
            with open(pkg_json_path, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

            # Framework detection
            if "next" in deps:
                profile["framework"] = "Next.js"
                profile["confidence"] = "Confirmed"
                profile["detection_evidence"].append({"file": "package.json", "indicator": "next dependency"})
                profile["recommended_references"].append("nextjs-security.md")
                profile["recommended_rules"].extend(["TG-CLIENT-*", "TG-PLATFORM-001"])
            elif "@nestjs/core" in deps:
                profile["framework"] = "NestJS"
                profile["confidence"] = "Confirmed"
                profile["detection_evidence"].append({"file": "package.json", "indicator": "NestJS dependency"})
                profile["recommended_references"].append("nestjs-security.md")
            elif "@sveltejs/kit" in deps:
                profile["framework"] = "SvelteKit"
                profile["confidence"] = "Confirmed"
                profile["detection_evidence"].append({"file": "package.json", "indicator": "SvelteKit dependency"})
            elif "nuxt" in deps:
                profile["framework"] = "Nuxt"
                profile["confidence"] = "Confirmed"
                profile["detection_evidence"].append({"file": "package.json", "indicator": "Nuxt dependency"})
            elif "astro" in deps:
                profile["framework"] = "Astro"
                profile["confidence"] = "Confirmed"
                profile["detection_evidence"].append({"file": "package.json", "indicator": "Astro dependency"})
            elif "express" in deps:
                profile["framework"] = "Express"
                profile["confidence"] = "Confirmed"
                profile["detection_evidence"].append({"file": "package.json", "indicator": "express dependency"})
                profile["recommended_references"].append("express-security.md")
            elif "react" in deps:
                profile["framework"] = "React / Vite"
                profile["confidence"] = "Confirmed"
                profile["detection_evidence"].append({"file": "package.json", "indicator": "react dependency"})
                profile["recommended_references"].append("react-vite-security.md")

            # ORM / Data layer detection
            if "@prisma/client" in deps or "prisma" in deps:
                profile["data_layer"] = "Prisma ORM"
            elif "drizzle-orm" in deps:
                profile["data_layer"] = "Drizzle ORM"
            elif "typeorm" in deps:
                profile["data_layer"] = "TypeORM"
            elif "mongoose" in deps:
                profile["data_layer"] = "Mongoose"
            elif "@supabase/supabase-js" in deps:
                profile["data_layer"] = "Supabase"
                profile["recommended_references"].append("supabase-security.md")
            elif "firebase" in deps or "firebase-admin" in deps:
                profile["data_layer"] = "Firebase"
                profile["recommended_references"].append("firebase-security.md")
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # C. Go Ecosystem
    # -------------------------------------------------------------------------
    go_mod = project_root / "go.mod"
    if go_mod.is_file():
        profile["language"] = "Go"
        profile["ecosystem_family"] = "go"
        profile["confidence"] = "Confirmed"
        profile["detection_evidence"].append({"file": "go.mod", "indicator": "Go module manifest"})
        profile["recommended_rules"].extend(["TG-SEC-*", "TG-INPUT-001", "TG-INPUT-002", "TG-DB-004", "TG-SSRF-*"])
        profile["recommended_references"].append("go-security.md")

        try:
            go_content = go_mod.read_text(encoding="utf-8", errors="ignore")
            if "github.com/gin-gonic/gin" in go_content:
                profile["framework"] = "Gin"
            elif "github.com/gofiber/fiber" in go_content:
                profile["framework"] = "Fiber"
            elif "github.com/labstack/echo" in go_content:
                profile["framework"] = "Echo"
            elif "github.com/go-chi/chi" in go_content:
                profile["framework"] = "Chi"

            if "gorm.io/gorm" in go_content:
                profile["data_layer"] = "GORM"
            elif "github.com/jmoiron/sqlx" in go_content:
                profile["data_layer"] = "SQLx"
            elif "database/sql" in go_content or "github.com/lib/pq" in go_content or "github.com/go-sql-driver/mysql" in go_content:
                profile["data_layer"] = "database/sql"
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # D. Rust Ecosystem
    # -------------------------------------------------------------------------
    cargo_toml = project_root / "Cargo.toml"
    if cargo_toml.is_file() and profile["language"] == "Unknown":
        profile["language"] = "Rust"
        profile["ecosystem_family"] = "rust"
        profile["confidence"] = "Confirmed"
        profile["detection_evidence"].append({"file": "Cargo.toml", "indicator": "Cargo package manifest"})
        profile["recommended_rules"].extend(["TG-SEC-*", "TG-INPUT-001", "TG-DB-004", "TG-BIZ-001"])
        profile["recommended_references"].append("rust-security.md")

        try:
            cargo_content = cargo_toml.read_text(encoding="utf-8", errors="ignore")
            if "actix-web" in cargo_content:
                profile["framework"] = "Actix-web"
            elif "axum" in cargo_content:
                profile["framework"] = "Axum"
            elif "rocket" in cargo_content:
                profile["framework"] = "Rocket"

            if "diesel" in cargo_content:
                profile["data_layer"] = "Diesel ORM"
            elif "sqlx" in cargo_content:
                profile["data_layer"] = "SQLx"
            elif "sea-orm" in cargo_content:
                profile["data_layer"] = "SeaORM"
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # E. Java / Kotlin Ecosystem
    # -------------------------------------------------------------------------
    pom_files = [project_root / "pom.xml"] + list(project_root.glob("*/pom.xml"))[:10]
    gradle_files = [project_root / "build.gradle", project_root / "build.gradle.kts"] + list(project_root.glob("*/build.gradle*"))[:10]
    has_jvm_manifest = any(f.is_file() for f in pom_files + gradle_files)
    if has_jvm_manifest and profile["language"] == "Unknown":
        java_files = list(project_root.glob("**/*.java"))
        kt_files = list(project_root.glob("**/*.kt"))
        is_kotlin = (project_root / "build.gradle.kts").is_file() or (len(kt_files) > len(java_files) and len(kt_files) > 0)
        profile["language"] = "Kotlin" if is_kotlin else "Java"
        profile["ecosystem_family"] = "jvm"
        profile["confidence"] = "Confirmed"
        ev_file = "build.gradle.kts" if (project_root / "build.gradle.kts").is_file() else ("build.gradle" if (project_root / "build.gradle").is_file() else "pom.xml")
        profile["detection_evidence"].append({"file": ev_file, "indicator": f"{profile['language']} build configuration"})
        profile["recommended_rules"].extend(["TG-SEC-*", "TG-AUTH-*", "TG-INPUT-001", "TG-INPUT-002", "TG-DB-004"])
        profile["recommended_references"].append("java-security.md")

        check_content = ""
        for jf in (pom_files + gradle_files)[:15]:
            if jf.is_file():
                try:
                    check_content += jf.read_text(encoding="utf-8", errors="ignore") + "\n"
                except Exception:
                    pass

        if "quarkus" in check_content:
            profile["framework"] = "Quarkus"
        elif "spring-boot" in check_content or "springframework" in check_content:
            profile["framework"] = "Spring Boot"
        elif "ktor" in check_content:
            profile["framework"] = "Ktor"
        elif "micronaut" in check_content:
            profile["framework"] = "Micronaut"

        if "hibernate" in check_content or "spring-boot-starter-data-jpa" in check_content or "quarkus-hibernate" in check_content:
            profile["data_layer"] = "Hibernate / JPA"
        elif "jooq" in check_content:
            profile["data_layer"] = "jOOQ"

    # -------------------------------------------------------------------------
    # F. C# / .NET Ecosystem
    # -------------------------------------------------------------------------
    if (csproj_files or sln_files) and profile["language"] == "Unknown":
        profile["language"] = "C#"
        profile["ecosystem_family"] = "dotnet"
        profile["confidence"] = "Confirmed"
        ev_file = str(csproj_files[0].relative_to(project_root)) if csproj_files else str(sln_files[0].relative_to(project_root))
        profile["detection_evidence"].append({"file": ev_file, "indicator": ".NET project or solution manifest"})
        profile["recommended_rules"].extend(["TG-SEC-*", "TG-AUTH-*", "TG-INPUT-001", "TG-DB-004"])
        profile["recommended_references"].append("csharp-security.md")

        csproj_content = ""
        for cf in csproj_files[:10]:
            try:
                csproj_content += cf.read_text(encoding="utf-8", errors="ignore") + "\n"
            except Exception:
                pass

        if "Microsoft.NET.Sdk.Web" in csproj_content or "Microsoft.AspNetCore" in csproj_content or "Swashbuckle" in csproj_content:
            profile["framework"] = "ASP.NET Core"
        if "Microsoft.EntityFrameworkCore" in csproj_content:
            profile["data_layer"] = "Entity Framework Core"
        elif "Dapper" in csproj_content:
            profile["data_layer"] = "Dapper"

    # -------------------------------------------------------------------------
    # G. PHP Ecosystem
    # -------------------------------------------------------------------------
    composer_json = project_root / "composer.json"
    if composer_json.is_file() and profile["language"] == "Unknown":
        profile["language"] = "PHP"
        profile["ecosystem_family"] = "php"
        profile["confidence"] = "Confirmed"
        profile["detection_evidence"].append({"file": "composer.json", "indicator": "PHP Composer manifest"})
        profile["recommended_rules"].extend(["TG-SEC-*", "TG-INPUT-001", "TG-INPUT-002", "TG-PLATFORM-*"])
        profile["recommended_references"].append("polyglot-security-matrix.md")

        try:
            with open(composer_json, "r", encoding="utf-8") as f:
                c_data = json.load(f)
            reqs = {**c_data.get("require", {}), **c_data.get("require-dev", {})}
            if "laravel/framework" in reqs:
                profile["framework"] = "Laravel"
                profile["data_layer"] = "Eloquent ORM"
            elif "symfony/framework-bundle" in reqs or any("symfony/" in k for k in reqs):
                profile["framework"] = "Symfony"
                profile["data_layer"] = "Doctrine ORM"
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # H. Ruby Ecosystem
    # -------------------------------------------------------------------------
    gemfile = project_root / "Gemfile"
    if gemfile.is_file() and profile["language"] == "Unknown":
        profile["language"] = "Ruby"
        profile["ecosystem_family"] = "ruby"
        profile["confidence"] = "Confirmed"
        profile["detection_evidence"].append({"file": "Gemfile", "indicator": "Ruby Bundler manifest"})
        profile["recommended_rules"].extend(["TG-SEC-*", "TG-AUTH-*", "TG-INPUT-001", "TG-DB-004"])
        profile["recommended_references"].append("polyglot-security-matrix.md")

        try:
            g_content = gemfile.read_text(encoding="utf-8", errors="ignore")
            if "rails" in g_content:
                profile["framework"] = "Ruby on Rails"
                profile["data_layer"] = "ActiveRecord"
            elif "sinatra" in g_content:
                profile["framework"] = "Sinatra"
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # I. Elixir Ecosystem
    # -------------------------------------------------------------------------
    mix_exs = project_root / "mix.exs"
    if mix_exs.is_file() and profile["language"] == "Unknown":
        profile["language"] = "Elixir"
        profile["ecosystem_family"] = "elixir"
        profile["confidence"] = "Confirmed"
        profile["detection_evidence"].append({"file": "mix.exs", "indicator": "Elixir Mix manifest"})
        profile["recommended_references"].append("polyglot-security-matrix.md")
        try:
            m_content = mix_exs.read_text(encoding="utf-8", errors="ignore")
            if "phoenix" in m_content:
                profile["framework"] = "Phoenix"
                profile["data_layer"] = "Ecto"
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # J. Dart / Flutter Ecosystem
    # -------------------------------------------------------------------------
    pubspec = project_root / "pubspec.yaml"
    if pubspec.is_file() and profile["language"] == "Unknown":
        profile["language"] = "Dart"
        profile["ecosystem_family"] = "dart"
        profile["confidence"] = "Confirmed"
        profile["detection_evidence"].append({"file": "pubspec.yaml", "indicator": "Dart pubspec manifest"})
        try:
            p_content = pubspec.read_text(encoding="utf-8", errors="ignore")
            if "flutter:" in p_content:
                profile["framework"] = "Flutter"
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # K. Fallback: Extension Census (When No Manifest or Custom Structure)
    # -------------------------------------------------------------------------
    census = census_file_extensions(project_root)
    profile["extension_census"] = census

    if profile["language"] == "Unknown" and census:
        top_lang = max(census.items(), key=lambda x: x[1])[0]
        profile["language"] = top_lang
        profile["confidence"] = "Inferred from file census"
        profile["detection_evidence"].append({
            "file": "source files",
            "indicator": f"{census[top_lang]} {top_lang} source file(s) found"
        })
        family_map = {
            "Go": "go", "Rust": "rust", "Java": "jvm", "Kotlin": "jvm",
            "C#": "dotnet", "PHP": "php", "Ruby": "ruby", "Python": "python",
            "TypeScript": "javascript", "JavaScript": "javascript",
            "C": "native", "C++": "native", "Swift": "apple", "Dart": "dart"
        }
        profile["ecosystem_family"] = family_map.get(top_lang, "universal")

    # -------------------------------------------------------------------------
    # L. Monorepo & Multi-Package Workspace Integration
    # -------------------------------------------------------------------------
    try:
        from monorepo_detector import scan_workspace
        ws_res = scan_workspace(str(project_root))
        if ws_res.get("is_monorepo"):
            profile["is_monorepo"] = True
            profile["monorepo_type"] = ws_res.get("monorepo_type", "monorepo")
            profile["sub_stacks"] = ws_res.get("packages", [])
            languages_found = list(set(
                p["language"] for p in ws_res.get("packages", []) 
                if p.get("language") and p["language"] != "unknown"
            ))
            profile["sub_languages"] = languages_found
            if len(languages_found) > 1:
                profile["ecosystem_family"] = "polyglot_monorepo"
                profile["recommended_rules"].extend(["TG-SEC-*", "TG-AUTH-*", "TG-PLATFORM-*"])
    except Exception:
        profile["is_monorepo"] = False
        profile["sub_stacks"] = []

    return profile


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Universal Polyglot Stack Detector")
    parser.add_argument("path", nargs="?", default=".", help="Target project root directory")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    project_root = Path(args.path).resolve()
    profile = detect_stack(project_root)

    if args.json:
        print(json.dumps(profile, indent=2))
    else:
        evidence = profile["detection_evidence"][0]["file"] if profile["detection_evidence"] else "heuristic"
        print("## Detected Stack (Universal Polyglot)")
        print(f"- Language: {profile['language']}")
        print(f"- Ecosystem Family: {profile.get('ecosystem_family', 'universal')}")
        print(f"- Framework: {profile['framework']}")
        print(f"- Data layer: {profile['data_layer']}")
        print(f"- Dependency files: {', '.join(profile['dependency_files']) if profile['dependency_files'] else 'None'}")
        print(f"- Detection confidence: {profile['confidence']} ({evidence})")


if __name__ == "__main__":
    main()
