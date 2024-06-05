import rasterio
import numpy as np
import os
import glob

RUTA_IMAGENES = "Imagenes/"


b4 = rasterio.open(glob.glob(os.path.join(RUTA_IMAGENES, '*B4*'))).read(1)
b5 = rasterio.open(glob.glob(os.path.join(RUTA_IMAGENES, '*B5*'))).read(1)

red = b4.astype('float64')
nir = b5.astype('float64')

ndvi=np.where(
    (nir+red)==0., #It will return 0 for No Data value
    0, 
    (nir-red)/(nir+red))


b4data = rasterio.open(glob.glob(os.path.join(RUTA_IMAGENES, '*B4*')))
ndviTiff = rasterio.open(f'{RUTA_IMAGENES}ndvi.tiff','w',driver='Gtiff',
                          width = b4data.width, 
                          height = b4data.height, 
                          count=1, crs=b4data.crs, 
                          transform=b4data.transform, 
                          dtype='float64')
ndviTiff.write(ndvi,1)
ndviTiff.close()