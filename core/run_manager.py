"""
TorusGuard v6 Run Folder & Artifact Registry Manager
Creates and manages isolated run directories under runs/<run-id>/ containing:
- manifest.json
- summary.md
- findings.md
- remediation.md
- apply-plan.md
- recheck.md
- evidence.json
- diff-summary.md
- changed-files.txt
- sarif.json (optional)
- logs/
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


class RunManager:
    """
    Manages the lifecycle of an isolated TorusGuard run directory.
    """

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        target_name: str = "workspace",
        command: str = "audit",
        run_id: Optional[str] = None,
    ):
        self.base_dir = base_dir or Path(".torusguard/runs")
        self.target_name = target_name
        self.command = command

        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        self.run_id = run_id or f"run-{timestamp}-{target_name}"
        self.run_path = self.base_dir / self.run_id

        # Subdirectories
        self.logs_dir = self.run_path / "logs"
        self.patches_dir = self.run_path / "patches"
        self.bundles_dir = self.run_path / "bundles"

        # Standard Artifact Paths
        self.manifest_file = self.run_path / "manifest.json"
        self.summary_file = self.run_path / "summary.md"
        self.findings_file = self.run_path / "findings.md"
        self.remediation_file = self.run_path / "remediation.md"
        self.apply_plan_file = self.run_path / "apply-plan.md"
        self.recheck_file = self.run_path / "recheck.md"
        self.evidence_file = self.run_path / "evidence.json"
        self.diff_summary_file = self.run_path / "diff-summary.md"
        self.changed_files_file = self.run_path / "changed-files.txt"
        self.sarif_file = self.run_path / "sarif.json"

        self._init_directories()

    def _init_directories(self):
        self.run_path.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.patches_dir.mkdir(parents=True, exist_ok=True)
        self.bundles_dir.mkdir(parents=True, exist_ok=True)

    def get_git_commit(self) -> Optional[str]:
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0:
                return res.stdout.strip()
        except Exception:
            pass
        return None

    def write_manifest(
        self,
        status_counts: Optional[Dict[str, int]] = None,
        extra_meta: Optional[Dict[str, Any]] = None,
    ):
        """
        Writes the standard manifest.json.
        """
        counts = status_counts or {
            "total_findings": 0,
            "confirmed": 0,
            "high_confidence": 0,
            "needs_review": 0,
            "remediated": 0,
            "verified_fixed": 0,
            "regressed": 0,
        }

        manifest_data = {
            "version": "v6.0.0",
            "run_id": self.run_id,
            "target_name": self.target_name,
            "command": self.command,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "git_commit": self.get_git_commit(),
            "status_counts": counts,
            "artifacts": {
                "manifest": "manifest.json",
                "summary": "summary.md",
                "findings": "findings.md",
                "remediation": "remediation.md",
                "apply_plan": "apply-plan.md",
                "recheck": "recheck.md",
                "evidence": "evidence.json",
                "diff_summary": "diff-summary.md",
                "changed_files": "changed-files.txt",
                "sarif": "sarif.json",
            },
        }

        if extra_meta:
            manifest_data.update(extra_meta)

        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)

    def write_evidence(self, evidence_data: List[Dict[str, Any]]):
        with open(self.evidence_file, "w", encoding="utf-8") as f:
            json.dump(evidence_data, f, indent=2)

    def write_changed_files(self, files: List[str]):
        with open(self.changed_files_file, "w", encoding="utf-8") as f:
            f.write("\n".join(files) + "\n")

    def write_summary(self, content: str):
        with open(self.summary_file, "w", encoding="utf-8") as f:
            f.write(content)

    def write_findings(self, content: str):
        with open(self.findings_file, "w", encoding="utf-8") as f:
            f.write(content)

    def write_remediation(self, content: str):
        with open(self.remediation_file, "w", encoding="utf-8") as f:
            f.write(content)

    def write_apply_plan(self, content: str):
        with open(self.apply_plan_file, "w", encoding="utf-8") as f:
            f.write(content)

    def write_diff_summary(self, content: str):
        with open(self.diff_summary_file, "w", encoding="utf-8") as f:
            f.write(content)

    def write_recheck(self, content: str):
        with open(self.recheck_file, "w", encoding="utf-8") as f:
            f.write(content)

    def write_sarif(self, sarif_dict: Dict[str, Any]):
        with open(self.sarif_file, "w", encoding="utf-8") as f:
            json.dump(sarif_dict, f, indent=2)
