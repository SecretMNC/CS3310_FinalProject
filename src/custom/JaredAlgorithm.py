#import difficult_datasets as dd

def recursive_search(list_of_edges):
    """
    Recursively finds the minimum biclique cover for the given edges.
    The Bipartite Dimension Problem seeks to find the minimum number of 
    complete bipartite subgraphs (bicliques) needed to cover all edges.
    
    Strategy: Find the largest biclique, remove it, then recursively process remaining edges.
    
    Args:
        list_of_edges: List of tuples or lists [(u, v), ...] representing edges
        
    Returns:
        List of bicliques, where each biclique is represented as a dict:
        {'U': set of left vertices, 'V': set of right vertices}
    """
    # Convert edges to tuples if they're lists
    list_of_edges = [tuple(edge) if isinstance(edge, list) else edge for edge in list_of_edges]
    
    # Base case: if no edges left, return empty list
    if not list_of_edges or len(list_of_edges) == 0:
        return []
    
    # Build adjacency information for all vertices
    u_neighbors = {}  # u_node -> set of v neighbors
    v_neighbors = {}  # v_node -> set of u neighbors
    all_u_vertices = set()
    all_v_vertices = set()
    
    for u, v in list_of_edges:
        if u not in u_neighbors:
            u_neighbors[u] = set()
        if v not in v_neighbors:
            v_neighbors[v] = set()
        u_neighbors[u].add(v)
        v_neighbors[v].add(u)
        all_u_vertices.add(u)
        all_v_vertices.add(v)
    
    # Find the LARGEST maximal biclique by checking all possibilities
    largest_biclique = None
    largest_size = 0
    
    for u_start, v_start in list_of_edges:
        # Initialize with one edge
        U_set = {u_start}
        V_set = {v_start}
        
        # Expand to find a maximal biclique
        for u in all_u_vertices:
            if u not in U_set:
                if V_set.issubset(u_neighbors.get(u, set())):
                    U_set.add(u)
        
        for v in all_v_vertices:
            if v not in V_set:
                if U_set.issubset(v_neighbors.get(v, set())):
                    V_set.add(v)
        
        # Refine until the biclique is maximal
        changed = True
        while changed:
            changed = False
            
            # Remove any U vertex not connected to all V vertices
            U_set = {u for u in U_set if V_set.issubset(u_neighbors.get(u, set()))}
            
            # Remove any V vertex not connected to all U vertices
            V_set = {v for v in V_set if U_set.issubset(v_neighbors.get(v, set()))}
            
            # Try to add more vertices
            for u in all_u_vertices:
                if u not in U_set and V_set.issubset(u_neighbors.get(u, set())):
                    U_set.add(u)
                    changed = True
            
            for v in all_v_vertices:
                if v not in V_set and U_set.issubset(v_neighbors.get(v, set())):
                    V_set.add(v)
                    changed = True
        
        # Check if this is the largest biclique found so far
        biclique_size = len(U_set) * len(V_set)
        if biclique_size > largest_size:
            largest_size = biclique_size
            largest_biclique = {'U': U_set, 'V': V_set}
    
    # If no biclique found, return empty (shouldn't happen with valid edges)
    if largest_biclique is None:
        return []
    
    # Remove edges covered by this biclique
    covered_edges = {(u, v) for u in largest_biclique['U'] for v in largest_biclique['V']}
    remaining_edges = [edge for edge in list_of_edges if edge not in covered_edges]
    
    # Recursively find cover for remaining edges
    rest_of_cover = recursive_search(remaining_edges)
    
    # Return this biclique plus the rest
    return [largest_biclique] + rest_of_cover 






if __name__ == "__main__":
    #import difficult_datasets as dd
    graph = dd.difficult_graphs["Crown_S11"]
    
    # Call recursive_search to find biclique cover
    biclique_cover = recursive_search(graph)
    
    print(f"Found {len(biclique_cover)} bicliques:")
    for i, biclique in enumerate(biclique_cover, 1):
        print(f"Biclique {i}:")
        print(f"  U (left):  {sorted(biclique['U'])}")
        print(f"  V (right): {sorted(biclique['V'])}")
        print(f"  Edges covered: {len(biclique['U']) * len(biclique['V'])}")
        print()
    
    print(f"Total bipartite dimension k = {len(biclique_cover)}")