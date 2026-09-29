"""
TorusGuard Polyglot Parser
Unified Tree-sitter parser wrapper with language auto-detection and resilient
fallback parsing across Python, JavaScript, TypeScript, Go, Rust, Java, Ruby, PHP, and C#.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import re

from core.ast_walker import FunctionCall, Assignment, ImportStatement, StringLiteral, TreeSitterWalker
from core.symbol_table import SymbolTable


LANGUAGE_EXTENSIONS: Dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".rb": "ruby",
    ".php": "php",
    ".cs": "csharp",
}


@dataclass
class ParseResult:
    file_path: str
    language: str
    function_calls: List[FunctionCall] = field(default_factory=list)
    assignments: List[Assignment] = field(default_factory=list)
    imports: List[ImportStatement] = field(default_factory=list)
    string_literals: List[StringLiteral] = field(default_factory=list)
    symbol_table: SymbolTable = field(default_factory=SymbolTable)
    is_tree_sitter: bool = False
    raw_content: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "language": self.language,
            "function_calls_count": len(self.function_calls),
            "assignments_count": len(self.assignments),
            "imports_count": len(self.imports),
            "is_tree_sitter": self.is_tree_sitter,
        }


class PolyglotParser:
    """Parses source files into Tree-sitter ASTs or fallback token models with language auto-detection."""

    def __init__(self):
        self._parsers: Dict[str, Any] = {}
        self._init_tree_sitter()

    def _init_tree_sitter(self):
        try:
            import tree_sitter
            # Python
            try:
                import tree_sitter_python
                py_lang = tree_sitter.Language(tree_sitter_python.language())
                self._parsers["python"] = tree_sitter.Parser(py_lang)
            except Exception:
                pass

            # JavaScript
            try:
                import tree_sitter_javascript
                js_lang = tree_sitter.Language(tree_sitter_javascript.language())
                self._parsers["javascript"] = tree_sitter.Parser(js_lang)
            except Exception:
                pass

            # TypeScript / TSX
            try:
                import tree_sitter_typescript
                ts_lang = tree_sitter.Language(tree_sitter_typescript.language_typescript())
                self._parsers["typescript"] = tree_sitter.Parser(ts_lang)
                tsx_lang = tree_sitter.Language(tree_sitter_typescript.language_tsx())
                self._parsers["tsx"] = tree_sitter.Parser(tsx_lang)
            except Exception:
                pass

            # Go
            try:
                import tree_sitter_go
                go_lang = tree_sitter.Language(tree_sitter_go.language())
                self._parsers["go"] = tree_sitter.Parser(go_lang)
            except Exception:
                pass

        except Exception:
            pass

    def detect_language(self, file_path: Path) -> str:
        ext = file_path.suffix.lower()
        return LANGUAGE_EXTENSIONS.get(ext, "unknown")

    def parse_file(self, file_path: Path) -> ParseResult:
        lang = self.detect_language(file_path)
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return ParseResult(file_path=str(file_path), language=lang)

        source_bytes = content.encode("utf-8")
        ts_parser = self._parsers.get(lang)

        if ts_parser is not None:
            try:
                tree = ts_parser.parse(source_bytes)
                calls = TreeSitterWalker.extract_function_calls(tree.root_node, source_bytes)
                assigns = TreeSitterWalker.extract_assignments(tree.root_node, source_bytes)
                imports = TreeSitterWalker.extract_imports(tree.root_node, source_bytes, lang)
                strings = TreeSitterWalker.extract_string_literals(tree.root_node, source_bytes)

                sym_table = SymbolTable(str(file_path))
                for a in assigns:
                    sym_table.add_variable(name=a.target, line=a.line_number, expression=a.value_expression)
                for imp in imports:
                    for alias, orig in imp.alias_map.items():
                        sym_table.add_import_alias(alias, orig)

                return ParseResult(
                    file_path=str(file_path),
                    language=lang,
                    function_calls=calls,
                    assignments=assigns,
                    imports=imports,
                    string_literals=strings,
                    symbol_table=sym_table,
                    is_tree_sitter=True,
                    raw_content=content
                )
            except Exception:
                pass

        # Resilient Fallback Parser
        return self._fallback_parse(str(file_path), content, lang)

    def _fallback_parse(self, file_path: str, content: str, lang: str) -> ParseResult:
        lines = content.splitlines()
        calls: List[FunctionCall] = []
        assigns: List[Assignment] = []
        imports: List[ImportStatement] = []
        strings: List[StringLiteral] = []
        sym_table = SymbolTable(file_path)

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//", "/*", "*")):
                continue

            # Assignments
            assign_match = re.match(r"^(?:const|let|var)?\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(?::=[=]?|=)\s*(.+)$", stripped)
            if assign_match:
                target = assign_match.group(1).strip()
                val = assign_match.group(2).strip()
                assigns.append(Assignment(target=target, value_expression=val, line_number=line_num, column=0))
                sym_table.add_variable(target, line_num, expression=val)

            # Function calls (e.g. foo(x), obj.method(y))
            call_matches = re.finditer(r"([a-zA-Z_][a-zA-Z0-9_\.]*)\s*\((.*?)\)", stripped)
            for cm in call_matches:
                func_name = cm.group(1)
                args_str = cm.group(2)
                args = [a.strip() for a in args_str.split(",") if a.strip()]
                calls.append(FunctionCall(
                    name=func_name,
                    full_call=cm.group(0),
                    arguments=args,
                    line_number=line_num,
                    column=cm.start()
                ))

            # Imports
            if "import " in stripped or "require(" in stripped or "from " in stripped:
                imp_match = re.search(r"(?:from\s+([a-zA-Z0-9_\.]+)\s+import\s+([a-zA-Z0-9_,\s]+)|import\s+([a-zA-Z0-9_\.]+))", stripped)
                if imp_match:
                    mod = imp_match.group(1) or imp_match.group(3) or ""
                    names = [n.strip() for n in (imp_match.group(2) or "").split(",") if n.strip()]
                    imports.append(ImportStatement(module=mod, imported_names=names, line_number=line_num))

        return ParseResult(
            file_path=file_path,
            language=lang,
            function_calls=calls,
            assignments=assigns,
            imports=imports,
            string_literals=strings,
            symbol_table=sym_table,
            is_tree_sitter=False,
            raw_content=content
        )
