import rasterio
import numpy as np

"""
El cálculo de índices y su implementación fue pensado teniendo en cuenta
las bandas que corresponden a satélites Landsat 8.
"""

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
    b3 = rasterio.open(b3_file).read(1)
    b5 = rasterio.open(b5_file).read(1)

    green = b3.astype('float64')
    nir = b5.astype('float64')

    ndwi=np.where(
        (nir+green)==0., #It will return 0 for No Data value
        0, 
        (green-nir)/(nir+green))


    b3data = rasterio.open(b3_file)
    ndwiTiff = rasterio.open(output_file,'w',driver='Gtiff',
                            width = b3data.width, 
                            height = b3data.height, 
                            count=1, crs=b3data.crs, 
                            transform=b3data.transform, 
                            dtype='float64')
    ndwiTiff.write(ndwi,1)
    ndwiTiff.close()


def calcular_ndbi(b5_file, b6_file, output_file):
    b6 = rasterio.open(b6_file).read(1)
    b5 = rasterio.open(b5_file).read(1)

    swir = b6.astype('float64')
    nir = b5.astype('float64')

    ndbi=np.where(
        (nir+swir)==0., 
        0, 
        (swir-nir)/(nir+swir))


    b6data = rasterio.open(b6_file)
    ndbiTiff = rasterio.open(output_file,'w',driver='Gtiff',
                            width = b6data.width, 
                            height = b6data.height, 
                            count=1, crs=b6data.crs, 
                            transform=b6data.transform, 
                            dtype='float64')
    ndbiTiff.write(ndbi,1)
    ndbiTiff.close()


def calcular_ndbai(b6_file, b10_file, output_file):
    # ndbai = (swir1 - swir2) / (swir1 + swir2)
    b6 = rasterio.open(b6_file).read(1)
    b10 = rasterio.open(b10_file).read(1)

    swir = b6.astype('float64')
    tirs1 = b10.astype('float64')

    ndbai=np.where(
        (tirs1+swir)==0., 
        0, 
        (swir-tirs1)/(tirs1+swir))


    b6data = rasterio.open(b6_file)
    ndbaiTiff = rasterio.open(output_file,'w',driver='Gtiff',
                            width = b6data.width, 
                            height = b6data.height, 
                            count=1, crs=b6data.crs, 
                            transform=b6data.transform, 
                            dtype='float64')
    ndbaiTiff.write(ndbai,1)
    ndbaiTiff.close()


def calcular_ndmi(b5_file, b6_file, output_file):
    # ndmi = (nir-swir1) / (swir1 + nir)
    b5 = rasterio.open(b5_file).read(1)
    b6 = rasterio.open(b6_file).read(1)

    nir = b5.astype('float64')
    swir = b6.astype('float64')

    ndmi=np.where(
        (swir+nir)==0., 
        0, 
        (nir-swir)/(swir+nir))


    b6data = rasterio.open(b6_file)
    ndmiTiff = rasterio.open(output_file,'w',driver='Gtiff',
                            width = b6data.width, 
                            height = b6data.height, 
                            count=1, crs=b6data.crs, 
                            transform=b6data.transform, 
                            dtype='float64')
    ndmiTiff.write(ndmi,1)
    ndmiTiff.close()


