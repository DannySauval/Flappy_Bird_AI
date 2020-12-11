"""
    This file stores the constants of the code.
    It makes it easier to change parameters without touching the code.
"""

# WORLD CONSTANTS
WORLD = dict(
    WIDTH = 288,
    HEIGHT = 512,
    FLOOR_BIAS = 450,
    FPS = 120)

# BIRD CONSTANTS
BIRD = dict(
    POP_SIZE = 1000,
    WEIGHTS1 = (4, 7),
    WEIGHTS2 = (7, 1),
    GRAVITY = 0.200,
    JUMP_HEIGHT = 5,
    FITNESS_STEP = 0.1)

# Pipe constants
PIPE = dict(
    PIPE_SPEED = 2,
    PIPE_SPACING = 300)

# Game constants
PLAYER = dict(
    MANUAL_PLAY = False)
