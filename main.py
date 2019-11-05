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

    def run(self):
        running = True

        block = None
        while running:
            if not block:
                block = Square(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.calculate_collision(block, 1, 0): 
                            break
                        block.update_position(1, 0)
                    elif event.key == pygame.K_LEFT:
                        if self.calculate_collision(block, -1, 0): 
                            break
                        block.update_position(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        if self.calculate_collision(block, 0, 1): 
                            break
                        block.update_position(0, 1)
                    self.update_screen(block)

            if not self.calculate_collision(block, 0, 1): 
                time.sleep(0.05)
                block.update_position(0, 1)
                self.update_screen(block)
            else:
                self.store_block(block)
            
            if self.lose_checking():
                running = False

            print(block.blocks)

    def update_screen(self, block):
        self.screen.fill((0,0,0))
        block.draw_moving_block()
        self.draw_stationary_blocks()
        pygame.display.update()

    def store_block(self, tetromino):
        for block in tetromino.blocks:
            self.grid[block[0]][block[1]] = 1

    def draw_stationary_blocks(self):
        for col in range(len(self.grid)):
            for row in range(len(self.grid[col])):
                if self.grid[col][row] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255), 
                                    (col * 50, row * 50, 50, 50))

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
                print("You lose")
                return True
        else:
            return False

class Square:
    def __init__(self, screen):
        self.blocks =  [[5, 0], [5, 1], [6,0], [6, 1]]
        self.screen = screen

    def update_position(self, dx, dy):
        for block in self.blocks:
            block[0] += dx
            block[1] += dy

    def draw_moving_block(self):
        for block in self.blocks:
            pygame.draw.rect(self.screen, (255, 255, 255), 
                            (block[0] * 50, block[1] * 50, 50, 50))


if __name__ == "__main__":
    game = Game(10, 20)
    game.run()