import networkx as nx

def example_graph1():
    # balanced example graph
    G = nx.DiGraph()
    G.add_nodes_from(range(1, 6))
    G.add_edges_from([
        (1, 4), (4, 3), (3, 2), (2, 1),
        (2, 6), (6, 5), (5, 2)
    ])
    return G

def three_agents():
    G = nx.DiGraph()
    G.add_nodes_from(range(1, 3))
    G.add_edges_from([
        (1, 2), (2, 3), (3, 1)
    ])
    return G