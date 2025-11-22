import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from src.discrete import discrete_consensus_sim_complete
from src.continuous import continuous_consensus
from src.util import example_graph1, three_agents


def display(X0, x, steps):
    """
    Graphs the 2D consensus with a slider to see its progress over time.
    """
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 4)
    axfreq = fig.add_axes([0.2, 0.02, 0.65, 0.03])
    freq_slider = Slider(
        ax=axfreq,
        label='Step k',
        valmin=1,  # minimun value of range
        valmax=x.shape[0] - 1,  # maximum value of range
        valinit=steps,
        valstep=1.  # step between values
    )
    plt.title(f"2D formation based on discrete-time consensus, epsilon = {epsilon}")
    plt.xlabel("x")
    plt.ylabel("y")
    lines = ax.plot(x[:, :, 0], x[:, :, 1])
    ax.scatter(x[steps - 1, :, 0], x[steps - 1, :, 1], facecolors="none", edgecolors="r", linewidths=2)

    avg = np.average(X0, axis=0)
    ax.scatter(avg[0], avg[1])

    # The difference probably comes from numerical instability
    # or the fact that this is discrete time based
    print(f"Expected meetup point (exact average) : {avg}")
    print(f"Final state positions (after {steps} steps): {x[-1]}")
    ax.set_aspect('equal', adjustable='box')

    def update(val: float):
        """Callback function that is called when the slider is moved"""
        val = int(val)
        ax.clear()
        ax.plot(x[:val, :, 0], x[:val, :, 1])
        ax.scatter(x[val - 1, :, 0], x[val - 1, :, 1], facecolors="none", edgecolors="r", linewidths=2)
        ax.scatter(avg[0], avg[1])

    freq_slider.on_changed(update)
    plt.show()

if __name__ == "__main__":
    """
    Runs the consensus algorithm in 2D, the state of each agent is its (x, y)
    position on the graph.
    Can be run in discrete or consensus time, based on the commented version.
    Average position consensus is displayed with a red dot
    """
    # Define the graph used for consensus
    G = example_graph1()
    epsilon = 0.1

    # Initial state vector for each agent
    X0 = np.array([
        [-1.6, -1.1],
        [-1.2, -1.6],
        [-2, -2],
        [-2.1, -3.1],
        [-3, -1],
        [-1, -2]
    ])

    # Note : you can add offsets if you want to achieve formations

    # - Discrete time consensus
    steps = 50
    x = discrete_consensus_sim_complete(G, epsilon, X0, steps=steps)

    # - Continuous time consensus
    # t = np.arange(0, 8, 0.01)
    # steps = len(t)
    # x = continuous_consensus(G, X0, t, offsets=np.array([array([ 0.478125  , -0.00833333]), array([-0.23203125,  0.35416667]), array([-0.24609375, -0.34583333])]))

    display(X0, x, steps)
