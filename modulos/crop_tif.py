"""
crop_tif.py

Este módulo contiene funciones para recortar archivos TIF utilizando shapefiles de 
línea de corte con la herramienta gdalwarp de GDAL.

Dependencias:
-------------
- subprocess: Permite la ejecución de comandos del sistema.

Funciones:
----------
- crop_tif(input_tif, 
            output_tif,
            cutline_shapefile): Recorta un archivo TIF utilizando un shapefile 
                                de línea de corte usando gdalwarp.

    Args:
        input_tif (str): Ruta al archivo TIF de entrada que se recortará.
        output_tif (str): Ruta donde se guardará el archivo TIF recortado.
        cutline_shapefile (str): Ruta al shapefile que define la línea de corte para el recorte.

    Descripción:
    ------------
    Esta función utiliza la herramienta gdalwarp de GDAL para recortar un archivo TIF 
    utilizando un shapefile de línea de corte. El proceso consiste en construir un 
    comando gdalwarp con los parámetros adecuados, que incluyen el shapefile como línea de corte
    y la opción para recortar según esta línea. Si el comando se ejecuta correctamente, se 
    guarda el archivo TIF recortado en la ubicación especificada por `output_tif`.

Ejemplo de uso:
---------------
from modulos.crop_tif import crop_tif

crop_tif('/ruta/a/input.tif', '/ruta/a/output.tif', '/ruta/a/cutline.shp')
"""

import subprocess

def crop_tif(input_tif, output_tif, cutline_shapefile):
    """
    Recorta un archivo TIF utilizando un shapefile de línea de corte usando gdalwarp.

    Args:
        input_TIF (str): Ruta al archivo TIF de entrada que se recortará.
        output_TIF (str): Ruta donde se guardará el archivo TIF recortado.
        cutline_shapefile (str): Ruta al shapefile que define la línea de corte para el recorte.

    Descripción:
    ------------
    Esta función utiliza la herramienta gdalwarp de GDAL para recortar un archivo TIF 
    utilizando un shapefile de línea de corte. El proceso consiste en construir un 
    comando gdalwarp con los parámetros adecuados, que incluyen el shapefile como línea de corte
    y la opción para recortar según esta línea. Si el comando se ejecuta correctamente, se 
    guarda el archivo TIF recortado en la
    ubicación especificada por `output_TIF`.
    """
    # Construir el comando gdalwarp
    comando_gdalwarp = [
        "gdalwarp",
        "-cutline", cutline_shapefile,
        "-crop_to_cutline",
        input_tif,
        output_tif
    ]

    # Ejecutar el comando gdalwarp
    try:
        subprocess.run(comando_gdalwarp, check=True)
        print("El comando gdalwarp se ejecutó correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar gdalwarp: {e}")
