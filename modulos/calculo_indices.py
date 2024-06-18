import rasterio
import numpy as np


def calcular_ndvi(b4_file, b5_file, output_file):
    b4 = rasterio.open(b4_file).read(1)
    b5 = rasterio.open(b5_file).read(1)

    red = b4.astype('float64')
    nir = b5.astype('float64')

    ndvi=np.where(
        (nir+red)==0., #It will return 0 for No Data value
        0, 
        (nir-red)/(nir+red))


    b4data = rasterio.open(b4_file)
    ndviTiff = rasterio.open(output_file,'w',driver='Gtiff',
                            width = b4data.width, 
                            height = b4data.height, 
                            count=1, crs=b4data.crs, 
                            transform=b4data.transform, 
                            dtype='float64')
    ndviTiff.write(ndvi,1)
    ndviTiff.close()


def calcular_ndwi(b3_file, b5_file, output_file):
    b4 = rasterio.open(b3_file).read(1)
    b5 = rasterio.open(b5_file).read(1)

    red = b4.astype('float64')
    nir = b5.astype('float64')

    ndvi=np.where(
        (nir+red)==0., #It will return 0 for No Data value
        0, 
        (nir-red)/(nir+red))


    b3data = rasterio.open(b3_file)
    ndviTiff = rasterio.open(output_file,'w',driver='Gtiff',
                            width = b3data.width, 
                            height = b3data.height, 
                            count=1, crs=b3data.crs, 
                            transform=b3data.transform, 
                            dtype='float64')
    ndviTiff.write(ndvi,1)
    ndviTiff.close()
