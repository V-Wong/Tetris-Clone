import pygame
from pygame.locals import *
import random
import time


class Game:
    def __init__(self, width, height):
        self.grid_width = width
        self.grid_height = height

        self.y = 0
        self.x = self.grid_width/2

        self.grid = [[i for i in range(self.grid_width)] for j in range(self.grid_height)]

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

            if not self.calculate_collision(0, 2): 
                time.sleep(0.05)
                self.y += 1
                self.update_screen()

    def update_screen(self):
        self.screen.fill((0,0,0))
        self.draw_block()
        pygame.display.update()

    def draw_block(self):
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (self.x * 50, self.y * 50, 50, 50))

    def calculate_collision(self, dx, dy):
        return (not (0 <= self.x + dx < self.grid_width)
                or not (0 <= self.y + dy <= self.grid_height))


if __name__ == "__main__":
    game = Game(10, 20)
    game.run()