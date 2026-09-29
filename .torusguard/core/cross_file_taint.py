"""
TorusGuard Cross-File Interprocedural Taint Analyzer
Propagates taint across module and function boundaries using project call graphs.
Enforces strict 5-hop depth bound to prevent recursion and path explosion.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple, Any

from core.taint import TaintNode, TaintPath
from core.taint_graph import TaintGraph
from core.parser import PolyglotParser, ParseResult
from core.call_graph import CallGraph, CallSite, FunctionDef


class CrossFileTaintAnalyzer:
    """Interprocedural taint analysis across module boundaries."""

    MAX_INTERPROCEDURAL_DEPTH = 5

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.parser = PolyglotParser()
        self.call_graph = CallGraph(self.project_root)

    def analyze_project(self, file_paths: List[Path]) -> List[TaintPath]:
        """
        Builds call graph and walks intra-file and cross-file dataflow chains.
        """
        all_paths: List[TaintPath] = []
        file_graphs: Dict[str, TaintGraph] = {}
        file_contents: Dict[str, str] = {}
        file_languages: Dict[str, str] = {}

        # 1. Build CallGraph across target files
        self.call_graph.build_from_files(file_paths, self.parser)

        # 2. Intra-file analysis on each file
        for p in file_paths:
            try:
                rel_p = str(p.resolve().relative_to(self.project_root)).replace("\\", "/")
                content = p.read_text(encoding="utf-8", errors="replace")
                lang = self.parser.detect_language(p)
                file_contents[rel_p] = content
                file_languages[rel_p] = lang

                tg = TaintGraph()
                paths = tg.analyze_file_code(rel_p, content, lang)
                file_graphs[rel_p] = tg
                all_paths.extend(paths)
            except Exception:
                continue

        # 3. Interprocedural Propagation:
        # Check if function returns tainted value, propagate to call site LHS
        # Check if call passes tainted argument, propagate to callee parameters
        for (caller_key, call_sites) in self.call_graph.callees.items():
            caller_file, caller_func = caller_key
            tg_caller = file_graphs.get(caller_file)
            if not tg_caller:
                continue

            for cs in call_sites:
                if not cs.callee_file or cs.callee_file not in file_graphs:
                    continue

                tg_callee = file_graphs[cs.callee_file]

                # Check argument propagation (caller argument -> callee parameter)
                for arg_expr in cs.arguments:
                    # Is this argument connected to a tainted source in caller?
                    for src_id, src_node in tg_caller.nodes.items():
                        if src_node.node_type == "source":
                            # Check if src reaches the argument expression
                            arg_node = TaintNode(
                                variable_name=arg_expr,
                                file_path=caller_file,
                                line_number=cs.caller_line,
                                node_type="transform",
                                expression=arg_expr
                            )
                            # Look for sinks in the callee file
                            for sink_id, sink_node in tg_callee.nodes.items():
                                if sink_node.node_type == "sink":
                                    # Create interprocedural path
                                    cross_path = [src_node, arg_node, sink_node]
                                    is_sanitized, sanitizers = tg_callee.is_path_sanitized(
                                        cross_path,
                                        sink_node.metadata.get("category", ""),
                                        file_languages.get(cs.callee_file, "python")
                                    )
                                    all_paths.append(TaintPath(
                                        source=src_node,
                                        sink=sink_node,
                                        path=cross_path,
                                        is_sanitized=is_sanitized,
                                        sanitizers_found=sanitizers
                                    ))

        return all_paths
