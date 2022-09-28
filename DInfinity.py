import time
import sys
import numpy as np
import pygame


class Triangle:

    def __init__(self):
        self.ac_coefficient = 0.0
        self.af_coefficient = 0.0
        self.r_tangent = 0.0
        self.slope = 0.0

    def set_ac(self, ac):
        self.ac_coefficient = ac

    def set_af(self, af):
        self.af_coefficient = af

    def set_r(self, r):
        self.r_tangent = r

    def set_slope(self, sl):
        self.slope = sl


def find_max_in_dict(dictionary):
    maxi = dictionary[1]
    key = 1
    for i, j in dictionary.items():
        if j > maxi:
            key = i
            maxi = j
    return key, maxi


if __name__ == "__main__":
    pygame.init()
    board_size = 420
    board_no_of_cells = 6
    board = np.zeros([board_no_of_cells, board_no_of_cells], dtype='int8')
    DEM = np.array([[78, 72, 69, 71, 58, 49], [74, 67, 56, 49, 46, 50],
                    [69, 53, 44, 37, 38, 48], [64, 58, 55, 22, 31, 24],
                    [68, 61, 47, 21, 16, 19], [74, 53, 34, 12, 11, 12]])
    print(DEM)
    # triangles = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None}
    # ac_coefficient = {1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 4}
    # af_coefficient = {1: 1, 2: -1, 3: 1, 4: -1, 5: 1, 6: -1, 7: 1, 8: -1}
    # r_tangent = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    # slope = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    triangles = [Triangle() for _ in range(8)]
    for i in range(board_no_of_cells):
        for j in range(board_no_of_cells):
            if i > 0 and j < board_no_of_cells - 1:
                slope1, slope2 = np.round(DEM[i, j] - DEM[i, j + 1], 5), np.round(DEM[i, j + 1] - DEM[i - 1, j + 1], 5)
                r_tangent = np.arctan(slope2/slope1)
                triangles[0].set_r(r_tangent)
                triangles[0].set_slope(np.sqrt(slope1**2 + slope2**2))
                if r_tangent < 0:
                    triangles[0].set_r(0)
                    triangles[0].set_slope(slope1)
                if r_tangent > np.arctan(1):
                    triangles[0].set_r(np.arctan(1))
                    triangles[0].set_slope(np.round((DEM[i, j] - DEM[i - 1, j - 1]) / 1.4, 5))
            if i > 0 and j < board_no_of_cells - 1:
                slope1, slope2 = np.round(DEM[i, j] - DEM[i - 1, j], 5), np.round(DEM[i - 1, j] - DEM[i - 1, j + 1], 5)
                r_tangent = np.arctan(slope2/slope1)
                triangles[1].set_r(r_tangent)
                triangles[1].set_slope(np.sqrt(slope1 ** 2 + slope2 ** 2))
                if r_tangent < 0:
                    triangles[1].set_r(0)
                    triangles[1].set_slope(slope1)
                if r_tangent > np.arctan(1):
                    r_tangent[1].set_r(np.arctan(1))
                    triangles[1].set_slope(np.round((DEM[i, j] - DEM[i - 1, j + 1]) / 1.4, 5))
            if i > 0 and j > 0:
                slope1, slope2 = np.round(DEM[i, j] - DEM[i - 1, j], 5), np.round(DEM[i - 1, j] - DEM[i - 1, j - 1], 5)
                r_tangent = np.arctan(slope2 / slope1)
                triangles[2].set_r(r_tangent)
                triangles[2].set_slope(np.sqrt(slope1 ** 2 + slope2 ** 2))
                if r_tangent < 0:
                    triangles[2].set_r(0)
                    triangles[2].set_slope(slope1)
                if r_tangent > np.arctan(1):
                    triangles[2].set_r(np.arctan(1))
                    triangles[2].set_slope(np.round((DEM[i, j] - DEM[i - 1, j - 1]) / 1.4, 5))
            if i > 0 and j > 0:
                slope1, slope2 = np.round(DEM[i, j] - DEM[i, j - 1], 5), np.round(DEM[i, j - 1] - DEM[i - 1, j - 1], 5)
                r_tangent = np.arctan(slope2 / slope1)
                triangles[3].set_r(r_tangent)
                triangles[3].set_slope(np.sqrt(slope1 ** 2 + slope2 ** 2))
                if r_tangent < 0:
                    triangles[3].set_r(0)
                    triangles[3].set_slope(slope1)
                if r_tangent > np.arctan(1):
                    triangles[3].set_r(np.arctan(1))
                    triangles[3].set_slope(np.round((DEM[i, j] - DEM[i - 1, j - 1]) / 1.4, 5))
            if i < board_no_of_cells - 1 and j > 0:
                slope1, slope2 = np.round(DEM[i, j] - DEM[i, j - 1], 5), np.round(DEM[i, j - 1] - DEM[i + 1, j - 1], 5)
                r_tangent = np.arctan(slope2 / slope1)
                triangles[4].set_r(r_tangent)
                triangles[4].set_slope(np.sqrt(slope1 ** 2 + slope2 ** 2))
                if r_tangent < 0:
                    triangles[4].set_r(0)
                    triangles[4].set_slope(slope1)
                if r_tangent > np.arctan(1):
                    triangles[4].set_r(np.arctan(1))
                    triangles[4].set_slope(np.round((DEM[i, j] - DEM[i + 1, j - 1]) / 1.4, 5))
            if i < board_no_of_cells - 1 and j > 0:
                slope1, slope2 = np.round(DEM[i, j] - DEM[i + 1, j], 5), np.round(DEM[i + 1, j] - DEM[i + 1, j - 1], 5)
                r_tangent = np.arctan(slope2 / slope1)
                triangles[5].set_r(r_tangent)
                triangles[5].set_slope(np.sqrt(slope1 ** 2 + slope2 ** 2))
                if r_tangent < 0:
                    triangles[5].set_r(0)
                    triangles[5].set_slope(slope1)
                if r_tangent > np.arctan(1):
                    triangles[5].set_r(np.arctan(1))
                    triangles[5].set_slope(np.round((DEM[i, j] - DEM[i + 1, j - 1]) / 1.4, 5))
            if i < board_no_of_cells - 1 and j < board_no_of_cells - 1:
                slope1, slope2 = np.round(DEM[i, j] - DEM[i + 1, j], 5), np.round(DEM[i + 1, j] - DEM[i + 1, j + 1], 5)
                r_tangent = np.arctan(slope2 / slope1)
                triangles[6].set_r(r_tangent)
                triangles[6].set_slope(np.sqrt(slope1 ** 2 + slope2 ** 2))
                if r_tangent < 0:
                    triangles[6].set_r(0)
                    triangles[6].set_slope(slope1)
                if r_tangent > np.arctan(1):
                    triangles[6].set_r(np.arctan(1))
                    triangles[6].set_slope(np.round((DEM[i, j] - DEM[i + 1, j + 1]) / 1.4, 5))
            if i < board_no_of_cells - 1 and j < board_no_of_cells - 1:
                slope1, slope2 = np.round(DEM[i, j] - DEM[i, j + 1], 5), np.round(DEM[i, j + 1] - DEM[i + 1, j + 1], 5)
                r_tangent = np.arctan(slope2 / slope1)
                triangles[7].set_r(r_tangent)
                triangles[7].set_slope(np.sqrt(slope1 ** 2 + slope2 ** 2))
                if r_tangent < 0:
                    triangles[7].set_r(0)
                    triangles[7].set_slope(slope1)
                if r_tangent > np.arctan(1):
                    triangles[7].set_r(np.arctan(1))
                    triangles[7].set_slope(np.round((DEM[i, j] - DEM[i + 1, j + 1]) / 1.4, 5))
            # r_prim_coef = find_max_in_dict(slope)
            # TODO zwróć obiekt z największym slope'm
            # r_g_coef = np.round(af_coefficient[r_prim_coef[0]]
            #              * r_prim_coef + ac_coefficient[r_prim_coef[0]]*np.pi/2, 5)
            # TODO jak wyzej

# TODO rozdzielić spływ na komórki
