"""
TorusGuard Continuous File Watcher
Monitors target workspace files for changes, debounces filesystem events,
and triggers continuous differential security re-scans.
"""

from pathlib import Path
from typing import Dict, List, Set, Callable, Optional
import time


class FileWatcher:
    """Lightweight polling and mtime watcher with debouncing."""

    def __init__(self, target_root: Path, check_interval_sec: float = 0.5):
        self.target_root = target_root.resolve()
        self.interval = check_interval_sec
        self.file_mtimes: Dict[str, float] = {}

    def get_snapshot(self, extensions: Optional[Set[str]] = None) -> Dict[str, float]:
        exts = extensions or {".py", ".js", ".ts", ".tsx", ".go", ".rs", ".java", ".php", ".rb", ".cs"}
        snapshot: Dict[str, float] = {}
        try:
            for p in self.target_root.rglob("*"):
                if p.is_file() and p.suffix.lower() in exts:
                    if ".git" in p.parts or "node_modules" in p.parts or ".torusguard" in p.parts:
                        continue
                    try:
                        snapshot[str(p)] = p.stat().st_mtime
                    except Exception:
                        pass
        except Exception:
            pass
        return snapshot

    def watch(
        self,
        on_change_callback: Callable[[List[str]], None],
        stop_condition: Optional[Callable[[], bool]] = None
    ) -> None:
        """Polls for file modifications and triggers `on_change_callback`."""
        self.file_mtimes = self.get_snapshot()

        while True:
            if stop_condition and stop_condition():
                break

            time.sleep(self.interval)
            current_snapshot = self.get_snapshot()

            changed_files: List[str] = []
            for path_str, mtime in current_snapshot.items():
                if path_str not in self.file_mtimes or self.file_mtimes[path_str] != mtime:
                    changed_files.append(path_str)

            if changed_files:
                self.file_mtimes = current_snapshot
                on_change_callback(changed_files)
