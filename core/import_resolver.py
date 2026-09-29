"""
TorusGuard Import Resolver
Resolves language-specific import specifiers to canonical file system paths.
Supports Python, JavaScript, TypeScript, and Go.
"""

from pathlib import Path
from typing import Optional, List


COMMON_EXTENSIONS = [
    ".py", ".ts", ".tsx", ".js", ".mjs", ".cjs", ".go"
]


class ImportResolver:
    """Resolves relative and package imports to on-disk source files."""

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()

    def resolve(self, importing_file: Path, import_module: str) -> Optional[Path]:
        """
        Resolves `import_module` referenced by `importing_file` to an absolute Path on disk.
        """
        if not import_module:
            return None

        importing_file = importing_file.resolve()
        current_dir = importing_file.parent

        # 1. Relative import (e.g. ./utils, ../db, .services)
        if import_module.startswith("."):
            # Python style: .models or ..utils
            if import_module.startswith(".."):
                rel_parts = import_module.lstrip(".")
                target_dir = current_dir.parent
                cand = target_dir / rel_parts.replace(".", "/")
            elif import_module.startswith("."):
                rel_parts = import_module.lstrip(".")
                cand = current_dir / rel_parts.replace(".", "/")
            else:
                cand = current_dir / import_module

            resolved = self._try_extensions(cand)
            if resolved:
                return resolved

        # 2. Direct path relative to current directory
        direct_cand = current_dir / import_module
        resolved = self._try_extensions(direct_cand)
        if resolved:
            return resolved

        # 3. Project root relative import (e.g. core.taint, src.services.auth)
        dotted_cand = self.project_root / import_module.replace(".", "/")
        resolved = self._try_extensions(dotted_cand)
        if resolved:
            return resolved

        # 4. Check under common subdirectories (src, app, lib, internal)
        for sub in ("src", "app", "lib", "internal"):
            sub_cand = self.project_root / sub / import_module.replace(".", "/")
            resolved = self._try_extensions(sub_cand)
            if resolved:
                return resolved

        return None

    def _try_extensions(self, base_path: Path) -> Optional[Path]:
        # Check direct file with extension already
        if base_path.is_file():
            return base_path

        # Check with each extension
        for ext in COMMON_EXTENSIONS:
            cand = base_path.with_suffix(ext)
            if cand.is_file():
                return cand

        # Check directory index / __init__
        if base_path.is_dir():
            py_init = base_path / "__init__.py"
            if py_init.is_file():
                return py_init
            for ext in (".ts", ".js", ".tsx"):
                idx = base_path / f"index{ext}"
                if idx.is_file():
                    return idx

        return None
