import pygame
from pygame.locals import *
import random
import time
import sys


class Game:
    def __init__(self, width, height):
        self.grid_width = width
        self.grid_height = height

        self.y = 0
        self.x = 5

        self.grid = [[0 for i in range(self.grid_height)] for j in range(self.grid_width)]

        self.screen = pygame.display.set_mode(
                    (self.grid_width * 50, self.grid_height * 50))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.calculate_collision(1, 0): 
                            break
                        self.x += 1
                    elif event.key == pygame.K_LEFT:
                        if self.calculate_collision(-1, 0): 
                            break
                        self.x -= 1
                    elif event.key == pygame.K_DOWN:
                        if self.calculate_collision(0, 1): 
                            break
                        self.y += 1
                    self.update_screen()

            if not self.calculate_collision(0, 1): 
                time.sleep(0.05)
                self.y += 1
                self.update_screen()
            else: 
                self.store_block()
                self.x = 5
                self.y = 0


    def update_screen(self):
        self.screen.fill((0,0,0))
        self.draw_moving_block()
        self.draw_stationary_blocks()
        pygame.display.update()

    def draw_moving_block(self):
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (self.x * 50, self.y * 50, 50, 50))

    def store_block(self):
        self.grid[self.x][self.y] = 1

    def draw_stationary_blocks(self):
        for col in range(len(self.grid)):
            for row in range(len(self.grid[col])):
                if self.grid[col][row] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255), 
                                    (col * 50, row * 50, 50, 50))

    def calculate_collision(self, dx, dy):
        return (not (0 <= self.x + dx < self.grid_width)
                or not (0 <= self.y + dy < self.grid_height)
                or self.grid[self.x + dx][self.y + dy])


if __name__ == "__main__":
    game = Game(10, 20)
    game.run()