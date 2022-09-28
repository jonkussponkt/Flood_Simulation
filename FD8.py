import time
import sys
import numpy as np
import pygame


def calculate_volumes(DEM):
    DEM_cells_volumes = np.zeros(DEM.shape)
    for i in range(DEM.shape[0]):
        for j in range(DEM.shape[1]):
            max_height = -1
            if j < board_no_of_cells - 1 and DEM[i, j + 1] - DEM[i, j] > max_height:
                max_height = DEM[i, j + 1] - DEM[i, j]
            if i < board_no_of_cells - 1 and j < board_no_of_cells - 1 \
                    and (DEM[i + 1, j + 1] - DEM[i, j]) / 1.4 > max_height:
                max_height = (DEM[i + 1, j + 1] - DEM[i, j]) / 1.4
            if i < board_no_of_cells - 1 and DEM[i + 1, j] - DEM[i, j] > max_height:
                max_height = DEM[i + 1, j] - DEM[i, j]
            if i < board_no_of_cells - 1 and j > 0 and (DEM[i + 1, j - 1] - DEM[i, j]) / 1.4 > max_height:
                max_height = (DEM[i + 1, j - 1] - DEM[i, j]) / 1.4
            if j > 0 and DEM[i, j - 1] - DEM[i, j] > max_height:
                max_height = DEM[i, j - 1] - DEM[i, j]
            if i > 0 and j > 0 and (DEM[i - 1, j - 1] - DEM[i, j]) / 1.4 > max_height:
                max_height = (DEM[i - 1, j - 1] - DEM[i, j]) / 1.4
            if i > 0 and DEM[i - 1, j] - DEM[i, j] > max_height:
                max_height = DEM[i - 1, j] - DEM[i, j]
            if i > 0 and j < board_no_of_cells - 1 and (DEM[i - 1, j + 1] - DEM[i, j]) / 1.4 > max_height:
                max_height = (DEM[i - 1, j + 1] - DEM[i, j]) / 1.4
            if max_height < 0:
                DEM_cells_volumes[i, j] = np.inf
            else:
                DEM_cells_volumes[i, j] = max_height
    return DEM_cells_volumes


