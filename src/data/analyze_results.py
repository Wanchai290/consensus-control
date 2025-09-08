import numpy as np
from matplotlib import pyplot as plt


def achievement_progress_plot():
    data = np.load("line/achievement.npy")  # shape : (n steps, m , 1)
    # data = np.array([
    #     [0.3, 6, 2],
    #     [1.2, 3, 1],
    #     [1.6, 1, 0],
    # ])

    # reformat data to be on a scale from 0 to 100
    s = np.sum(data, axis=1)
    s = 100. * (np.max(s) - s) / (np.max(s))
    plt.figure(figsize=(9, 3))
    plt.tight_layout()
    plt.plot(s)
    plt.title(f"Global formation achievement progress | Maximum achievement : {np.max(s):.2f} %")
    plt.xlabel("Discrete time steps (k)")
    plt.ylabel("Progress (%)")
    plt.show()

if __name__ == '__main__':
    achievement_progress_plot()