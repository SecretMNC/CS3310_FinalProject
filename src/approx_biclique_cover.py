
from typing import Generator, Optional
from graph import Graph
from bipartite import CompleteBipartiteGraph
import random
from math import isqrt


def approx_biclique_cover(G: Graph, k: Optional[int] = None) -> Generator[CompleteBipartiteGraph, None, None]:
    
    def uncovered_neighbors(v):
        return {w for e in E if (v in e) for w in e.vertices() if (v != w)}
    
    k = isqrt(G.m)+1 if (k is None) else k      # number of samples
    E = set(G.C.keys())                         # uncovered edges

    while len(E) > 0:

        u, v = next(iter(E)).vertices()
        B = CompleteBipartiteGraph({u}, {v})    # backup biclique in case loop results in empty graph, so algorithm always makes progress

        E_sample = E if (len(E) <= k) else set(random.sample(list(E), k))
        most_covered_edges = 0                  # most number of uncovered edges covered with a biclique

        for e in E_sample:

            u, v = e.vertices()
            L = uncovered_neighbors(u)
            R = uncovered_neighbors(v) - L

            # loop until convergence on biclique
            while L and R:
                L_old, R_old = L, R
                L = set.intersection(*[uncovered_neighbors(v) for v in R])
                R = set.intersection(*[uncovered_neighbors(v) for v in L]) - L
                if (L_old == L) and (R_old == R):
                    break

            b = CompleteBipartiteGraph(L, R)
            covered_edges = len(E.intersection(set(b.C.keys())))
            if (covered_edges > most_covered_edges):
                B = b
                most_covered_edges = covered_edges
        
        E -= set(B.C.keys())        # remove edges that are now covered by B

        yield B


def approx_biclique_cover_number(G : Graph, k : Optional[int] = None) -> int:
    return sum(1 for _ in approx_biclique_cover(G, k))


def dataset_to_graph_object(edges_list):
    """
    Converts a list of tuples [(u, v), ...] into a Graph object.
    """
    G = Graph()

    # 1. Collect all unique vertices first
    all_vertices = set()
    for u, v in edges_list:
        all_vertices.add(u)
        all_vertices.add(v)

    # 2. Add vertices to Graph
    # We unpack the set into arguments
    G.add_vertex(*all_vertices)

    # 3. Add Edges
    for u, v in edges_list:
        # Create the specific Edge object required by the class
        edge_obj = Graph.Edge(u, v)
        G.add_edge(edge_obj)

    return G

if __name__ == "__main__":
    crown_edges = [(0, 3), (0, 4), (1, 3), (1, 5), (2, 4), (2, 5)]

    # Convert it
    my_graph = dataset_to_graph_object(crown_edges)

    # Run the heuristic
    cover_count = approx_biclique_cover_number(my_graph)
    print(f"Approximated K: {cover_count}")