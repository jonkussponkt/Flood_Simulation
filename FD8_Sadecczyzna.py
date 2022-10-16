import numpy as np
import rasterio as rio
from mayavi import mlab
from queue import PriorityQueue


def calculate_volumes(DEM):                     # wyliczanie maksymalnej objętosci dla każdej komórki jako
    DEM_cells_volumes = np.zeros(DEM.shape)     # max różnicy wzniesień do potęgi 3
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
            if max_height <= 0:  # jeżeli mamy komórkę, wokół której nie ma komórki o mniejszej wysokości, to
                                 # przyjmujemy sobie nieskończoną objętość
                DEM_cells_volumes[i, j] = np.inf
            else:
                DEM_cells_volumes[i, j] = np.power(max_height, 3)  # wyliczamy objętość jak dla sześcianu
    return DEM_cells_volumes


if __name__ == "__main__":
    DEM_tif = r"C:\Users\Jan\PycharmProjects\inzynierka\img\dem_Sadecczyzna_przyciete.tif"
    with rio.open(DEM_tif) as f:
        DEM_tif = f.read(1)
    DEM = np.asarray(DEM_tif)
    DEM_x, DEM_y = DEM.shape
    DEM_cells_volumes = calculate_volumes(DEM)  # obliczamy dozwolone objętości komórek
    flow_accumulation = np.zeros(DEM.shape)+2.0  # zalewamy DEM wodą
    x = np.arange(0, DEM.shape[1])
    y = np.arange(0, DEM.shape[0])
    X, Y = np.meshgrid(x, y)
    print(np.sum(flow_accumulation.flatten()))
    for _ in range(5):  # TODO: tu będzie warunek przerwania
        changes = 0.0
        for i in range(DEM_x):  # wyliczamy wartości akumulacji wody w komórce
            for j in range(DEM_y):
                priority_of_slopes = PriorityQueue()
                neighborhood = {1: 0, 2: 0, 4: 0, 8: 0, 16: 0, 32: 0, 64: 0, 128: 0}
                coordinates = {1: (i, j + 1), 2: (i + 1, j + 1), 4: (i + 1, j), 8: (i + 1, j - 1),
                               16: (i, j - 1), 32: (i - 1, j - 1), 64: (i - 1, j), 128: (i - 1, j + 1)}
                sum_slope = 0.0
                if j < DEM_y - 1:  # zabezpieczenie warunków brzegowych
                    if flow_accumulation[i, j + 1] < DEM_cells_volumes[i, j + 1]:  #
                        neighborhood[1] = np.round(DEM[i, j] - DEM[i, j + 1], 5)   # wyliczamy różnicę wysokości
                        #  jeśli pixel sąsiadujący jest niżej to dodajemy go do kolejki wg priorytetu różnicy wysokości
                        if neighborhood[1] > 0:
                            # dodaję minus przed wartością, gdyż priority queue w Pythonie to kolejka 'minimum'
                            priority_of_slopes.put((-neighborhood[1], 1))
                if i < DEM_x - 1 and j < DEM_y - 1:
                    if flow_accumulation[i + 1, j + 1] < DEM_cells_volumes[i + 1, j + 1]:
                        # różnica wys. po przekątnej, dlatego dodatkowo dzielimy przez sqrt(2)=1.4
                        neighborhood[2] = np.round((DEM[i, j] - DEM[i + 1, j + 1]) / 1.4, 5)
                        if neighborhood[2] > 0:
                            priority_of_slopes.put((-neighborhood[2], 2))
                if i < DEM_x - 1:
                    if flow_accumulation[i + 1, j] < DEM_cells_volumes[i + 1, j]:
                        neighborhood[4] = np.round(DEM[i, j] - DEM[i + 1, j], 5)
                        if neighborhood[4] > 0:
                            priority_of_slopes.put((-neighborhood[4], 4))
                if i < DEM_x - 1 and j > 0:
                    if flow_accumulation[i + 1, j - 1] < DEM_cells_volumes[i + 1, j - 1]:
                        neighborhood[8] = np.round((DEM[i, j] - DEM[i + 1, j - 1]) / 1.4, 5)
                        if neighborhood[8] > 0:
                            priority_of_slopes.put((-neighborhood[8], 8))
                if j > 0:
                    if flow_accumulation[i, j - 1] < DEM_cells_volumes[i, j - 1]:
                        neighborhood[16] = np.round(DEM[i, j] - DEM[i, j - 1], 5)
                        if neighborhood[16] > 0:
                            priority_of_slopes.put((-neighborhood[16], 16))
                if i > 0 and j > 0:
                    if flow_accumulation[i - 1, j - 1] < DEM_cells_volumes[i - 1, j - 1]:
                        neighborhood[32] = np.round((DEM[i, j] - DEM[i - 1, j - 1]) / 1.4, 5)
                        if neighborhood[32] > 0:
                            priority_of_slopes.put((-neighborhood[32], 32))
                if i > 0:
                    if flow_accumulation[i - 1, j] < DEM_cells_volumes[i - 1, j]:
                        neighborhood[64] = np.round(DEM[i, j] - DEM[i - 1, j], 5)
                        if neighborhood[64] > 0:
                            priority_of_slopes.put((-neighborhood[64], 64))
                if i > 0 and j < DEM_y - 1:
                    if flow_accumulation[i - 1, j + 1] < DEM_cells_volumes[i - 1, j + 1]:
                        neighborhood[128] = np.round((DEM[i, j] - DEM[i - 1, j + 1]) / 1.4, 5)
                        if neighborhood[128] > 0:
                            priority_of_slopes.put((-neighborhood[128], 128))
                sum_slope = sum([x for x in list(neighborhood.values()) if x > 0])  # suma nachyleń
                if sum_slope > 0:
                    sum_to_subtract = 0.0  # wyliczamy wartość, którą należy odjąć od aktualnie rozpatrywanej komórki
                    while not priority_of_slopes.empty():
                        # po kolei wyciągamy z kolejki największe różnice wysokości
                        slope = priority_of_slopes.get()
                        # wyliczamy wartość wody, która przepłynie z komórki o wsp [i,j] względem tego jaką
                        # część nachylenia stanowi nachylenie wzgl obecnej komórki
                        current_change = np.round(
                            np.round(-slope[0] / sum_slope, 5) * flow_accumulation[i, j], 5)
                        current_coords = coordinates[slope[1]]
                        # jeżeli może dojść do przepełnienia komórki, tzn obecny poziom wody + zmiana jest większa
                        # od max objętości, to dopełniamy komórkę do max
                        if flow_accumulation[current_coords] + current_change > DEM_cells_volumes[current_coords]:
                            temp = DEM_cells_volumes[current_coords] - flow_accumulation[current_coords]
                            flow_accumulation[current_coords] += temp
                            sum_to_subtract += temp
                        # w przeciwnym przypadku, czyli gdy nie dojdzie do przepełnienia to po prostu dodajemy
                        # nowy przypływ do komórki
                        else:
                            flow_accumulation[current_coords] += current_change
                            sum_to_subtract += current_change
                    # od aktualnie rozpatrywanej komórki odejmujemy sumę odpływów do sąsiadów
                    flow_accumulation[i, j] -= sum_to_subtract
    print(np.sum(flow_accumulation.flatten()))
    flow_accumulation += DEM - 2.0
    flow_accumulation[np.where(flow_accumulation > DEM)] += 2.0
    while True:
        surf_water = mlab.surf(flow_accumulation, color=(0, 0.66, 1.0))
        surf_water.actor.actor.scale = [1.0, 1.0, 0.1]
        surf_water.actor.property.opacity = 0.2
        surf_height = mlab.surf(DEM, colormap='Greens')
        surf_height.actor.actor.scale = [1.0, 1.0, 0.1]
        mlab.view(160, 120)
        mlab.show()
