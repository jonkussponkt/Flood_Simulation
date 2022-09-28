import matplotlib.pyplot as plt
import numpy as np
import rasterio as rio
from IPython.display import Image
import os
os.environ["R_HOME"] = r"C:\Program Files\R\R-4.1.2"

import rpy2.robjects as ro
import rpy2.robjects.numpy2ri
import rpy2.robjects.packages as rpackages


def rayshade(z, image_path=None, zscale=10, fov=0, theta=210, zoom=0.7, phi=35, windowsize=(1000, 800)):
    # Output path.
    if not image_path:
        image_path = r"C:\Users\Jan\PycharmProjects\inzynierka\img\dem_sad_test.png"
        # Import needed packages.
        rpackages.importr('rayshader')

        # Convert array to matrix.
        z = np.asarray(z)
        rows, cols = z.shape
        z_mat = ro.r.matrix(z, nrow=rows, ncol=cols)
        ro.globalenv['elmat'] = z_mat

        # Save python state to r.
        ro.globalenv['img_path'] = image_path
        ro.globalenv['zscale'] = zscale
        ro.globalenv['fov'] = fov
        ro.globalenv['theta'] = theta
        ro.globalenv['zoom'] = zoom
        ro.globalenv['phi'] = phi
        ro.globalenv['windowsize'] = ro.IntVector(windowsize)

        # Do the render.
        ro.r('''
            elmat %>%
              sphere_shade(texture = "imhof4") %>%
              add_water(detect_water(elmat), color = "blue") %>%
              plot_3d(elmat, zscale = zscale, fov = fov, theta = theta, zoom = zoom, phi = phi, windowsize = windowsize)
            Sys.sleep(0.2)
            render_snapshot(img_path)
        ''')

        # Return path.
        return image_path


rpy2.robjects.numpy2ri.activate()
DEM = r"C:\Users\Jan\PycharmProjects\inzynierka\img\dem_Sadecczyzna_przyciete.tif"
with rio.open(DEM) as f:
    z = f.read(1)
plt.imshow(z)
plt.show()
img_path = rayshade(z)

Image(filename=img_path)
