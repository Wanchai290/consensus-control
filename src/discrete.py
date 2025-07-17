import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from util import example_graph1, three_agents


def discrete_consensus(G: nx.DiGraph, epsilon: float, X0: np.ndarray, steps: int, offsets: np.ndarray = None):
    if offsets is not None:
        assert offsets.shape == X0.shape, "Offsets must have same shape as start vector"
        offset_addon = lambda: offsets
    else:
        offset_addon = lambda: 0

    def max_in_degree(G: nx.DiGraph):
        # G.in_degree has tuple (id, in_degree)
        # retrieve maximum in_degree value at index 1
        return max(G.in_degree, key=lambda s: s[1])[1]

    # we want in-degree Laplacian matrix. docs say to use G.reverse() to get it
    L = nx.laplacian_matrix(G.reverse(copy=False)).toarray()

    # Discrete-time version
    d = max_in_degree(G)
    if not epsilon * d < 1:
        raise ValueError("epsilon * delta value superior to 1, change epsilon")
    print(f"Epsilon = {epsilon} | Max in-degree = {d}")
    x = [X0]

    # Perron matrix version
    P = np.identity(L.shape[0]) - epsilon * L
    last = X0
    for _ in range(steps):
        last = P @ last + epsilon * offset_addon()
        x.append(last)

    return np.array(x)

if __name__ == '__main__':
    G = three_agents()
    epsilon = 0.4
    # X0 = np.array([-1, 2, 6, 3, -3, 1])
    X0 = np.array([4, 1, -2])
    steps = 10
    x = discrete_consensus(G, epsilon, X0, steps, np.array([-1, -1, 2]))

    # +1 for initial step
    plt.plot(range(steps + 1), x)
    plt.grid()
    plt.show()