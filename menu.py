"""
A dropdown menu. (partially based on
https://stackoverflow.com/questions/59236523/trying-creating-dropdown-menu-pygame-but-got-stuck/65369938#65369938
"""
from typing import List

import pygame


class Menu:
    """A dropdown menu for the user to interact with."""
    options: List[str]
    shape: pygame.Rect
    current_choice: int
    current_text: str
    show_menu: bool

    def __init__(self, options: List[str], shape: pygame.Rect) -> None:
        """Initialize a new Menu object."""
        self.options = options
        self.shape = shape
        self.current_choice = -1
        self.current_text = 'Select Option'
        self.show_menu = False

    def draw(self, screen: pygame.Surface) -> None:
        """Draw a Menu object."""
        pygame.draw.rect(screen, 'wheat1', self.shape)

        menu_font = pygame.font.SysFont('arial', self.shape.width // 8)
        menu_text = menu_font.render(self.current_text, True, (10, 10, 10))

        screen.blit(menu_text, menu_text.get_rect(center=self.shape.center))

        if self.show_menu:
            for i in range(len(self.options)):
                opt_rect = self.shape.copy()
                opt_rect.y += (i + 1) * opt_rect.height
                pygame.draw.rect(screen, 'salmon', opt_rect)
                text = menu_font.render(self.options[i], True, (10, 10, 10))
                screen.blit(text, text.get_rect(center=opt_rect.center))

    def update(self, screen: pygame.Surface, event: pygame.event.Event) -> None:
        """Update the Menu object."""
        button_pressed = event.button
        mouse_pos = event.pos

        if button_pressed == 1:
            if self.show_menu:
                for i in range(len(self.options)):
                    opt_rect = self.shape.copy()
                    opt_rect.y += (i + 1) * self.shape.height
                    if opt_rect.collidepoint(mouse_pos):
                        self.current_choice = i
                        self.current_text = self.options[i]
                        print(self.current_text)

            self.show_menu = bool(self.shape.collidepoint(mouse_pos))

            print(self.show_menu)

        self.draw(screen)
