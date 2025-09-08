from matplotlib import pyplot as plt

if __name__ == "__main__":
    import numpy as np
    data = np.load("line/real_results.npy")
    colors = ['burlywood', 'salmon', 'dodgerblue']
    legend_final = False
    for i in range(data.shape[1]):
        plt.plot(data[:, i, 0], data[:, i, 1], c=colors[i])
        plt.scatter(data[0, i, 0], data[0, i, 1], c=colors[i])
        if not legend_final:
            plt.scatter(data[-1, i, 0], data[-1, i, 1], marker="x", c='r', s=65, label="Final position")
            legend_final = True
        else:
            plt.scatter(data[-1, i, 0], data[-1, i, 1], marker="x", c='r', s=65)

    plt.xlabel("x coordinate")
    plt.ylabel("z altitude")
    plt.legend()
    plt.title("Trajectories of the drones during consensus")
    plt.show()