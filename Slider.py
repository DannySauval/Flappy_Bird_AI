"""
    Slider class from https://www.dreamincode.net/forums/topic/401541-buttons-and-sliders-in-pygame/
"""

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
ORANGE = (200, 100, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
TRANS = (1, 1, 1)

from settings import WORLD

class Slider():
    def __init__(self, name, val, mini, maxi, pos, font):
        self.val = val  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = pos  # x-location on screen
        self.ypos = WORLD['HEIGHT']
        self.surf = pygame.surface.Surface((100, 50))
        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction
        self.name = name
        self.font = pygame.font.SysFont("Arial", 16)

        self.txt_surf = self.font.render(self.name + " " + str(self.val), 1, BLACK)
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))

        # Static graphics - slider background #
        self.surf.fill(GREY)
        pygame.draw.rect(self.surf, RED, [0, 0, 100, 50], 3)
        pygame.draw.rect(self.surf, WHITE, [10, 30, 80, 5], 0)

        # dynamic graphics - button surface #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(TRANS)
        self.button_surf.set_colorkey(TRANS)
        pygame.draw.circle(self.button_surf, BLACK, (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, ORANGE, (10, 10), 4, 0)

    def draw(self, screen):
        """ Combination of static and dynamic graphics in a copy of
    the basic slide surface
    """
        # static
        surf = self.surf.copy()

        # dynamic
        surf.fill(GREY)
        pygame.draw.rect(surf, RED, [0, 0, 100, 50], 3)
        pygame.draw.rect(surf, WHITE, [10, 30, 80, 5], 0)
        surf.blit(self.txt_surf, self.txt_rect)
        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # move of button box to correct screen position

        # screen
        screen.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """
    The dynamic part; reacts to movement of the slider button.
    """
        self.val = int((pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini)
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi
        self.txt_surf = self.font.render(self.name + " " + str(self.val), 1, BLACK)