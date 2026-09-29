"""
TorusGuard Taint Engine — Directed Taint Flow Graph
Builds Def->Use chains, walks reachability paths, detects sanitization points,
and enumerates source-to-sink vulnerability paths.
"""

from collections import deque
from typing import List, Dict, Set, Optional, Any, Tuple
from core.taint import TaintNode, TaintEdge, TaintPath, TaintPropagator
from core.taint_rules import get_sources_for_language, get_sinks_for_language, get_sanitizers_for_language


class TaintGraph:
    """Directed graph tracking taint flow from sources to sinks."""

    def __init__(self):
        self.nodes: Dict[str, TaintNode] = {}
        self.edges: List[TaintEdge] = []
        self.adjacency: Dict[str, List[TaintEdge]] = {}
        self.reverse_adjacency: Dict[str, List[TaintEdge]] = {}

    def add_node(self, node: TaintNode) -> TaintNode:
        nid = node.node_id()
        if nid not in self.nodes:
            self.nodes[nid] = node
            self.adjacency[nid] = []
            self.reverse_adjacency[nid] = []
        return self.nodes[nid]

    def add_edge(self, from_node: TaintNode, to_node: TaintNode, edge_type: str = "assignment", line_number: int = 0) -> TaintEdge:
        fn = self.add_node(from_node)
        tn = self.add_node(to_node)
        edge = TaintEdge(from_node=fn, to_node=tn, edge_type=edge_type, line_number=line_number)
        self.edges.append(edge)
        self.adjacency[fn.node_id()].append(edge)
        self.reverse_adjacency[tn.node_id()].append(edge)
        return edge

    def find_tainted_paths(self, source: TaintNode, sink: TaintNode, max_depth: int = 8) -> List[List[TaintNode]]:
        """
        BFS/DFS to find all paths from source to sink.
        Returns a list of node paths.
        """
        source_id = source.node_id()
        sink_id = sink.node_id()

        if source_id not in self.nodes or sink_id not in self.nodes:
            return []

        paths: List[List[TaintNode]] = []
        # Queue contains: (current_node_id, [current_path])
        queue = deque([(source_id, [self.nodes[source_id]])])

        while queue:
            curr_id, current_path = queue.popleft()

            if len(current_path) > max_depth:
                continue

            if curr_id == sink_id:
                paths.append(current_path)
                continue

            visited_ids = {n.node_id() for n in current_path}

            for edge in self.adjacency.get(curr_id, []):
                next_id = edge.to_node.node_id()
                if next_id not in visited_ids:
                    queue.append((next_id, current_path + [edge.to_node]))

        return paths

    def is_path_sanitized(self, path: List[TaintNode], sink_category: str, language: str) -> Tuple[bool, List[TaintNode]]:
        """
        Check if any node in the path acts as a sanitizer for the target sink category.
        """
        sanitizers = get_sanitizers_for_language(language)
        sanitizers_found = []

        for node in path:
            if node.node_type == "sanitizer":
                sanitizers_found.append(node)
                continue

            # Check if node expression or pattern contains a sanitizer
            for s in sanitizers:
                if s["pattern"] in node.expression or s["pattern"] in node.pattern:
                    if not sink_category or sink_category in s.get("cleans", []):
                        sanitizers_found.append(node)
                        break

        return len(sanitizers_found) > 0, sanitizers_found

    def analyze_file_code(
        self,
        file_path: str,
        code_content: str,
        language: str = "python"
    ) -> List[TaintPath]:
        """
        Parses source lines into Def-Use taint graph and discovers source->sink flows.
        Supports variable re-assignments, transformations, and sanitizers.
        """
        import re

        sources_catalog = get_sources_for_language(language)
        sinks_catalog = get_sinks_for_language(language)
        sanitizers_catalog = get_sanitizers_for_language(language)

        lines = code_content.splitlines()
        detected_sources: List[TaintNode] = []
        detected_sinks: List[Tuple[TaintNode, Dict[str, Any]]] = []

        # Current tainted variables mapping: var_name -> latest TaintNode
        tainted_vars: Dict[str, TaintNode] = {}

        # 1. First pass: Scan line-by-line for source introductions, assignments, and sink invocations
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//", "/*", "*")):
                continue

            # Check for direct sources
            # Example: user_input = request.GET["id"] or data = req.body
            for src_spec in sources_catalog:
                src_pat = src_spec["pattern"]
                if src_pat in stripped:
                    # Look for assignment LHS
                    var_name = ""
                    # Handle assignment `x = ...` or `const x = ...` or `let x = ...` or `x := ...`
                    assign_match = re.match(r"^(?:const|let|var)?\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(?::=[=]?|=)\s*(.+)$", stripped)
                    if assign_match:
                        var_name = assign_match.group(1).strip()
                    else:
                        var_name = f"anon_src_{line_num}"

                    src_node = TaintNode(
                        variable_name=var_name,
                        file_path=file_path,
                        line_number=line_num,
                        node_type="source",
                        expression=stripped,
                        pattern=src_pat,
                        category=src_spec.get("category", "user_input"),
                        metadata={"framework": src_spec.get("framework", ""), "label": src_spec.get("label", "")}
                    )
                    self.add_node(src_node)
                    detected_sources.append(src_node)
                    if var_name:
                        tainted_vars[var_name] = src_node

            # Check for propagation via assignments: LHS = RHS where RHS contains a tainted variable
            assign_match = re.match(r"^(?:const|let|var)?\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(?::=[=]?|=)\s*(.+)$", stripped)
            if assign_match:
                lhs_var = assign_match.group(1).strip()
                rhs_expr = assign_match.group(2).strip()

                # Check if RHS applies a sanitizer
                is_sanitized = False
                for san_spec in sanitizers_catalog:
                    if san_spec["pattern"] in rhs_expr:
                        # Sanitized assignment!
                        san_node = TaintNode(
                            variable_name=lhs_var,
                            file_path=file_path,
                            line_number=line_num,
                            node_type="sanitizer",
                            expression=rhs_expr,
                            pattern=san_spec["pattern"],
                            metadata={"cleans": san_spec.get("cleans", [])}
                        )
                        self.add_node(san_node)
                        # Link if any tainted var was input to sanitizer
                        for tv_name, tv_node in list(tainted_vars.items()):
                            if re.search(r"\b" + re.escape(tv_name) + r"\b", rhs_expr):
                                self.add_edge(tv_node, san_node, edge_type="argument", line_number=line_num)
                        tainted_vars[lhs_var] = san_node
                        is_sanitized = True
                        break

                if not is_sanitized:
                    # Check if RHS mentions any known tainted variable
                    for tv_name, tv_node in list(tainted_vars.items()):
                        if re.search(r"\b" + re.escape(tv_name) + r"\b", rhs_expr):
                            transform_node = TaintNode(
                                variable_name=lhs_var,
                                file_path=file_path,
                                line_number=line_num,
                                node_type="transform",
                                expression=rhs_expr
                            )
                            self.add_node(transform_node)
                            self.add_edge(tv_node, transform_node, edge_type="assignment", line_number=line_num)
                            tainted_vars[lhs_var] = transform_node

            # Check for Sinks
            for sink_spec in sinks_catalog:
                sink_pat = sink_spec["pattern"]
                if sink_pat in stripped:
                    sink_node = TaintNode(
                        variable_name="",
                        file_path=file_path,
                        line_number=line_num,
                        node_type="sink",
                        expression=stripped,
                        pattern=sink_pat,
                        category=sink_spec.get("category", ""),
                        metadata=sink_spec
                    )
                    self.add_node(sink_node)
                    detected_sinks.append((sink_node, sink_spec))

                    # Check which tainted variables are passed into or present in the sink line
                    for tv_name, tv_node in list(tainted_vars.items()):
                        if re.search(r"\b" + re.escape(tv_name) + r"\b", stripped):
                            self.add_edge(tv_node, sink_node, edge_type="call", line_number=line_num)

        # 2. Path Finding & Resolution
        results: List[TaintPath] = []
        for sink_node, sink_spec in detected_sinks:
            for src_node in detected_sources:
                paths = self.find_tainted_paths(src_node, sink_node)
                for node_path in paths:
                    is_sanitized, sanitizers = self.is_path_sanitized(node_path, sink_spec.get("category", ""), language)
                    results.append(TaintPath(
                        source=src_node,
                        sink=sink_node,
                        path=node_path,
                        is_sanitized=is_sanitized,
                        sanitizers_found=sanitizers,
                        confidence_penalty=-40 if is_sanitized else 0
                    ))

        return results
