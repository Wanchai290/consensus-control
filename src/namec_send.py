import time

from cbf import zeroing_cbf, Obstacle
import zmq
import json
import numpy as np

"""JSON request format to this solver server
{
    "obstacles": [
        [0., 0.],
        ...
    ],
    "rob_pos": [0., 0.],
    "alpha": 0.,
    "v_nom": [0., 0.]
}
"""
if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    OBS_PENALTY_POSITIVE = [Obstacle(xy=np.array([4., 0.5]), r=0.67), Obstacle(xy=np.array([4., -0.5]), r=0.72)]
    OBS_PENALTY_NEGATIVE = [Obstacle(xy=np.array([-4., 0.5]), r=0.67), Obstacle(xy=np.array([-4., -0.5]), r=0.72)]
    
    # LA CONSTANTE DE LA MORT
    our_team_on_positive = False

    while True:
        print("wait for msg")
        message = socket.recv()
        print("msg received")
        data = json.loads(message)
        rob_pos = data["rob_pos"]
        v_nom = np.array(data["v_nom"])
        t_start = time.time()
        try:
            alpha = data["alpha"]
            obstacles = list(map(lambda obs: Obstacle(xy=np.array(obs), r=0.25), data["obstacles"]))
            if our_team_on_positive:
                obstacles.extend(OBS_PENALTY_NEGATIVE)
            else:
                obstacles.extend(OBS_PENALTY_POSITIVE)
            sol = zeroing_cbf(rob_pos, v_nom, alpha, obstacles)
        except (ValueError, IndexError) as e:
            print(e)
            sol = {'x': v_nom}
        print("Solver compute time : ", (time.time() - t_start) * 1000.)
        optimal_v = list(sol['x'])
        socket.send_json({"optimal_v": optimal_v})
