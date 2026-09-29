"""
TorusGuard Rules Registry
Centralized repository loading and validating canonical security rules
across all 22 architectural rule families.
"""

from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
import re


CANONICAL_FAMILIES = [
    "TG-SEC", "TG-AUTH", "TG-DB", "TG-INPUT", "TG-RATE", "TG-AGENT",
    "TG-SSRF", "TG-WEBHOOK", "TG-WS", "TG-CSRF", "TG-GQL", "TG-SUPPLY",
    "TG-BIZ", "TG-CACHE", "TG-CLIENT", "TG-PLATFORM", "TG-DIFF",
    "TG-EDGE", "TG-CONT", "TG-GIT", "TG-REDOS", "TG-RAG"
]


@dataclass
class CanonicalRule:
    rule_id: str
    family: str
    title: str
    severity: str
    category: str
    description: str
    remediation_guidance: str = ""
    file_path: str = ""
    detection_patterns: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RulesRegistry:
    """Centralized loader and validator for TorusGuard rules."""

    def __init__(self, rules_root: Optional[Path] = None):
        self.rules_root = rules_root or self._locate_rules_dir()
        self.rules: Dict[str, CanonicalRule] = {}
        self.load()

    def _locate_rules_dir(self) -> Path:
        base = Path(__file__).resolve().parent.parent / ".torusguard" / "rules"
        if base.exists():
            return base
        return Path.cwd() / ".torusguard" / "rules"

    def load(self) -> None:
        if not self.rules_root.exists():
            return

        for p in self.rules_root.glob("**/*.md"):
            if p.name.startswith("README") or p.name.startswith("TORUSGUARD"):
                continue

            content = p.read_text(encoding="utf-8", errors="replace")
            rule = self._parse_rule_markdown(p, content)
            if rule:
                self.rules[rule.rule_id] = rule

    def _parse_rule_markdown(self, path: Path, content: str) -> Optional[CanonicalRule]:
        filename = path.stem
        # Extract rule_id from filename or first heading
        rule_id_match = re.search(r"(TG-[A-Z]+-\d{3})", filename)
        if not rule_id_match:
            rule_id_match = re.search(r"#\s*(TG-[A-Z]+-\d{3})", content)
        if not rule_id_match:
            return None

        rule_id = rule_id_match.group(1)
        family = rule_id.rsplit("-", 1)[0]

        # Extract title
        title = filename.replace(rule_id, "").strip(" -_").replace("-", " ").title()
        title_match = re.search(r"#\s*(?:TG-[A-Z]+-\d{3}[\s:—-]+)?(.+)", content)
        if title_match:
            cand_title = title_match.group(1).strip()
            if cand_title and not cand_title.startswith("TG-"):
                title = cand_title

        # Severity
        severity = "High"
        sev_match = re.search(r"(?i)severity[:\s*|`]+(Critical|High|Medium|Low)", content)
        if sev_match:
            severity = sev_match.group(1).capitalize()

        # Description
        desc = ""
        desc_match = re.search(r"(?i)(?:###?\s*Description|##\s*Overview|Summary)[:\s]*\n([^\n#]+)", content)
        if desc_match:
            desc = desc_match.group(1).strip()
        else:
            desc = title

        # Remediation
        remed = ""
        rem_match = re.search(r"(?i)(?:###?\s*Remediation|###?\s*Mitigation|Fix)[:\s]*\n([^\n#]+)", content)
        if rem_match:
            remed = rem_match.group(1).strip()

        return CanonicalRule(
            rule_id=rule_id,
            family=family,
            title=title,
            severity=severity,
            category=family.replace("TG-", "").lower(),
            description=desc,
            remediation_guidance=remed,
            file_path=str(path)
        )

    def get_rule(self, rule_id: str) -> Optional[CanonicalRule]:
        return self.rules.get(rule_id)

    def get_rules_by_family(self, family: str) -> List[CanonicalRule]:
        fam_norm = family.upper()
        if not fam_norm.startswith("TG-"):
            fam_norm = f"TG-{fam_norm}"
        return [r for r in self.rules.values() if r.family == fam_norm]

    def get_rules_by_severity(self, severity: str) -> List[CanonicalRule]:
        return [r for r in self.rules.values() if r.severity.lower() == severity.lower()]

    def all_rules(self) -> List[CanonicalRule]:
        return sorted(self.rules.values(), key=lambda r: r.rule_id)

    def count(self) -> int:
        return len(self.rules)
