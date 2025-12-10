from collections import defaultdict
from itertools import combinations
from math import inf

class BicliqueGenerator:
    """
    Takes in graph edge data in the form of list[list[u,v]]
    Formats edge data into two adjacency dictionaries
    Finds maximal bicliques and returns them as bitmasks.
    """
    def __init__(self, edges):
        self.edges = edges
        self.adj_u = defaultdict(set)
        self.adj_v = defaultdict(set)

        self.edge_index = dict()
        self.num_edges = len(edges)

        for idx, edge in enumerate(edges):
            self.edge_index[tuple(edge)] = idx

        unique_u_nodes = set()
        # This loop grabs u nodes and builds adjacency lists simultaneously
        for node_u, node_v in edges:
            unique_u_nodes.add(node_u)
            self.adj_u[node_u].add(node_v)
            self.adj_v[node_v].add(node_u)

        self.u_nodes = sorted(list(unique_u_nodes))

    def find_maximal_bicliques(self):

        found_bicliques = set()
        biclique_masks = []

        # Iterates through all subset sizes of the u nodes
        for size in range(1, len(self.u_nodes) + 1):
            for subset in combinations(self.u_nodes, size):
                # Intersection of all V-neighbors with subset of u nodes
                v_common = self.find_intersection(subset, 1)

                if not v_common:
                    continue
                # Intersection of all U-neighbors with v_common
                maximal_u = self.find_intersection(v_common, 2)

                b_sig = (frozenset(maximal_u), frozenset(v_common))

                if b_sig not in found_bicliques:
                    found_bicliques.add(b_sig)

                    mask = 0
                    for u_node in maximal_u:
                        for v_node in v_common:
                            if (u_node, v_node) in self.edge_index:
                                idx = self.edge_index[(u_node, v_node)]
                                mask |= (1 << idx)

                    biclique_masks.append(mask)

        return biclique_masks

    def find_intersection(self, edge_set, trip_num: int):
        sets_to_intersect = []
        if trip_num == 1:
            adj = self.adj_u
        elif trip_num == 2:
            adj = self.adj_v
        else:
            print("trip_num must be a 1 or 2")
            quit(1)

        for node in edge_set:
            sets_to_intersect.append(adj[node])
        if sets_to_intersect:
            output_intersection = set.intersection(*sets_to_intersect)
        else:
            output_intersection = set()

        return output_intersection


class BicliqueCoverSolver:
    """
    Takes in edge data and makes a generator object, finding all max bicliques
    Uses bitmasking and bitwise operations to find where a biclique is needed for covering
    Returns the exact Bipartite dimension.
    """
    def __init__(self, edges):
        # Instantiates helper class to get the bitmasks
        generator = BicliqueGenerator(edges)
        self.biclique_masks = generator.find_maximal_bicliques()

        self.num_edges = len(edges)
        self.full_mask = (1 << self.num_edges) - 1  # The target
        self.memo = {}

    def solve(self, mask=0):
        """
        This is where the Dynamic Programming happens.
        Takes in a mask which is whatever the current state of edge covering is.
        The bitmask is a series of 1's and 0's,
        1 = covered at that index
        0 = uncovered at that index
        The algorithm runs until all bits are 1 (covered, base case)
        Returns the minimum biclique cover number for the graph of edges.
        """
        # Check Memo
        if mask in self.memo:
            return self.memo[mask]

        # Base Case (Done?)
        if mask == self.full_mask:
            return 0

        target_edge = -1
        for idx in range(0, self.num_edges):
            if (mask & (1 << idx)) == 0:
                target_edge = idx
                break

        best_cost = inf
        for candidate in self.biclique_masks:
            if (candidate >> target_edge) & 1:
                new_mask = mask | candidate
                cost = 1 + self.solve(new_mask)
                best_cost = min(best_cost, cost)
            else:
                continue

        self.memo[mask] = best_cost
        return best_cost

if __name__ == "__main__":
    test_edges = [(0, 10), (0, 11), (1, 10), (1, 11), (2, 12)]
    solver = BicliqueCoverSolver(test_edges)
    print(solver.solve())