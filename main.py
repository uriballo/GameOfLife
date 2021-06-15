import pygame
import numpy as np
import time

pygame.init()

# Screen setup.
scWidth = 1000
scHeight = 1000
screen = pygame.display.set_mode((scWidth, scHeight))
background = 25, 25, 25  # Background color.
screen.fill(background)

# Number of Cells.
cX, cY = 50, 50

# Cells dimensions.
dimCW = scWidth / cX
dimCH = scHeight / cY

# Current state of the game.
state = np.zeros((cX, cY))

pauseGame = True

while True:

    newState = np.copy(state)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            pauseGame = not pauseGame

        click = pygame.mouse.get_pressed(3)
        if sum(click) > 0:
            posX, posY = pygame.mouse.get_pos()
            cellX, cellY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newState[cellX, cellY] = not click[2]

    screen.fill(background)

    for y in range(0, cX):
        for x in range(0, cY):
            if not pauseGame:
                # Number of neighbours.
                nNeigh = state[(x - 1) % cX, (y - 1) % cY] + \
                         state[(x)     % cX, (y - 1) % cY] + \
                         state[(x + 1) % cX, (y - 1) % cY] + \
                         state[(x - 1) % cX, (y)     % cY] + \
                         state[(x + 1) % cX, (y)     % cY] + \
                         state[(x - 1) % cX, (y + 1) % cY] + \
                         state[(x)     % cX, (y + 1) % cY] + \
                         state[(x + 1) % cX, (y + 1) % cY]

                # RULE 1
                if state[x, y] == 0 and nNeigh == 3:
                    newState[x, y] = 1

                # RULE 2
                elif state[x, y] == 1 and (nNeigh < 2 or nNeigh > 3):
                    newState[x, y] = 0

            # Creating cell grid.
            cellXY = [((x) * dimCW, y * dimCH),
                        ((x + 1) * dimCW, y * dimCH),
                        ((x + 1) * dimCW, (y + 1) * dimCW),
                        ((x) * dimCW, (y + 1) * dimCH)]

            if newState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), cellXY, 1)

            else:
                pygame.draw.polygon(screen, (255, 255, 255), cellXY, 0)

    state = np.copy(newState)

    time.sleep(0.05)

    pygame.display.flip()
