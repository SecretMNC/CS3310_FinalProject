
from src.graph import Graph
from src.bipartite import CompleteBipartiteGraph
from src.approx_biclique_cover import approx_biclique_cover
from statistics import mean
from time import time


def main():

    files = [
        (Graph, "./test/test_data/test1"),
        (Graph, "./test/test_data/test2"),
        (CompleteBipartiteGraph, "./test/test_data/test3"),
        (Graph, "./test/test_data/test4")
    ]
    N = 5      # number of iterations

    for graph_type, file in files:

        G = graph_type.from_file(file, Graph.Edge)
        CBG_sets = []
        times = []

        for _ in range(N):

            start = time()
            new_CBG_sets = list(approx_biclique_cover(G))
            stop = time()
            times.append(stop - start)

            if (len(new_CBG_sets) < len(CBG_sets)) or (len(CBG_sets) == 0):
                CBG_sets = new_CBG_sets

        print(f"Approximation on graph G(|V|={G.n}, |E|={G.m}) results in a set of {len(CBG_sets)} biclique cover(s):\n")
        for i, CBG in enumerate(CBG_sets):
            print(f"\t({i+1}) \tU: {CBG.U}, \tV: {CBG.V}")
        print()

        cover = CBG_sets[0].union(*CBG_sets[1:]) if (len(CBG_sets) > 1) else CBG_sets[0]

        print(f"Covers all edges?: {cover == G}")
        print(f"Average runtime over {N} evaluations: \t{mean(times)} s\n\n")
    
    
    # Output:

    # Approximation on graph G(|V|=10, |E|=24) results in a set of 6 biclique cover(s):

    #         (1)     U: {6, 7},      V: {8, 9, 3, 5}
    #         (2)     U: {2},         V: {1, 3, 5, 7, 8}
    #         (3)     U: {4},         V: {1, 5, 6, 9, 10}
    #         (4)     U: {10, 3},     V: {8, 1}
    #         (5)     U: {10},        V: {9}
    #         (6)     U: {5},         V: {8}

    # Covers all edges?: True
    # Average runtime over 5 evaluations:     0.001157236099243164 s


    # Approximation on graph G(|V|=12, |E|=17) results in a set of 4 biclique cover(s):

    #         (1)     U: {1, 2, 3},   V: {8, 7}
    #         (2)     U: {4, 5},      V: {8, 9, 10}
    #         (3)     U: {11, 6},     V: {9, 7}
    #         (4)     U: {12},        V: {10}

    # Covers all edges?: True
    # Average runtime over 5 evaluations:     0.0006251335144042969 s


    # Approximation on graph G(|V|=30, |E|=200) results in a set of 1 biclique cover(s):

    #         (1)     U: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},     V: {11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30}

    # Covers all edges?: True
    # Average runtime over 5 evaluations:     0.015773677825927736 s


    # Approximation on graph G(|V|=259, |E|=1203) results in a set of 33 biclique cover(s):

    #         (1)     U: {73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83},        V: {96, 97, 98, 99, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95}
    #         (2)     U: {213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223},     V: {224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239}
    #         (3)     U: {160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 158, 159},    V: {151, 152, 153, 154, 155, 156, 157}
    #         (4)     U: {192, 193, 194, 195, 196, 197, 198, 199, 200, 201},  V: {202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212}
    #         (5)     U: {12, 13, 14, 15, 16, 17, 18, 19, 20},        V: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
    #         (6)     U: {100, 101, 102, 103, 104, 105},      V: {106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119}
    #         (7)     U: {184, 185, 186, 187, 188, 189, 190, 191},    V: {174, 175, 176, 177, 178, 179, 180, 181, 182, 183}
    #         (8)     U: {46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56},        V: {39, 40, 41, 42, 43, 44, 45}
    #         (9)     U: {32, 33, 34, 35, 36, 37, 38, 27, 28, 29, 30, 31},    V: {21, 22, 23, 24, 25, 26}
    #         (10)    U: {140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150},     V: {134, 135, 136, 137, 138, 139}
    #         (11)    U: {64, 65, 66, 67, 68, 69, 70, 71, 72},        V: {57, 58, 59, 60, 61, 62, 63}
    #         (12)    U: {128, 129, 130, 131, 132, 133, 126, 127},    V: {120, 121, 122, 123, 124, 125}
    #         (13)    U: {258},       V: {186, 182}
    #         (14)    U: {21},        V: {248, 253}
    #         (15)    U: {244},       V: {107, 100}
    #         (16)    U: {122, 127},  V: {245}
    #         (17)    U: {231, 215},  V: {259}
    #         (18)    U: {157, 167},  V: {249}
    #         (19)    U: {188, 174},  V: {241}
    #         (20)    U: {247},       V: {9, 19}
    #         (21)    U: {254},       V: {130, 123}
    #         (22)    U: {101, 111},  V: {256}
    #         (23)    U: {255},       V: {194, 207}
    #         (24)    U: {246},       V: {115, 102}
    #         (25)    U: {243},       V: {88, 76}
    #         (26)    U: {187, 175},  V: {251}
    #         (27)    U: {211, 197},  V: {250}
    #         (28)    U: {5, 15},     V: {252}
    #         (29)    U: {242},       V: {41, 52}
    #         (30)    U: {193, 206},  V: {257}
    #         (31)    U: {129, 123},  V: {240}
    #         (32)    U: {33},        V: {248}
    #         (33)    U: {30},        V: {253}

    # Covers all edges?: True
    # Average runtime over 5 evaluations:     0.537295913696289 s


if __name__ == "__main__":
    main()
