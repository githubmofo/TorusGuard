"""
TorusGuard Symbol Table Engine
Per-file symbol resolution for tracking variable definitions, scopes, types,
and import aliases across language scopes.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class VariableInfo:
    name: str
    defined_line: int
    scope_name: str = "global"
    assigned_expression: str = ""
    is_tainted: bool = False
    inferred_type: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)


class SymbolTable:
    """Tracks variable definitions, scopes, and types within a single file."""

    def __init__(self, file_path: str = ""):
        self.file_path = file_path
        self.variables: Dict[str, List[VariableInfo]] = {}
        self.import_aliases: Dict[str, str] = {}
        self.function_defs: Dict[str, int] = {}

    def add_variable(
        self,
        name: str,
        line: int,
        scope: str = "global",
        expression: str = "",
        is_tainted: bool = False,
        inferred_type: str = "unknown"
    ) -> VariableInfo:
        var_info = VariableInfo(
            name=name,
            defined_line=line,
            scope_name=scope,
            assigned_expression=expression,
            is_tainted=is_tainted,
            inferred_type=inferred_type
        )
        if name not in self.variables:
            self.variables[name] = []
        self.variables[name].append(var_info)
        return var_info

    def resolve_variable(self, name: str, at_line: int) -> Optional[VariableInfo]:
        """
        Given a variable name and current line, returns its most recent definition
        preceding or at that line.
        """
        defs = self.variables.get(name, [])
        candidate = None
        for d in defs:
            if d.defined_line <= at_line:
                if candidate is None or d.defined_line > candidate.defined_line:
                    candidate = d
        return candidate

    def add_import_alias(self, alias: str, canonical_name: str) -> None:
        """Register an import alias (e.g. `from flask import request as req`)."""
        self.import_aliases[alias] = canonical_name

    def get_import_alias(self, alias: str) -> Optional[str]:
        """Resolve an alias to its canonical symbol or module."""
        return self.import_aliases.get(alias)

    def mark_tainted(self, name: str, at_line: int) -> None:
        var_info = self.resolve_variable(name, at_line)
        if var_info:
            var_info.is_tainted = True
        else:
            self.add_variable(name=name, line=at_line, is_tainted=True)

    def is_tainted(self, name: str, at_line: int) -> bool:
        var_info = self.resolve_variable(name, at_line)
        return var_info.is_tainted if var_info else False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "variables": {k: [v.defined_line for v in vs] for k, vs in self.variables.items()},
            "import_aliases": self.import_aliases,
            "functions": self.function_defs
        }
