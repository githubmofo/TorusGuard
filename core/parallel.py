"""
TorusGuard Parallel Audit Executor
Executes multi-threaded static security scanning across files with deterministic result collation.
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional


class ParallelAuditExecutor:
    """Distributes file analysis across a thread pool with deterministic output ordering."""

    def __init__(self, max_workers: Optional[int] = None):
        self.max_workers = max_workers or min(os.cpu_count() or 4, 8)

    def scan_files_parallel(
        self,
        files: List[Path],
        scan_fn: Callable[[Path], List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """
        Executes `scan_fn` across all files in parallel.
        Returns deterministically ordered list of all findings.
        """
        if not files:
            return []

        # If only a few files, avoid thread pool overhead
        if len(files) <= 3:
            all_findings = []
            for f in files:
                all_findings.extend(scan_fn(f))
            return all_findings

        all_findings: List[Dict[str, Any]] = []
        file_results: Dict[str, List[Dict[str, Any]]] = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {executor.submit(scan_fn, f): str(f) for f in files}
            for future in as_completed(future_to_file):
                f_str = future_to_file[future]
                try:
                    res = future.result()
                    file_results[f_str] = res
                except Exception:
                    file_results[f_str] = []

        # Deterministic sort by original file order
        for f in files:
            f_str = str(f)
            if f_str in file_results:
                all_findings.extend(file_results[f_str])

        return all_findings
