import time
import statistics

import JaredAlgorithm
import kevin_DP_algo

import test_graphs as dd
"""
def edges_to_matrix(edges):
    
    #Converts list of tuples [(u, v)...] to Adjacency Matrix.
    
    if not edges:
        return []

    # Flatten to find the highest node ID (e.g. if max node is 10 size is 11)
    max_id = max(max(u, v) for u, v in edges)
    size = max_id + 1

    matrix = [[0] * size for _ in range(size)]

    # Fill 1s
    for u, v in edges:
        matrix[u][v] = 1
        matrix[v][u] = 1

    return matrix
"""
"""
def edges_to_graph_obj(edges):
    
    # Converts list of tuples to Tate's Graph object.
    
    G = Graph()
    if not edges:
        return G

    # Add vertices first
    all_nodes = set()
    for u, v in edges:
        all_nodes.add(u)
        all_nodes.add(v)
    G.add_vertex(*all_nodes)

    # Add edges
    for u, v in edges:
        G.add_edge(Graph.Edge(u, v))
    return G
"""

# Wrappers

def run_kevin(edges):
    """
    Wrapper for Kevin's Custom Dynamic Programming Solver.
    """
    # Create solver instance
    solver = kevin_DP_algo.BicliqueCoverSolver(edges)
    # Run with a high max_k limit (15) so it doesn't error out on Hard graphs (k=9)
    return solver.solve()


def run_tate(edges):
    """
    Wrapper for Tate's Custom Algorithm.
    """
    # 1. Convert Data to Graph Object
    #G = edges_to_graph_obj(edges)
    # 2. Run Algorithm
    return #approx_biclique_cover.approx_biclique_cover_number(G)


def run_jared(edges):
    """
    Wrapper for Jared's Custom Algorithm.
    """
    return len(JaredAlgorithm.recursive_search(edges))



def main():
    # Driver code
    algorithms = {
        "Kevin (Custom, DP)": run_kevin,
        #"Tate (Custom)": run_tate,
        "Jared (Custom)": run_jared
    }

    graphs_to_test = {
        "Easy (Matching 6)": dd.TEST_DATA["Easy_Matching_6"],
        "Medium (Matching 8)": dd.TEST_DATA["Medium_Matching_8"],
        "Hard (Matching 10)": dd.TEST_DATA["Hard_Dense_Half_10"]
    }

    print(f"{'ALGORITHM':<20} | {'DATASET':<20} | {'AVG TIME (s)':<12} | {'RESULT (k)':<10}")
    print("-" * 75)

    for algo_name, algo_func in algorithms.items():

        for graph_name, edges in graphs_to_test.items():

            run_times = []
            results = []

            # Run 5 times for average
            for i in range(5):
                t_start = time.perf_counter()

                try:
                    k = algo_func(edges)
                except Exception as e:
                    # Catch errors so one crash doesn't stop everything
                    k = "ERR"

                t_end = time.perf_counter()

                run_times.append(t_end - t_start)
                results.append(k)

            avg_time = statistics.mean(run_times)

            final_k = results[-1]

            print(f"{algo_name:<20} | {graph_name:<20} | {avg_time:.6f}s    | k={final_k}")

        print("-" * 75)


if __name__ == "__main__":
    main()