"""
    This file stores the constants of the code.
    It makes it easier to change parameters without touching the code.
"""

# WORLD CONSTANTS
WORLD = dict(
    WIDTH = 288,
    HEIGHT = 512,
    FLOOR_BIAS = 450)

# BIRD CONSTANTS
# TODO : Make it compatible with X weights, maybe using a list
BIRD = dict(
    POP_SIZE = 200,
    WEIGHTS1 = (4, 7),
    WEIGHTS2 = (7, 1),
    GRAVITY = 0.125,
    JUMP_HEIGHT = 4,
    FITNESS_STEP = 0.1)

# Pipe constants
PIPE = dict(
    PIPE_SPEED = 2,
    PIPE_SPACING = 250)
