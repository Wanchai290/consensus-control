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
    """Wrapper to use the consensus solver for a start vector X0 of any NxN dimension"""

    def consensus_solver(init_vec: np.ndarray, t: np.ndarray):
        """
        Solves the consensus problem for the given initial 1D vector,
        at time steps t
        :param init_vec: 1xN vector of initial values
        :param t: time steps to solve for
        """
        L = nx.laplacian_matrix(G.reverse(copy=False)).toarray()

        def model(x, t):
            return np.dot(-L, x)

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
    G = example_graph1()
    # nx.draw(G, with_labels=True)
    # plt.show()

    # Start vector for all nodes
    X0 = np.array([5, 3, -1, 2, -6, 3])

    # Time steps to solve at
    t = np.arange(0, 8, 0.0001)

    x = continuous_consensus(G, X0, t)

    plt.plot(t, x)
    plt.show()

