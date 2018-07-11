import cell
import sys
import numpy
import pygame
pygame.init()

w = 30
size = width, height = 601, 601
cols = int(width / w)
rows = int(height / w)

totalMines = 25
canvas = pygame.display.set_mode(size)
pygame.display.set_caption('Minesweeper')

grid = [[None for i in range(cols)] for j in range(rows)]
options = list()

for i in range(cols):
    for j in range(rows):
        grid[i][j] = cell.Cell(i, j, w, grid)
        options.append([i, j])

mines = numpy.random.choice(range(len(options)), totalMines, replace=False)
for m in mines:
    i = options[m][0]
    j = options[m][1]
    grid[i][j].mine = True

for i in range(cols):
    for j in range(rows):
        grid[i][j].countMines()

def gameOver():
    for i in range(cols):
        for j in range(rows):
            grid[i][j].revealed = True

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                for i in range(cols):
                    for j in range(rows):
                        if grid[i][j].contains(mouseX, mouseY):
                            grid[i][j].reveal()
                            if grid[i][j].mine:
                                gameOver()

        canvas.fill((255, 255, 255))
        for i in range(cols):
            for j in range(rows):
                grid[i][j].show(canvas)
        pygame.display.update()

if __name__ == '__main__':
    main()