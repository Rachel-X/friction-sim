"""Visualizing the friction simulator."""
import math
from typing import List

import pygame
from pygame.colordict import THECOLORS
from basic_calculations import calculate_if_slips, get_friction_force, get_normal_force, \
    get_ramp_height, get_ramp_length

SCREEN_SIZE = 1000, 750  # width, then height


def draw_ramp_mass(screen: pygame.Surface, ramp_angle: float) -> None:
    """Draw the mass and ramp for visualizing the set-up.

    Preconditions:
        - 0.0 <= ramp_angle <= 45.0
    """
    rad_angle = math.radians(ramp_angle)
    ramp_height = get_ramp_height(ramp_angle, SCREEN_SIZE[0])
    ramp_length = get_ramp_length(ramp_angle, SCREEN_SIZE[0])
    ramp_base = math.sqrt(ramp_length ** 2 - ramp_height ** 2)
    # Note: the base of the ramp is the screen width divided by 2

    ramp_coords = [(screen.get_width() / 4, screen.get_height() * 0.5 + ramp_height / 2),
                   (screen.get_width() * 0.75, screen.get_height() * 0.5 + ramp_height / 2),
                   (screen.get_width() * 0.75, screen.get_height() * 0.5 - ramp_height / 2)]

    mass_coords = [(screen.get_width() / 2 + ramp_base / 4,
                    screen.get_height() * 0.5 - ramp_height / 4),
                   (ramp_coords[1][0], screen.get_height() * 0.5 - ramp_height / 2),
                   (ramp_coords[1][0] - (math.sin(rad_angle) * (ramp_length / 4)),
                    screen.get_height() * 0.5 - ramp_height / 2 -
                    math.cos(rad_angle) * (ramp_length / 4)),
                   (screen.get_width() / 2 + ramp_base / 4 -
                    (math.sin(rad_angle) * (ramp_length / 4)),
                    screen.get_height() * 0.5 - math.cos(rad_angle) * (ramp_length / 4) -
                    ramp_height / 4)]

    pygame.draw.polygon(screen, THECOLORS['salmon'], ramp_coords)
    pygame.draw.polygon(screen, THECOLORS['gold'], mass_coords)


def draw_stats(screen: pygame.Surface, ramp_angle: float, mass: float,
               materials: List[str] = None) -> None:
    """Draw the statistics in the top left corner of the screen.

    These stats include the angle of the ramp, the mass of the block in kg, and the
    normal force perpendicular to the ramp surface.

    Preconditions:
        - 0.0 <= ramp_angle <= 45.0
        - 0.0 <= mass
        - materials[0] in {'ice', 'steel', 'wood', 'aluminum'} and
            materials[1] in {'ice', 'steel', 'wood', 'aluminum'}
    """
    pygame.draw.rect(screen, 'wheat1', (0, 0, screen.get_width() // 5, screen.get_height() // 3))

    rad_angle = math.radians(ramp_angle)
    # this number of sig figs is arbitrary -- not really good science
    # also note that these two assume the default value of gravity, 9.8
    normal_force_display = round(get_normal_force(mass, rad_angle), 2)

    if materials is not None:
        friction_force_display = round(get_friction_force(mass, rad_angle, materials), 2)
    else:
        friction_force_display = 'N/A'

    title_font = pygame.font.SysFont('arialrounded', 25)
    text_font = pygame.font.SysFont('arial', 20)

    title_text = title_font.render('Stats', True, (10, 10, 10))
    angle_text = text_font.render('Ramp Angle: ' + str(ramp_angle), True, (10, 10, 10))
    mass_text = text_font.render('Mass: ' + str(mass), True, (10, 10, 10))
    normal_text = text_font.render('Normal Force: ' + str(normal_force_display),
                                   True, (10, 10, 10))
    friction_text = text_font.render('Friction Force: ' + str(friction_force_display),
                                     True, (10, 10, 10))

    screen.blit(title_text, (1, 1))
    screen.blit(angle_text, (1, (screen.get_height() // 3) // 5))
    screen.blit(mass_text, (1, (screen.get_height() // 3) * 0.4))
    screen.blit(normal_text, (1, (screen.get_height() // 3) * 0.6))
    screen.blit(friction_text, (1, (screen.get_height() // 3) * 0.8))


def draw_about_slipping(screen: pygame.Surface, ramp_angle: float, mass: float,
                        materials: List[str]) -> None:
    """Draw the necessary text for showing whether the mass slips down the ramp, given
    ramp_angle in degrees.

    Preconditions:
        - 0.0 <= ramp_angle <= 45.0
        - 0.0 <= mass
        - materials[0] in {'ice', 'steel', 'wood', 'aluminum'} and
            materials[1] in {'ice', 'steel', 'wood', 'aluminum'}
    """
    title_font = pygame.font.SysFont('arialrounded', 28)
    text_font = pygame.font.SysFont('arial', 24)

    question_text = title_font.render('Does the mass slip?', True, (10, 10, 10))
    answer = calculate_if_slips(mass, materials, ramp_angle)

    if answer:
        answer_text = text_font.render('Yes.', True, (10, 10, 10))
    else:
        answer_text = text_font.render('No.', True, (10, 10, 10))

    screen.blit(question_text, (screen.get_width() // 4, 25))
    screen.blit(answer_text, (screen.get_width() // 4 + 5, 55))
