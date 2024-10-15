"""
main.py

Este módulo es el punto de entrada para procesar carpetas de imágenes y rutas de {
polígonos utilizando varias funciones de procesamiento de imágenes y análisis geoespacial.

Dependencias:
-------------
- os: Proporciona una forma de usar funcionalidades dependientes del sistema operativo.
- subprocess: Permite la ejecución de comandos del sistema.
- argparse: Facilita la escritura de interfaces de línea de comandos amigables.
- rasterio: Biblioteca para leer y escribir datos raster.
- matplotlib: Biblioteca para la generación de gráficos en Python.
- modulos.cropTIF: Módulo para recortar imágenes TIF.
- modulos.calculo_indices: Módulo para calcular índices como NDVI, NDWI, NDBI y NDBAI.
- modulos.clasificador: Módulo para clasificar imágenes en diferentes clases y urbanización.
- modulos.calculo_de_atracción: Módulo para calcular el campo de atracción basado 
                                en la proximidad de viviendas.
- modulos.obtener_densidad_inicial: Módulo para obtener la densidad inicial de una región.

Argumentos:
-----------
- --carpeta_recortadas: Carpeta para imágenes recortadas.
- --carpeta_no_recortadas: Carpeta para imágenes no recortadas.
- --ruta_poligono: Ruta del archivo de polígono.
- --ruta_datos_ovitrampas: Ruta del archivo de datos de ovitrampas.

Ejemplo de uso:
---------------
python main.py  --carpeta_recortadas /ruta/a/carpeta_recortadas 
                --carpeta_no_recortadas /ruta/a/carpeta_no_recortadas 
                --ruta_poligono /ruta/a/poligono 
                --ruta_datos_ovitrampas /ruta/a/datos_ovitrampas
"""

import os
import subprocess
import argparse
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from modulos.crop_tif import crop_tif
from modulos.calculo_indices import calcular_ndvi, calcular_ndwi, calcular_ndbi, calcular_ndbai
from modulos.clasificador import clasificar_clases, clasificar_urbanizacion
from modulos.calculo_de_atracción import calculo_campo_atraccion
from modulos.obtener_densidad_inicial import obtener_densidad_inicial

parser = argparse.ArgumentParser(description="Procesar carpetas de imágenes y ruta del polígono.")

parser.add_argument('--carpeta_recortadas',
                    type=str,
                    help='Carpeta para imágenes recortadas')

parser.add_argument('--carpeta_no_recortadas',
                    type=str,
                    help='Carpeta para imágenes no recortadas')

parser.add_argument('--ruta_poligono',
                    type=str,
                    help='Ruta del archivo de polígono')

parser.add_argument('--ruta_datos_ovitrampas',
                    type=str,
                    help='Ruta del archivo de datos de ovitrampas')

args = parser.parse_args()

if not args.carpeta_recortadas:
    carpeta_recortadas = input("Por favor, ingrese la carpeta para imágenes recortadas: ")
else:
    carpeta_recortadas = args.carpeta_recortadas

if not args.carpeta_no_recortadas:
    carpeta_no_recortadas = input("Por favor, ingrese la carpeta para imágenes no recortadas: ")
else:
    carpeta_no_recortadas = args.carpeta_no_recortadas

if not args.ruta_poligono:
    ruta_poligono = input("Por favor, ingrese la ruta del archivo de polígono: ")
else:
    ruta_poligono = os.path.abspath(args.ruta_poligono)

if not args.ruta_datos_ovitrampas:
    ruta_datos_ovitrampas = input("Por favor, ingrese la ruta del archivo de datos de ovitrampas: ")
else:
    ruta_datos_ovitrampas = os.path.abspath(args.ruta_datos_ovitrampas)


if os.path.exists(carpeta_recortadas):
    print(f"La carpeta '{carpeta_recortadas}' existe.")
    os.system(f"rm -rf {carpeta_recortadas}/*")
else:
    print(f"La carpeta '{carpeta_recortadas}' no existe. Se creará ahora.")
    try:
        os.makedirs(carpeta_recortadas)
        print(f"Se ha creado la carpeta '{carpeta_recortadas}/'.")
    except OSError as e:
        print(f"No se pudo crear la carpeta '{carpeta_recortadas}': {e}")

# Itera sobre los archivos en el directorio
for nombre_archivo in os.listdir(carpeta_no_recortadas):
    if nombre_archivo.endswith(".TIF") or nombre_archivo.endswith(".tif"):
        ruta_completa = os.path.join(carpeta_no_recortadas, nombre_archivo)
        crop_tif(ruta_completa, f"{carpeta_recortadas}/{nombre_archivo}", ruta_poligono)


