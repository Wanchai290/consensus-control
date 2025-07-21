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

    s = np.array([obstacles[0].xy - p])
    for i in range(1, len(obstacles)):
        s = np.append(s, [obstacles[i].xy - p], axis=0)
    G = matrix(s)
    h = matrix([
        gen_obstacle(o) for o in obstacles
    ])

    return solvers.qp(P, q, G, h, options={'show_progress': False})


def obstacles_except(teams_data, robot_id: int, robot_team: str):
    """
    Create obstacles to avoid all robots except `robot_id` in `robot_team`.
    Used to control an agent robot with CBF.
    """
    # nifty hack
    # iterate over all robot positions, except robot blue 0
    return [Obstacle(teams_data[team][i].pos, r=0.3)
           for team in teams_data.keys()  # foreach team
           for i in teams_data[team]  # for each robot id
           if i != robot_id or team != robot_team  # but not robot blue 0
           and teams_data[team][i] is not None]

if __name__ == '__main__':
    from ssl_traj.main import Controller
    grSimController = Controller()

    target = np.array([1, 1])
    # obs = [
    #     Obstacle(xy=np.array([[0., 0.]]), r=0.1),
    #     Obstacle(xy=np.array([[0., 1.]]), r=0.1)
    # ]
    def order_single(teams_data):
        obs = obstacles_except(teams_data, 0, robot_team="blue")
        blue0 = teams_data["blue"][0]
        blue0_pos = blue0.pos
        cmd = target - blue0_pos
        sol = zeroing_cbf(blue0_pos, cmd, alpha=9, obstacles=obs)
        print(f"Offset : {np.linalg.norm(sol['x'] - matrix(cmd)) ** 2}")
        return {"blue": {0: sol["x"]}}

    grSimController.run(
        duration=-1,
        velocity_orders=order_single
    )
