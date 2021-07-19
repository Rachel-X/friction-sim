"""Visualizing the friction simulator."""
import math
import pygame
from pygame.colordict import THECOLORS
from basic_calculations import get_normal_force, get_ramp_height, get_ramp_length
import interactions

SCREEN_SIZE = 1000, 750  # width, then height


def draw_base_set_up(ramp_angle: float, mass: float) -> None:
    """Display a simple ramp with a rectangular mass on it with an angle above
    the horizontal of ramp_angle, which is an angle in degrees.

    Preconditions:
        - 0 <= ramp_angle < 90
        - 0 < mass
    """
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Friction Simulator')
    icon = pygame.image.load('square_icon.png')
    pygame.display.set_icon(icon)
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

        pygame.draw.polygon(screen, THECOLORS['salmon'], ramp_coords)
        pygame.draw.polygon(screen, THECOLORS['gold'], mass_coords)

        draw_stats(screen, ramp_angle, mass)

        pygame.display.flip()  # updates the display

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            interactions.handle_mouse_click(event, screen)

    pygame.display.quit()


def draw_stats(screen: pygame.Surface, ramp_angle: float, mass: float) -> None:
    """Draw the statistics in the top left corner of the screen.

    These stats include the angle of the ramp, the mass of the block in kg, and the
    normal force perpendicular to the ramp surface.
    """
    pygame.draw.rect(screen, 'wheat1', (0, 0, screen.get_width() // 5, screen.get_height() // 3))

    # this number of sig figs is arbitrary -- not really good science
    normal_force_display = round(get_normal_force(mass, ramp_angle), 2)

    title_font = pygame.font.SysFont('arialrounded', 25)
    text_font = pygame.font.SysFont('arial', 20)

    title_text = title_font.render('Stats', True, (10, 10, 10))
    angle_text = text_font.render('Ramp Angle: ' + str(ramp_angle), True, (10, 10, 10))
    mass_text = text_font.render('Mass: ' + str(mass), True, (10, 10, 10))
    normal_text = text_font.render('Normal Force: ' + str(normal_force_display),
                                   True, (10, 10, 10))

    screen.blit(title_text, (1, 1))
    screen.blit(angle_text, (1, (screen.get_height() // 3) // 4))
    screen.blit(mass_text, (1, (screen.get_height() // 3) // 2))
    screen.blit(normal_text, (1, (screen.get_height() // 3) * 0.75))


if __name__ == '__main__':
    draw_base_set_up(30, 25)
