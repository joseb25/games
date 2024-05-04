# -*- coding: utf-8 -*-
"""
Created on Sat May  4 11:19:00 2024

@author: JBN
"""

import pygame
import time
import random

# Initialize pygame
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1000, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont("comicsans", 30)
pygame.display.set_caption("My First Game")

# Load and scale the spaceship image
spaceship = pygame.image.load("Alien-Battleship.png")
spaceship = pygame.transform.scale(spaceship, (50, 50))
spaceship_width, spaceship_height = spaceship.get_size()

STAR_WIDTH = 8
STAR_HEIGHT = 16
STAR_VEL = 3

PLAYER_VEL = 5

# Try loading the image
try:
    BG = pygame.image.load("gameUniverse.jpeg")
except pygame.error as e:
    print(f"Unable to load image: {e}")
    BG = pygame.Surface((WIDTH, HEIGHT))
    BG.fill((0, 0, 0))  # Set to black if the image is not found

def draw(spaceship_pos, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    WIN.blit(spaceship, spaceship_pos)

    time_text = FONT.render(f"Time: {round(elapsed_time)}s",  1, "white")
    WIN.blit(time_text, (10,  10))

    for star in stars:
        pygame.draw.rect(WIN, pygame.Color("white"), star)

    pygame.display.update()

def main():
    run = True

    spaceship_pos = [WIDTH // 2 - spaceship_width // 2, HEIGHT - spaceship_height]
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(5):
                star_x  =   random.randint(0, WIDTH - STAR_WIDTH)
                star  =  pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)  # Ensure the value doesn't drop below 200
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_pos[0] - PLAYER_VEL > 0:  # Check left boundary
            spaceship_pos[0] -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and spaceship_pos[0] + PLAYER_VEL + spaceship_width < WIDTH:  # Check right boundary
            spaceship_pos[0] += PLAYER_VEL    

        spaceship_rect = pygame.Rect(spaceship_pos[0], spaceship_pos[1], spaceship_width, spaceship_height)

        for star in stars[:]:
            star.y += STAR_VEL  # Move stars downward

            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(spaceship_rect):  # Check for collision with spaceship
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("Game Over!", 1, "red")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(spaceship_pos, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()
