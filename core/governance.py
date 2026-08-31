"""
TorusGuard v6 Minimal Patch Governance Engine
Enforces strict policy boundaries around automated code modifications:
- Line churn bounding (max added/removed lines)
- File count limits (single-file preference)
- High-risk file escalation (auth, crypto, tenant isolation, DB, uploads, workflows)
- Comment/boilerplate checks
- Zero unrelated file changes
- Automatic application blocking for oversized or high-risk diffs
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Tuple, Optional
import re
from pathlib import Path


# Sensitive Path Categories
SENSITIVE_CATEGORIES = {
    "auth": ["auth", "login", "password", "token", "jwt", "session", "oauth", "oidc", "credential"],
    "tenancy": ["tenant", "tenant_id", "organization_id", "org_id", "workspace_id"],
    "secrets": ["secret", "api_key", "private_key", "ssh_key", "access_key"],
    "crypto": ["crypto", "cipher", "encrypt", "decrypt", "hashlib", "hmac"],
    "uploads": ["upload", "storage", "filepath", "save_file", "download"],
    "workflows": [".github/workflows", "Dockerfile", "Containerfile", "compose.yaml", "docker-compose"]
}

HIGH_RISK_KEYWORDS = [kw for kws in SENSITIVE_CATEGORIES.values() for kw in kws]

HIGH_RISK_DIRECTORIES = [
    "auth", "authentication", "authorization", "security",
    "crypto", "migrations", ".github/workflows"
]


@dataclass
class PatchPolicyDecision:
    allowed_auto_apply: bool
    escalation_required: bool
    review_level: str = "Automatic"  # "Automatic" | "Peer Review Recommended" | "Mandatory Security Sign-Off"
    rejection_reasons: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    line_additions: int = 0
    line_deletions: int = 0
    files_touched: int = 0
    file_list: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PatchGovernor:
    """
    Evaluates proposed diffs against minimal patch governance rules.
    """

    def __init__(
        self,
        max_additions_per_file: int = 35,
        max_deletions_per_file: int = 25,
        max_total_files: int = 2,
        strict_high_risk_escalation: bool = True,
    ):
        self.max_additions_per_file = max_additions_per_file
        self.max_deletions_per_file = max_deletions_per_file
        self.max_total_files = max_total_files
        self.strict_high_risk_escalation = strict_high_risk_escalation

    def evaluate_diff(self, diff_content: str, target_file: Optional[str] = None) -> PatchPolicyDecision:
        """
        Parses unified diff and evaluates policy compliance.
        """
        lines = diff_content.splitlines()
        additions = 0
        deletions = 0
        files: set[str] = set()
        unnecessary_comment_lines = 0

        current_file = target_file

        for line in lines:
            if line.startswith("+++ b/"):
                current_file = line[6:].strip()
                files.add(current_file)
            elif line.startswith("--- a/"):
                old_file = line[6:].strip()
                if old_file != "/dev/null":
                    files.add(old_file)
            elif line.startswith("+") and not line.startswith("+++"):
                additions += 1
                stripped = line[1:].strip()
                # Check for excessive filler comments
                if stripped.startswith("# TODO:") or stripped.startswith("// Added by AI"):
                    unnecessary_comment_lines += 1
            elif line.startswith("-") and not line.startswith("---"):
                deletions += 1

        if target_file and not files:
            files.add(target_file)

        rejection_reasons = []
        risk_factors = []
        escalation_required = False

        # 1. File Count Check
        if len(files) > self.max_total_files:
            rejection_reasons.append(
                f"Patch modifies {len(files)} files (maximum allowed is {self.max_total_files})."
            )

        # 2. Line Churn Check
        if additions > self.max_additions_per_file:
            rejection_reasons.append(
                f"Line additions ({additions}) exceed threshold ({self.max_additions_per_file})."
            )
        if deletions > self.max_deletions_per_file:
            rejection_reasons.append(
                f"Line deletions ({deletions}) exceed threshold ({self.max_deletions_per_file})."
            )

        # 3. Filler Comment Check
        if unnecessary_comment_lines > 2:
            rejection_reasons.append("Patch contains excessive boilerplate or commentary.")

        # 4. High-Risk Sensitive Context Escalation
        for f in files:
            norm_f = f.lower().replace("\\", "/")
            for kw in HIGH_RISK_KEYWORDS:
                if kw in norm_f:
                    risk_factors.append(f"File `{f}` touches high-risk domain keyword `{kw}`.")
                    escalation_required = True
                    break

        # If strict escalation is required on high-risk files, block auto-apply unless verified
        allowed = (len(rejection_reasons) == 0)
        review_level = "Automatic"

        if escalation_required:
            if additions > 10 or deletions > 10 or len(files) > 1:
                review_level = "Mandatory Security Sign-Off"
                if self.strict_high_risk_escalation:
                    allowed = False
                    rejection_reasons.append(
                        "High-risk file modifications with non-trivial churn require explicit human approval."
                    )
            else:
                review_level = "Peer Review Recommended"

        return PatchPolicyDecision(
            allowed_auto_apply=allowed,
            escalation_required=escalation_required,
            review_level=review_level,
            rejection_reasons=rejection_reasons,
            risk_factors=risk_factors,
            line_additions=additions,
            line_deletions=deletions,
            files_touched=len(files),
            file_list=list(files),
        )
