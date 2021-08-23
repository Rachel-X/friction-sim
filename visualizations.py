"""Visualizing the friction simulator."""
import math
from typing import List

import pygame
from pygame.colordict import THECOLORS
from basic_calculations import calculate_if_slips, get_friction_force, get_normal_force, \
    get_ramp_height, get_ramp_length, MATERIALS
from menu import Menu
from button import ArrowButton

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

    menu_rect1 = pygame.Rect(screen.get_width() * 0.75, 5, 100, 30)
    menu_rect2 = pygame.Rect(screen.get_width() * 0.75 + menu_rect1.width + 10, 5, 100, 30)
    materials = list(MATERIALS.keys())
    mats_menu1 = Menu(materials, menu_rect1)
    mats_menu2 = Menu(materials, menu_rect2)

    ramp_arrow_up_shape = pygame.Rect((screen.get_width() // 5) * 0.75,
                                      (screen.get_height() // 3) // 5,
                                      15, 25)
    ramp_arrow_up = ArrowButton(True, ramp_arrow_up_shape)
    ramp_arrow_down_shape = pygame.Rect((screen.get_width() // 5) * 0.85,
                                        (screen.get_height() // 3) // 5,
                                        15, 25)
    ramp_arrow_down = ArrowButton(False, ramp_arrow_down_shape)

    while True:

        draw_ramp_mass(screen, ramp_angle)

        mats_menu1.draw(screen)
        mats_menu2.draw(screen)

        mats1 = mats_menu1.current_choice
        mats2 = mats_menu2.current_choice

        if mats1 >= 0 and mats2 >= 0:
            draw_stats(screen, ramp_angle, mass, [mats_menu1.current_text,
                                                  mats_menu2.current_text])
            draw_about_slipping(screen, ramp_angle, mass, [mats_menu1.current_text,
                                                           mats_menu2.current_text])
        else:
            draw_stats(screen, ramp_angle, mass)

        ramp_arrow_up.draw(screen)
        ramp_arrow_down.draw(screen)

        pygame.display.flip()  # updates the display

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            mats_menu1.update(screen, event)
            mats_menu2.update(screen, event)
            angle1 = ramp_arrow_up.update(event)
            angle2 = ramp_arrow_down.update(event)
            # print(str(angle1) + ' and ' + str(angle2))
            screen.fill('aliceblue')

            if ramp_angle != angle1 and angle1 is not None:
                ramp_angle = angle1
                ramp_arrow_down.current_value = angle1
                # print('here! 1: ' + str(angle1))
            elif ramp_angle != angle2 and angle2 is not None:
                ramp_angle = angle2
                ramp_arrow_up.current_value = angle2
                # print('here, 2: ' + str(angle2))

    pygame.display.quit()


def draw_ramp_mass(screen: pygame.Surface, ramp_angle: float) -> None:
    """Actually drawing ramp and mass."""
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

    pygame.draw.polygon(screen, THECOLORS['salmon'], ramp_coords)
    pygame.draw.polygon(screen, THECOLORS['gold'], mass_coords)


def draw_stats(screen: pygame.Surface, ramp_angle: float, mass: float,
               materials: List[str] = None) -> None:
    """Draw the statistics in the top left corner of the screen.

    These stats include the angle of the ramp, the mass of the block in kg, and the
    normal force perpendicular to the ramp surface.
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
    ramp_angle in degrees."""
    title_font = pygame.font.SysFont('arialrounded', 28)
    text_font = pygame.font.SysFont('arial', 24)

    question_text = title_font.render('Does the mass slip?', True, (10, 10, 10))
    answer = calculate_if_slips(mass, materials, ramp_angle)

    if answer:
        answer_text = text_font.render('Yes.', True, (10, 10, 10))
    else:
        answer_text = text_font.render('No.', True, (10, 10, 10))

    screen.blit(question_text, (screen.get_width() / 3, 25))
    screen.blit(answer_text, (screen.get_width() / 3 + 5, 55))


if __name__ == '__main__':
    draw_base_set_up(30, 15)
