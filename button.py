"""A button class! (test)"""
from typing import Optional

import pygame


class ArrowButton:
    """A simple button for user interaction."""
    point_up: bool
    shape: pygame.Rect
    current_value: int

    def __init__(self, point_up: bool, shape: pygame.Rect, current_value: int = 30) -> None:
        """Create a new ArrowButton."""
        self.point_up = point_up
        self.shape = shape
        self.current_value = current_value

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button.
        """
        my_image = pygame.image.load('proper_arrow_icon.png').convert_alpha()
        my_image = pygame.transform.scale(my_image, (self.shape.width, self.shape.height))

        if not self.point_up:
            my_image = pygame.transform.flip(my_image, False, True)

        screen.blit(my_image, my_image.get_rect(center=self.shape.center))

    def update(self, event: pygame.event.Event) -> Optional[int]:
        """Handle changes."""
        button_pressed = event.button
        mouse_pos = event.pos

        if button_pressed == 1 and self.shape.collidepoint(mouse_pos):
            if self.point_up:
                self.current_value += 1
                return self.current_value
            else:
                self.current_value -= 1
                return self.current_value

        return None
