import json
from datetime import datetime
from pathlib import Path
from typing import Optional

class RunFolder:
    """
    Manages the per-run folder state and artifacts for a TorusGuard execution.
    Creates a unique directory (e.g., .torusguard/runs/run-YYYYMMDD-HHMMSS) containing
    findings.md, remediation.md, recheck.md, metadata.json, patches/, and logs/.
    """
    def __init__(self, output_root: str = ".torusguard/runs", run_name: Optional[str] = None):
        self.output_root = Path(output_root).resolve()
        
        if run_name:
            self.run_id = run_name
        else:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            self.run_id = f"run-{timestamp}"
            
        self.run_path = self.output_root / self.run_id
        
        # Subdirectories
        self.patches_dir = self.run_path / "patches"
        self.logs_dir = self.run_path / "logs"
        
        # Files
        self.findings_file = self.run_path / "findings.md"
        self.remediation_file = self.run_path / "remediation.md"
        self.recheck_file = self.run_path / "recheck.md"
        self.metadata_file = self.run_path / "metadata.json"
        
        self._initialize_folders()
        self._write_metadata()

    def _initialize_folders(self):
        self.run_path.mkdir(parents=True, exist_ok=True)
        self.patches_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def _write_metadata(self):
        metadata = {
            "run_id": self.run_id,
            "created_at": datetime.now().isoformat(),
            "status": "initialized"
        }
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

    def get_path(self, item: str) -> Path:
        """Helper to get a path within the run structure."""
        paths = {
            "findings.md": self.findings_file,
            "remediation.md": self.remediation_file,
            "recheck.md": self.recheck_file,
            "metadata.json": self.metadata_file,
            "patches": self.patches_dir,
            "logs": self.logs_dir
        }
        return paths.get(item, self.run_path / item)
