import pygame
from pygame.locals import *
import random
import time
import sys

import tetrominos as Tetrominos
from tetrominos import Tetromino

GRID_SIZE = 72
BLACK = (255, 255, 255)


class Game:
    def __init__(self, width: int, height: int):
        self.grid_width = width
        self.grid_height = height
        self.score = 0

        self.grid = [[0 for _ in range(self.grid_width)]
                     for _ in range(self.grid_height)]

        self.screen = pygame.display.set_mode((self.grid_width * GRID_SIZE + 1550 + 144,
                                               self.grid_height * GRID_SIZE))

        pygame.key.set_repeat(100, 50)
    
        self.tetromino_types = [Tetrominos.L, Tetrominos.T, 
                                Tetrominos.Square, Tetrominos.Line]

    def run(self):
        running = True
        tetromino = None
        hold = None
        cycle = 0

        next_tetromino = random.choice(self.tetromino_types)(self.screen)

        while running:
            if not tetromino:
                tetromino = random.choice(self.tetromino_types)(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN):
                        self.move_piece(tetromino, event.key)
                    elif event.key == pygame.K_z:
                        self.rotate_piece(tetromino)
                    elif event.key == pygame.K_c:
                        if hold:
                            tetromino, hold = hold.__class__(self.screen), tetromino.__class__(self.screen)
                        else:
                            hold = tetromino.__class__(self.screen)
                            tetromino = random.choice(self.tetromino_types)(self.screen)

            if not self.calculate_collision(tetromino, 0, 1): 
                if cycle % 25 == 0:
                    tetromino.update_position(0, 1)
            else:
                self.store_block(tetromino)
                tetromino = next_tetromino
                next_tetromino = random.choice(self.tetromino_types)(self.screen)
            
            if self.lose_checking():
                running = False

            row = self.row_checking()
            if row:
                del self.grid[row]
                self.grid.insert(0, [0 for i in range(self.grid_width)])

            cycle += 1

            if tetromino:
                self.update_screen(tetromino, next_tetromino)
            
    def update_screen(self, tetromino: Tetromino, next_tetromino: Tetromino):
        self.screen.fill((40, 40, 40))
        tetromino.draw_moving_block()
        self.draw_stationary_blocks()
        pygame.display.update()

    def move_piece(self, tetromino: Tetromino, key: pygame.key):
        if key == pygame.K_RIGHT:
            if not self.calculate_collision(tetromino, 1, 0): 
                tetromino.update_position(1, 0)
        elif key == pygame.K_LEFT:
            if not self.calculate_collision(tetromino, -1, 0): 
                tetromino.update_position(-1, 0)
        elif key == pygame.K_DOWN:
            if not self.calculate_collision(tetromino, 0, 1): 
                tetromino.update_position(0, 1)

    def rotate_piece(self, tetromino: Tetromino):
        tetromino.rotate()
        if self.calculate_collision(tetromino, 0, 0):
            tetromino.rotate()
            tetromino.rotate()
            tetromino.rotate()

    def store_block(self, tetromino: Tetromino):
        for block in tetromino.blocks:
            self.grid[block[1]][block[0]] = tetromino.colour

    def draw_stationary_blocks(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col]:
                    pygame.draw.rect(self.screen, self.grid[row][col], 
                                     (col * GRID_SIZE, 
                                      row * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(self.screen, BLACK, 
                                     (col * GRID_SIZE,
                                      row * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE), 1)

    def calculate_collision(self, tetromino: Tetromino, dx: int, dy: int):
        for block in tetromino.blocks:
            if (not (0 <= block[0] + dx < self.grid_width)
                    or not (0 <= block[1] + dy < self.grid_height)
                    or self.grid[block[1] + dy][block[0] + dx]):
                return True
        else:
            return False

    def row_checking(self):
        for row in range(len(self.grid)):
            if all(self.grid[row]):
                return row
        else:
            return None

    def lose_checking(self):
        for col in self.grid[0]:
            if col:
                return True
        else:
            return False


if __name__ == "__main__":
    while True:
        game = Game(10, 20)
        game.run()
        input()