#!/usr/bin/env python3
"""
TorusGuard Stack Detector Utility
Inspects project directory to detect programming language, frameworks, ORM/data layer,
and dependency manifests. Outputs canonical stack block and structured JSON.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

def detect_stack(project_root: Path) -> Dict[str, Any]:
    profile = {
        "language": "Unknown",
        "framework": "None",
        "data_layer": "None",
        "dependency_files": [],
        "detection_evidence": [],
        "confidence": "Needs Review",
        "recommended_rules": [
            "TG-SEC-*",
            "TG-INPUT-*",
            "TG-AUTH-*"
        ],
        "recommended_references": []
    }

    # 1. Inspect dependency manifests
    dep_candidates = ["pyproject.toml", "requirements.txt", "Pipfile", "package.json", "package-lock.json", "pnpm-lock.yaml"]
    for dc in dep_candidates:
        if (project_root / dc).is_file():
            profile["dependency_files"].append(dc)

    # 2. Check Python ecosystem
    manage_py = project_root / "manage.py"
    settings_py = list(project_root.glob("**/settings.py"))
    
    if manage_py.is_file() or settings_py:
        profile["language"] = "Python"
        profile["framework"] = "Django"
        profile["data_layer"] = "Django ORM"
        profile["confidence"] = "Confirmed"
        profile["detection_evidence"].append({
            "file": "manage.py" if manage_py.is_file() else str(settings_py[0].relative_to(project_root)),
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

    # Check for FastAPI / Flask if not Django
    if profile["framework"] == "None":
        for py_file in list(project_root.glob("*.py")) + list(project_root.glob("app/**/*.py")) + list(project_root.glob("src/**/*.py")):
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                if "FastAPI(" in content or "from fastapi" in content:
                    profile["language"] = "Python"
                    profile["framework"] = "FastAPI"
                    profile["confidence"] = "Confirmed"
                    profile["detection_evidence"].append({
                        "file": str(py_file.relative_to(project_root)),
                        "indicator": "FastAPI application instantiation"
                    })
                    profile["recommended_references"].append("fastapi-security.md")
                elif "Flask(__name__)" in content or "from flask" in content:
                    profile["language"] = "Python"
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
            except Exception:
                continue

    # 3. Check JavaScript / TypeScript ecosystem
    pkg_json_path = project_root / "package.json"
    if pkg_json_path.is_file():
        profile["language"] = "TypeScript" if list(project_root.glob("**/*.ts*")) else "JavaScript"
        try:
            with open(pkg_json_path, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            
            if "next" in deps:
                profile["framework"] = "Next.js"
                profile["confidence"] = "Confirmed"
                profile["detection_evidence"].append({"file": "package.json", "indicator": "next dependency"})
                profile["recommended_references"].append("nextjs-security.md")
                profile["recommended_rules"].extend(["TG-CLIENT-*", "TG-PLATFORM-001"])
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

            if "@supabase/supabase-js" in deps:
                profile["data_layer"] = "Supabase"
                profile["recommended_references"].append("supabase-security.md")
            elif "firebase" in deps or "firebase-admin" in deps:
                profile["data_layer"] = "Firebase"
                profile["recommended_references"].append("firebase-security.md")
        except Exception:
            pass

    return profile


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Stack Detector")
    parser.add_argument("path", nargs="?", default=".", help="Target project root directory")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    project_root = Path(args.path).resolve()
    profile = detect_stack(project_root)

    if args.json:
        print(json.dumps(profile, indent=2))
    else:
        evidence = profile["detection_evidence"][0]["file"] if profile["detection_evidence"] else "heuristic"
        print(f"## Detected Stack")
        print(f"- Language: {profile['language']}")
        print(f"- Framework: {profile['framework']}")
        print(f"- Data layer: {profile['data_layer']}")
        print(f"- Dependency files: {', '.join(profile['dependency_files']) if profile['dependency_files'] else 'None'}")
        print(f"- Detection confidence: {profile['confidence']} ({evidence})")

if __name__ == "__main__":
    main()
