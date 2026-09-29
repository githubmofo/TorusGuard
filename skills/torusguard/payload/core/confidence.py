"""
TorusGuard Multi-Signal Evidence-Chain Confidence Calibration Engine
Calibrates finding confidence (0-100) using 7 weighted empirical signals:
rule severity, taint path confirmation, taint depth, sanitizer absence,
framework context match, evidence snippet quality, and test fixture suppression.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Tuple, Optional


SEVERITY_BASE_SCORES = {
    "Critical": 90,
    "High": 75,
    "Medium": 50,
    "Low": 25,
    "Informational": 10
}


@dataclass
class EvidenceSignals:
    rule_severity: str = "High"
    taint_path_confirmed: bool = False
    taint_depth: Optional[int] = None
    sanitizer_present: bool = False
    framework_context_match: bool = True
    has_multiline_evidence: bool = True
    is_test_or_mock: bool = False
    memory_boost: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ConfidenceCalibrator:
    """Computes evidence-chain calibrated confidence scores."""

    @staticmethod
    def calculate_score(signals: EvidenceSignals) -> Tuple[int, str, Dict[str, Any]]:
        # 1. rule_severity_base (weight 0.20)
        sev_base = SEVERITY_BASE_SCORES.get(signals.rule_severity, 50)
        w_sev = 0.20 * sev_base

        # 2. taint_path_confirmed (weight 0.25)
        taint_score = 100 if signals.taint_path_confirmed else 0
        w_taint = 0.25 * taint_score

        # 3. taint_depth (weight 0.10)
        # direct=100, 1-hop=80, 2-hop=60, 3+=40; if no taint path, 0
        if signals.taint_path_confirmed:
            d = signals.taint_depth if signals.taint_depth is not None else 0
            if d == 0:
                depth_score = 100
            elif d == 1:
                depth_score = 80
            elif d == 2:
                depth_score = 60
            else:
                depth_score = 40
        else:
            depth_score = 0
        w_depth = 0.10 * depth_score

        # 4. sanitizer_absence (weight 0.15)
        san_score = 0 if signals.sanitizer_present else 100
        w_san = 0.15 * san_score

        # 5. framework_context_match (weight 0.10)
        ctx_score = 100 if signals.framework_context_match else 50
        w_ctx = 0.10 * ctx_score

        # 6. evidence_snippet_quality (weight 0.10)
        snippet_score = 100 if signals.has_multiline_evidence else 50
        w_snippet = 0.10 * snippet_score

        # 7. test fixture penalty
        test_penalty = -50 if signals.is_test_or_mock else 0

        # Memory boost (-30 to +20)
        mem_boost = signals.memory_boost

        raw_total = (
            w_sev +
            w_taint +
            w_depth +
            w_san +
            w_ctx +
            w_snippet +
            test_penalty +
            mem_boost
        )

        final_score = int(round(min(max(raw_total, 0), 100)))

        # Assign band
        if final_score >= 90:
            band = "Confirmed"
        elif final_score >= 70:
            band = "High Confidence"
        elif final_score >= 50:
            band = "Medium Confidence"
        else:
            band = "Needs Review"

        breakdown = {
            "rule_severity_score": sev_base,
            "taint_path_confirmed": signals.taint_path_confirmed,
            "taint_depth": signals.taint_depth,
            "sanitizer_present": signals.sanitizer_present,
            "framework_context_match": signals.framework_context_match,
            "has_multiline_evidence": signals.has_multiline_evidence,
            "is_test_or_mock": signals.is_test_or_mock,
            "test_penalty": test_penalty,
            "memory_boost": mem_boost,
            "total_score": final_score,
            "classification_band": band
        }

        return final_score, band, breakdown
