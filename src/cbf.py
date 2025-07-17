import numpy as np
from cvxopt import matrix, solvers
from collections import namedtuple

Obstacle = namedtuple('Obstacle', ['xy', 'r'])

def zeroing_cbf(p: np.ndarray, v_nom: np.ndarray, alpha: float,
                obstacles: list[Obstacle]):
    """
    Zeroing CBF for robot at position `p` and with velocity `v_nom` originally applied.
    All obstacles will have the same `alpha` parameter applied
    """
    if alpha <= 0.:
        raise ValueError("alpha must be > 0.")

    # CBF solve
    ## Objective function
    P = matrix(2 * np.identity(2))
    q = matrix(-2 * v_nom)

    ## Constraints
    def gen_obstacle(obs: Obstacle):
        D = obs.r
        return (alpha / 2.) * (np.linalg.norm(p - obs.xy) ** 2 - D ** 2)

    s = np.array(obstacles[0].xy - p)
    for i in range(1, len(obstacles)):
        s = np.append(s, [[0, 1]] - p, axis=0)
    G = matrix(s)
    h = matrix([
        gen_obstacle(o) for o in obstacles
    ])

    return solvers.qp(P, q, G, h, options={'show_progress': False})


if __name__ == '__main__':
    print(__import__(__name__.split('.')[0]))
    from ssl_traj.main import Controller
    grSimController = Controller()

    target = np.array([1, 1])
    obs = [
        Obstacle(xy=np.array([[0., 0.]]), r=0.1),
        Obstacle(xy=np.array([[0., 1.]]), r=0.1)
    ]
    def orders(teams_data):
        blue0 = teams_data["blue"][0]
        blue0_pos = blue0.pos
        cmd = target - blue0_pos
        sol = zeroing_cbf(blue0_pos, cmd, alpha=4, obstacles=obs)
        print(f"Offset : {np.linalg.norm(sol['x'] - matrix(cmd)) ** 2}")
        return {"blue": {0: sol["x"]}}

    grSimController.run(
        duration=-1,
        velocity_orders=orders
    )
