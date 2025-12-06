"""Writen by Kevin Pett
Exact algorithm for the Bipartite Dimension problem."""

import sys
import itertools
from collections import defaultdict
import time
from toy_datasets import graphs, expected_k
from difficult_datasets import difficult_graphs
from test_graphs import TEST_DATA

try:
    from pysat.solvers import Minisat22
except ImportError:
    print("Error: Library 'python-sat' is missing.")
    print("Please install it running: pip install python-sat")
    sys.exit(1)

print_all = False

class BicliqueCoverSolver:

    def __init__(self, edges: list[tuple[int, int]]):
        """
        Initialize with a list of edges (u, v).
        Assumes U vertices are the first element, V vertices are the second.
        """
        self.original_edges = set(tuple(e) for e in edges)

        # Extract unique U and V sets
        self.u_nodes = sorted(list(set(u_ for u_, v_ in edges)))
        self.v_nodes = sorted(list(set(v_ for u_, v_ in edges)))

        # Build Adjacency Dictionary (for twin reduction)
        self.adj_u = defaultdict(set)  # Neighbors of U
        self.adj_v = defaultdict(set)  # Neighbors of V

        for u_, v_ in edges:
            self.adj_u[u_].add(v_)
            self.adj_v[v_].add(u_)

    def _get_signature(self, neighbors: set) -> tuple:
        """Helper to make neighbor sets hashable for twin detection."""
        return tuple(sorted(list(neighbors)))

    def twin_reduction(self):
        """
        Phase 1: Kernelization.
        Iteratively merges 'True Twins' until the graph is stable.
        True Twins are vertices in the same partition with identical neighbors.
        """
        stable = False

        # Working sets of vertices
        curr_u = self.u_nodes[:]
        curr_v = self.v_nodes[:]

        while not stable:
            stable = True

            # Reduce U Set
            u_signatures = {}  # Sig -> vertex representative
            new_u = []

            for u_ in curr_u:
                # Calculate signature based on CURRENT neighbors in V
                # Consider neighbors that still exist in curr_v
                valid_neighbors = self.adj_u[u_].intersection(curr_v)
                sig = self._get_signature(valid_neighbors)

                if sig in u_signatures:
                    # Found a twin! discard 'u', keep the representative
                    stable = False
                else:
                    u_signatures[sig] = u_
                    new_u.append(u_)
            curr_u = new_u

            # Reduce V Set
            v_signatures = {}
            new_v = []

            for v_ in curr_v:
                # Calculate signature based on CURRENT neighbors in U
                valid_neighbors = self.adj_v[v_].intersection(curr_u)
                sig = self._get_signature(valid_neighbors)

                if sig in v_signatures:
                    stable = False
                else:
                    v_signatures[sig] = v_
                    new_v.append(v_)
            curr_v = new_v

        return curr_u, curr_v

    def solve(self, max_k=9):
        """
        Main Loop: Tries k=1, k=2... up to max_k.
        """
        if print_all:
            print(f"Original Graph: {len(self.u_nodes)} U-nodes, {len(self.v_nodes)} V-nodes.")

        # 1. Kernelize + timer
        kernel_start = time.perf_counter()
        k_u, k_v = self.twin_reduction()
        kernel_end = time.perf_counter()
        if print_all:
            print(f"Kernelization time = {(kernel_end - kernel_start):.6f}s")
            print(f"Kernel Reduced: {len(k_u)} U-nodes, {len(k_v)} V-nodes.")

        # 2. Iterate k
        for k in range(1, max_k + 1):
            # If kernel size > 2^k, it's impossible
            if len(k_u) > 2 ** k or len(k_v) > 2 ** k:
                if print_all:
                    print(f"k={k}: Impossible (Kernel size exceeds 2^k fingerprint limit)")
                    continue
            if print_all:
                print(f"Checking k={k} using SAT...", end=" ")
            if self._check_k_sat(k, k_u, k_v):
                if print_all:
                    print("SAT! Found exact cover.")
                return k
            else:
                if print_all:
                    print("UNSAT.")

        return -1  # Not found within max_k

    def _check_k_sat(self, k, active_u, active_v):
        """
        Phase 2 & 3: Encoding and Solving.
        Translates the Kernel factorization into CNF and solves.
        """
        encode_start = time.perf_counter()
        solver = Minisat22()

        m, n = len(active_u), len(active_v)

        # SAT Variable IDs
        # W variables (m rows * k cols): 1 to m*k
        # H variables (k rows * n cols): m*k + 1 to m*k + n*k
        encode_start = time.perf_counter()
        def w_var(row_idx, biclique_idx):
            return 1 + (row_idx * k) + biclique_idx

        def h_var(biclique_idx, col_idx):
            return 1 + (m * k) + (biclique_idx * n) + col_idx

        # Generate clauses
        # Cover the adjacency matrix of the kernel
        for i, u_node in enumerate(active_u):
            for j, v_node in enumerate(active_v):

                # Check if edge exists in original data
                has_edge = v_node in self.adj_u[u_node]

                if not has_edge:
                    # constraint: For all z, NOT(W_iz AND H_zj)
                    # CNF: (NOT W_iz OR NOT H_zj)
                    for z in range(k):
                        solver.add_clause([-w_var(i, z), -h_var(z, j)])

                else:
                    # Since k is small, we distribute it: (W1H1 v W2H2...)
                    # This generates 2^k clauses.

                    # Generate all combinations of choosing either W or H for each biclique
                    for pattern in itertools.product([0, 1], repeat=k):
                        clause = []
                        for z, choice in enumerate(pattern):
                            # choice 0 -> W, choice 1 -> H
                            if choice == 0:
                                clause.append(w_var(i, z))
                            else:
                                clause.append(h_var(z, j))
                        solver.add_clause(clause)
        encode_end = time.perf_counter()
        if print_all:
            print(f"\nEncoding time = {(encode_end - encode_start):.6f}s")

        solver_start = time.perf_counter()
        is_sat = solver.solve()
        solver_end = time.perf_counter()
        if print_all:
            print(f"Solver time = {(solver_end - solver_start):.6f}s")

        solver.delete()
        return is_sat

