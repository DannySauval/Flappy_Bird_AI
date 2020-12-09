import random
import pygame

from NeuralNetwork import NeuralNetwork

from settings import BIRD, WORLD

class Bird:
    high_score = 0
    alive_birds = 0

    bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()

    def __init__(self, weights_list):
        self.score = 0   # Number of pipes
        self.fitness = 0 # Number of frames until dead
        self.bird_movement = 0
        self.alive = True
        self.next_pipe_index = 0
        self.net = NeuralNetwork(weights_list)

        self.gravity = BIRD['GRAVITY']
        self.jump_height = BIRD['JUMP_HEIGHT']
        # If it's the first bird we declare, we want to load the image
        self.bird_rect = Bird.bird_surface.get_rect(center = (50, WORLD['HEIGHT']/2))

        Bird.alive_birds += 1

    def reset(self):
        self.score = 0
        self.bird_movement = 0
        self.bird_rect = Bird.bird_surface.get_rect(center = (50, WORLD['HEIGHT']/2))
        self.alive = True
        self.next_pipe_index = 0

    def update_highscore(self):
        if self.score > Bird.high_score:
            Bird.high_score = int(self.score)

    def check_collision(self, pipes):
        """
            Returns False if there is a collision or if the bird gets out of the screen.
            Returns True otherwise.
        """
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe):
                return False
        if self.bird_rect.top <= -90 or self.bird_rect.bottom >= WORLD['FLOOR_BIAS']:
            return False
        return True

    def make_decision(self, pipes):
        # if len(pipes) > self.next_pipe_index + 1:
        if pipes[self.next_pipe_index].right - self.bird_rect.right < 0:
            self.next_pipe_index = (self.next_pipe_index+2)%6 # Next bottom pipe
            self.score += 1
        inputs = []
        # X Distance to next pipes
        inputs.append(pipes[self.next_pipe_index].left - self.bird_rect.right)
        # Y Distance to top pipe
        inputs.append(self.bird_rect.top - pipes[self.next_pipe_index+1].bottom)
        # Y Distance to bottom pipe
        inputs.append(pipes[self.next_pipe_index].top - self.bird_rect.bottom)
        # Y Position of the bird
        inputs.append(self.bird_rect.centery)

        if self.net.make_decision(inputs):
            self.jump()

    def jump(self):
        self.bird_movement = -self.jump_height

    def update(self, screen, pipe_list):
        if self.alive:
            self.fitness += BIRD['FITNESS_STEP']
            self.update_highscore()

            self.bird_movement += self.gravity
            self.bird_rect.centery += self.bird_movement
            screen.blit(Bird.bird_surface, self.bird_rect)

            self.alive = self.check_collision(pipe_list)
            if not self.alive:
                Bird.alive_birds -= 1
       