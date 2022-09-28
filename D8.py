import numpy as np
import pygame
import sys


if __name__ == "__main__":
    pygame.init()
    board_size = 420
    board_no_of_cells = 6
    DEM = np.array([[78, 72, 69, 71, 58, 49], [74, 67, 56, 49, 46, 50],
                    [69, 53, 44, 37, 38, 48], [64, 58, 55, 22, 31, 24],
                    [68, 61, 47, 21, 16, 19], [74, 53, 34, 12, 11, 12]])
    block_size = 70
    screen = pygame.display.set_mode((board_size, board_size))
    directions_array = np.zeros([board_no_of_cells, board_no_of_cells], dtype='int32')
    for i in range(board_no_of_cells):
        for j in range(board_no_of_cells):
            neighborhood = {0: -8000, 1: -8001, 2: -8002, 4: -8003, 8: -8004,
                            16: -8005, 32: -8006, 64: -8007, 128: -8008}
            maxi = 0
            if j < board_no_of_cells - 1:
                neighborhood[1] = DEM[i, j] - DEM[i, j + 1]
                if neighborhood[1] > neighborhood[maxi] and neighborhood[1] > 0:
                    maxi = 1
            if i < board_no_of_cells - 1 and j < board_no_of_cells - 1:
                neighborhood[2] = (DEM[i, j] - DEM[i + 1, j + 1]) / 1.4
                if neighborhood[2] > neighborhood[maxi] and neighborhood[2] > 0:
                    maxi = 2
            if i < board_no_of_cells - 1:
                neighborhood[4] = DEM[i, j] - DEM[i + 1, j]
                if neighborhood[4] > neighborhood[maxi] and neighborhood[4] > 0:
                    maxi = 4
            if i < board_no_of_cells - 1 and j > 0:
                neighborhood[8] = (DEM[i, j] - DEM[i + 1, j - 1]) / 1.4
                if neighborhood[8] > neighborhood[maxi] and neighborhood[8] > 0:
                    maxi = 8
            if j > 0:
                neighborhood[16] = DEM[i, j] - DEM[i, j - 1]
                if neighborhood[16] > neighborhood[maxi] and neighborhood[16] > 0:
                    maxi = 16
            if i > 0 and j > 0:
                neighborhood[32] = (DEM[i, j] - DEM[i - 1, j - 1]) / 1.4
                if neighborhood[32] > neighborhood[maxi] and neighborhood[32] > 0:
                    maxi = 32
            if i > 0:
                neighborhood[64] = DEM[i, j] - DEM[i - 1, j]
                if neighborhood[64] > neighborhood[maxi] and neighborhood[64] > 0:
                    maxi = 64
            if i > 0 and j < board_no_of_cells - 1:
                neighborhood[128] = (DEM[i, j] - DEM[i - 1, j + 1]) / 1.4
                if neighborhood[128] > neighborhood[maxi] and neighborhood[128] > 0:
                    maxi = 128
            directions_array[i, j] = maxi
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
        screen.fill((0, 0, 0))

        font_color = (0, 0, 0)  # black font
        font_size = 25
        font = pygame.font.Font('freesansbold.ttf', font_size)
        # Drawing
        for i in range(0, board_size, block_size):
            for j in range(0, board_size, block_size):
                colors = {0: (192, 192, 192), 1: (10, 200, 0), 2: (0, 91, 0), 4: (0, 198, 255), 8: (0, 119, 255),
                          16: (0, 33, 255), 32: (226, 1, 255), 64: (213, 52, 0), 128: (255, 212, 0)}
                rectangle = pygame.Rect(j, i, block_size, block_size)
                pygame.draw.rect(screen, colors[directions_array[i // 70, j // 70]], rectangle, 0)
                text = font.render(str(int(directions_array[i // 70, j // 70])), True, font_color)
                rectangle.center = (j+block_size//2, i+block_size)
                screen.blit(text, rectangle)
        pygame.display.update()
