import numpy
import pygame
pygame.init()
pygame.font.init()

class Cell(object):
    def __init__(self, i, j, w, mesh):
        self.i = i
        self.j = j
        self.x = i * w
        self.y = j * w
        self.w = w
        self.nhbCount = 0
        self.mine = False
        self.revealed = False
        self.flagged = False
        self.mesh = mesh

    def countMines(self):
        rows = len(self.mesh)
        cols = len(self.mesh[0])

        if self.mine:
            return None

        total = 0

        for xoff in range(-1, 2):
            for yoff in range(-1, 2):
                i = self.i + xoff
                j = self.j + yoff
                if (i > -1 and i < rows and j > -1 and j < cols):
                    nhb = self.mesh[i][j]
                    if nhb.mine:
                        total += 1
        self.nhbCount = total

    def show(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.w), 2)
        if self.flagged:
            pygame.draw.rect(screen, (245, 152, 0), (self.x, self.y, self.w, self.w))
            pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.w), 2)
        if self.revealed:
            if self.mine:
                pygame.draw.circle(screen, (127, 127, 127), (int(self.x + self.w*0.5), int(self.y + self.w*0.5)), int(self.w*0.25))
                pygame.draw.circle(screen, (0, 0, 0), (int(self.x + self.w*0.5), int(self.y + self.w*0.5)), int(self.w*0.25), 1)
            else:
                pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.w, self.w))
                pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.w), 2)
                text = pygame.font.SysFont("Arial", int(self.w * 0.5))
                text.set_bold(True)
                if self.nhbCount > 0:
                    textsurface = text.render(str(self.nhbCount), False, (0, 0, 0))
                    screen.blit(textsurface, (int(self.x + self.w*0.4), int(self.y + self.w*0.25)))
    
    def contains(self, x, y):
        return (x > self.x and x < self.x + self.w and y > self.y and y < self.y + self.w)

    def putFlag(self):
        self.flagged = True

    def removeFlag(self):
        self.flagged = False

    def reveal(self):
        self.revealed = True
        if (self.nhbCount == 0) and (not self.mine):
            self.floodFill()

    def floodFill(self):
        rows = len(self.mesh)
        cols = len(self.mesh[0])
        for xoff in range(-1, 2):
            for yoff in range(-1, 2):
                i = self.i + xoff
                j = self.j + yoff
                if (i > -1 and i < rows and j > -1 and j < cols):
                    nhb = self.mesh[i][j]
                    if (not nhb.mine) and (not nhb.revealed) and (not nhb.flagged):
                        nhb.reveal()
