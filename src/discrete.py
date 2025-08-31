import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from src.util import example_graph1, three_agents, max_in_degree


def discrete_consensus_cfunc(G: nx.DiGraph, epsilon: float, X0: np.ndarray, offsets: np.ndarray = None,
                             common_drift: np.ndarray = np.array(0.)):
    """
    Similar to discrete_consensus_step(), except it returns the control function to apply instead to the states
    Pre-requisites:
        The value of node i in graph G should be X0[i] (i.e. start node ordering at 0).
        Same for offsets array.
    Args: See discrete_consensus_step()
        common_drift: Used to move all agents in a certain direction
    Returns:
        Control function of shape X0 to apply to all agents (
    """
    u_k = np.zeros(X0.shape)
    for node in G.nodes():
        s = 0
        for neighbour in G.neighbors(node):
            s += X0[neighbour] - X0[node]
            if offsets is not None:
                s += offsets[node]
        u_k[node] = epsilon * (s + common_drift)
    return u_k

def discrete_consensus_step(G: nx.DiGraph, epsilon: float, X0: np.ndarray, offsets: np.ndarray = None):
    """
    Performs one iteration of the discrete consensus algorithm.
    Parameters:
        - G: Graph to consider for the agents
        - epsilon: Step size. The maximum degree (delta) times epsilon should be inferior to 1
        - X0: Reference step
        - (Optional): Relative offsets to apply between the agents
    Returns:
        The next state vector x[k+1] of all agents i.
    """
    if offsets is not None:
        assert offsets.shape == X0.shape, (
            "Offsets must have same shape as start vector. "
            f"Different shapes detected : (offsets) {offsets.shape} != {X0.shape} (X0)")
        offset_addon = lambda: offsets
    else:
        offset_addon = lambda: 0

    L = nx.laplacian_matrix(G).toarray()

    # Discrete-time version
    d = max_in_degree(G)
    if not epsilon * d < 1:
        raise ValueError("epsilon * delta value superior to 1, change epsilon")
    # print(f"Epsilon = {epsilon} | Max in-degree = {d}")

    # Perron matrix version
    P = np.identity(L.shape[0]) - epsilon * L

    x_next = P @ X0 + epsilon * offset_addon()
    return np.array(x_next)

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
        # Perron matrix version
        last = discrete_consensus_step(G, epsilon, last, offsets)
        x.append(last)

        # Control function version
        # ctrl = discrete_consensus_cfunc(G, epsilon, last, offsets)
        # x.append(last + ctrl)
        # last = x[-1]
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