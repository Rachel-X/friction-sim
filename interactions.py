"""Code for getting user input."""

import pygame
from pygame.colordict import THECOLORS


def handle_mouse_click(event: pygame.event.Event, screen: pygame.Surface) -> None:
    """Handle a mouse click event."""
    button_pressed = event.button
    mouse_pos = event.pos

    if mouse_pos[0] < 75 and mouse_pos[1] < 25 and button_pressed == 1:
        print('hello!')
        pygame.draw.rect(screen, 'grey', (0, 0, 75, 25))
        pygame.draw.rect(screen, 'grey', (0, 0, 75, 25))
        pygame.display.update()  # todo: read tutorial about a better way to do this
        pygame.time.wait(150)
        # pygame.display.update()

    # todo: finish based on a1_part2
