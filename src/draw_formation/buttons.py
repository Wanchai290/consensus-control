import threading
import typing

import numpy as np
import pygame

from src.draw_formation import node_handler
from src.draw_formation.drawer import SCREEN_SIZE
BUTTONS_Y_TOP = 650.

def offsets_access():
    """Ensures thread-safe access to the computed offsets variable,
    so that a developer might not try to access it directly."""

    calculated_offsets: list[tuple[int, int]] = []
    """Offsets computed for the current drawing"""
    co_lock = threading.Lock()

    def setter(new):
        nonlocal calculated_offsets
        co_lock.acquire()
        calculated_offsets = new
        co_lock.release()
        print(new)

    def getter():
        nonlocal calculated_offsets
        co_lock.acquire()
        val = calculated_offsets
        co_lock.release()
        return val

    return getter, setter

get_offsets, set_offsets = offsets_access()


def in_box_generator(draw_box) -> typing.Callable[[float, float], bool]:
    return lambda x,y: (draw_box[0] <= x <= draw_box[0] + draw_box[2]
                        and draw_box[1] <= y <= draw_box[1] + draw_box[3])

WORLD_MAX_X = 4.5
WORLD_MAX_Y = 3.

def convert_pygame_to_world(pg_coords):
    """
    Ratio converter that translates screen coordinates to the coordinates
    used in the Ibuki laboratory's experiment zone.

    Screen coordinates start from the top-left, then go down and to the right.
    Ibuki laboratory's zone start from the center, then go up and to the right.

    The origin difference is transformed by applying an offset of the screen's size divided by 2.
    Difference in direction is transformed by just flipping the sign.

    No need to flip y coordinate because distance vectors are relative.
    """
    x, y = pg_coords
    x = x - SCREEN_SIZE[0] / 2.  # offset to allow negative coordinates
    x = x * (WORLD_MAX_X / SCREEN_SIZE[0])  # ratio down coordinate

    y = y - SCREEN_SIZE[1] / 2.
    y = y * (WORLD_MAX_Y / SCREEN_SIZE[1])
    return x, y

CLEAR_BUTTON_CDS = (
    10,
    BUTTONS_Y_TOP,
    SCREEN_SIZE[0] / 3. - 40,
    SCREEN_SIZE[1] - BUTTONS_Y_TOP - 10
)
UPDATE_BUTTON_CDS = (
    20 + SCREEN_SIZE[0] / 3. - 40,
    BUTTONS_Y_TOP,
    SCREEN_SIZE[0] / 3.,
    SCREEN_SIZE[1] - BUTTONS_Y_TOP - 10
)
REMOVE_ALL_LINKS_BUTTON_CDS = (
    30 + 2 * SCREEN_SIZE[0] / 3. - 40,
    BUTTONS_Y_TOP,
    SCREEN_SIZE[0] / 3.,
    SCREEN_SIZE[1] - BUTTONS_Y_TOP - 10
)

clear_button_clicked = in_box_generator(CLEAR_BUTTON_CDS)
update_button_clicked = in_box_generator(UPDATE_BUTTON_CDS)
remove_links_button_clicked = in_box_generator(REMOVE_ALL_LINKS_BUTTON_CDS)

def click(event: pygame.event.Event):
    """
    Handles click of one button in the button area
    """
    mouse_pos = pygame.mouse.get_pos()
    if clear_button_clicked(*mouse_pos):
        node_handler.nodes.clear()
    elif update_button_clicked(*mouse_pos):
        # upload to some library
        # retrieve node coordinates & convert them to world frame
        num_nodes = len(node_handler.nodes)
        node_poses = [0] * num_nodes
        for nid in node_handler.nodes.keys():
            node_poses[nid] = np.array(convert_pygame_to_world(node_handler.get_node(nid).coords))

        # compute offsets
        offsets = [np.zeros(2)] * num_nodes
        for nid in node_handler.nodes.keys():
            for neigh_id in node_handler.get_node(nid).neighbours:
                offsets[nid] += node_poses[neigh_id] - node_poses[nid]
        set_offsets(offsets)


    elif remove_links_button_clicked(*mouse_pos):
        for i in range(len(node_handler.nodes)):
            node_handler.nodes[i].neighbours.clear()

def render_text_in_box(screen, draw_box, text, font):
    """Computes the center position of a draw_box to put the text in, and returns it"""
    text = font.render(text, True, (255, 255, 255))
    textpos = text.get_rect(centerx=(draw_box[0] + (draw_box[0] + draw_box[2])) / 2., centery=(draw_box[1] + (draw_box[1] + draw_box[3])) / 2.)
    screen.blit(text, textpos)

def draw(screen: pygame.Surface):
    font = pygame.font.SysFont(pygame.font.get_default_font(), 28)
    pygame.draw.rect(screen, "blue", pygame.Rect(*CLEAR_BUTTON_CDS))
    pygame.draw.rect(screen, "blue", pygame.Rect(*UPDATE_BUTTON_CDS))
    pygame.draw.rect(screen, "blue", pygame.Rect(*REMOVE_ALL_LINKS_BUTTON_CDS))
    render_text_in_box(screen, UPDATE_BUTTON_CDS, "Update", font)
    render_text_in_box(screen, CLEAR_BUTTON_CDS, "Clear", font)
    render_text_in_box(screen, REMOVE_ALL_LINKS_BUTTON_CDS, "Remove all links", font)