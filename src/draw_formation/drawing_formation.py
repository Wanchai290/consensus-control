SCREEN_SIZE = (1280, 720)


def main(default_offsets: tuple = None):
    # Example file showing a basic pygame "game loop"
    import pygame
    import numpy as np

    import node_handler
    import node_mover
    import linker
    import buttons
    buttons.set_offsets(default_offsets)

    pygame.display.set_caption("Formation drawing app (Tatusya Ibuki laboratory)")
    if not pygame.font:
        print("Warning: pygame.font module not loaded. Text rendering will surely crash the program.")

    # -- Constants
    NODE_DRAW_RADIUS = 16.
    def node_near_mouse(mouse_pos):
        """
        If mouse very close to a node, returns the node clicked.
        Otherwise, returns None
        Args:
            mouse_pos: Position of the mouse
        """
        for node in node_handler.nodes.values():
            if np.linalg.norm(node.coords - mouse_pos) < NODE_DRAW_RADIUS:
                return node
        return None

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont(pygame.font.get_default_font(), 28)

    def drawing_area_click(event: pygame.event.Event):
        left_click, middle_click, right_click = pygame.mouse.get_pressed()
        near = node_near_mouse(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if left_click:
                if near is not None:
                    node_mover.start_moving(near)
                else:
                    n = node_handler.create_node()
                    n.coords = mouse_pos
            elif right_click:
                if near is not None:
                    node_handler.delete_node(near)
            elif middle_click:
                if near is not None:
                    linker.set_highlighted(near)

        elif event.type == pygame.MOUSEBUTTONUP:
            # only handling left click released
            node_mover.stop_moving(pygame.mouse.get_pos())


    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                mouse_pos = np.array(pygame.mouse.get_pos())
                if mouse_pos[1] > buttons.BUTTONS_Y_TOP:
                    buttons.click(event)
                else:
                    drawing_area_click(event)

        # -- Rendering
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # draw all nodes
        for node in node_handler.nodes.values():
            pose = node.coords if not node.is_moving else pygame.mouse.get_pos()

            # draw the node
            pygame.draw.circle(screen, "red", pose, NODE_DRAW_RADIUS)
            text = font.render(str(node.id), True, (255, 255, 255))
            textpos = text.get_rect(centerx=pose[0], centery=pose[1])
            screen.blit(text, textpos)

            # draw the links of the node (from center of start node, to edge)
            start = node.coords
            for friend_id in node.neighbours:
                end = node_handler.get_node(friend_id).coords
                pygame.draw.line(screen, "green", start, end, width=3)

        # highlight a given node
        highlighted = linker.get_highlighted()
        if highlighted is not None:
            pygame.draw.circle(screen, "yellow", highlighted.coords, NODE_DRAW_RADIUS + 8, width=5)

        # draw buttons
        buttons.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == '__main__':
    main()