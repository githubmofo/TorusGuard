"""
TorusGuard Incremental Static Scanner & Hash Cache
Identifies modified or newly added source files using cryptographic content hashes
to enable sub-second re-scans on large codebases.
"""

from pathlib import Path
from typing import Dict, List, Set, Optional, Any, Tuple
import json
import hashlib
import time


class IncrementalScanner:
    """Manages file modification tracking and AST cache persistence."""

    def __init__(self, target_root: Path, cache_file: Optional[Path] = None):
        self.target_root = target_root.resolve()
        if cache_file:
            self.cache_file = cache_file.resolve()
        else:
            cache_dir = self.target_root / ".torusguard" / "cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
            self.cache_file = cache_dir / "ast_cache.json"

        self.cache_data: Dict[str, Dict[str, Any]] = self._load_cache()

    def _load_cache(self) -> Dict[str, Dict[str, Any]]:
        if self.cache_file.is_file():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_cache(self) -> None:
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache_data, f, indent=2)
        except Exception:
            pass

    @staticmethod
    def compute_file_hash(file_path: Path) -> str:
        """Computes SHA256 of file content."""
        h = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            return h.hexdigest()
        except Exception:
            return ""

    def get_changed_files(self, all_files: List[Path]) -> Tuple[List[Path], List[Path]]:
        """
        Compares current file hashes to cache.
        Returns (changed_files, unchanged_files).
        """
        changed: List[Path] = []
        unchanged: List[Path] = []

        for f in all_files:
            try:
                rel_path = str(f.resolve().relative_to(self.target_root)).replace("\\", "/")
            except Exception:
                rel_path = str(f).replace("\\", "/")

            current_hash = self.compute_file_hash(f)
            cached_entry = self.cache_data.get(rel_path)

            if cached_entry and cached_entry.get("hash") == current_hash:
                unchanged.append(f)
            else:
                changed.append(f)

        return changed, unchanged

    def get_cached_findings(self, file_path: Path) -> List[Dict[str, Any]]:
        try:
            rel_path = str(file_path.resolve().relative_to(self.target_root)).replace("\\", "/")
        except Exception:
            rel_path = str(file_path).replace("\\", "/")
        entry = self.cache_data.get(rel_path)
        if entry:
            return entry.get("findings", [])
        return []

    def update_file_cache(self, file_path: Path, findings: List[Dict[str, Any]]) -> None:
        try:
            rel_path = str(file_path.resolve().relative_to(self.target_root)).replace("\\", "/")
        except Exception:
            rel_path = str(file_path).replace("\\", "/")
        current_hash = self.compute_file_hash(file_path)
        self.cache_data[rel_path] = {
            "hash": current_hash,
            "timestamp": time.time(),
            "findings_count": len(findings),
            "findings": findings
        }
