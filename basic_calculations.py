"""Some simple calculations needed for the friction simulator.

Copyright 2021 (c) Rachel Xie
"""
import math

# CONSTANTS
GRAVITY = 9.8  # m/s^2


def get_ramp_height(ramp_angle: float, screen_width: int) -> float:
    """Return the height of the ramp based on ramp_angle and width of the screen
    on which it will be displayed.

    Preconditions:
        - 0 <= ramp_angle <= 90
    """
    rad_angle = math.radians(ramp_angle)

    return (screen_width / 2) * math.tan(rad_angle)


def get_ramp_length(ramp_angle: float, screen_width: int) -> float:
    """Return the length of the slope part of the ramp (the hypotenuse) for the
    given ramp_angle and screen_width.

    Preconditions:
        - 0 <= ramp_angle <= 90
    """
    base = screen_width / 2
    height = get_ramp_height(ramp_angle, screen_width)

    return math.sqrt(base ** 2 + height ** 2)


def get_weight(m: float, g: float = GRAVITY) -> float:
    """Return the weight of the object with the given mass m, as well as its components."""
    return m * g


def get_normal_force(m: float, incline: float, g: float = GRAVITY) -> float:
    """Return the normal force of an object with mass m, on an ramp that is
    incline degrees from the horizontal, with the given coefficients of
    friction."""
    # todo: it'd make more sense for these two functions to give you components, collapse them?
    weight = get_weight(m, g)

    # weight time cos of the incline gives the component into the ramp
    adj_component = math.cos(incline) * weight  # todo: does this do what i think it does?

    return adj_component


def get_weight_comps(m: float, incline: float = 0.0, g: float = GRAVITY) -> tuple[float, float, float]:
    """Return the weight of the object with the given mass m, as well as components."""
    weight = m * g

    adj_component = math.cos(incline) * weight  # this is also normal force, going into ramp
    opp_component = math.sin(incline) * weight  # component along ramp

    return weight, adj_component, opp_component


def object_slips(m: float, mu_obj: float, mu_ramp: float, incline: float = 0.0,
                 g: float = GRAVITY) -> bool:
    """Return whether an object of mass m will slip under given conditions."""
    weight, normal_force, down_ramp_force = get_weight(m, incline, g)

    # how does mu work again??
    max_friction_force = mu_obj * normal_force

    return max_friction_force <= down_ramp_force
