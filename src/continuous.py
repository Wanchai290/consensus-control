import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def example_graph1():
    G = nx.DiGraph()
    G.add_nodes_from(range(1, 6))
    G.add_edges_from([
        (1, 4), (4, 3), (3, 2), (2, 1), (2, 4),
        (2, 6), (6, 5), (5, 2)
    ])
    return G

G = example_graph1()
# nx.draw(G, with_labels=True)
# plt.show()

L = nx.laplacian_matrix(G.reverse(copy=False)).toarray()

# Start vector for all nodes
X0 = [5, 3, -1, 2, -6, 3]

# ODE solve
t = np.arange(0, 8, 0.0001)

def model(x, t):
    return np.dot(-L, x)

x = odeint(model, X0, t)
plt.plot(t, x)
plt.show()

