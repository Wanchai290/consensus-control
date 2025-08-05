import networkx as nx

def example_graph1():
    # balanced example graph
    G = nx.DiGraph()
    G.add_nodes_from(range(6))
    G.add_edges_from([
        (0, 3), (3, 2), (2, 1), (1, 0),
        (1, 5), (5, 4), (4, 1)
    ])
    return G

def three_agents():
    G = nx.DiGraph()
    G.add_nodes_from(range(3))
    G.add_edges_from([
        (0, 1), (1, 2), (2, 0)
    ])
    return G

def max_in_degree(G: nx.DiGraph):
    # G.in_degree has tuple (id, in_degree)
    # retrieve maximum in_degree value at index 1
    return max(G.in_degree, key=lambda s: s[1])[1]
