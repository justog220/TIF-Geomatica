import rasterio
import numpy as np

"""
El cálculo de índices y su implementación fue pensado teniendo en cuenta
las bandas que corresponden a satélites Landsat 8.
"""

def calcular_ndvi(b4_file, b5_file, output_file):
    """Calcula el Índice de Vegetación de Diferencia Normalizada (NDVI) a partir de archivos raster de bandas 4 y 5.

    Args:
        b4_file (str): Ruta al archivo raster de la banda roja (banda 4).
        b5_file (str): Ruta al archivo raster de la banda infrarroja cercana (banda 5).
        output_file (str): Ruta donde se guardará el archivo raster resultante del NDVI.

    Descripción:
    ------------
    Esta función calcula el NDVI utilizando las fórmulas estándar:
    NDVI = (NIR - Red) / (NIR + Red)
    donde NIR es el valor de la banda infrarroja cercana y Red es el valor de la banda roja.

    La función utiliza rasterio para abrir los archivos de entrada (banda 4 y banda 5), realiza el cálculo del NDVI
    para cada píxel, y luego guarda el resultado en un nuevo archivo raster especificado por `output_file`
    """
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
    """
    Calcula el Índice de Agua de Diferencia Normalizada (NDWI) a partir de archivos raster de bandas 3 y 5.

    Args:
        b3_file (str): Ruta al archivo raster de la banda verde (banda 3).
        b5_file (str): Ruta al archivo raster de la banda infrarroja cercana (banda 5).
        output_file (str): Ruta donde se guardará el archivo raster resultante del NDWI.

    Descripción:
    ------------
    Esta función calcula el NDWI utilizando las fórmulas estándar:
    NDWI = (Green - NIR) / (Green + NIR)
    donde Green es el valor de la banda verde y NIR es el valor de la banda infrarroja cercana.

    La función utiliza rasterio para abrir los archivos de entrada (banda 3 y banda 5), realiza el cálculo del NDWI
    para cada píxel, y luego guarda el resultado en un nuevo archivo raster especificado por `output_file`.
    """
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
    """
    Calcula el Índice de Diferencia de Brillo Normalizado (NDBI) a partir de archivos raster de bandas 5 y 6.

    Args:
        b5_file (str): Ruta al archivo raster de la banda infrarroja cercana (banda 5).
        b6_file (str): Ruta al archivo raster de la banda infrarroja de onda corta (banda 6).
        output_file (str): Ruta donde se guardará el archivo raster resultante del NDBI.

    Descripción:
    ------------
    Esta función calcula el NDBI utilizando las fórmulas estándar:
    NDBI = (SWIR - NIR) / (SWIR + NIR)
    donde SWIR es el valor de la banda infrarroja de onda corta y NIR es el valor de la banda infrarroja cercana.

    La función utiliza rasterio para abrir los archivos de entrada (banda 5 y banda 6), realiza el cálculo del NDBI
    para cada píxel, y luego guarda el resultado en un nuevo archivo raster especificado por `output_file`.
    """
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
    """
    Calcula el Índice Normalizado de Diferencia de Bareness y Albedo Integrado (NDBaI) a partir de archivos raster de bandas 6 y 10.

    Args:
        b6_file (str): Ruta al archivo raster de la banda de infrarrojo de onda corta (SWIR1 o banda 6).
        b10_file (str): Ruta al archivo raster de la banda de sensor infrarrojo térmico de onda larga (TIRS1 o banda 10).
        output_file (str): Ruta donde se guardará el archivo raster resultante del NDBaI.

    Descripción:
    ------------
    Esta función calcula el NDBaI utilizando la fórmula estándar:
    NDBaI = (SWIR1 - TIRS1) / (SWIR1 + TIRS1)
    donde SWIR1 es el valor de la banda de infrarrojo de onda corta (banda 6) y TIRS1 es el valor de la banda de sensor infrarrojo térmico de onda larga (banda 10).

    La función utiliza rasterio para abrir los archivos de entrada (banda 6 y banda 10), realiza el cálculo del NDBaI
    para cada píxel, y luego guarda el resultado en un nuevo archivo raster especificado por `output_file`.
    """
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
    """
    Calcula el Índice Normalizado de Diferencia de Humedad (NDMI) a partir de archivos raster de bandas 5 y 6.

    Args:
        b5_file (str): Ruta al archivo raster de la banda infrarroja cercana (NIR o banda 5).
        b6_file (str): Ruta al archivo raster de la banda infrarroja de onda corta (SWIR1 o banda 6).
        output_file (str): Ruta donde se guardará el archivo raster resultante del NDMI.

    Descripción:
    ------------
    Esta función calcula el NDMI utilizando la fórmula estándar:
    NDMI = (NIR - SWIR1) / (NIR + SWIR1)
    donde NIR es el valor de la banda infrarroja cercana y SWIR1 es el valor de la banda infrarroja de onda corta.

    La función utiliza rasterio para abrir los archivos de entrada (banda 5 y banda 6), realiza el cálculo del NDMI
    para cada píxel, y luego guarda el resultado en un nuevo archivo raster especificado por `output_file`.
    """
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


