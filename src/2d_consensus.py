import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from discrete import example_graph1, discrete_consensus

if __name__ == "__main__":
    G = example_graph1()
    epsilon = 0.1
    X0 = np.array([
        [-1.6, -1.1],
        [-1.2, -1.6],
        [-2, -2],
        [-2.1, -3.1],
        [-3, -1],
        [-1, -2]
    ])

    steps = 50
    x = discrete_consensus(G, epsilon, X0, steps)

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    axfreq = fig.add_axes([0.2, 0.02, 0.65, 0.03])
    freq_slider = Slider(
        ax=axfreq,
        label='Step k',
        valmin=1,  # minimun value of range
        valmax=x.shape[0] - 1,  # maximum value of range
        valinit=steps,
        valstep=1.  # step between values
    )

    lines = ax.plot(x[:, :, 0], x[:, :, 1])
    ax.scatter(x[steps - 1, :, 0], x[steps - 1, :, 1], facecolors="none", edgecolors="r", linewidths=2)


    def update(val: float):
        val = int(val)
        ax.clear()
        ax.plot(x[:val, :, 0], x[:val, :, 1])
        ax.scatter(x[val - 1, :, 0], x[val - 1, :, 1], facecolors="none", edgecolors="r", linewidths=2)

    freq_slider.on_changed(update)
    plt.show()
