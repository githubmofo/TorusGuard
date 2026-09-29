"""
TorusGuard Polyglot AST Walker
Extracts structured primitives (FunctionCall, Assignment, ImportStatement, StringLiteral)
from Tree-sitter AST nodes and fallback parsers across polyglot languages.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional


@dataclass
class FunctionCall:
    name: str
    full_call: str
    arguments: List[str]
    line_number: int
    column: int
    receiver: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Assignment:
    target: str
    value_expression: str
    line_number: int
    column: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ImportStatement:
    module: str
    imported_names: List[str]
    alias_map: Dict[str, str] = field(default_factory=dict)
    line_number: int = 0
    is_relative: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StringLiteral:
    value: str
    line_number: int
    column: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TreeSitterWalker:
    """
    Traverses Tree-sitter parse trees and extracts normalized language constructs.
    """

    @staticmethod
    def extract_function_calls(root_node, source_bytes: bytes) -> List[FunctionCall]:
        calls: List[FunctionCall] = []

        def visit(node):
            # Python: call -> function, arguments
            # JS/TS: call_expression -> function, arguments
            # Go: call_expression -> function, argument_list
            if node.type in ("call", "call_expression"):
                func_child = node.child_by_field_name("function")
                args_child = node.child_by_field_name("arguments") or node.child_by_field_name("argument_list")

                func_name = ""
                receiver = None
                if func_child:
                    func_text = source_bytes[func_child.start_byte:func_child.end_byte].decode("utf-8", errors="replace")
                    func_name = func_text
                    if "." in func_text:
                        parts = func_text.split(".")
                        receiver = ".".join(parts[:-1])

                args_list: List[str] = []
                if args_child:
                    for ch in args_child.children:
                        if ch.type not in (",", "(", ")"):
                            arg_text = source_bytes[ch.start_byte:ch.end_byte].decode("utf-8", errors="replace").strip()
                            if arg_text:
                                args_list.append(arg_text)

                line_num = node.start_point[0] + 1
                col = node.start_point[1]
                call_text = source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace")

                calls.append(FunctionCall(
                    name=func_name,
                    full_call=call_text,
                    arguments=args_list,
                    line_number=line_num,
                    column=col,
                    receiver=receiver
                ))

            for ch in node.children:
                visit(ch)

        visit(root_node)
        return calls

    @staticmethod
    def extract_assignments(root_node, source_bytes: bytes) -> List[Assignment]:
        assignments: List[Assignment] = []

        def visit(node):
            # Python: assignment -> left, right
            # JS/TS: variable_declarator (name, value), assignment_expression (left, right)
            # Go: short_var_declaration (left, right), assignment_statement (left, right)
            target = ""
            val_expr = ""
            line_num = node.start_point[0] + 1
            col = node.start_point[1]

            if node.type == "assignment":  # Python
                left = node.child_by_field_name("left")
                right = node.child_by_field_name("right")
                if left and right:
                    target = source_bytes[left.start_byte:left.end_byte].decode("utf-8", errors="replace").strip()
                    val_expr = source_bytes[right.start_byte:right.end_byte].decode("utf-8", errors="replace").strip()
                    assignments.append(Assignment(target=target, value_expression=val_expr, line_number=line_num, column=col))

            elif node.type == "variable_declarator":  # JS/TS
                name = node.child_by_field_name("name")
                val = node.child_by_field_name("value")
                if name:
                    target = source_bytes[name.start_byte:name.end_byte].decode("utf-8", errors="replace").strip()
                    if val:
                        val_expr = source_bytes[val.start_byte:val.end_byte].decode("utf-8", errors="replace").strip()
                    assignments.append(Assignment(target=target, value_expression=val_expr, line_number=line_num, column=col))

            elif node.type == "assignment_expression":  # JS/TS
                left = node.child_by_field_name("left")
                right = node.child_by_field_name("right")
                if left and right:
                    target = source_bytes[left.start_byte:left.end_byte].decode("utf-8", errors="replace").strip()
                    val_expr = source_bytes[right.start_byte:right.end_byte].decode("utf-8", errors="replace").strip()
                    assignments.append(Assignment(target=target, value_expression=val_expr, line_number=line_num, column=col))

            elif node.type in ("short_var_declaration", "assignment_statement"):  # Go
                left = node.child_by_field_name("left")
                right = node.child_by_field_name("right")
                if left and right:
                    target = source_bytes[left.start_byte:left.end_byte].decode("utf-8", errors="replace").strip()
                    val_expr = source_bytes[right.start_byte:right.end_byte].decode("utf-8", errors="replace").strip()
                    assignments.append(Assignment(target=target, value_expression=val_expr, line_number=line_num, column=col))

            for ch in node.children:
                visit(ch)

        visit(root_node)
        return assignments

    @staticmethod
    def extract_imports(root_node, source_bytes: bytes, language: str) -> List[ImportStatement]:
        imports: List[ImportStatement] = []

        def visit(node):
            line_num = node.start_point[0] + 1

            # Python imports
            if node.type == "import_statement":
                raw = source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace").strip()
                # e.g. import os, sys as s
                names = []
                alias_map = {}
                for ch in node.children:
                    if ch.type == "dotted_name":
                        mod = source_bytes[ch.start_byte:ch.end_byte].decode("utf-8", errors="replace").strip()
                        names.append(mod)
                    elif ch.type == "aliased_import":
                        n = ch.child_by_field_name("name")
                        a = ch.child_by_field_name("alias")
                        if n and a:
                            name_str = source_bytes[n.start_byte:n.end_byte].decode("utf-8", errors="replace").strip()
                            alias_str = source_bytes[a.start_byte:a.end_byte].decode("utf-8", errors="replace").strip()
                            names.append(name_str)
                            alias_map[alias_str] = name_str
                for n in names:
                    imports.append(ImportStatement(module=n, imported_names=[n], alias_map=alias_map, line_number=line_num))

            elif node.type == "import_from_statement":
                # from module import a, b as c
                module_name = ""
                mod_child = node.child_by_field_name("module_name")
                if mod_child:
                    module_name = source_bytes[mod_child.start_byte:mod_child.end_byte].decode("utf-8", errors="replace").strip()
                names = []
                alias_map = {}
                for ch in node.children:
                    if ch.type == "dotted_name" and ch != mod_child:
                        names.append(source_bytes[ch.start_byte:ch.end_byte].decode("utf-8", errors="replace").strip())
                    elif ch.type == "aliased_import":
                        n = ch.child_by_field_name("name")
                        a = ch.child_by_field_name("alias")
                        if n and a:
                            n_str = source_bytes[n.start_byte:n.end_byte].decode("utf-8", errors="replace").strip()
                            a_str = source_bytes[a.start_byte:a.end_byte].decode("utf-8", errors="replace").strip()
                            names.append(n_str)
                            alias_map[a_str] = n_str
                is_rel = module_name.startswith(".")
                imports.append(ImportStatement(
                    module=module_name,
                    imported_names=names,
                    alias_map=alias_map,
                    line_number=line_num,
                    is_relative=is_rel
                ))

            # JS/TS imports: import_statement
            elif node.type == "import_statement":
                raw = source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace").strip()
                source_child = node.child_by_field_name("source")
                source_mod = ""
                if source_child:
                    source_mod = source_bytes[source_child.start_byte:source_child.end_byte].decode("utf-8", errors="replace").strip().strip("'\"")
                names = []
                alias_map = {}
                for ch in node.children:
                    if ch.type == "import_clause":
                        clause_str = source_bytes[ch.start_byte:ch.end_byte].decode("utf-8", errors="replace").strip()
                        names.append(clause_str)
                is_rel = source_mod.startswith(".")
                imports.append(ImportStatement(
                    module=source_mod,
                    imported_names=names,
                    alias_map=alias_map,
                    line_number=line_num,
                    is_relative=is_rel
                ))

            # Go imports: import_declaration
            elif node.type == "import_declaration":
                for ch in node.children:
                    if ch.type in ("import_spec", "import_spec_list"):
                        for spec in (ch.children if ch.type == "import_spec_list" else [ch]):
                            if spec.type == "import_spec":
                                path_child = spec.child_by_field_name("path")
                                if path_child:
                                    path_str = source_bytes[path_child.start_byte:path_child.end_byte].decode("utf-8", errors="replace").strip().strip('"')
                                    name_child = spec.child_by_field_name("name")
                                    alias = ""
                                    if name_child:
                                        alias = source_bytes[name_child.start_byte:name_child.end_byte].decode("utf-8", errors="replace").strip()
                                    alias_map = {alias: path_str} if alias else {}
                                    imports.append(ImportStatement(
                                        module=path_str,
                                        imported_names=[path_str],
                                        alias_map=alias_map,
                                        line_number=spec.start_point[0] + 1
                                    ))

            for ch in node.children:
                visit(ch)

        visit(root_node)
        return imports

    @staticmethod
    def extract_string_literals(root_node, source_bytes: bytes) -> List[StringLiteral]:
        literals: List[StringLiteral] = []

        def visit(node):
            if node.type in ("string", "string_literal", "raw_string_literal", "template_string"):
                text = source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace")
                literals.append(StringLiteral(
                    value=text.strip("\"'`"),
                    line_number=node.start_point[0] + 1,
                    column=node.start_point[1]
                ))
            for ch in node.children:
                visit(ch)

        visit(root_node)
        return literals
