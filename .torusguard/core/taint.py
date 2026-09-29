"""
TorusGuard Taint Engine — Core Taint Models & Propagation Dataclasses
Defines source, sink, sanitizer entities and dataflow propagation primitives.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Set


@dataclass
class TaintSource:
    pattern: str
    framework: str
    label: str
    category: str
    language: str
    line_number: int = 0
    file_path: str = ""
    variable_name: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TaintSink:
    pattern: str
    category: str
    rule_id: str
    severity: str
    language: str
    line_number: int = 0
    file_path: str = ""
    argument_name: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TaintSanitizer:
    pattern: str
    cleans: List[str]
    language: str
    line_number: int = 0
    file_path: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TaintNode:
    variable_name: str
    file_path: str
    line_number: int
    node_type: str  # "source" | "transform" | "sink" | "sanitizer"
    expression: str = ""
    pattern: str = ""
    category: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def node_id(self) -> str:
        return f"{self.file_path}:{self.line_number}:{self.variable_name}:{self.node_type}"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TaintEdge:
    from_node: TaintNode
    to_node: TaintNode
    edge_type: str  # "assignment" | "argument" | "return" | "attribute" | "call"
    line_number: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_node": self.from_node.node_id(),
            "to_node": self.to_node.node_id(),
            "edge_type": self.edge_type,
            "line_number": self.line_number,
        }


@dataclass
class TaintPath:
    source: TaintNode
    sink: TaintNode
    path: List[TaintNode]
    is_sanitized: bool = False
    sanitizers_found: List[TaintNode] = field(default_factory=list)
    confidence_penalty: int = 0

    @property
    def depth(self) -> int:
        return max(0, len(self.path) - 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source.to_dict(),
            "sink": self.sink.to_dict(),
            "depth": self.depth,
            "is_sanitized": self.is_sanitized,
            "sanitizers_found": [s.to_dict() for s in self.sanitizers_found],
            "path_nodes": [n.to_dict() for n in self.path],
        }


class TaintPropagator:
    """
    Evaluates statement-level and expression-level taint transfer.
    Determines if assignment, function call, or operation propagates taint
    from RHS variables to LHS target.
    """

    @staticmethod
    def propagates_taint(source_vars: Set[str], expression: str) -> bool:
        """Checks if any currently tainted variable appears in the expression."""
        if not source_vars or not expression:
            return False
        import re
        tokens = set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", expression))
        return bool(tokens.intersection(source_vars))

    @staticmethod
    def is_sanitizer_expression(expression: str, sanitizers: List[Dict[str, Any]], category: str) -> Optional[Dict[str, Any]]:
        """Returns the matching sanitizer if the expression applies a known sanitizer for the category."""
        for s in sanitizers:
            if s["pattern"] in expression:
                if not category or category in s.get("cleans", []):
                    return s
        return None
