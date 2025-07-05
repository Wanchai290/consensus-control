import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from util import example_graph1


def discrete_consensus(G: nx.DiGraph, epsilon: float, X0: np.ndarray, steps: int):

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
        last = P @ last
        x.append(last)

    return np.array(x)

if __name__ == '__main__':
    G = example_graph1()
    epsilon = 0.4
    X0 = np.array([-1, 2, 6, 3, -3, 1])
    steps = 10
    x = discrete_consensus(G, epsilon, X0, steps)

    # +1 for initial step
    plt.plot(range(steps + 1), x)
    plt.grid()
    plt.show()