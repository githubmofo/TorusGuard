"""
TorusGuard v6 Remediation Bundle Generator
Constructs self-contained, structured remediation packages per cluster or finding containing:
- finding.md
- remediation.md
- minimal_patch_plan.md
- verify-after-change.md
- metadata.json
"""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional


@dataclass
class RemediationBundle:
    bundle_id: str
    finding_id: str
    rule_id: str
    title: str
    target_files: List[str]
    risk_severity: str
    what_is_wrong: str
    why_it_matters: str
    what_should_change: str
    proposed_diff: str
    verification_steps: str
    cluster_id: Optional[str] = None
    created_at: str = ""

    def write_to_directory(self, base_dir: Path) -> Path:
        bundle_dir = base_dir / self.bundle_id
        bundle_dir.mkdir(parents=True, exist_ok=True)

        # 1. finding.md
        with open(bundle_dir / "finding.md", "w", encoding="utf-8") as f:
            f.write(f"# Finding: {self.title}\n\n")
            f.write(f"- **Finding ID:** `{self.finding_id}`\n")
            f.write(f"- **Rule ID:** `{self.rule_id}`\n")
            f.write(f"- **Severity:** {self.risk_severity}\n")
            if self.cluster_id:
                f.write(f"- **Root-Cause Cluster:** `{self.cluster_id}`\n")
            f.write(f"- **Target Files:** {', '.join(f'`{tf}`' for tf in self.target_files)}\n\n")
            f.write("## What Is Wrong\n")
            f.write(f"{self.what_is_wrong}\n\n")
            f.write("## Why It Matters\n")
            f.write(f"{self.why_it_matters}\n")

        # 2. remediation.md
        with open(bundle_dir / "remediation.md", "w", encoding="utf-8") as f:
            f.write(f"# Remediation Guide: {self.title}\n\n")
            f.write("## What Should Change\n")
            f.write(f"{self.what_should_change}\n\n")
            f.write("## Target Files to Modify\n")
            for tf in self.target_files:
                f.write(f"- `{tf}`\n")

        # 3. minimal_patch_plan.md
        with open(bundle_dir / "minimal_patch_plan.md", "w", encoding="utf-8") as f:
            f.write(f"# Minimal Patch Plan for `{self.finding_id}`\n\n")
            f.write("```diff\n")
            f.write(self.proposed_diff.strip() + "\n")
            f.write("```\n")

        # 4. verify-after-change.md
        with open(bundle_dir / "verify-after-change.md", "w", encoding="utf-8") as f:
            f.write(f"# Verification Steps for `{self.finding_id}`\n\n")
            f.write(f"{self.verification_steps}\n\n")
            f.write("### Recheck Command\n")
            f.write("```bash\n/torusguard recheck\n```\n")

        # 5. metadata.json
        meta = {
            "bundle_id": self.bundle_id,
            "finding_id": self.finding_id,
            "rule_id": self.rule_id,
            "title": self.title,
            "cluster_id": self.cluster_id,
            "target_files": self.target_files,
            "risk_severity": self.risk_severity,
            "created_at": self.created_at,
        }
        with open(bundle_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        return bundle_dir


class BundleManager:
    """
    Factory for generating remediation bundles from findings and clusters.
    """

    @staticmethod
    def create_bundle(finding: Dict[str, Any], cluster_id: Optional[str] = None) -> RemediationBundle:
        f_id = finding.get("finding_id", "fnd-01")
        rule_id = finding.get("rule_id", "TG-GENERIC")
        title = finding.get("title", "Security Finding")
        target = finding.get("target", {})
        file_path = target.get("file_path", "app.py")
        severity = finding.get("severity", "High")

        bundle_id = f"bundle-{f_id}"

        what_is_wrong = finding.get(
            "what_is_wrong",
            f"The component in `{file_path}` violates security rule `{rule_id}`."
        )
        why_it_matters = finding.get(
            "why_it_matters",
            "This vulnerability could allow attackers to bypass authorization, access unauthorized tenant data, or inject malicious payloads."
        )
        what_should_change = finding.get(
            "what_should_change",
            f"Apply least-invasive framework-idiomatic hardening to `{file_path}`."
        )
        proposed_diff = finding.get(
            "proposed_diff",
            f"--- a/{file_path}\n+++ b/{file_path}\n@@ -1,3 +1,3 @@\n-# Unsafe pattern\n+# Hardened pattern\n"
        )
        verification_steps = finding.get(
            "verification_steps",
            f"Run `/torusguard recheck` on `{file_path}` to confirm vulnerability resolution."
        )

        return RemediationBundle(
            bundle_id=bundle_id,
            finding_id=f_id,
            rule_id=rule_id,
            title=title,
            target_files=[file_path],
            risk_severity=severity,
            what_is_wrong=what_is_wrong,
            why_it_matters=why_it_matters,
            what_should_change=what_should_change,
            proposed_diff=proposed_diff,
            verification_steps=verification_steps,
            cluster_id=cluster_id,
        )
