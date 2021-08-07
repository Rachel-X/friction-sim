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
    """Return the height of the ramp (shaped like a right triangle) based on
    ramp_angle and width of the screen on which it will be displayed. ramp_angle
    represents an angle in degrees.

    Preconditions:
        - 0 <= ramp_angle < 90
        - 0 < screen_width

    >>> get_ramp_height(30, 50)
    14.433756729740644
    >>> get_ramp_height(42, 147)
    66.17969725589124
    >>> get_ramp_height(0, 150)
    0.0
    >>> get_ramp_height(89, 500)
    14322.490407689786
    """
    rad_angle = math.radians(ramp_angle)

    return (screen_width / 2) * math.tan(rad_angle)


def get_ramp_length(ramp_angle: float, screen_width: int) -> float:
    """Return the length of the slope part of the ramp (the hypotenuse) for the
    given ramp_angle and screen_width. ramp_angle represents an angle in degrees.

    Preconditions:
        - 0 <= ramp_angle < 90
        - 0 < screen_width

    >>> get_ramp_length(30, 50)
    28.867513459481287
    >>> get_ramp_length(42, 147)
    98.90400562606865
    >>> get_ramp_length(0, 150)
    75.0
    >>> get_ramp_length(89, 500)
    14324.672124637476
    """
    base = screen_width / 2
    height = get_ramp_height(ramp_angle, screen_width)

    return math.sqrt(base ** 2 + height ** 2)


def calculate_if_slips(mass: float, materials: List[str], ramp_angle: float,
                       g: float = GRAVITY) -> bool:
    """Return whether an object of the given mass will slip under the given conditions.
    ramp_angle represents an angle in degrees.

    Preconditions:
        - 0 <= ramp_angle < 90
        - 0 < mass
        - len(materials) == 2
        - materials[0] in {'ice', 'steel', 'wood', 'aluminum'} and
            materials[1] in {'ice', 'steel', 'wood', 'aluminum'}
        - 0 <= g

    >>> calculate_if_slips(15, ['steel', 'steel'], 30)
    False
    >>> calculate_if_slips(20, ['ice', 'aluminum'], 40)
    True
    >>> calculate_if_slips(20, ['ice', 'aluminum'], 40, 0)
    False
    """
    rad_angle = math.radians(ramp_angle)
    weight = mass * g
    friction_force = get_friction_force(mass, rad_angle, materials, g)
    down_ramp_comp = weight * math.sin(rad_angle)

    return friction_force < down_ramp_comp


def get_friction_force(mass: float, incline: float, materials: List[str],
                       g: float = GRAVITY) -> float:
    """Return the friction force of an object with given mass, on a ramp that is
    incline radians from the horizontal.

    Preconditions:
        - 0 <= incline < math.pi / 2
        - 0 < mass
        - len(materials) == 2
        - materials[0] in {'ice', 'steel', 'wood', 'aluminum'} and
            materials[1] in {'ice', 'steel', 'wood', 'aluminum'}
        - 0 <= g

    >>> get_friction_force(15, math.pi / 4, ['steel', 'steel'])
    81.07686353084954
    >>> get_friction_force(20, math.pi / 6, ['ice', 'aluminum'])
    16.974097914175
    >>> get_friction_force(20, math.pi / 6, ['ice', 'aluminum'], 0)
    0.0
    """
    normal_force = get_normal_force(mass, incline, g)
    mu = MATERIALS[materials[0]][materials[1]]

    return normal_force * mu


def get_normal_force(mass: float, incline: float, g: float = GRAVITY) -> float:
    """Return the normal force of an object with given mass, on a ramp that is
    incline radians from the horizontal.

    Preconditions:
        - 0 <= incline < math.pi / 2
        - 0 < mass
        - 0 <= g

    >>> get_normal_force(15, math.pi / 6)
    127.30573435631248
    >>> get_normal_force(20, math.pi / 4)
    138.59292911256333
    >>> get_normal_force(15, math.pi / 6, 0)
    0.0
    >>> get_normal_force(15, math.pi / 4, 1.0)
    10.606601717798213
    """
    weight = mass * g

    # weight times cos of the incline gives the component into the ramp
    adj_component = math.cos(incline) * weight

    return adj_component


if __name__ == '__main__':
    import doctest
    doctest.testmod()

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
