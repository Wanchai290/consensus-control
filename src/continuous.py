import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

from src.util import example_graph1, three_agents

def continuous_consensus(G: nx.DiGraph, X0: np.ndarray, t: np.ndarray, offsets: np.ndarray = None):
    """
    Wrapper to use the consensus solver for a start vector X0 of any NxN dimension
    Parameters:
        - G: networkx DiGraph describing the N agents
        - X0: initial values vector
        - t: Sequence of time steps to solve at
        - (optional) offsets: Array of N offsets between agents
    """

    if offsets is not None:
        assert offsets.shape == X0.shape, "Offsets must have same shape as start vector"

    def consensus_solver(init_vec: np.ndarray, t: np.ndarray):
        """
        Solves the consensus problem for the given initial 1D vector,
        at time steps t
        :param init_vec: 1xN vector of initial values
        :param t: time steps to solve for
        """

        L = nx.laplacian_matrix(G).toarray()

        def model(x, t):
            if offsets is None:
                return np.dot(-L, x)
            else:
                return np.dot(-L, x) - offsets

        return np.array(odeint(model, init_vec, t))


    if len(X0.shape) == 1:
        sol = consensus_solver(X0, t)
        return sol
    else:
        sol = consensus_solver(X0[:, 0], t)

        # required shape : [Time, NumAgents, xi]
        sol = sol[:, :, np.newaxis]
        for i in range(1, X0.shape[1]):
            s = consensus_solver(X0[:, i], t)
            s = s[:, :, np.newaxis]
            sol = np.append(sol, s, axis=2)
        return sol


if __name__ == '__main__':
    G = three_agents()
    # nx.draw(G, with_labels=True)
    # plt.show()

    # Start vector for all nodes
    # X0 = np.array([5, 3, -1, 2, -6, 3])
    X0 = np.array([4, 1, -2])

    # Time steps to solve at
    t = np.arange(0, 8, 0.0001)

    # x = continuous_consensus(G, X0, t)
    x = continuous_consensus(G, X0, t, offsets=np.array([1, 1, -2]))

    plt.plot(t, x)
    plt.title("Continuous-time consensus with offsets")
    plt.xlabel("Time t")
    plt.ylabel("Agent value")
    plt.legend((1, 2, 3))
    plt.show()

