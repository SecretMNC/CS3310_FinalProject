
from typing import Set, Dict, Iterator, Optional, Literal, Type
from src.graph import Graph



BipartiteSubset = Literal["U", "V"]

class BipartiteGraph(Graph):

    def __init__(self, U: Optional[Set[int]] = None, V: Optional[Set[int]] = None, *E : Graph.Edge) -> None:
        super().__init__()
        self._U : Set[int] = set() if (U is None) else U
        self._V = set() if (V is None) else V
        if len(self.U.intersection(self.V)) > 0:
            raise ValueError("U and V are not independent")
        self._E : Dict[int, Set["Graph.Edge"]] = {v: set() for v in {*self.U, *self.V}}
        if len(E) > 0:
            try:
                self.add_edge(*E)
            except ValueError as e:
                if e == "Edge does not connect vertices from U and V":
                    raise ValueError("Input graph is not bipartite")
                raise ValueError(e)

    @property
    def U(self):
        return self._U
    
    @property
    def n(self) -> int:
        return len(self.U) + len(self.V)
    
    @property
    def balanced(self) -> bool:
        return len(self.U) == len(self.V)
    
    @property
    def complete(self) -> bool:
        if (len(self.U) * len(self.V)) != self.m:
            return False
        return all(self.adjacent(u) == self.V for u in self.U)
    
    def add_vertex(self, v1 : int, *V: int, subset : BipartiteSubset = "U") -> "BipartiteGraph":
        if subset not in ("U", "V"):
            raise ValueError("Invalid bipartite subset specification")
        add_set = self._U if (subset == "U") else self._V
        for v in (v1, *V):
            if v not in {*self.vertices()}:
                add_set.add(v)
                self._E[v] = set()
        return self

    def remove_vertex(self, v : int) -> None:
        if v in self.V:
            remove_set = self._V
        elif v in self.U:
            remove_set = self._U
        else:
            return
        remove_set.remove(v)
        E = self._E[v]
        for e in E:
            del self._C[e]
        del self._E[v]
        remove_dict = {}
        for u, E_u in self._E.items():
            remove_dict[u] = []
            for e_u in E_u:
                if v in e_u:
                    remove_dict[u].append(e_u)
                    if e_u in self._C:
                        del self._C[e_u]
        for u, remove_list in remove_dict.items():
            for e in remove_list:
                self._E[u].remove(e)
    
    def add_edge(self, e1 : Graph.Edge, *E: Graph.Edge) -> "BipartiteGraph":
        for e in (e1, *E):
            if not all(map(lambda S: len(S.intersection({*e.vertices()})) == 1, (self.U, self.V))):
                raise ValueError("Edge does not connect vertices from U and V")
            if e in self.C:
                raise ValueError("Edge already exists")
            self._C[e] = e.w
            for u in e.outgoing():
                self._E[u].add(e)
        return self

    def star(self, v : int) -> "BipartiteGraph":
        G = BipartiteGraph(U={v})
        for e in self.E[v]:
            G.add_vertex(*e.vertices(), subset="V")
            G.add_edge(e)
        return G
    
    def copy(self) -> "BipartiteGraph":
        return BipartiteGraph(self.U.copy(), self.V.copy(), *map(lambda e: e.copy(), self.C.keys()))
    
    def vertices(self) -> Iterator[int]:
        yield from self.U
        yield from self.V

    def to_general_graph(self) -> "Graph":
        return Graph(self.U.copy().union(self.V.copy()), *map(lambda e: e.copy(), self.C.keys()))

    # @staticmethod
    # def from_file(file_name : str, edge_type : Type["Graph.Edge"]) -> "BipartiteGraph":
    #     if not issubclass(edge_type, Graph.Edge):
    #         raise TypeError("edge_type is not a valid Edge type")
    #     G = BipartiteGraph()
    #     with open(f"{file_name}.txt", "r") as f:
    #         for line in map(lambda x: tuple(map(int, x.strip().split())), f.readlines()):
    #             G.add_vertex(*line[:2])
    #             G.add_edge(edge_type(*line))
    #     return G

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, BipartiteGraph):
            return (((self.V == obj.V) and (self.U == obj.U)) or ((self.V == obj.U) and (self.U == obj.V))) and (set(self.C.keys()) == set(obj.C.keys()))
        if isinstance(obj, Graph):
            return self.to_general_graph() == obj
        return False



class CompleteBipartiteGraph(BipartiteGraph):

    def __init__(self, U: Optional[Set[int]] = None, V: Optional[Set[int]] = None) -> None:
        super().__init__(U)
        this_V = set() if (V is None) else V
        if len(this_V) > 0:
            self.add_vertex(*this_V, subset="V")
    
    @property
    def complete(self) -> bool:
        return True
    
    def add_vertex(self, v1: int, *V: int, subset: BipartiteSubset = "U") -> "CompleteBipartiteGraph":
        if subset not in ("U", "V"):
            raise ValueError("Invalid bipartite subset specification")
        add_set, other_set = (self._U, self._V) if (subset == "U") else (self._V, self._U)
        for v in (v1, *V):
            if v not in {*self.vertices()}:
                add_set.add(v)
                self._E[v] = set()
                for w in other_set:
                    e = Graph.Edge(v, w)
                    self._E[w].add(e)
                    self._E[v].add(e)
                    self._C[e] = e.w
        return self

    # def add_edge(self, e1 : Graph.Edge, *E: Graph.Edge) -> "CompleteBipartiteGraph":
    #     for e in (e1, *E):
    #         pass
    
    def star(self, v : int) -> "CompleteBipartiteGraph":
        G = CompleteBipartiteGraph(U={v})
        for e in self.E[v]:
            G.add_vertex(*e.vertices(), subset="V")
        return G

    def copy(self) -> "CompleteBipartiteGraph":
        G = CompleteBipartiteGraph(self.U.copy(), self.V.copy())
        for e in self.C.keys():
            if isinstance(e, Graph.DirectedEdge) or (e.w is not None):
                G.add_edge(e.copy())
        return G

    @staticmethod
    def from_file(file_name : str, edge_type : Type["Graph.Edge"]) -> "Graph":
        with open(f"{file_name}.txt", "r") as f:
            U = set(map(int, f.readline().strip().split()))
            V = set(map(int, f.readline().strip().split()))
            return CompleteBipartiteGraph(U, V)

