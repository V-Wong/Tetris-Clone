import pygame

GRID_SIZE = 75


class Tetromino:
    def __init__(self, screen: pygame.display):
        self.blocks = []
        self.screen = screen
        self.colour = ()

    def update_position(self, dx: int, dy: int):
        for block in self.blocks:
            block[0] += dx
            block[1] += dy

    def draw_moving_block(self):
        for block in self.blocks:
            pygame.draw.rect(self.screen, self.colour, 
                            (block[0] * GRID_SIZE, block[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.screen, (255, 255, 255), 
                            (block[0] * GRID_SIZE, block[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def rotate(self):
        pass


class Square(Tetromino):
    def __init__(self, screen: pygame.display):
        self.blocks =  [[6, 0], [6, 1], [7,0], [7, 1]]
        self.screen = screen
        self.colour = (0, 255, 255)
        self.rotation = 0
        

class Line(Tetromino):
    def __init__(self, screen: pygame.display):
        self.blocks =  [[6, 0], [6, 1], [6, 2], [6, 3]]
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
    def __init__(self, screen: pygame.display):
        self.blocks =  [[6, 0], [7, 0], [8, 0], [7, 1]]
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
        self.blocks =  [[6, 0], [7, 0], [8, 0], [8, 1]]
        self.screen = screen
        self.colour = (0, 0, 255)
        self.rotation = 0

    def rotate(self):
        pivot = self.blocks[1]

        if self.rotation % 4 == 0:
            self.blocks[0] = [pivot[0], pivot[1] - 1]
            self.blocks[2] = [pivot[0] - 1, pivot[1] - 1]
            self.blocks[3] = [pivot[0], pivot[1] + 1]

        elif self.rotation % 4 == 1:
            self.blocks[0] = [pivot[0] - 1, pivot[1]]
            self.blocks[2] = [pivot[0] + 1, pivot[1] - 1]
            self.blocks[3] = [pivot[0] + 1, pivot[1]]

        elif self.rotation % 4 == 2:
            self.blocks[0] = [pivot[0] + 1, pivot[1] - 1]
            self.blocks[2] = [pivot[0], pivot[1] - 1]
            self.blocks[3] = [pivot[0], pivot[1] + 1]

        elif self.rotation % 4 == 3:
            self.blocks[0] = [pivot[0] + 1, pivot[1] + 1]
            self.blocks[2] = [pivot[0] - 1, pivot[1]]
            self.blocks[3] = [pivot[0] + 1, pivot[1]]

        self.rotation += 1