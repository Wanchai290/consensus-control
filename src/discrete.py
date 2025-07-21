import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from util import example_graph1, three_agents


def discrete_consensus_step(G: nx.DiGraph, epsilon: float, X0: np.ndarray, offsets: np.ndarray = None):
    """
    Performs one iteration of the discrete consensus algorithm
    Parameters:
        - G: Graph to consider for the agents
        - epsilon: Step size. The maximum degree (delta) times epsilon should be inferior to 1
        - X0: Reference step
        - (Optional): Relative offsets to apply between the agents
    """
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

    # Perron matrix version
    P = np.identity(L.shape[0]) - epsilon * L
    step_x = P @ X0 + epsilon * offset_addon()
    return np.array(step_x)

def discrete_consensus_sim_complete(G: nx.DiGraph, epsilon: float, X0: np.ndarray, offsets: np.ndarray = None, steps: int = 10):
    """
    Simulates n steps of the discrete consensus algorithm.
    Parameters:
        See discrete_consensus_step() function
        - steps: Number of steps to perform
    """
    x = [X0]
    last = X0
    for _ in range(steps):
        last = discrete_consensus_step(G, epsilon, last, offsets)
        x.append(last)
    return np.array(x)

if __name__ == '__main__':
    G = three_agents()
    epsilon = 0.4
    # X0 = np.array([-1, 2, 6, 3, -3, 1])
    X0 = np.array([4, 1, -2])
    steps = 10

    # Reference point : agent 1 -> coordinate (0) (it's the new basis in some way)
    # Offsets explanation:
    # - Agent 0: -1 (from 0 to 1)
    # - Agent 1: -1 (from 1 to 2)
    # - Agent 2: 2 (from 2 to 0)
    offsets = np.array([-1, -1, 2])

    x = discrete_consensus_sim_complete(G, epsilon, X0, offsets=offsets, steps=steps)

    # +1 for initial step
    plt.plot(range(steps + 1), x)
    plt.grid()
    plt.show()