print("\nCálculo de índices:")
archivo_b4 = subprocess.run(f"ls {carpeta_recortadas}/*B4.TIF",
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            check=False).stdout.strip("\n")

archivo_b5 = subprocess.run(f"ls {carpeta_recortadas}/*B5.TIF",
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            check=False).stdout.strip("\n")

RUTA_NDVI = f"{carpeta_recortadas}/ndvi.TIF"
calcular_ndvi(os.path.abspath(archivo_b4), os.path.abspath(archivo_b5), RUTA_NDVI)

print("\t- Se calculó el NDVI")

archivo_b3 = subprocess.run(f"ls {carpeta_recortadas}/*B3.TIF",
                            shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            check=False).stdout.strip("\n")

calcular_ndwi(os.path.abspath(archivo_b3),
              os.path.abspath(archivo_b5),
              f"{carpeta_recortadas}/ndwi.TIF")

print("\t- Se calculó el NDWI")

print("*"*30)
print("\nComienza clasificación de clases.")

ARCHIVO_CLASES = f"{carpeta_recortadas}/class.TIF"

clasificar_clases("ImagenesRecortadas/ndvi.TIF", "ImagenesRecortadas/ndwi.TIF", ARCHIVO_CLASES)

# Abrir el archivo TIFF con rasterio
with rasterio.open(ARCHIVO_CLASES) as src:
    # Leer la banda de clasificación
    clasificacion = src.read(1, masked=True)  # Se utiliza masked=True para ignorar los valores \
                                              #fuera de rango si los hay

    # Obtener perfil de la imagen para obtener la transformación y la extensión
    profile = src.profile

# Definir los colores para cada clase
colors = ['brown', 'green', 'yellow', 'blue']  # Ajusta los colores según tu clasificación

# Crear un mapa de colores personalizado
cmap = ListedColormap(colors)

# Crear una figura y un eje utilizando matplotlib
fig, ax = plt.subplots(figsize=(10, 10))

# Mostrar la imagen de clasificación
im = ax.imshow(clasificacion, cmap=cmap, vmin=1, vmax=4, interpolation='none')

# Definir etiquetas para la barra de colores
cbar = ax.figure.colorbar(im, ax=ax, ticks=[1, 2, 3, 4], orientation='vertical')

cbar.ax.set_yticklabels(['Suelo expuesto',
                         'Vegetación baja', 
                         'Vegetación alta', 
                         'Agua'])  
cbar.set_label('Clases')

ax.set_title('Clasificación de Imagen')

plt.show()

print("\nFinaliza clasificación de clases.")

#-------------------------------------------------

print("*"*30)
print("\nComienza cálculo de campo de atracción.")



RUTDA_NDBI = f"{carpeta_recortadas}/ndbi.TIF"
RUTA_NDBAI = f"{carpeta_recortadas}/ndbai.TIF"
RUTA_NDMI = f"{carpeta_recortadas}/ndmi.TIF"

print("\t- Se calcula el índice NDBI")
archivo_b6 = subprocess.run(f"ls {carpeta_recortadas}/*B6.TIF",
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            check=False).stdout.strip("\n")

archivo_b5 = subprocess.run(f"ls {carpeta_recortadas}/*B5.TIF",
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            check=False).stdout.strip("\n")

calcular_ndbi(os.path.abspath(archivo_b5), os.path.abspath(archivo_b6), os.path.abspath(RUTDA_NDBI))

print("\t- Se calcula el índice NDBaI")
archivo_b10 = subprocess.run(f"ls {carpeta_recortadas}/*B10.TIF",
                             shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             text=True,
                             check=False).stdout.strip("\n")

calcular_ndbai(os.path.abspath(archivo_b6), os.path.abspath(archivo_b10), RUTA_NDBAI)

print("\t- Se calcula el índice NDMI")
calcular_ndbi(os.path.abspath(archivo_b5), os.path.abspath(archivo_b6), os.path.abspath(RUTA_NDMI))


print("\t- Se clasifica la urbanización")
urbanizacion = clasificar_urbanizacion(os.path.abspath(RUTDA_NDBI),
                                       os.path.abspath(RUTA_NDBAI),
                                       os.path.abspath(RUTA_NDMI),
                                       os.path.abspath(RUTA_NDVI))

atraccion = calculo_campo_atraccion(urbanizacion)


#-------------------------------------------------

print("*"*30)
print("\nComienza cálculo del mapa de densidad inicial.")

mapa_de_densidad = obtener_densidad_inicial(os.path.abspath(archivo_b4),
                                            ruta_datos_ovitrampas)
