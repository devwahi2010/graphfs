from collections import deque, defaultdict
from typing import List, Dict, Set
from .models import Node, Edge

def neighbors(node_id, edge_types=None):
    qs = Edge.objects.filter(src_id=node_id)
    if edge_types:
        qs = qs.filter(edge_type__in=edge_types)
    return list(qs.values_list('dst_id', flat=True))

def shortest_path_bfs(src_id, dst_id, edge_types=None) -> List[str]:
    if src_id == dst_id:
        return [src_id]
    q = deque([src_id])
    parent = {src_id: None}
    while q:
        u = q.popleft()
        for v in neighbors(u, edge_types):
            if v not in parent:
                parent[v] = u
                if v == dst_id:
                    path = [v]
                    while parent[path[-1]] is not None:
                        path.append(parent[path[-1]])
                    path.reverse()
                    return path
                q.append(v)
    return []

def detect_cycles(limit: int = 20) -> List[List[str]]:
    edge_types = [Edge.EdgeType.CONTAINS, Edge.EdgeType.SYMLINK, Edge.EdgeType.TAGGED]
    graph = defaultdict(list)
    for (src, dst) in Edge.objects.filter(edge_type__in=edge_types).values_list('src_id','dst_id'):
        graph[src].append(dst)

    visited: Set[str] = set()
    stack: Set[str] = set()
    cycles = []

    def dfs(u, path):
        if len(cycles) >= limit:
            return
        visited.add(u)
        stack.add(u)
        path.append(u)
        for v in graph[u]:
            if v not in visited:
                dfs(v, path)
            elif v in stack:
                if v in path:
                    idx = path.index(v)
                    cyc = path[idx:].copy()
                    if cyc:
                        cycles.append(cyc)
                        if len(cycles) >= limit:
                            return
        stack.remove(u)
        path.pop()

    for node_id in list(graph.keys()):
        if node_id not in visited:
            dfs(node_id, [])

    return cycles

def k_hop_subgraph(center_id, k=2, edge_types=None) -> Dict:
    seen = set([center_id])
    frontier = set([center_id])
    nodes = set([center_id])
    edges = set()

    for _ in range(k):
        next_frontier = set()
        for u in list(frontier):
            qs_out = Edge.objects.filter(src_id=u)
            if edge_types:
                qs_out = qs_out.filter(edge_type__in=edge_types)
            for e in qs_out:
                nodes.add(e.dst_id)
                edges.add((str(e.id), e.src_id, e.dst_id, e.edge_type))
                if e.dst_id not in seen:
                    next_frontier.add(e.dst_id)
                    seen.add(e.dst_id)

            qs_in = Edge.objects.filter(dst_id=u)
            if edge_types:
                qs_in = qs_in.filter(edge_type__in=edge_types)
            for e in qs_in:
                nodes.add(e.src_id)
                edges.add((str(e.id), e.src_id, e.dst_id, e.edge_type))
                if e.src_id not in seen:
                    next_frontier.add(e.src_id)
                    seen.add(e.src_id)

        frontier = next_frontier

    node_objs = Node.objects.filter(id__in=list(nodes))

    return {
        "nodes": [
            {"data": {"id": str(n.id), "label": n.name, "type": n.type}}
            for n in node_objs
        ],
        "edges": [
            {"data": {"id": eid, "source": src, "target": dst, "type": etype}}
            for (eid, src, dst, etype) in edges
        ]
    }
