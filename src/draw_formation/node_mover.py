from src.draw_formation.node_handler import Node

_moving = None

def start_moving(node: Node):
    global _moving
    _moving = node
    _moving.is_moving = True

def stop_moving(mouse_pos: tuple[int, int]):
    global _moving
    if _moving is not None:
        _moving.coords = mouse_pos
        _moving.is_moving = False
        _moving = None