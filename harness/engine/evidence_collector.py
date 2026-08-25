"""
TorusGuard Validation Evidence Collector (v0.5.2)
Collects technical replay evidence, SHA-256 execution checksums, and environment snapshots.
"""

import hashlib
import json
import datetime
import platform
import subprocess
from pathlib import Path
from typing import Dict, Any, List


class ValidationEvidenceCollector:
    """
    Captures complete cryptographic and environmental evidence for validation runs.
    """

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()

    def capture_environment_snapshot(self) -> Dict[str, str]:
        git_commit = "unknown"
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=str(self.root_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            if res.returncode == 0:
                git_commit = res.stdout.strip()[:12]
        except Exception:
            pass

        return {
            "os": f"{platform.system()} {platform.release()} ({platform.machine()})",
            "python_version": platform.python_version(),
            "git_commit": git_commit,
            "runner_mode": "Deterministic Local Replay",
            "engine_version": "v0.5.2",
            "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

    @staticmethod
    def compute_run_checksum(data: Dict[str, Any]) -> str:
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
