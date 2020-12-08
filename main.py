"""
    Importing PyGame module.
    PyGame handles graphics and inputs/outputs.
"""
import pygame
import sys
import random
from Bird import Bird

import numpy as np

from settings import *

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, FLOOR_BIAS))
    screen.blit(floor_surface, (floor_x_pos + WIDTH, FLOOR_BIAS))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (350, random_pipe_pos - 150))

    return bottom_pipe, top_pipe

def data_display():
    score_surface = game_font.render(f'GEN HS : {int(best_gen_highscore)}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (WIDTH-100, 10))
    screen.blit(score_surface, score_rect)

    score_surface = game_font.render(f'HS : {int(Bird.high_score)}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (WIDTH-100, 30))
    screen.blit(score_surface, score_rect)

    score_surface = game_font.render(f'BA : {int(Bird.alive_birds)}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (WIDTH-100, 50))
    screen.blit(score_surface, score_rect)

    score_surface = game_font.render(f'GEN : {int(current_generation)}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (WIDTH-100, 70))
    screen.blit(score_surface, score_rect)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

pygame.init()

game_active = True

# Window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load('assets/flappy_bird_icon.png')
pygame.display.set_caption("Flappy Bird AI")
pygame.display.set_icon(icon)

# Setting up framerate
clock = pygame.time.Clock()

# Font
game_font = pygame.font.Font('assets/04B_19.ttf', 20)

# Images import
bg_surface = pygame.image.load('assets/background-day.png').convert()

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0
 
bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_rect = bird_surface.get_rect(center = (50, HEIGHT/2))

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
pipe_height = [200, 300, 400]
pipe_list.extend(create_pipe())

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (WIDTH/2, HEIGHT/2))

def model_crossover(parent1_w, parent2_w):
    new_son1_w = []
    new_son2_w = []

    new_son1_w.append(parent1_w[0])
    new_son2_w.append(parent2_w[0])

    if random.uniform(0,1) > .80:
        gene1 = random.randint(0, len(new_son1_w[0])-1)
        gene2 = random.randint(0, len(new_son1_w[0])-1)

        new_son1_w[0][gene1] = parent2_w[0][gene2]
        new_son2_w[0][gene2] = parent1_w[0][gene1]

    new_son1_w.append(parent1_w[1])
    new_son2_w.append(parent2_w[1])

    if random.uniform(0,1) > .80:
        gene1 = random.randint(0, len(new_son1_w[1])-1)
        gene2 = random.randint(0, len(new_son1_w[1])-1)

        new_son1_w[1][gene1] = parent2_w[1][gene2]
        new_son2_w[1][gene2] = parent1_w[1][gene1]

    return [new_son1_w, new_son2_w]

def model_mutate(weights_list):
    output = [weights_list[0].copy(), weights_list[1].copy()]

    for weights in output:
        for weight in weights:
            for i, w in enumerate(weight):
                if np.random.uniform(0, 1) > 0.8:
                    change = np.random.uniform(-.5,0.5)
                    weight[i] += change
    return output

# Generating first generation of birds
# Birds' nn's weights are random
def generate_pop():
    gen_birds = []
    for _ in range(POP_SIZE):
        weights = [np.random.randn(4, 7), np.random.randn(7, 1)]
        gen_bird = Bird(weights)
        gen_birds.append(gen_bird)
    return gen_birds

def new_bird_batch():
    gen_birds = []
    # son1_w, son2_w = model_crossover(Bird.best_bird1_w, Bird.best_bird2_w)

    gen_birds.append(Bird(best_bird_weights)) # We want to keep the previous parents
    for _ in range(POP_SIZE-1):
        gen_birds.append(Bird(model_mutate(best_bird_weights)))

    return gen_birds

def save_weights(weights_list, filename):
    """
        Make it compatible with N weights
    """
    np.savetxt(filename+".001", weights_list[0])
    np.savetxt(filename+".002", weights_list[1])

def load_weights(filename):
    """
        Change output name, too confusing with funnction's name
    """
    loaded_weights = []

    loaded_weights.append(np.loadtxt(filename+".001"))
    loaded_weights[0] = loaded_weights[0].reshape(WEIGHTS1[0] , WEIGHTS1[1])

    loaded_weights.append(np.loadtxt(filename+".002"))
    loaded_weights[1] = loaded_weights[1].reshape(WEIGHTS2[0] , WEIGHTS2[1])

    return loaded_weights

birds = generate_pop()

best_bird_weights = []
best_bird_fitness = 0

timer = 0

current_generation = 0
best_gen_highscore = 0

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                for bird in birds:
                    bird.jump()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
            if event.key == pygame.K_c:
                # reset
                for bird in birds:
                    if bird.fitness > best_bird_fitness:
                        best_bird_weights = bird.net.weights
                        best_bird_fitness = bird.fitness

                if Bird.high_score > best_gen_highscore:
                    best_gen_highscore = Bird.high_score

                birds.clear()
                birds = new_bird_batch()
                Bird.high_score = 0
                game_active = True
                pipe_list.clear()
                timer = 0
                pipe_list.extend(create_pipe())

                save_weights(best_bird_weights, "weights")
                current_generation += 1

    """
        TODO : Two lists, rather go through the alive_bird_list to avoid iterating over known dead birds.
    """
    for bird in birds:
        bird.make_decision(pipe_list)

    timer += 1
    if timer >= 100:
        pipe_list.extend(create_pipe())
        timer = 0

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        if Bird.alive_birds == 0:
            game_active = False
        for bird in birds:
            bird.update(screen, pipe_list)

        if game_active == False:
            # reset
            """
                Get the bird with the best fitness.
            """
            for bird in birds:
                if bird.fitness > best_bird_fitness:
                    best_bird_weights = bird.net.weights
                    best_bird_fitness = bird.fitness

            if Bird.high_score > best_gen_highscore:
                best_gen_highscore = Bird.high_score

            birds.clear()
            birds = new_bird_batch()
            Bird.high_score = 0
            game_active = True
            pipe_list.clear()
            timer = 0
            pipe_list.extend(create_pipe())

            save_weights(best_bird_weights, "weights")

            current_generation += 1

        # Pipes 
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        data_display()
    else:
        screen.blit(game_over_surface, game_over_rect)

    # Floor
    floor_x_pos -= 1
    draw_floor()

    if floor_x_pos <= -WIDTH:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(1000)

pygame.quit()
