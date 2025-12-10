
from typing import Set, Dict, Tuple, Iterator, Optional, Type, Union
from itertools import repeat



class Graph:


    class Edge:
        
        def __init__(self, u : int, v : int, w : Optional[int] = None) -> None:
            self._vertices : Set[int] = {u, v}
            self._weight : Optional[int] = w
        
        @property
        def w(self) -> Optional[int]:
            return self._weight
        
        def __eq__(self, edge: object) -> bool:
            if isinstance(edge, Graph.Edge):
                return (self._vertices == edge._vertices) and (self.w == edge.w)
            if isinstance(edge, set):
                return (not (self._vertices - edge)) and (self.w is None)
            raise TypeError(f"Equality is not defined between Edge and {type(edge).__name__}")

        def __hash__(self) -> int:
            return hash((frozenset(self._vertices), self.w))
        
        def __contains__(self, v : int):
            return v in self._vertices
        
        def outgoing(self) -> Iterator[int]:
            yield from self._vertices
        
        def incoming(self) -> Iterator[int]:
            yield from self._vertices
        
        def vertices(self) -> Iterator[int]:
            if len(self._vertices) == 1:
                yield from repeat(next(iter(self._vertices)), times=2)
            else:
                yield from self._vertices
        
        def copy(self) -> "Graph.Edge":
            return Graph.Edge(*self.vertices(), self.w)
    

    class DirectedEdge(Edge):

        def __init__(self, u: int, v: int, w: Optional[int] = None) -> None:
            if u == v:
                raise ValueError("A directed edge cannot self-loop")
            super().__init__(u, v, w)
            self._direction : Tuple[int, int] = (u, v)
        
        def __eq__(self, edge: object) -> bool:
            if isinstance(edge, Graph.DirectedEdge):
                return (self._direction == edge._direction) and (self.w == edge.w)
            if isinstance(edge, tuple):
                return (self._direction == edge) and (self.w is None)
            if isinstance(edge, Graph.Edge):
                raise TypeError("Equality is not defined between DirectedEdge and Edge (undirected)")
            raise TypeError(f"Equality is not defined between DirectedEdge and {type(edge).__name__}")
        
        def __hash__(self) -> int:
            return hash((self._direction, self.w))
        
        def outgoing(self) -> Iterator[int]:
            yield self._direction[0]
        
        def incoming(self) -> Iterator[int]:
            yield self._direction[1]
        
        def vertices(self) -> Iterator[int]:
            yield from self._vertices
        
        def copy(self) -> "Graph.DirectedEdge":
            return Graph.DirectedEdge(*self._direction, self.w)


    def __init__(self, V : Optional[Set[int]] = None, *E : "Graph.Edge") -> None:
        self._V : Set[int] = set() if (V is None) else V
        self._E : Dict[int, Set["Graph.Edge"]] = {v: set() for v in self._V}
        self._C : Dict["Graph.Edge", Optional[int]] = {}
        if len(E) > 0:
            self.add_edge(*E)
    
    @property
    def V(self) -> Set[int]:
        return self._V
    
    @property
    def E(self) -> Dict[int, Set["Graph.Edge"]]:
        return self._E
    
    @property
    def C(self) -> Dict["Graph.Edge", Optional[int]]:
        return self._C

    @property
    def n(self) -> int:
        return len(self.V)
    
    @property
    def m(self) -> int:
        return len(self.C.keys())
    
    @property
    def total_cost(self) -> int:
        return sum(filter(None, self.C.values()))
    
    def add_vertex(self, v1 : int, *V : int) -> "Graph":
        for v in (v1, *V):
            if v not in self.V:
                self.V.add(v)
                self._E[v] = set()
        return self
    
    def remove_vertex(self, v : int) -> None:
        if v in self.V:
            self._V.remove(v)
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
    
    def add_edge(self, e1 : "Graph.Edge", *E : "Graph.Edge") -> "Graph":
        for e in (e1, *E):
            if self.V.intersection(e.vertices()) != {*e.vertices()}:
                raise KeyError("Edge vertex (or vertices) not found")
            if e in self.C:
                raise ValueError("Edge already exists")
            self._C[e] = e.w
            for u in e.outgoing():
                self._E[u].add(e)
        return self
    
    def adjacent(self, v : int) -> Set[int]:
        return {w for e in self.E[v] for w in e.incoming()} - {v}
    
    def star(self, v : int) -> "Graph":
        G = Graph({v})
        for e in self.E[v]:
            G.add_vertex(*e.vertices())
            G.add_edge(e)
        return G
    
    def copy(self) -> "Graph":
        return Graph(self.V.copy(), *map(lambda e: e.copy(), self.C.keys()))
    
    def vertices(self) -> Iterator[int]:
        yield from self.V

    def union(self, G1 : "Graph", *G2: "Graph") -> "Graph":
        G = self.to_general_graph()
        for g in map(lambda gi: gi.to_general_graph(), (G1, *G2)):
            if g.n > 0:
                G.add_vertex(*g.V)
            for e in g.C.keys():
                if e not in G.C:
                    G.add_edge(e)
        return G
    
    def to_general_graph(self) -> "Graph":
        return self.copy()

    @staticmethod
    def from_file(file_name : str, edge_type : Type["Graph.Edge"]) -> "Graph":
        if not issubclass(edge_type, Graph.Edge):
            raise TypeError("edge_type is not a valid Edge type")
        G = Graph()
        with open(f"{file_name}.txt", "r") as f:
            for line in map(lambda x: tuple(map(int, x.strip().split())), f.readlines()):
                G.add_vertex(*line[:2])
                G.add_edge(edge_type(*line))
        return G
    
    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Graph):
            return (self.V == obj.V) and (set(self.C.keys()) == set(obj.C.keys()))
        return False
    
    def __contains__(self, item : Union[int, "Graph.Edge"]):
        if isinstance(item, int):
            return item in self.vertices()
        if isinstance(item, Graph.Edge):
            return item in self.C.keys()
        raise TypeError("Graph membership is only defined for vertices and edges")
    
    def __repr__(self) -> str:
        return ", ".join([f"{v}: {str(self.adjacent(v))}" for v in self.vertices()])

