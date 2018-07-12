import cell
import sys
import numpy
import pygame
pygame.init()
pygame.font.init()

totalMines = int(input("Enter the number of mines: "))
cols = int(input("Enter the number of rows: "))
rows = int(input("Enter the number of columns: "))

w = 40
size = width, height = w * rows, w * cols + 35

if totalMines > cols * rows:
    print("ERROR: the number of mines exceeds the number of cells.")
    sys.exit()

canvas = pygame.display.set_mode(size)
pygame.display.set_caption('Minesweeper')

grid = [[None for j in range(cols)] for i in range(rows)]
options = list()

for i in range(rows):
    for j in range(cols):
        grid[i][j] = cell.Cell(i, j, w, grid)
        options.append([i, j])

mines = numpy.random.choice(range(len(options)), totalMines, replace=False)
for m in mines:
    i = options[m][0]
    j = options[m][1]
    grid[i][j].mine = True

for i in range(rows):
    for j in range(cols):
        grid[i][j].countMines()

def defeat():
    for i in range(rows):
        for j in range(cols):
            grid[i][j].revealed = True

def main():
    loser = False
    winner = False
    score = 0
    while True:
        canvas.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                if event.button == 1:
                    for i in range(rows):
                        for j in range(cols):
                            if grid[i][j].contains(mouseX, mouseY) and (not grid[i][j].flagged):
                                grid[i][j].reveal()
                                if grid[i][j].mine:
                                    defeat()
                                    loser = True

                elif event.button == 3:
                    for i in range(rows):
                        for j in range(cols):
                            if grid[i][j].contains(mouseX, mouseY) and (not grid[i][j].flagged) and (not grid[i][j].revealed):
                                grid[i][j].putFlag()
                                score += 1
                            elif grid[i][j].contains(mouseX, mouseY) and (grid[i][j].flagged):
                                grid[i][j].removeFlag()
                                score -= 1
        mientras = list()
        for i in range(rows):
            for j in range(cols):
                if not grid[i][j].mine:
                    mientras.append(grid[i][j].revealed)
        winner = all(item == True for item in mientras)

        textScore = pygame.font.SysFont("Arial", 15)
        textScore.set_bold(True)
        message = textScore.render("Mines: {}".format(totalMines - score), True, (0, 0, 0))
        
        if loser:
            message = textScore.render("Game Over: defeat", True, (255, 0, 0))
        elif winner:
            message = textScore.render("Game Over: victory", True, (255, 0, 0))

        canvas.blit(message, (int(width * 0.1), int(height - 20)))

        for i in range(rows):
            for j in range(cols):
                grid[i][j].show(canvas)
        pygame.display.update()

if __name__ == '__main__':
    main()