def run_test(graph_name, test_num, actual_k ='?'):
    """
    Takes a graph's name that's meant to be used on a dictionary of graphs,
    which test iteration number this is,
    and can take the value of the actual k parameter.
    """
    if print_all:
        print(f"Test #{test_num}: {graph_name = } (Expected k={actual_k})")
    exact_solver = BicliqueCoverSolver(TEST_DATA[graph_name])
    if print_all:
        print(f"Calculated Bipartite Dimension: {exact_solver.solve()}\n")

def main():
    # Uses toy datasets for testing accuracy of the exact FPT algorithm
    all_runtimes = []
    for idx, graph in enumerate(TEST_DATA):
        runtimes = []
        print("=================================================\n")
        for iteration in range(1, 6):
            total_runtime_start = time.perf_counter()
            run_test(graph, expected_k[idx])
            total_runtime_end = time.perf_counter()
            runtimes.append(total_runtime_end - total_runtime_start)
            print(f"Total runtime for test #{iteration}:")
            print(f"{runtimes[iteration-1]:.6f}\n")
            print(f"-------------------------------------------")
        print(f"\n*** Average runtime for 5 tests of {graph} ***")
        print(f"     {(sum(runtimes) / 5):.8f}s\n")
        print("=================================================\n")
        all_runtimes.append(sum(runtimes) / 5)

    print("All average runtimes in order of input:")
    for idx, graph in enumerate(TEST_DATA):
        print(f"{graph} avg time: {all_runtimes[idx]:.8f}")


def import_main(dataset):

    for idx, graph in enumerate(dataset.graphs):
        runtimes = []
        for iteration in range(1, 6):
            total_runtime_start = time.perf_counter()
            run_test(graph, expected_k[idx], iteration)
            total_runtime_end = time.perf_counter()
            runtimes.append(total_runtime_end - total_runtime_start)
            #print(f"Total runtime for test #{iteration}:")
            #print(f"{runtimes[iteration-1]:.6f}\n")
            print(f"-------------------------------------------")
        print(f"\n*** Average runtime for 5 tests of {graph} with Exact FPT Algorithm***")
        print(f"     {(sum(runtimes) / 5):.8f}s\n")

if __name__ == "__main__":
    print_all = True
    main()