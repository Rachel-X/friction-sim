"""Some simple calculations needed for the friction simulator.

Sources for the value of mu in coefficients.csv and MATERIALS
were https://www.engineersedge.com/coeffients_of_friction.htm
and Nelson Physics 11 textbook. Where ranges were given,
the lowest value was chosen. For the value of aluminum on ice,
the recommended value from The Friction of Saline Ice on
Aluminum by Christopher Wallen-Russell and Ben Lishman was used.
"""
import math
from typing import List

# CONSTANTS
GRAVITY = 9.8  # m/s^2
MATERIALS = {
    'aluminum': {'steel': 0.61, 'aluminum': 1.1, 'wood': 0.2, 'ice': 0.1},
    'steel': {'steel': 0.78, 'aluminum': 0.61, 'wood': 0.2, 'ice': 0.1},
    'wood': {'steel': 0.2, 'aluminum': 0.2, 'wood': 0.25, 'ice': 0.05},
    'ice': {'steel': 0.1, 'aluminum': 0.1, 'wood': 0.05, 'ice': 0.1}
}


def get_ramp_height(ramp_angle: float, screen_width: int) -> float:
    """Return the height of the ramp based on ramp_angle and width of the screen
    on which it will be displayed.

    Preconditions:
        - 0 <= ramp_angle < 90
        - 0 < screen_width
    """
    rad_angle = math.radians(ramp_angle)

    return (screen_width / 2) * math.tan(rad_angle)


def get_ramp_length(ramp_angle: float, screen_width: int) -> float:
    """Return the length of the slope part of the ramp (the hypotenuse) for the
    given ramp_angle and screen_width.

    Preconditions:
        - 0 <= ramp_angle < 90
        - 0 < screen_width
    """
    base = screen_width / 2
    height = get_ramp_height(ramp_angle, screen_width)

    return math.sqrt(base ** 2 + height ** 2)


def calculate_if_slips(mass: float, materials: List[str], ramp_angle: float,
                       g: float = GRAVITY) -> bool:
    """Return whether an object of the given mass will slip under the given conditions.

    Preconditions:
        - 0 <= ramp_angle < 90
        - 0 < mass
        - len(materials) == 2
        - materials[0] in {'ice', 'steel', 'wood', 'aluminum'} and
            materials[1] in {'ice', 'steel', 'wood', 'aluminum'}
    """
    rad_angle = math.radians(ramp_angle)
    weight = mass * g
    normal_force = get_normal_force(mass, ramp_angle, g)
    friction_force = get_friction_force(mass, ramp_angle, materials, g)
    down_ramp_comp = weight * math.sin(rad_angle)

    return friction_force < down_ramp_comp


def get_friction_force(mass: float, incline: float, materials: List[str],
                       g: float = GRAVITY) -> float:
    """Return the friction force of an object with given mass, on a ramp that is
    incline radians from the horizontal.

    """
    normal_force = get_normal_force(mass, incline, g)
    mu = MATERIALS[materials[0]][materials[1]]

    return normal_force * mu


def get_normal_force(mass: float, incline: float, g: float = GRAVITY) -> float:
    """Return the normal force of an object with given mass, on a ramp that is
    incline radians from the horizontal.

    Preconditions:
        - 0 <= incline < math.pi / 2
    """
    # todo: it'd make more sense for these two functions to give you components, collapse them?
    weight = mass * g

    # weight times cos of the incline gives the component into the ramp
    adj_component = math.cos(incline) * weight

    return adj_component


# def get_weight_comps(m: float, incline: float = 0.0, g: float = GRAVITY) -> \
#         tuple[float, float, float]:
#     """Return the weight of the object with the given mass m, as well as components."""
#     weight = m * g
#
#     adj_component = math.cos(incline) * weight  # this is also normal force, going into ramp
#     opp_component = math.sin(incline) * weight  # component along ramp
#
#     return weight, adj_component, opp_component
#
#
# def object_slips(m: float, mu_obj: float, mu_ramp: float, incline: float = 0.0,
#                  g: float = GRAVITY) -> bool:
#     """Return whether an object of mass m will slip under given conditions.
#
#     Values of mu are from the coefficients.csv file. (They represent static friction.)
#     """
#     weight, normal_force, down_ramp_force = get_weight(m, incline, g)
#
#     # how does mu work again??
#     max_friction_force = mu_obj * normal_force
#
#     return max_friction_force <= down_ramp_force
