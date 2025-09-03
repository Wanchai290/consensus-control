import typing
import pygame

import node_handler
from drawing_formation import SCREEN_SIZE
BUTTONS_Y_TOP = 650.

def in_box_generator(draw_box) -> typing.Callable[[float, float], bool]:
    return lambda x,y: (draw_box[0] <= x <= draw_box[0] + draw_box[2]
                        and draw_box[1] <= y <= draw_box[1] + draw_box[3])

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
        pass
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