import networkx as nx
import numpy as np

from src.cbf import obstacles_except, zeroing_cbf
from src.discrete import discrete_consensus_step

if __name__ == '__main__':
    from ssl_traj.main import Controller
    G = nx.DiGraph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])

    # Reference: agent 0
    square = np.array([
        (1, 1), (1, -1), (-1, -1), (-1, 1)
    ])
    PID_P = 3.
    def formation_orders(teams_data):
        agents = [i for i in range(4)]
        agent_positions = np.array([teams_data["blue"][rob_id].pos for rob_id in agents])
        target_positions = discrete_consensus_step(G, epsilon=0.95, X0=agent_positions, offsets=square)
        target_speeds = PID_P * (target_positions - agent_positions)
        agent_obstacles = [obstacles_except(teams_data, rob_id, "blue") for rob_id in agents]

        solutions = [zeroing_cbf(agent_positions[rob_id], target_speeds[rob_id], 0.3, agent_obstacles[rob_id])
                        for rob_id in agents]
        final_speeds = [s['x'] for s in solutions]
        return {"blue": {rob_id: final_speeds[rob_id] for rob_id in agents}}

    grSimController = Controller()
    grSimController.run(duration=-1, velocity_orders=formation_orders)