if __name__ == "__main__":
    pygame.init()
    board_size = 420
    board_no_of_cells = 6
    # board = np.zeros([board_no_of_cells, board_no_of_cells], dtype='int8')
    DEM = np.array([[78, 72, 69, 71, 58, 49], [74, 67, 56, 49, 46, 50],
                    [69, 53, 44, 37, 38, 48], [64, 58, 55, 22, 31, 24],
                    [68, 61, 47, 21, 16, 19], [74, 53, 34, 12, 11, 12]])
    # DEM_cells_volumes = np.ones(DEM.shape)*50  # max accumulation of cells # TODO algorytm wyzn obj każdej komórki
    # DEM_cells_volumes[np.where(DEM == np.max(DEM))] = np.inf
    DEM_cells_volumes = calculate_volumes(DEM)
    flow_accumulation = np.zeros((board_no_of_cells, board_no_of_cells))
    flow_accumulation[0, 0] = 100
    block_size = 70
    screen = pygame.display.set_mode((board_size, board_size))
    tps_clock = pygame.time.Clock()
    tps_delta = 0.0
    tps_max = 5.0
    start = time.time()
    screen.fill((0, 0, 0))
    changes = 0.0
    previous_changes = 2.0
    # np.abs(previous_changes - changes) > 1.0
    # while np.abs(previous_changes - changes) > 1.0:  # TODO 2 warunek przerwania algorytmu
    while True:
        sum_between_iterations = 0.0
        previous_changes = changes
        changes = 0.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
        screen.fill((0, 0, 0))
        for i in range(board_no_of_cells):
            # tps_delta += tps_clock.tick() / 1000
            # # print("tick")g
            # while tps_delta > 1 / tps_max:
            for j in range(board_no_of_cells):
                neighborhood = {1: 0, 2: 0, 4: 0, 8: 0, 16: 0, 32: 0, 64: 0, 128: 0}
                if j < board_no_of_cells - 1 and flow_accumulation[i, j + 1] < DEM_cells_volumes[i, j + 1]:
                    neighborhood[1] = np.round(DEM[i, j] - DEM[i, j + 1], 5)
                if i < board_no_of_cells - 1 and j < board_no_of_cells - 1 \
                        and flow_accumulation[i + 1, j + 1] < DEM_cells_volumes[i, j + 1]:
                    neighborhood[2] = np.round((DEM[i, j] - DEM[i + 1, j + 1]) / 1.4, 5)
                if i < board_no_of_cells - 1 and flow_accumulation[i + 1, j] < DEM_cells_volumes[i + 1, j]:
                    neighborhood[4] = np.round(DEM[i, j] - DEM[i + 1, j], 5)
                if i < board_no_of_cells - 1 and j > 0 \
                        and flow_accumulation[i + 1, j - 1] < DEM_cells_volumes[i + 1, j - 1]:
                    neighborhood[8] = np.round((DEM[i, j] - DEM[i + 1, j - 1]) / 1.4, 5)
                if j > 0 and flow_accumulation[i, j - 1] < DEM_cells_volumes[i, j - 1]:
                    neighborhood[16] = np.round(DEM[i, j] - DEM[i, j - 1], 5)
                if i > 0 and j > 0 and flow_accumulation[i - 1, j - 1] < DEM_cells_volumes[i - 1, j - 1]:
                    neighborhood[32] = np.round((DEM[i, j] - DEM[i - 1, j - 1]) / 1.4, 5)
                if i > 0 and flow_accumulation[i - 1, j] < DEM_cells_volumes[i - 1, j]:
                    neighborhood[64] = np.round(DEM[i, j] - DEM[i - 1, j], 5)
                if i > 0 and j < board_no_of_cells - 1 \
                        and flow_accumulation[i - 1, j + 1] < DEM_cells_volumes[i - 1, j + 1]:
                    neighborhood[128] = np.round((DEM[i, j] - DEM[i - 1, j + 1]) / 1.4, 5)
                sum_slope = sum([x for x in list(neighborhood.values()) if x > 0])
                changes = 0.0
                if sum_slope > 0:
                    sum_of_changes = 0.0
                    sum_to_subtract = 0.0  # new value of flow_accumulation[i, j] cell
                    if neighborhood[1] > 0:
                        current_change = np.round(
                            np.round(neighborhood[1] / sum_slope, 5) * flow_accumulation[i, j], 5)
                        if flow_accumulation[i, j + 1] + current_change > DEM_cells_volumes[i, j + 1]:
                            temp = DEM_cells_volumes[i, j + 1] - flow_accumulation[i, j + 1]
                            flow_accumulation[i, j + 1] += temp
                            sum_to_subtract += temp
                            # new_cell_value += DEM_cells_volumes[i, j + 1] - current_change
                            # flow_accumulation[i, j] = DEM_cells_volumes[i, j + 1] - current_change
                        else:
                            flow_accumulation[i, j + 1] += current_change
                            sum_of_changes += current_change
                            sum_to_subtract += current_change
                        changes += current_change
                    if neighborhood[2] > 0:
                        current_change = np.round(
                            np.round(neighborhood[2] / sum_slope, 5) * flow_accumulation[i, j], 5)
                        if flow_accumulation[i + 1, j + 1] + current_change > DEM_cells_volumes[i + 1, j + 1]:
                            temp = DEM_cells_volumes[i + 1, j + 1] - flow_accumulation[i + 1, j + 1]
                            flow_accumulation[i + 1, j + 1] += temp
                            sum_to_subtract += temp
                            # new_cell_value += DEM_cells_volumes[i + 1, j + 1] - current_change
                            # flow_accumulation[i, j] -= DEM_cells_volumes[i + 1, j + 1] - current_change
                        else:
                            flow_accumulation[i + 1, j + 1] += current_change
                            sum_of_changes += current_change
                            sum_to_subtract += current_change
                            # flow_accumulation[i, j] -= current_change
                        changes += current_change
                    if neighborhood[4] > 0:
                        current_change = np.round(
                            np.round(neighborhood[4] / sum_slope, 5) * flow_accumulation[i, j], 5)
                        if flow_accumulation[i + 1, j] + current_change > DEM_cells_volumes[i + 1, j]:
                            temp = DEM_cells_volumes[i + 1, j] - flow_accumulation[i + 1, j]
                            flow_accumulation[i + 1, j] += temp
                            sum_to_subtract += temp
                            # new_cell_value += DEM_cells_volumes[i + 1, j] - current_change
                            # flow_accumulation[i, j] -= DEM_cells_volumes[i + 1, j] - flow_accumulation[i, j]
                        else:
                            flow_accumulation[i + 1, j] += current_change
                            sum_of_changes += current_change
                            sum_to_subtract += current_change
                            # flow_accumulation[i, j] -= current_change
                        changes += current_change
                    if neighborhood[8] > 0:
                        current_change = np.round(
                            np.round(neighborhood[8] / sum_slope, 5) * flow_accumulation[i, j], 5)
                        if flow_accumulation[i + 1, j - 1] + current_change > DEM_cells_volumes[i + 1, j - 1]:
                            temp = DEM_cells_volumes[i + 1, j - 1] - flow_accumulation[i + 1, j - 1]
                            flow_accumulation[i + 1, j - 1] += temp
                            sum_to_subtract += temp
                            # new_cell_value += DEM_cells_volumes[i + 1, j - 1] - current_change
                            # flow_accumulation[i, j] -= DEM_cells_volumes[i + 1, j - 1] - current_change
                        else:
                            flow_accumulation[i + 1, j - 1] += current_change
                            sum_of_changes += current_change
                            sum_to_subtract += current_change
                            # flow_accumulation[i, j] -= current_change
                        changes += current_change
                    if neighborhood[16] > 0:
                        current_change = np.round(
                            np.round(neighborhood[16] / sum_slope, 5) * flow_accumulation[i, j], 5)
                        if flow_accumulation[i, j - 1] + current_change > DEM_cells_volumes[i, j - 1]:
                            temp = DEM_cells_volumes[i, j - 1] - flow_accumulation[i, j - 1]
                            flow_accumulation[i, j - 1] += temp
                            sum_to_subtract += temp
                            # new_cell_value += DEM_cells_volumes[i, j - 1] - current_change
                            # flow_accumulation[i, j] -= DEM_cells_volumes[i, j - 1] - current_change
                        else:
                            flow_accumulation[i, j - 1] += current_change
                            sum_of_changes += current_change
                            sum_to_subtract += current_change
                            # flow_accumulation[i, j] -= current_change
                        changes += current_change
                    if neighborhood[32] > 0:
                        current_change = np.round(
                            np.round(neighborhood[32] / sum_slope, 5) * flow_accumulation[i, j], 5)
                        if flow_accumulation[i - 1, j - 1] + current_change > DEM_cells_volumes[i - 1, j - 1]:
                            temp = DEM_cells_volumes[i - 1, j - 1] - flow_accumulation[i - 1, j - 1]
                            flow_accumulation[i - 1, j - 1] += temp
                            sum_to_subtract += temp
                            # new_cell_value += DEM_cells_volumes[i - 1, j - 1] - current_change
                            # flow_accumulation[i, j] -= DEM_cells_volumes[i - 1, j - 1] - current_change
                        else:
                            flow_accumulation[i - 1, j - 1] += current_change
                            sum_of_changes += current_change
                            sum_to_subtract += current_change
                            # flow_accumulation[i, j] -= current_change
                        changes += current_change
                    if neighborhood[64] > 0:
                        current_change = np.round(
                            np.round(neighborhood[64] / sum_slope, 5) * flow_accumulation[i, j], 5)
                        if flow_accumulation[i - 1, j] + current_change > DEM_cells_volumes[i - 1, j]:
                            temp = DEM_cells_volumes[i - 1, j] - flow_accumulation[i, j]
                            flow_accumulation[i - 1, j] += temp
                            sum_to_subtract += temp
                            # new_cell_value += DEM_cells_volumes[i - 1, j] - current_change
                            # flow_accumulation[i, j] -= DEM_cells_volumes[i, j] - current_change
                        else:
                            flow_accumulation[i - 1, j] += current_change
                            sum_of_changes += current_change
                            sum_to_subtract += current_change
                            # flow_accumulation[i, j] -= current_change
                        changes += current_change
                    if neighborhood[128] > 0:
                        current_change = np.round(
                            np.round(neighborhood[128] / sum_slope, 5) * flow_accumulation[i, j], 5)
                        if flow_accumulation[i - 1, j + 1] + current_change > DEM_cells_volumes[i - 1, j + 1]:
                            temp = DEM_cells_volumes[i - 1, j + 1] - flow_accumulation[i - 1, j + 1]
                            flow_accumulation[i - 1, j + 1] += temp
                            sum_to_subtract += temp
                            # flow_accumulation[i, j] -= DEM_cells_volumes[i - 1, j + 1] - current_change
                        else:
                            flow_accumulation[i - 1, j + 1] += current_change
                            sum_of_changes += current_change
                            sum_to_subtract += current_change
                            # flow_accumulation[i, j] -= current_change
                        changes += current_change
                    # flow_accumulation[i, j] -= sum_of_changes  # TODO do zmiany
                    flow_accumulation[i, j] -= sum_to_subtract
                # animacja
                print(flow_accumulation)

                font_color = (0, 0, 0)  # black font
                font_size = 10
                font = pygame.font.Font('freesansbold.ttf', font_size)
                colors = {(0, 1): (100, 255, 255), (1, 10): (100, 192, 255), (10, 40): (64, 120, 255),
                          (40, 60): (17, 74, 255), (60, 80): (0, 20, 232), (80, 110): (43, 56, 137)}
                for p in range(0, board_size, block_size):
                    for k in range(0, board_size, block_size):
                        rectangle = pygame.Rect(k, p, block_size, block_size)
                        color = (255, 255, 255)
                        for m, n in colors.items():
                            if flow_accumulation[p // 70, k // 70] - 0.019 > 0 \
                                    and m[0] < flow_accumulation[p // 70, k // 70] <= m[1]:
                                color = n
                                break
                        pygame.draw.rect(screen, color, rectangle, 0)
                        text = font.render(str(np.round(flow_accumulation[p // 70, k // 70], 2)), True, font_color)
                        rectangle.center = (k + block_size // 2, p + block_size)
                        screen.blit(text, rectangle)
                        pygame.display.update()
            tps_delta -= 1 / tps_max
            time.sleep(2.0)
        print(changes)


# 1 głębokość
# TODO 1.2 napisać algorytm obliczania objętości każdej komórki
# 2 warunek przerwania algorytmu
# TODO 3 animacja z DEMem
# TODO 4 przewidywanie czasu (i prędkości)
# TODO 5 (numeryczny model pokrycia terenu)
