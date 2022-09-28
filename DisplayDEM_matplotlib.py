import numpy as np
import rasterio as rio
import time

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm

import os
os.environ["R_HOME"] = r"C:\Program Files\R\R-4.1.2"
import rpy2.robjects as ro
import rpy2.robjects.numpy2ri
import rpy2.robjects.packages as rpackages


rpy2.robjects.numpy2ri.activate()
DEM_tif = r"C:\Users\Jan\PycharmProjects\inzynierka\img\dem_Sadecczyzna_przyciete.tif"
with rio.open(DEM_tif) as f:
    DEM_tif = f.read(1)
DEM = np.asarray(DEM_tif)
fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection='3d')
x = np.arange(0, DEM.shape[1])
y = np.arange(0, DEM.shape[0])
X, Y = np.meshgrid(x, y)
DEM_volumes = np.zeros(DEM.shape)+np.min(DEM)
# DEM_volumes[np.where(DEM == np.min(DEM))] = 400
ax.plot_surface(X, Y, DEM, color='green')  # cmap=cm.gist_earth)
ax.plot_surface(X, Y, DEM_volumes, color='blue')
# ax.contour(X, Y, DEM, cmap=cm.gist_earth)
# ax.plot_wireframe(X, Y, DEM)
ax.set_title('Powódź')
plt.show()
