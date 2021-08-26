"""The file from which the simulator should be run."""
import pygame
from pygame.colordict import THECOLORS
from basic_calculations import MATERIALS
from FrictionSim.visualizations import draw_about_slipping, draw_ramp_mass, draw_stats
from menu import Menu
from button import ArrowButton

SCREEN_SIZE = 1000, 750  # width, then height


def run_sim(ramp_angle: float, mass: float) -> None:
    """Display a simple ramp with a rectangular mass on it with an angle above
    the horizontal of ramp_angle, which is an angle in degrees.

    Preconditions:
        - 0.0 <= ramp_angle <= 45.0
        - 0.0 < mass
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
    mats_menu1 = Menu(materials, menu_rect1, 'Select Material')
    mats_menu2 = Menu(materials, menu_rect2, 'Select Material')

    ramp_arrow_up_shape = pygame.Rect((screen.get_width() // 5) * 0.75,
                                      (screen.get_height() // 3) // 5,
                                      15, 25)
    ramp_arrow_up = ArrowButton(True, ramp_arrow_up_shape, int(ramp_angle))
    ramp_arrow_down_shape = pygame.Rect((screen.get_width() // 5) * 0.85,
                                        (screen.get_height() // 3) // 5,
                                        15, 25)
    ramp_arrow_down = ArrowButton(False, ramp_arrow_down_shape, int(ramp_angle))

    mass_arrow_up_shape = pygame.Rect((screen.get_width() // 5) * 0.75,
                                      (screen.get_height() // 3) * 0.4,
                                      15, 25)
    mass_arrow_up = ArrowButton(True, mass_arrow_up_shape, int(mass))
    mass_arrow_down_shape = pygame.Rect((screen.get_width() // 5) * 0.85,
                                        (screen.get_height() // 3) * 0.4,
                                        15, 25)
    mass_arrow_down = ArrowButton(False, mass_arrow_down_shape, int(mass))

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

        mass_arrow_up.draw(screen)
        mass_arrow_down.draw(screen)

        pygame.display.flip()  # updates the display

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            mats_menu1.update(screen, event)
            mats_menu2.update(screen, event)
            angle1 = ramp_arrow_up.update(event)
            angle2 = ramp_arrow_down.update(event)
            mass1 = mass_arrow_up.update(event)
            mass2 = mass_arrow_down.update(event)
            screen.fill('aliceblue')

            if ramp_angle != angle1 and angle1 is not None and 0 <= angle1 <= 45:
                ramp_angle = angle1
                ramp_arrow_down.current_value = angle1
            elif ramp_angle != angle2 and angle2 is not None and 0 <= angle2 <= 45:
                ramp_angle = angle2
                ramp_arrow_up.current_value = angle2

            if mass != mass1 and mass1 is not None and 0 < mass1:
                mass = mass1
                mass_arrow_down.current_value = mass1
            elif mass != mass2 and mass2 is not None and 0 < mass2:
                mass = mass2
                mass_arrow_up.current_value = mass2

    pygame.display.quit()


if __name__ == '__main__':
    run_sim(30, 15)
