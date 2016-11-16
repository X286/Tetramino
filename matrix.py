import pygame
import random

class GameObject (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color='#FF0000'):
        super(GameObject, self).__init__()

        self.image = pygame.Surface([width, height])

        if type(color) == str:
            self.color = pygame.Color(color)
        else:
            self.color = color
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def loadImage(self, path_to_img):
        x, y = self.rect.x, self.rect.y
        self.image = pygame.image.load(path_to_img)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def setSurface(self, surface):
        x, y = self.rect.x, self.rect.y
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


    def draw (self,screen):
        screen.blit (self.image, (self.rect.x, self.rect.y))


class Tetra (GameObject):
    def __init__(self, x, y, width, height, color='#FF0000'):
        super(Tetra, self).__init__(x, y, width, height, color=color)

    def update (self, where, speed):
        if where == 'left':
            self.rect.x -= speed
        if where == 'right':
            self.rect.x += speed
        if where == 'none':
            self.rect.y += speed

    def draw(self, screen):

        screen.blit(self.image, (self.rect.x, self.rect.y))


class Matrix (object):

    def __init__(self, x, y, width, height, offset, matrix):
        self.x, self.x0 = x, x
        self.y, self.y0 = y, y
        self.width, self.height, self.offset = width, height, offset
        self.matrix = matrix[0]
        self.matrix_name = matrix[1]
        self.get_matrix()

    def get_matrix(self):
        for k, i in enumerate (self.matrix):
            for z, j in enumerate (i):

                j[0] = self.x+z*(self.width + self.offset)
                j[1] = self.y+k*(self.height + self.offset)

    def move_matrixY(self, speed, where):
        if (where == 'down'):
            self.y += speed
            self.get_matrix()

        if (where == 'up'):
            self.y -= speed
            self.get_matrix()

    def move_matrixX(self, speed,  where):
        if (where == 'left'):
            self.x -= speed
            self.get_matrix()
        if (where == 'right'):
            self.x += speed
            self.get_matrix()



    def drop_to_default(self):
        self.x = self.x0
        self.y = self.y0


class Figure (object):

    def __init__(self, matrix):
        self.matrix = matrix
        self.figure = pygame.sprite.Group ()
        self.rotateCount = 0
        self.color = (random.randint (200,255), random.randint (100,250), random.randint (0,10))
        for k, i in enumerate(self.matrix.matrix):
            for z, j in enumerate(i):
                if j[2] == 1:
                    self.figure.add(Tetra (j[0], j[1], self.matrix.width, self.matrix.height, color=self.color))

    def moveLine_left(self, speed):
        self.matrix.move_matrixX(speed, 'left')
        self.figure = pygame.sprite.Group()
        for k, i in enumerate(self.matrix.matrix):
            for z, j in enumerate(i):
                if j[2] == 1:
                    self.figure.add(Tetra(j[0], j[1], self.matrix.width, self.matrix.height , color=self.color))

    def moveLine_right(self, speed):
        self.matrix.move_matrixX(speed, 'right')
        self.figure = pygame.sprite.Group()
        for k, i in enumerate(self.matrix.matrix):
            for z, j in enumerate(i):
                if j[2] == 1:
                    self.figure.add(Tetra(j[0], j[1], self.matrix.width, self.matrix.height, color=self.color))

    def moveLine_down(self, speed):
        self.matrix.move_matrixY(speed, 'down')
        self.figure = pygame.sprite.Group()
        for k, i in enumerate(self.matrix.matrix):
            for z, j in enumerate(i):
                if j[2] == 1:
                    self.figure.add(Tetra(j[0], j[1], self.matrix.width, self.matrix.height, color=self.color))

    def moveLine_up(self, speed):
        self.matrix.move_matrixY(speed, 'up')
        self.figure = pygame.sprite.Group()
        for k, i in enumerate(self.matrix.matrix):
            for z, j in enumerate(i):
                if j[2] == 1:
                    self.figure.add(Tetra(j[0], j[1], self.matrix.width, self.matrix.height, color=self.color))

    def rotate(self, neworder):
        self.figure = pygame.sprite.Group()
        for k, i in enumerate(self.matrix.matrix):
            for z, j in enumerate(i):
                    j[2] = neworder[k, z]
                    if j[2] == 1:
                        self.figure.add(Tetra(j[0], j[1], self.matrix.width, self.matrix.height, color=self.color))

class Text (object):
    def __init__(self, size, color= '#FF0000'):
        pygame.font.init()
        self.__myfont = pygame.font.SysFont('verdana', size)
        self.text = 'Score: 0'
        self.colour = pygame.Color(color)
        self.isBold = 0

    def writeOn (self, scr, (x, y)):
        sruf = self.__myfont.render(self.text, self.isBold, self.colour)
        scr.blit(sruf, (x, y))


class GroupSprt (object):
    def move_all_down(self, group, speed):
        for sprite in group:
            sprite.rect.y +=speed


class Net (object):
    def __init__(self, netoffsetX, netoffsetY, width, height, line_width, offset = 10, color = '#C0C0C0'):
        self.group = pygame.sprite.Group()
        for x in range (netoffsetX, netoffsetX+width, offset):
            self.group.add(GameObject (x, netoffsetY, line_width, height, color))

        for y in range(netoffsetY, netoffsetY + height, offset):
            self.group.add(GameObject(netoffsetX, y, width, line_width, color))

    def draw (self, screen):
        self.group.draw(screen)

