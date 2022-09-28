import numpy as np
import rasterio as rio
import time
import scipy as sp

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from mayavi import mlab

import os

os.environ["R_HOME"] = r"C:\Program Files\R\R-4.1.2"
import rpy2.robjects as ro
import rpy2.robjects.numpy2ri
import rpy2.robjects.packages as rpackages


def calculate_volumes(DEM):
    DEM_cells_volumes = np.zeros(DEM.shape)
    for i in range(DEM.shape[0]):
        for j in range(DEM.shape[1]):
            max_height = -1
            if j < DEM_y - 1 and DEM[i, j + 1] - DEM[i, j] > max_height:
                max_height = DEM[i, j + 1] - DEM[i, j]
            if i < DEM_x - 1 and j < DEM_y - 1 \
                    and (DEM[i + 1, j + 1] - DEM[i, j]) / 1.4 > max_height:
                max_height = (DEM[i + 1, j + 1] - DEM[i, j]) / 1.4
            if i < DEM_x - 1 and DEM[i + 1, j] - DEM[i, j] > max_height:
                max_height = DEM[i + 1, j] - DEM[i, j]
            if i < DEM_x - 1 and j > 0 and (DEM[i + 1, j - 1] - DEM[i, j]) / 1.4 > max_height:
                max_height = (DEM[i + 1, j - 1] - DEM[i, j]) / 1.4
            if j > 0 and DEM[i, j - 1] - DEM[i, j] > max_height:
                max_height = DEM[i, j - 1] - DEM[i, j]
            if i > 0 and j > 0 and (DEM[i - 1, j - 1] - DEM[i, j]) / 1.4 > max_height:
                max_height = (DEM[i - 1, j - 1] - DEM[i, j]) / 1.4
            if i > 0 and DEM[i - 1, j] - DEM[i, j] > max_height:
                max_height = DEM[i - 1, j] - DEM[i, j]
            if i > 0 and j < DEM_y - 1 and (DEM[i - 1, j + 1] - DEM[i, j]) / 1.4 > max_height:
                max_height = (DEM[i - 1, j + 1] - DEM[i, j]) / 1.4
            if max_height < 0:
                DEM_cells_volumes[i, j] = np.inf
            else:
                DEM_cells_volumes[i, j] = np.power(max_height, 3)
    return DEM_cells_volumes


if __name__ == "__main__":
    rpy2.robjects.numpy2ri.activate()
    DEM_tif = r"C:\Users\Jan\PycharmProjects\inzynierka\img\dem_Sadecczyzna_przyciete.tif"
    with rio.open(DEM_tif) as f:
        DEM_tif = f.read(1)
    DEM = np.asarray(DEM_tif)
    flow_accumulation = np.zeros(DEM.shape)+2
    # flow_accumulation[np.where(DEM == np.max(DEM))] = 100
    DEM_x, DEM_y = DEM.shape
    block_size = 70
    DEM_cells_volumes = calculate_volumes(DEM)
    # print(DEM_cells_volumes)
    start = time.time()
    changes = 0.0
    previous_changes = 2.0
    # while np.abs(previous_changes - changes) > 1.0:  # TODO 2 warunek przerwania algorytmu
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection='3d')
    x = np.arange(0, DEM.shape[1])
    y = np.arange(0, DEM.shape[0])
    X, Y = np.meshgrid(x, y)
    for iteration in range(10):
        sum_between_iterations = 0.0
        previous_changes = changes
        changes = 0.0
        for i in range(DEM_x):
            for j in range(DEM_y):
                sum_to_subtract = 0.0
                neighborhood = {1: 0, 2: 0, 4: 0, 8: 0, 16: 0, 32: 0, 64: 0, 128: 0}
                if j < DEM_y - 1 and flow_accumulation[i, j + 1] < DEM_cells_volumes[i, j + 1]:
                    neighborhood[1] = np.round(DEM[i, j] - DEM[i, j + 1], 5)
                if i < DEM_x - 1 and j < DEM_y - 1 \
                        and flow_accumulation[i + 1, j + 1] < DEM_cells_volumes[i, j + 1]:
                    neighborhood[2] = np.round((DEM[i, j] - DEM[i + 1, j + 1]) / 1.4, 5)
                if i < DEM_x - 1 and flow_accumulation[i + 1, j] < DEM_cells_volumes[i + 1, j]:
                    neighborhood[4] = np.round(DEM[i, j] - DEM[i + 1, j], 5)
                if i < DEM_x - 1 and j > 0 \
                        and flow_accumulation[i + 1, j - 1] < DEM_cells_volumes[i + 1, j - 1]:
                    neighborhood[8] = np.round((DEM[i, j] - DEM[i + 1, j - 1]) / 1.4, 5)
                if j > 0 and flow_accumulation[i, j - 1] < DEM_cells_volumes[i, j - 1]:
                    neighborhood[16] = np.round(DEM[i, j] - DEM[i, j - 1], 5)
                if i > 0 and j > 0 and flow_accumulation[i - 1, j - 1] < DEM_cells_volumes[i - 1, j - 1]:
                    neighborhood[32] = np.round((DEM[i, j] - DEM[i - 1, j - 1]) / 1.4, 5)
                if i > 0 and flow_accumulation[i - 1, j] < DEM_cells_volumes[i - 1, j]:
                    neighborhood[64] = np.round(DEM[i, j] - DEM[i - 1, j], 5)
                if i > 0 and j < DEM_y - 1 \
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
                        if flow_accumulation[i, j + 1] + current_change > DEM_cells_volumes[i, j + 1] > \
                                flow_accumulation[i, j + 1]:
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
                        if flow_accumulation[i + 1, j + 1] + current_change > DEM_cells_volumes[i + 1, j + 1] > \
                                flow_accumulation[i + 1, j + 1]:
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
                        if flow_accumulation[i + 1, j] + current_change > DEM_cells_volumes[i + 1, j] > \
                                flow_accumulation[i + 1, j]:
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
                        if flow_accumulation[i + 1, j - 1] + current_change > DEM_cells_volumes[i + 1, j - 1] > \
                                flow_accumulation[i + 1, j - 1]:
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
                        if flow_accumulation[i, j - 1] + current_change > DEM_cells_volumes[i, j - 1] > \
                                flow_accumulation[i, j - 1]:
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
                        if flow_accumulation[i - 1, j - 1] + current_change > DEM_cells_volumes[i - 1, j - 1]\
                                > flow_accumulation[i, j]:
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
                        if flow_accumulation[i - 1, j] + current_change > DEM_cells_volumes[i - 1, j] > \
                                flow_accumulation[i, j]:
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
                        if flow_accumulation[i - 1, j + 1] + current_change > DEM_cells_volumes[i - 1, j + 1]\
                                > flow_accumulation[i, j]:
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
                    flow_accumulation[i, j] -= sum_to_subtract  # TODO problem1
        # animacja
    # print(flow_accumulation)
    print(np.sum(flow_accumulation.flatten()))
    flow_accumulation += DEM - 2.0
    flow_accumulation[np.where(flow_accumulation > DEM)] += 5.0
    while True:
        surf_water = mlab.surf(flow_accumulation, color=(0, 0.66, 1.0))
        surf_water.actor.actor.scale = [1.0, 1.0, 0.1]
        surf_water.actor.property.opacity = 0.2
        surf_height = mlab.surf(DEM, colormap='Greens')
        surf_height.actor.actor.scale = [1.0, 1.0, 0.1]
        mlab.view(160, 120)
        mlab.title('Powódź')
        mlab.savefig('img/flood_test_m.png')
        mlab.show()
