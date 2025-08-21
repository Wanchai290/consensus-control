import typing

import networkx as nx
import numpy as np
from pynput import keyboard
from threading import Lock

from cbf import obstacles_except, zeroing_cbf
from discrete import discrete_consensus_step, discrete_consensus_cfunc

if __name__ == '__main__':
    """
    Program used for testing the discrete consensus controller
    with the grSim simulator (must be installed separately).
    The formation can be controlled using the keys ZQSD.
    """
    from ssl_traj.main import Controller
    G = nx.DiGraph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])

    # Reference: agent 0
    square = np.array([
        (1, 1), (1, -1), (-1, -1), (-1, 1)
    ])

    def register_keyboard_listener() -> typing.Callable[[], np.array]:
        """
        Registers a global keyboard listener.
        It has been written this way to encapsulate all values required for
        the listener to work, so that they are not part of the simulation code.
        Thus, all variables required for the listener are in the lexical scope of this function.
        Returning a function that has access to this lexical scope allows for proper encapsulation.

        It also helps the developer not think about acquiring and releasing the lock properly
        to access the drift value.

        Returns:
            A function that returns the current drift value to apply
        """
        drift = 0.
        w_lock = Lock()

        def on_press(key):
            nonlocal drift, w_lock
            d = np.zeros(2)
            try:
                if key.char == 'z':
                    d += np.array([0., 0.5])
                if key.char == 'q':
                    d += np.array([-0.5, 0.])
                if key.char == 's':
                    d += np.array([0., -0.5])
                if key.char == 'd':
                    d += np.array([0.5, 0.])
                return d
            except AttributeError:
                # Special key pressed, just ignore
                d = np.zeros(2)

            # Update drift value
            w_lock.acquire()
            drift = d
            w_lock.release()


        def on_release(_):
            nonlocal drift
            drift = np.zeros(2)

        # Register keyboard listener
        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        listener.start()

        def get_drift():
            w_lock.acquire()
            d = drift
            w_lock.release()
            return np.array(d)

        return get_drift


    get_drift_value = register_keyboard_listener()

    def formation_orders(teams_data):
        agents = [i for i in range(4)]
        agent_positions = np.array([teams_data["blue"][rob_id].pos for rob_id in agents])

        # -- Using Perron matrix version of discrete consensus
        # PID_P = 3.
        # target_positions = discrete_consensus_step(G, epsilon=0.95, X0=agent_positions, offsets=square)
        # target_speeds = PID_P * (target_positions - agent_positions)

        # -- By directly getting the speed vectors to apply
        drift_value = get_drift_value()
        target_speeds = discrete_consensus_cfunc(G, epsilon=0.95, X0=agent_positions, offsets=square, common_drift=drift_value)

        # Define the list of obstacles as being all other robots, except itself
        agent_obstacles = [obstacles_except(teams_data, rob_id, "blue") for rob_id in agents]

        # Solve QP to get adapted speeds for each robot
        solutions = [zeroing_cbf(agent_positions[rob_id], target_speeds[rob_id], 0.3, agent_obstacles[rob_id])
                        for rob_id in agents]
        final_speeds = [s['x'] for s in solutions] # retrieve speed values
        return {"blue": {rob_id: final_speeds[rob_id] for rob_id in agents}}

    grSimController = Controller()
    grSimController.run(duration=-1, velocity_orders=formation_orders)