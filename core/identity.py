"""
TorusGuard v6 Stable Finding Identity & Fingerprinting Engine
Generates deterministic finding identifiers that survive line-number shifts,
minor refactorings, and file relocations within the same logical scope.
"""

import hashlib
import re
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict


def normalize_code_snippet(code: str) -> str:
    """
    Normalizes a code snippet to be whitespace- and comment-tolerant
    so small styling edits or empty lines don't change the region hash.
    """
    if not code:
        return ""
    lines = []
    for line in code.strip().splitlines():
        stripped = line.strip()
        # Remove single-line comments for hash stability if they are pure comment lines
        if stripped.startswith("#") or stripped.startswith("//"):
            continue
        # Normalize internal whitespace
        normalized = re.sub(r"\s+", " ", stripped)
        if normalized:
            lines.append(normalized)
    return "\n".join(lines)


@dataclass
class FindingFingerprint:
    rule_id: str
    normalized_path: str
    region_hash: str
    sink_signature: Optional[str] = None
    framework_marker: Optional[str] = None
    fingerprint_id: str = ""

    def __post_init__(self):
        if not self.fingerprint_id:
            self.fingerprint_id = self.compute_fingerprint_id()

    def compute_fingerprint_id(self) -> str:
        """
        Computes a stable hash based on (rule_id, normalized_path, region_hash, sink_signature).
        Format: TG-FND-<hash12>
        """
        data = f"{self.rule_id}|{self.normalized_path}|{self.region_hash}|{self.sink_signature or ''}|{self.framework_marker or ''}"
        h = hashlib.sha256(data.encode("utf-8")).hexdigest()[:12]
        # Clean rule id component for readable prefix
        rule_prefix = self.rule_id.replace("TG-", "").split("-")[0]
        return f"TG-{rule_prefix}-{h}"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class IdentityEngine:
    """
    Computes stable finding identities and persists fingerprint maps.
    """

    @staticmethod
    def generate_identity(
        rule_id: str,
        file_path: str,
        code_snippet: str,
        sink_signature: Optional[str] = None,
        framework_marker: Optional[str] = None,
        root_path: Optional[Path] = None,
    ) -> FindingFingerprint:
        """
        Generates a stable FindingFingerprint.
        """
        # Normalize file path relative to root
        norm_path = file_path.replace("\\", "/").lstrip("./")
        if root_path:
            try:
                norm_path = str(Path(file_path).resolve().relative_to(root_path.resolve())).replace("\\", "/")
            except Exception:
                norm_path = file_path.replace("\\", "/").lstrip("./")

        # Compute normalized region hash
        norm_code = normalize_code_snippet(code_snippet)
        region_hash = hashlib.sha256(norm_code.encode("utf-8")).hexdigest()[:16]

        return FindingFingerprint(
            rule_id=rule_id,
            normalized_path=norm_path,
            region_hash=region_hash,
            sink_signature=sink_signature,
            framework_marker=framework_marker,
        )
