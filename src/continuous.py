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


def continuous_consensus(G: nx.DiGraph, X0: np.ndarray, t: np.ndarray):
    L = nx.laplacian_matrix(G.reverse(copy=False)).toarray()

    def model(x, t):
        return np.dot(-L, x)

    # don't know how to fix this copy paste
    if len(X0.shape) == 1:
        sol = np.array(odeint(model, X0, t))
        return sol


    sol = np.array(odeint(model, X0[:, 0], t))
    # required shape : [Time, NumAgents, xi]
    sol = sol[:, :, np.newaxis]
    for i in range(1, X0.shape[1]):
        s = odeint(model, X0[:, i], t)
        s = s[:, :, np.newaxis]
        sol = np.append(sol, s, axis=2)
    return sol


if __name__ == '__main__':
    G = example_graph1()
    # nx.draw(G, with_labels=True)
    # plt.show()

    # Start vector for all nodes
    X0 = np.array([5, 3, -1, 2, -6, 3])

    # ODE solve
    t = np.arange(0, 8, 0.0001)

    x = continuous_consensus(G, X0, t)

    plt.plot(t, x)
    plt.show()

