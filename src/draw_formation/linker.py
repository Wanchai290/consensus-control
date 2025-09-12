from src.draw_formation import node_handler
from log import logger

_saved = None

def set_highlighted(node):
    global _saved
    if _saved is None:
        _saved = node
    else:
        logger.info(f"{_saved.id} and {node.id} | {node_handler.are_linked(_saved, node)}")
        if _saved.id == node.id:
            _saved = None
        # link or unlink operation
        elif node_handler.are_linked(_saved, node):
            node_handler.unlink(_saved, node)
        else:
            node_handler.link(_saved, node)
        _saved = None

def get_highlighted():
    global _saved
    return _saved
