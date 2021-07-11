"""Visualizing the friction simulator."""
import math
import pygame
from pygame.colordict import THECOLORS
from basic_calculations import get_ramp_height, get_ramp_length

SCREEN_SIZE = 1000, 750  # width, then height


def draw_base_set_up(ramp_angle: float) -> None:
    """Display a simple ramp with a rectangular mass on it with an angle above
    the horizontal of ramp_angle, which is an angle in degrees.

    Preconditions:
        - 0 <= ramp_angle <= 90
    """
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill(THECOLORS['aliceblue'])

    rad_angle = math.radians(ramp_angle)
    ramp_height = get_ramp_height(ramp_angle, SCREEN_SIZE[0])
    ramp_length = get_ramp_length(ramp_angle, SCREEN_SIZE[0])
    ramp_base = math.sqrt(ramp_length ** 2 - ramp_height ** 2)
    # the base of the ramp is also just the screen width divided by 2

    ramp_coords = [(screen.get_width() / 4, screen.get_height() * 0.75 + ramp_height / 2),
                   (screen.get_width() * 0.75, screen.get_height() * 0.75 + ramp_height / 2),
                   (screen.get_width() * 0.75, screen.get_height() * 0.75 - ramp_height / 2)]

    mass_coords = [(screen.get_width() / 2 + ramp_base / 4,
                    screen.get_height() * 0.75 - ramp_height / 4),
                   (ramp_coords[1][0], screen.get_height() * 0.75 - ramp_height / 2),
                   (ramp_coords[1][0] - (math.sin(rad_angle) * (ramp_length / 4)),
                    screen.get_height() * 0.75 - ramp_height / 2 -
                    math.cos(rad_angle) * (ramp_length / 4)),
                   (screen.get_width() / 2 + ramp_base / 4 -
                    (math.sin(rad_angle) * (ramp_length / 4)),
                    screen.get_height() * 0.75 - math.cos(rad_angle) * (ramp_length / 4) -
                    ramp_height / 4)]

    while True:
        # todo: move all this drawing nonsense to its own function
        # todo: figure out how to get input from pygame

        pygame.draw.polygon(screen, THECOLORS['mediumblue'], ramp_coords)
        pygame.draw.polygon(screen, THECOLORS['gold'], mass_coords)

        pygame.display.flip()  # updates the display

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            break

    pygame.display.quit()


if __name__ == '__main__':
    draw_base_set_up(5)
