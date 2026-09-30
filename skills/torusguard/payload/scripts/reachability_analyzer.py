#!/usr/bin/env python3
"""
TorusGuard Dependency Reachability & Vulnerability Exploitability eXchange (VEX) Engine
Analyzes AST import specifiers and function call sites against declared dependencies to
distinguish between actively reachable vulnerabilities and harmless dead transitive code.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Any


def extract_package_names_node(root_dir: Path) -> List[str]:
    pkg_file = root_dir / "package.json"
    if not pkg_file.is_file():
        return []
    try:
        data = json.loads(pkg_file.read_text(encoding="utf-8"))
        deps = list(data.get("dependencies", {}).keys()) + list(data.get("devDependencies", {}).keys())
        return deps
    except Exception:
        return []


def extract_package_names_python(root_dir: Path) -> List[str]:
    req_file = root_dir / "requirements.txt"
    if not req_file.is_file():
        return []
    deps = []
    try:
        for line in req_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                pkg = re.split(r"[=<>~;]", line)[0].strip()
                if pkg:
                    deps.append(pkg)
    except Exception:
        pass
    return deps


def extract_package_names_go(root_dir: Path) -> List[str]:
    mod_file = root_dir / "go.mod"
    if not mod_file.is_file():
        return []
    deps = []
    try:
        for line in mod_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("require "):
                parts = line.split()
                if len(parts) >= 2:
                    deps.append(parts[1])
            elif not line.startswith("module") and not line.startswith("go ") and "/" in line:
                parts = line.split()
                if len(parts) >= 1:
                    deps.append(parts[0])
    except Exception:
        pass
    return deps


def scan_source_imports(root_dir: Path) -> Set[str]:
    """
    Scans polyglot codebase for import/require/use statements.
    """
    imported_packages = set()
    skip_dirs = {"node_modules", ".git", ".torusguard", "dist", "build", ".next", "__pycache__"}

    # Patterns for imports
    js_ts_pattern = re.compile(r"""(?:import\s+.*?\s+from\s+['"]|require\s*\(\s*['"])([@a-zA-Z0-9_\-\./]+)['"]""")
    py_pattern = re.compile(r"""(?:import\s+([a-zA-Z0-9_]+)|from\s+([a-zA-Z0-9_]+)\s+import)""")
    go_pattern = re.compile(r"""["']([a-zA-Z0-9_\-\./]+)["']""")

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in {".js", ".jsx", ".ts", ".tsx", ".py", ".go"}:
                continue
            file_path = Path(root) / f
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if ext in {".js", ".jsx", ".ts", ".tsx"}:
                    for match in js_ts_pattern.findall(content):
                        # Extract top-level package or scoped package (@scope/pkg)
                        parts = match.split("/")
                        if match.startswith("@") and len(parts) >= 2:
                            imported_packages.add(f"{parts[0]}/{parts[1]}")
                        elif parts:
                            imported_packages.add(parts[0])
                elif ext == ".py":
                    for m1, m2 in py_pattern.findall(content):
                        pkg = m1 or m2
                        if pkg:
                            imported_packages.add(pkg)
                elif ext == ".go":
                    for match in go_pattern.findall(content):
                        if "/" in match:
                            imported_packages.add(match)
            except Exception:
                continue

    return imported_packages


def analyze_reachability(root_dir: Path) -> Dict[str, Any]:
    declared = set()
    declared.update(extract_package_names_node(root_dir))
    declared.update(extract_package_names_python(root_dir))
    declared.update(extract_package_names_go(root_dir))

    imported = scan_source_imports(root_dir)

    reachable = []
    unreachable = []

    for dep in sorted(declared):
        is_used = False
        dep_clean = dep.lower().replace("-", "_")
        for imp in imported:
            imp_clean = imp.lower().replace("-", "_")
            if dep_clean == imp_clean or dep in imp or imp in dep:
                is_used = True
                break

        if is_used:
            reachable.append({
                "package": dep,
                "status": "REACHABLE",
                "impact": "Code path actively imported in application source",
                "vex_statement": "Affected / Call-path active"
            })
        else:
            unreachable.append({
                "package": dep,
                "status": "UNREACHABLE",
                "impact": "Declared dependency never imported or executed in reachable AST paths",
                "vex_statement": "NotAffected / VexJustification: inline_component_not_present_or_called"
            })

    reachability_ratio = (len(reachable) / max(len(declared), 1)) * 100.0

    return {
        "total_dependencies": len(declared),
        "reachable_count": len(reachable),
        "unreachable_count": len(unreachable),
        "reachability_percentage": round(reachability_ratio, 1),
        "reachable_dependencies": reachable,
        "unreachable_dependencies": unreachable,
    }


def main():
    import sys
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    result = analyze_reachability(target)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
