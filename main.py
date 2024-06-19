import json
import os
import glob
import subprocess
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
from modulos.cropTIF import crop_TIF
from modulos.calculo_indices import *
from modulos.clasificador import clasificar_clases, clasificar_urbanizacion
from modulos.calculo_de_atracción import calculo_campo_atraccion

carpeta_recortadas = "ImagenesRecortadas"
carpeta_no_recortadas = "Imagenes"
ruta_poligono = os.path.abspath("data/ROI/poligono.shp")
print(ruta_poligono)

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
    if nombre_archivo.endswith(".TIF") or nombre_archivo.endswith(".tif"):  # Verifica la extensión del archivo
        ruta_completa = os.path.join(carpeta_no_recortadas, nombre_archivo)
        # Llama a la función procesar_archivo_tif con el nombre del archivo como parámetro
        crop_TIF(ruta_completa, f"{carpeta_recortadas}/{nombre_archivo}", ruta_poligono)


print("\nCálculo de índices:")
archivo_b4 = subprocess.run(f"ls {carpeta_recortadas}/*B4.TIF", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip("\n")
archivo_b5 = subprocess.run(f"ls {carpeta_recortadas}/*B5.TIF", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip("\n")

ruta_ndvi = f"{carpeta_recortadas}/ndvi.TIF"
calcular_ndvi(os.path.abspath(archivo_b4), os.path.abspath(archivo_b5), ruta_ndvi)

print("\t- Se calculó el NDVI")

archivo_b3 = subprocess.run(f"ls {carpeta_recortadas}/*B3.TIF", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip("\n")

calcular_ndwi(os.path.abspath(archivo_b3), os.path.abspath(archivo_b5), f"{carpeta_recortadas}/ndwi.TIF")

print("\t- Se calculó el NDWI")

print("*"*30)
print("\nComienza clasificación de clases.")

archivo_clases = "ImagenesRecortadas/class.TIF"

clasificar_clases("ImagenesRecortadas/ndvi.TIF", "ImagenesRecortadas/ndwi.TIF", archivo_clases)


import rasterio
import matplotlib.pyplot as plt
import earthpy.plot as ep



# Abrir el archivo TIFF con rasterio
with rasterio.open(archivo_clases) as src:
    # Leer la banda de clasificación
    clasificacion = src.read(1, masked=True)  # Se utiliza masked=True para ignorar los valores fuera de rango si los hay
    
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
cbar.ax.set_yticklabels(['Suelo expuesto', 'Vegetación baja', 'Vegetación alta', 'Agua'])  # Ajusta las etiquetas según tus clases
cbar.set_label('Clases')

# Añadir título
ax.set_title('Clasificación de Imagen')

# Mostrar la trama
plt.show()

print("\nFinaliza clasificación de clases.")

#-------------------------------------------------

print("*"*30)
print("\nComienza cálculo de campo de atracción.")



ruta_ndbi = f"{carpeta_recortadas}/ndbi.TIF"
ruta_ndbai = f"{carpeta_recortadas}/ndbai.TIF"
ruta_ndmi = f"{carpeta_recortadas}/ndmi.TIF"

print("\t- Se calcula el índice NDBI")
archivo_b6 = subprocess.run(f"ls {carpeta_recortadas}/*B6.TIF", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip("\n")
archivo_b5 = subprocess.run(f"ls {carpeta_recortadas}/*B5.TIF", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip("\n")
calcular_ndbi(os.path.abspath(archivo_b5), os.path.abspath(archivo_b6), os.path.abspath(ruta_ndbi))

print("\t- Se calcula el índice NDBaI")
archivo_b10 = subprocess.run(f"ls {carpeta_recortadas}/*B10.TIF", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip("\n")
calcular_ndbai(os.path.abspath(archivo_b6), os.path.abspath(archivo_b10), ruta_ndbai)

print("\t- Se calcula el índice NDMI")
calcular_ndbi(os.path.abspath(archivo_b5), os.path.abspath(archivo_b6), os.path.abspath(ruta_ndmi))


print("\t- Se clasifica la urbanización")
urbanizacion = clasificar_urbanizacion(os.path.abspath(ruta_ndbi), os.path.abspath(ruta_ndbai), os.path.abspath(ruta_ndmi), os.path.abspath(ruta_ndvi))

atraccion = calculo_campo_atraccion(urbanizacion)