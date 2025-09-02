from log import logger

# -- Node creation and handling
class Node:
    def __init__(self, id):
        self.id = id
        self.coords = None
        """(x, y) coordinates of the node on the screen"""
        self.neighbours = []
        self.is_moving = False
        """Whether the node is currently being moved by the user"""

nodes: dict[int, Node] = {}
"""Associates an integer to a node"""

def create_node():
    """Creates a new node using the latest available integer"""
    n = Node(len(nodes))
    nodes[n.id] = n
    return n

def delete_node(node):
    """Deletes node from the list of nodes displayed"""
    logger.info(f"Deleting node {node.id} with neighbours {node.neighbours}")
    for other_id in nodes.keys():
        if other_id == node.id:
            continue
        other = get_node(other_id)
        if node.id in other.neighbours:
            other.neighbours.remove(node.id)
    nodes.pop(node.id)

def are_linked(src, friend):
    """Returns True if there exists a directed arc from `src` to `friend`"""
    return friend.id in src.neighbours

def link(src, friend):
    """Creates a directed arc from `src` to `friend`"""
    src.neighbours.append(friend.id)
    logger.info(f"Linking {src.id} to {friend.id}")

def unlink(src, friend):
    """Removes the directed arc from `src` to `friend`"""
    src.neighbours.remove(friend.id)
    logger.info(f"{src.id} unlinked from {friend.id}")

def get_node(node_id):
    """Retrieve node with the given id"""
    return nodes[node_id]