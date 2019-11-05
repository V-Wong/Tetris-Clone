import pygame
from pygame.locals import *
import random
import time
import sys


class Game:
    def __init__(self, width, height):
        self.grid_width = width
        self.grid_height = height

        self.grid = [[0 for i in range(self.grid_height)] for j in range(self.grid_width)]

        self.screen = pygame.display.set_mode(
                    (self.grid_width * 50, self.grid_height * 50))

        self.tetromino_types = [Square, Line, T, L]

    def run(self):
        running = True

        tetromino = None
        while running:
            if not tetromino:
                tetromino = random.choice(self.tetromino_types)(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.calculate_collision(tetromino, 1, 0): 
                            break
                        tetromino.update_position(1, 0)
                    elif event.key == pygame.K_LEFT:
                        if self.calculate_collision(tetromino, -1, 0): 
                            break
                        tetromino.update_position(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        if self.calculate_collision(tetromino, 0, 1): 
                            break
                        tetromino.update_position(0, 1)
                    self.update_screen(tetromino)

            if not self.calculate_collision(tetromino, 0, 1): 
                time.sleep(0.05)
                tetromino.update_position(0, 1)
                self.update_screen(tetromino)
            else:
                self.store_block(tetromino)
                tetromino = None
            
            if self.lose_checking():
                running = False

    def update_screen(self, tetromino):
        self.screen.fill((0,0,0))
        tetromino.draw_moving_block()
        self.draw_stationary_blocks()
        pygame.display.update()

    def store_block(self, tetromino):
        for block in tetromino.blocks:
            self.grid[block[0]][block[1]] = tetromino.colour

    def draw_stationary_blocks(self):
        for col in range(len(self.grid)):
            for row in range(len(self.grid[col])):
                if self.grid[col][row]:
                    pygame.draw.rect(self.screen, self.grid[col][row], 
                                    (col * 50, row * 50, 50, 50))
                    pygame.draw.rect(self.screen, (255, 255, 255), 
                                    (col * 50, row * 50, 50, 50), 1)

    def calculate_collision(self, tetromino, dx, dy):
        for block in tetromino.blocks:
            if (not (0 <= block[0] + dx < self.grid_width)
                    or not (0 <= block[1] + dy < self.grid_height)
                    or self.grid[block[0] + dx][block[1] + dy]):
                return True
        else:
            return False

    def lose_checking(self):
        for col in self.grid:
            if col[0] == 1:
                return True
        else:
            return False


class Tetromino:
    def __init__(self, screen):
        pass

    def update_position(self, dx, dy):
        for block in self.blocks:
            block[0] += dx
            block[1] += dy

    def draw_moving_block(self):
        for block in self.blocks:
            pygame.draw.rect(self.screen, self.colour, 
                            (block[0] * 50, block[1] * 50, 50, 50))
            pygame.draw.rect(self.screen, (255, 255, 255), 
                            (block[0] * 50, block[1] * 50, 50, 50), 1)


class Square(Tetromino):
    def __init__(self, screen):
        self.blocks =  [[5, 0], [5, 1], [6,0], [6, 1]]
        self.screen = screen
        self.colour = (0, 255, 255)


class Line(Tetromino):
    def __init__(self, screen):
        self.blocks =  [[5, 0], [5, 1], [5, 2], [5, 3]]
        self.screen = screen
        self.colour = (255, 0, 0)


class T(Tetromino):
    def __init__(self, screen):
        self.blocks =  [[5, 0], [6, 0], [7, 0], [6, 1]]
        self.screen = screen
        self.colour = (0, 255, 0)


class L(Tetromino):
    def __init__(self, screen):
        self.blocks =  [[5, 0], [6, 0], [7, 0], [5, 1]]
        self.screen = screen
        self.colour = (0, 0, 255)


if __name__ == "__main__":
    game = Game(12, 20)
    game.run()