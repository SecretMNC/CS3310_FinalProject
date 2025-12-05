"""Created by Gemini 3 Thinking model for testing purposes."""


def generate_crown_graph(n):
    """
    Generates Crown Graph S_n.
    - Vertices: 2n (n in U, n in V).
    - Edges: u_i connects to v_j for all i != j.
    - Dimension: Exactly n.
    - Why predictable: We know exactly when it should finish.
    """
    edges = []
    for u in range(n):
        for v in range(n):
            if u != v:
                edges.append([u, v + n])
    return edges


def generate_disjoint_union(n1, n2):
    """
    Creates two separate Crown Graphs in the same dataset.
    - Graph: S_n1 + S_n2.
    - Vertices: 2*(n1 + n2).
    - Dimension: n1 + n2.
    - Difficulty: Tests if the solver can handle 'disconnected' complexity.
      It increases variables (N) without increasing density as much as a single large Crown.
    """
    edges = generate_crown_graph(n1)

    # Offset the second graph so nodes don't overlap
    offset = 2 * n1
    for u in range(n2):
        for v in range(n2):
            if u != v:
                # Add offset to both u and v for the second graph
                edges.append((u + offset, v + n2 + offset))

    return edges


def generate_modulo_graph(n, mod_val=3):
    """
    A deterministic dense graph that is NOT a Crown Graph.
    - Logic: Connect u_i to v_j if (i + j) is NOT divisible by mod_val.
    - Difficulty: High density but weird structure.
      Breaks the 'perfect symmetry' of Crown graphs that solvers often exploit.
    """
    edges = []
    for u in range(n):
        for v in range(n):
            if (u + v) % mod_val != 0:
                edges.append((u, v + n))
    return edges


# --- The "Goldilocks" Datasets ---

difficult_graphs = {
    # 1. Crown S8 (16 Nodes, Target k=8)
    # This is the next logical step after your S7.
    # It adds 2 nodes and 1 dimension. Should take ~1-5 seconds.
    "Crown_S8": generate_crown_graph(8),

    # 2. Crown S9 (18 Nodes, Target k=9)
    # 18 Nodes. This is where it starts getting heavy.
    # Likely 10-30 seconds.
    "Crown_S9": generate_crown_graph(9),

    # 3. Double Crown S5+S5 (20 Nodes, Target k=10)
    # Two separate S5 graphs.
    # Total nodes: 20. Target k: 10.
    # This is a test: Can the solver realize it's two small problems,
    # or will it choke on the combined size?
    "Union_S5_S5": generate_disjoint_union(5, 5),

    # 4. Modulo 10x10 (20 Nodes, Target k=Unknown/High)
    # A deterministic dense graph (20 nodes).
    # Structured differently than a crown. Good for checking solver robustness.
    "Modulo_Dense_10": generate_modulo_graph(10, mod_val=3),

    # 5. Crown S10 (20 Nodes, Target k=10)
    # The limit.
    # This is smaller than the S12 that stalled you, but significantly harder than S9.
    # If this runs too long, stop it.
    "Crown_S10": generate_crown_graph(10),

    "Crown_S11": generate_crown_graph(11)
}

if __name__ == "__main__":
    for name, edges in DIFFICULT_GRAPHS.items():
        print(f"Dataset '{name}': {len(edges)} edges")