"""
TorusGuard Project-Wide Call Graph Engine
Maps interprocedural call sites, function definitions, and caller/callee relationships
across module boundaries.
"""

from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set, Any
import re

from core.parser import PolyglotParser, ParseResult
from core.import_resolver import ImportResolver


@dataclass
class CallSite:
    caller_file: str
    caller_func: str
    caller_line: int
    callee_name: str
    callee_file: Optional[str] = None
    callee_line: Optional[int] = None
    arguments: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FunctionDef:
    file_path: str
    func_name: str
    start_line: int
    end_line: int = 0
    parameters: List[str] = field(default_factory=list)
    return_expressions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CallGraph:
    """Project-wide interprocedural function call graph."""

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.import_resolver = ImportResolver(self.project_root)
        # Key: (file_path, func_name) -> FunctionDef
        self.functions: Dict[Tuple[str, str], FunctionDef] = {}
        # Key: func_name -> list of FunctionDef (for quick symbol lookup)
        self.functions_by_name: Dict[str, List[FunctionDef]] = {}
        # Key: (file_path, func_name) -> list of CallSite where this func is caller
        self.callees: Dict[Tuple[str, str], List[CallSite]] = {}
        # Key: (file_path, func_name) -> list of CallSite where this func is callee
        self.callers: Dict[Tuple[str, str], List[CallSite]] = {}

    def register_function(self, fdef: FunctionDef) -> None:
        key = (fdef.file_path, fdef.func_name)
        self.functions[key] = fdef
        if fdef.func_name not in self.functions_by_name:
            self.functions_by_name[fdef.func_name] = []
        self.functions_by_name[fdef.func_name].append(fdef)

    def add_call(self, call: CallSite) -> None:
        caller_key = (call.caller_file, call.caller_func)
        if caller_key not in self.callees:
            self.callees[caller_key] = []
        self.callees[caller_key].append(call)

        if call.callee_file:
            callee_key = (call.callee_file, call.callee_name)
            if callee_key not in self.callers:
                self.callers[callee_key] = []
            self.callers[callee_key].append(call)

    def build_from_files(self, file_paths: List[Path], parser: PolyglotParser) -> None:
        """Parse files and construct functions and call edges."""
        parsed_results: Dict[str, ParseResult] = {}

        # Pass 1: Extract all function definitions
        for p in file_paths:
            try:
                res = parser.parse_file(p)
                rel_p = str(p.resolve().relative_to(self.project_root)).replace("\\", "/")
                parsed_results[rel_p] = res
                self._extract_function_defs(rel_p, res.raw_content, res.language)
            except Exception:
                continue

        # Pass 2: Extract call sites and link to callees
        for rel_p, res in parsed_results.items():
            abs_p = self.project_root / rel_p
            # Build import map: alias/name -> resolved Path
            resolved_imports: Dict[str, str] = {}
            for imp in res.imports:
                target_p = self.import_resolver.resolve(abs_p, imp.module)
                if target_p:
                    rel_target = str(target_p.resolve().relative_to(self.project_root)).replace("\\", "/")
                    for name in imp.imported_names:
                        resolved_imports[name] = rel_target
                    for alias, orig in imp.alias_map.items():
                        resolved_imports[alias] = rel_target

            # Process function calls
            for fc in res.function_calls:
                callee_name = fc.name
                callee_file = None
                callee_line = None

                # Method call e.g. mod.func
                if "." in callee_name:
                    prefix, actual_name = callee_name.split(".", 1)
                    if prefix in resolved_imports:
                        callee_file = resolved_imports[prefix]
                        callee_name = actual_name
                elif callee_name in resolved_imports:
                    callee_file = resolved_imports[callee_name]
                else:
                    # Check local in same file
                    if (rel_p, callee_name) in self.functions:
                        callee_file = rel_p

                # Find which enclosing function contains this call
                caller_func = self._find_enclosing_function(rel_p, fc.line_number)

                call_site = CallSite(
                    caller_file=rel_p,
                    caller_func=caller_func,
                    caller_line=fc.line_number,
                    callee_name=callee_name,
                    callee_file=callee_file,
                    arguments=fc.arguments
                )
                self.add_call(call_site)

    def _extract_function_defs(self, file_path: str, content: str, language: str) -> None:
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()

            # Python: def foo(a, b):
            py_m = re.match(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)", stripped)
            if py_m:
                fname = py_m.group(1)
                params = [p.strip() for p in py_m.group(2).split(",") if p.strip()]
                self.register_function(FunctionDef(file_path=file_path, func_name=fname, start_line=line_num, parameters=params))
                continue

            # JS/TS: function foo(a, b) or const foo = (a, b) =>
            js_m = re.match(r"^(?:async\s+)?function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)", stripped)
            if js_m:
                fname = js_m.group(1)
                params = [p.strip() for p in js_m.group(2).split(",") if p.strip()]
                self.register_function(FunctionDef(file_path=file_path, func_name=fname, start_line=line_num, parameters=params))
                continue

            arrow_m = re.match(r"^(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s*)?\((.*?)\)\s*=>", stripped)
            if arrow_m:
                fname = arrow_m.group(1)
                params = [p.strip() for p in arrow_m.group(2).split(",") if p.strip()]
                self.register_function(FunctionDef(file_path=file_path, func_name=fname, start_line=line_num, parameters=params))
                continue

            # Go: func foo(a string)
            go_m = re.match(r"^func\s+(?:\(.*?\)\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)", stripped)
            if go_m:
                fname = go_m.group(1)
                params = [p.strip() for p in go_m.group(2).split(",") if p.strip()]
                self.register_function(FunctionDef(file_path=file_path, func_name=fname, start_line=line_num, parameters=params))

    def _find_enclosing_function(self, file_path: str, line_num: int) -> str:
        candidates = [f for (fp, fn), f in self.functions.items() if fp == file_path and f.start_line <= line_num]
        if not candidates:
            return "<global>"
        candidates.sort(key=lambda f: f.start_line, reverse=True)
        return candidates[0].func_name

    def get_callers(self, file_path: str, func_name: str) -> List[CallSite]:
        return self.callers.get((file_path, func_name), [])

    def get_callees(self, file_path: str, func_name: str) -> List[CallSite]:
        return self.callees.get((file_path, func_name), [])
