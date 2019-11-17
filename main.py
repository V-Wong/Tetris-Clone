import pygame
from pygame.locals import *
import random
import time
import sys

import tetrominos as Tetrominos


class Game:
    def __init__(self, width, height):
        self.grid_width = width
        self.grid_height = height
        self.score = 0

        self.grid = [[0 for i in range(self.grid_width)] for j in range(self.grid_height)]

        self.screen = pygame.display.set_mode(
                    ((self.grid_width + 4) * 50, self.grid_height * 50))

        pygame.key.set_repeat(100, 50)
    
        self.tetromino_types = [Tetrominos.L, Tetrominos.T, Tetrominos.Square, Tetrominos.Line]

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
                    if event.key == pygame.K_RIGHT:
                        if not self.calculate_collision(tetromino, 1, 0): 
                            tetromino.update_position(1, 0)
                    elif event.key == pygame.K_LEFT:
                        if not self.calculate_collision(tetromino, -1, 0): 
                            tetromino.update_position(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        if not self.calculate_collision(tetromino, 0, 1): 
                            tetromino.update_position(0, 1)
                    elif event.key == pygame.K_z:
                        tetromino.rotate()
                        if self.calculate_collision(tetromino, 0, 0):
                            tetromino.rotate()
                            tetromino.rotate()
                            tetromino.rotate()
                    elif event.key == pygame.K_c:
                        if hold:
                            tetromino, hold = hold.__class__(self.screen), tetromino.__class__(self.screen)
                        else:
                            hold = tetromino.__class__(self.screen)
                            tetromino = random.choice(self.tetromino_types)(self.screen)

            if not self.calculate_collision(tetromino, 0, 1): 
                if cycle % 25 == 0:
                    tetromino.update_position(0, 0)
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
                self.update_screen(tetromino, next_tetromino, hold)
            
    def update_screen(self, tetromino, next_tetromino, hold):
        self.screen.fill((40, 40, 40))
        self.draw_next_tetromino(next_tetromino)
        self.draw_side_panel(hold)
        tetromino.draw_moving_block()
        self.draw_stationary_blocks()
        pygame.display.update()


    def draw_side_panel(self, hold):
        pygame.draw.rect(self.screen, (54, 54, 54), 
                (self.grid_width * 50, 0, 400, self.grid_height * 50))

        pygame.draw.rect(self.screen, (255, 255, 255), 
                (self.grid_width * 50, self.grid_height * 50 - 100, 200, 100))

    def draw_next_tetromino(self, next_tetromino):
        for block in next_tetromino.blocks:
            pygame.draw.rect(self.screen, next_tetromino.colour, 
                            ((block[0] + 10) * 50, (block[1] + 9) * 50, 50, 50))
            pygame.draw.rect(self.screen, (255, 255, 255), 
                            ((block[0] + 10) * 50, (block[1] + 9) * 50, 50, 50), 1)

    def draw_hold(self, hold):
        for block in hold.blocks:
            pygame.draw.rect(self.screen, hold.colour, 
                            ((block[0] + 10) * 50, (block[1] + 16) * 50, 50, 50))
            pygame.draw.rect(self.screen, (255, 255, 255), 
                            ((block[0] + 10) * 50, (block[1] + 16) * 50, 50, 50), 1)


    def store_block(self, tetromino):
        for block in tetromino.blocks:
            self.grid[block[1]][block[0]] = tetromino.colour

    def draw_stationary_blocks(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col]:
                    pygame.draw.rect(self.screen, self.grid[row][col], 
                                    (col * 50, row * 50, 50, 50))
                    pygame.draw.rect(self.screen, (255, 255, 255), 
                                    (col * 50, row * 50, 50, 50), 1)

    def calculate_collision(self, tetromino, dx, dy):
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
        game = Game(12, 20)
        game.run()
        input()