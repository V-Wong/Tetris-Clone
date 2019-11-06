import pygame
import random
import time
import sys


class Game:
    def __init__(self, width, height):
        self.grid_width = width
        self.grid_height = height
        self.score = 0

        self.grid = [[0 for i in range(self.grid_width)] for j in range(self.grid_height)]

        self.screen = pygame.display.set_mode(
                    (self.grid_width * 50 + 400, self.grid_height * 50))

        pygame.key.set_repeat(100, 50)
    
        self.tetromino_types = [T, L, Line, Square]

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
                    elif event.key == pygame.K_c:
                        if hold:
                            tetromino, hold = hold.__class__(self.screen), tetromino.__class__(self.screen)
                        else:
                            hold = tetromino.__class__(self.screen)
                            tetromino = random.choice(self.tetromino_types)(self.screen)
                    elif event.key == pygame.K_SPACE:
                        tetromino.update_position(0, 1)

            if not self.calculate_collision(tetromino, 0, 1): 
                if cycle % 100 == 0:
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
                self.score += 100

            cycle += 1

            if tetromino:
                self.update_screen(tetromino, next_tetromino, hold)
            
    def update_screen(self, tetromino, next_tetromino, hold):
        self.screen.fill((40, 40, 40))
        self.draw_panel()
        self.draw_score()
        self.draw_next_tetromino(next_tetromino)
        if hold:
            self.draw_hold(hold)
        tetromino.draw_moving_block()
        self.draw_stationary_blocks()
        pygame.display.update()

    def draw_panel(self):
        pygame.draw.rect(self.screen, (54, 54, 54), 
                        (self.grid_width * 50, 0, 400, self.grid_height * 50))
        pygame.font.init()

        pygame.draw.rect(self.screen, (40, 40, 40), 
                        ((self.grid_width + 1) * 50, 325, 300, 300))
        pygame.font.init()

        pygame.draw.rect(self.screen, (40, 40, 40), 
                        ((self.grid_width + 1) * 50, 675, 300, 300))
        pygame.font.init()

        myfont = pygame.font.SysFont("Arial", 70)
        letter = myfont.render(f"Tetris-Clone", 0, (255, 255, 255))
        self.screen.blit(letter, (self.grid_width * 50 + 15, 100))

        myfont = pygame.font.SysFont("Arial", 25)
        letter = myfont.render(f"V-Wong.github.io", 0, (255, 255, 255))
        self.screen.blit(letter, (self.grid_width * 50 + 110, 180))

        myfont = pygame.font.SysFont("Arial", 40)
        letter = myfont.render(f"Next", 0, (255, 255, 255))
        self.screen.blit(letter, ((self.grid_width + 3) * 50, (self.grid_height - 13) * 50))

        myfont = pygame.font.SysFont("Arial", 40)
        letter = myfont.render(f"Hold", 0, (255, 255, 255))
        self.screen.blit(letter, ((self.grid_width + 3) * 50, (self.grid_height - 6) * 50))

    def draw_score(self):
        pygame.font.init()
        myfont = pygame.font.SysFont("Arial", 40)
        letter = myfont.render(f"Score: {self.score}", 0, (255, 255, 255))
        self.screen.blit(letter, (self.grid_width * 50 + 130, 225))

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

    def rotate(self):
        pass


class Square(Tetromino):
    def __init__(self, screen):
        self.blocks =  [[5, 0], [5, 1], [6,0], [6, 1]]
        self.screen = screen
        self.colour = (0, 255, 255)
        self.rotation = 0


class Line(Tetromino):
    def __init__(self, screen):
        self.blocks =  [[5, 0], [5, 1], [5, 2], [5, 3]]
        self.screen = screen
        self.colour = (255, 0, 0)
        self.rotation = 0

    def rotate(self):
        if self.rotation % 4 == 0:
            y = self.blocks[3][1]

            i = -1
            for block in self.blocks:
                block[0], block[1] = block[0] + i, y
                i += 1

        elif self.rotation % 4 == 1:
            x = self.blocks[2][0]

            i = -3
            for block in self.blocks:
                block[0], block[1] = x, block[1] + i
                i += 1
            
        elif self.rotation % 4 == 2:
            y = self.blocks[3][1]

            i = -2
            for block in self.blocks:
                block[0], block[1] = block[0] + i, y
                i += 1

        elif self.rotation % 4 == 3:
            x = self.blocks[1][0]

            i = -3
            for block in self.blocks:
                block[0], block[1] = x, block[1] + i
                i += 1

        self.rotation += 1
        print(self.rotation)

class T(Tetromino):
    def __init__(self, screen):
        self.blocks =  [[5, 0], [6, 0], [7, 0], [6, 1]]
        self.screen = screen
        self.colour = (0, 255, 0)
        self.rotation = 0

    def rotate(self):
        if self.rotation % 4 == 0:
            self.blocks[0] = [self.blocks[0][0] + 1, self.blocks[0][1] - 1]
            self.blocks[2] = [self.blocks[2][0] - 1, self.blocks[2][1] + 1]
            self.blocks[3] = [self.blocks[3][0] - 1, self.blocks[3][1] - 1]
        elif self.rotation % 4 == 1:
            self.blocks[0] = [self.blocks[0][0] + 1, self.blocks[0][1] + 1]
            self.blocks[2] = [self.blocks[2][0] - 1, self.blocks[2][1] - 1]
            self.blocks[3] = [self.blocks[3][0] + 1, self.blocks[3][1] - 1]
        elif self.rotation % 4 == 2:
            self.blocks[0] = [self.blocks[0][0] - 1, self.blocks[0][1] + 1]
            self.blocks[2] = [self.blocks[2][0] + 1, self.blocks[2][1] - 1]
            self.blocks[3] = [self.blocks[3][0] + 1, self.blocks[3][1] + 1]
        elif self.rotation % 4 == 3:
            self.blocks[0] = [self.blocks[0][0] - 1, self.blocks[0][1] - 1]
            self.blocks[2] = [self.blocks[2][0] + 1, self.blocks[2][1] + 1]
            self.blocks[3] = [self.blocks[3][0] - 1, self.blocks[3][1] + 1]

 
        self.rotation += 1

class L(Tetromino):
    def __init__(self, screen):
        self.blocks =  [[5, 0], [6, 0], [7, 0], [5, 1]]
        self.screen = screen
        self.colour = (0, 0, 255)
        self.rotation = 0

    def rotate(self):
        pivot = self.blocks[0]

        if self.rotation % 4 == 0:
            self.blocks[1] = [pivot[0], pivot[1] - 1]
            self.blocks[2] = [pivot[0], pivot[1] - 2]
            self.blocks[3] = [pivot[0] - 1, pivot[1]]

        elif self.rotation % 4 == 1:
            self.blocks[1] = [pivot[0] + 1, pivot[1]]
            self.blocks[2] = [pivot[0], pivot[1] - 1]
            self.blocks[3] = [pivot[0] + 2, pivot[1]]

        elif self.rotation % 4 == 2:
            self.blocks[1] = [pivot[0] + 1, pivot[1]]
            self.blocks[2] = [pivot[0], pivot[1] + 1]
            self.blocks[3] = [pivot[0], pivot[1] + 2]

        elif self.rotation % 4 == 3:
            self.blocks[1] = [pivot[0], pivot[1] + 1]
            self.blocks[2] = [pivot[0] - 1, pivot[1]]
            self.blocks[3] = [pivot[0] - 2, pivot[1]]

        self.rotation += 1

if __name__ == "__main__":
    while True:
        game = Game(12, 20)
        game.run()
        input()