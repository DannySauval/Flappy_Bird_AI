import numpy as np
import sys
import random

from settings import WORLD, PIPE, BIRD
import pygame
from Bird import Bird
from NeuralNetwork import NeuralNetwork


class FlappBird:
    def __init__(self):
        pygame.init()

        # Window setup
        self.screen = pygame.display.set_mode((WORLD['WIDTH'], WORLD['HEIGHT']))
        pygame.display.set_caption("Flappy Bird AI")
        pygame.display.set_icon(pygame.image.load('assets/flappy_bird_icon.png'))

        Bird.clsinit()
        NeuralNetwork.clsinit()

        self.game_active = True

        # Setting up framerate
        self.clock = pygame.time.Clock()

        # Font
        self.game_font = pygame.font.Font('assets/04B_19.ttf', 20)

        # Images import
        self.bg_surface = pygame.image.load('assets/background-day.png').convert()

        self.floor_surface = pygame.image.load('assets/base.png').convert()
        self.floor_x_pos = 0

        self.pipe_surface = pygame.image.load('assets/pipe-green.png')
        self.pipe_list = []
        self.pipe_height = [200, 300, 400]

        for i in range(3):
            self.pipe_list.extend(self.create_pipe(i))

        self.game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
        self.game_over_rect = self.game_over_surface.get_rect(center = (WORLD['WIDTH']/2, WORLD['HEIGHT']/2))

        self.birds = self.generate_pop(mutated=False)

        self.best_bird_weights = []
        self.best_bird_fitness = 0

        self.timer = 0
        self.offscreen_pipe_index = 0
        self.addTimer = PIPE['PIPE_SPACING']

        self.current_generation = 0
        self.best_gen_highscore = 0

    def run(self):
        # Main loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active:
                        for bird in self.birds:
                            bird.jump()
                    
            keys = pygame.key.get_pressed()  #checking pressed keys
            if keys[pygame.K_LEFT]:
                self.move_pipes()
                self.timer += 1

            """
                TODO : Two lists, rather go through the alive_bird_list to avoid iterating over known dead birds.
            """
            # For each birds, decide if it's going to jump or not.
            for bird in self.birds:
                bird.make_decision(self.pipe_list)

            # Recycle offscreen pipe every addTimer frame.
            self.timer += 1
            if self.timer >= self.addTimer:
                self.pipe_list[self.offscreen_pipe_index], self.pipe_list[self.offscreen_pipe_index+1] = self.create_pipe(1)

                self.offscreen_pipe_index = (self.offscreen_pipe_index+2)%6
                self.timer = 0
                self.addTimer = PIPE['PIPE_SPACING']/PIPE['PIPE_SPEED']

            # Background
            self.screen.blit(self.bg_surface, (0, 0))

            if self.game_active:
                # Bird
                if Bird.alive_birds == 0:
                    self.game_active = False
                for bird in self.birds:
                    bird.update(self.screen, self.pipe_list)

                if not self.game_active:
                    self.reset_game()

                # Pipes 
                self.move_pipes()
                self.draw_pipes()
                self.data_display()
            else:
                self.screen.blit(self.game_over_surface, self.game_over_rect)

            # Floor
            self.draw_floor()

            pygame.display.update()
            self.clock.tick(1000)

        pygame.quit()

    def reset_game(self):
        """
            Reset all variables to start again with a new bird batch.
        """
        # Get the bird with the best fitness.
        for bird in self.birds:
            if bird.fitness > self.best_bird_fitness:
                self.best_bird_weights = bird.net.weights
                self.best_bird_fitness = bird.fitness

        if Bird.high_score > self.best_gen_highscore:
            self.best_gen_highscore = Bird.high_score

        self.birds.clear()
        self.birds = self.generate_pop(mutated=True)
        Bird.high_score = 0
        self.game_active = True
        self.timer = 0

        self.offscreen_pipe_index = 0
        self.addTimer = PIPE['PIPE_SPACING']
        
        self.reset_pipes()

        # save_weights(best_bird_weights, "weights")

        self.current_generation += 1

    def draw_floor(self):
        """
            Draws the floor and handles the landscape scrolling.
        """
        self.floor_x_pos -= 1
        self.screen.blit(self.floor_surface, (self.floor_x_pos, WORLD['FLOOR_BIAS']))
        self.screen.blit(self.floor_surface, (self.floor_x_pos + WORLD['WIDTH'], WORLD['FLOOR_BIAS']))

        if self.floor_x_pos <= -WORLD['WIDTH']:
            self.floor_x_pos = 0

    def create_pipe(self, pipe_number):
        """
            Returns a new pair of pipes, with random height.
        """
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop = ((pipe_number*PIPE['PIPE_SPACING'])+350, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom = ((pipe_number*PIPE['PIPE_SPACING'])+350, random_pipe_pos - 150))

        return bottom_pipe, top_pipe

    def data_display(self):
        """
            Prints what we want to be displayed on the screen.
        """
        self.blit_text(f'GEN HS : {int(self.best_gen_highscore)}', (WORLD['WIDTH']-100, 10), (255, 255, 255))
        self.blit_text(f'HS : {int(Bird.high_score)}', (WORLD['WIDTH']-100, 30), (255, 255, 255))
        self.blit_text(f'BA : {int(Bird.alive_birds)}', (WORLD['WIDTH']-100, 50), (255, 255, 255))
        self.blit_text(f'GEN : {int(self.current_generation)}', (WORLD['WIDTH']-100, 70), (255, 255, 255))

    def blit_text(self, text, pos, color):
        """
            Blits test on the screen using specified text string, position and color.
        """
        score_surface = self.game_font.render(text, True, color)
        score_rect = score_surface.get_rect(center = pos)
        self.screen.blit(score_surface, score_rect)

    def move_pipes(self):
        """
            Shifts all the pipes to the left.
        """
        for pipe in self.pipe_list:
            pipe.centerx -= PIPE['PIPE_SPEED']

    def draw_pipes(self):
        """
            Draws the bottom&top pipes on the screen.
        """
        for pipe in self.pipe_list:
            if pipe.bottom >= 512:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

    def reset_pipes(self):
        """
            Reset the pipes to initial position.
        """
        for i in range(3):
            self.pipe_list[i*2], self.pipe_list[(i*2)+1] = self.create_pipe(i)

    def model_mutate(self, weights_list):
        """
            Mutate the input weights.
            80% chance mutation. Mutation between [-0.5; 0.5[, uniform distribution.
        """
        mutated_weights = [weights_list[0].copy(), weights_list[1].copy()]

        for weights in mutated_weights:
            for weight in weights:
                for i, _ in enumerate(weight):
                    if np.random.uniform(0, 1) > 0.8:
                        change = np.random.uniform(-0.5,0.5)
                        weight[i] += change
        return mutated_weights

    def generate_pop(self, mutated=False):
        """
            Generate population randomly, or from a bird that we evolve.
        """
        gen_birds = []

        for _ in range(BIRD['POP_SIZE']):
            if not mutated:
                gen_birds.append(Bird([np.random.randn(4, 7), np.random.randn(7, 1)]))
            else:
                gen_birds.append(Bird(self.model_mutate(self.best_bird_weights)))

        return gen_birds

    def save_weights(self, weights_list, filename):
        """
            Save the weights as 1 file per layer weights.
            Not compatible with more than 2 layers.
        """
        np.savetxt(filename+".001", weights_list[0])
        np.savetxt(filename+".002", weights_list[1])

    def load_weights(self, filename):
        """
            Returns loaded weights, already reshaped and ready to use.
            Not compatible with more than 2 layers.
        """
        loaded_weights = []

        loaded_weights.append(np.loadtxt(filename+".001"))
        loaded_weights[0] = loaded_weights[0].reshape(BIRD['WEIGHTS1'][0] , BIRD['WEIGHTS1'][1])

        loaded_weights.append(np.loadtxt(filename+".002"))
        loaded_weights[1] = loaded_weights[1].reshape(BIRD['WEIGHTS2'][0] , BIRD['WEIGHTS2'][1])

        return loaded_weights


if __name__ == "__main__":
    game = FlappBird()
    game.run()
