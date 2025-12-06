import time
import difficult_datasets as dd


def handle_data(index_graph):
    # Create new empty matrix with same size as sorted_graph
    n = len(index_graph)//2
    new_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(2):
            if j == 0:
                row = index_graph[i][j]
            elif j == 1:
                col = index_graph[i][j]
        if col != row:
            new_matrix[row][col] = 1
            new_matrix[col][row] = 1
    return new_matrix



def sort_graph(graph):
    sorted_graph = sorted(graph, key=lambda x: sum(x), reverse=True)
    print("Sorted graph by number of trues in each row:")
    # Move all the trues to the left of the matrix so it form a triangle
    
    n = len(sorted_graph)
    for i in range(n):
        m = len(sorted_graph[i])
        true_count = sum(sorted_graph[i])
        for j in range(m):
            if j < true_count:
                sorted_graph[i][j] = 1
            else:
                sorted_graph[i][j] = 0
    print("Triangular form of the graph:")
    for row in sorted_graph:
        print(row)
    return sorted_graph

def find_largest_square_submatrix(matrix):
    n = len(matrix)
    # Create a list of the indexes of the last true (1) in each row
    last_true_indexes = []
    for i in range(n):
        last_index = -1
        for j in range(len(matrix[i]) - 1, -1, -1):  # Search from right to left
            if matrix[i][j] == 1:
                last_index = j
                break
        last_true_indexes.append(last_index+1) # Make 1 larger for math reasons
    print("Indexes of last true in each row:", last_true_indexes)
    large_size = 0
    size = -1
    index = -1
    indexes = last_true_indexes.copy()
    for i in range(len(indexes)):
        size = indexes[i] * (i+1)
        if size > large_size:
            large_size = size
            index = i
    print(f"Largest square sub-matrix size: {large_size} at row index: {index}")
    return index, indexes[index], large_size

def swap_trues(matrix, index, bottom_row):
    for i in range(index+1):
        for j in range(bottom_row):
            if matrix[i][j] == 1:
                matrix[i][j] = 0
    return matrix

def bipartite(graph):
    num_bq = 0
    if format:
        # Handle the data to get binary matrix
        readable_graph = handle_data(graph)
    else:
        readable_graph = graph
    while True:
        # Find how many trues are in each row
        counts = [sum(row) for row in readable_graph]
        print("Counts of trues in each row:", counts)

        # Sort the matrix by largest trues to least trues
        readable_graph = sort_graph(readable_graph)
        # Find the largest square sub-matrix of trues
        index, row, size = find_largest_square_submatrix(readable_graph)
        if size <= 1:
            num_bq += 1
            print("No more square sub-matrix of size > 1 found. Exiting.")
            break
        num_bq += 1
        # Change the trues to false in the sub-matrix
        readable_graph = swap_trues(readable_graph, index, row)
        print("Modified matrix after swapping trues to false in the sub-matrix:")
        for row in readable_graph:
            print(row)
    return num_bq

if __name__ == "__main__":

    format = False
    graph = [
        [0, 1, 1, 1, 1],
        [1, 0, 0, 1, 0],
        [1, 0, 1, 1, 0],
        [1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0]
    ]

    booleanMatrix16 = [
    [ 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1 ],
    ]
    graph8 = dd.difficult_graphs["Crown_S10"]

    start_time = time.time()
    num_bq = bipartite(graph)
    print(f"Number of bipartite subgraphs found: {num_bq}")
    end_time = time.time()

    print(f"Execution time: {end_time - start_time} seconds")