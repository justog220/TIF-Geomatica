# import json

# with open('data/param.json', 'r') as file:
#     param = json.load(file)
    
# alpha = param['alpha']
# beta = param['beta']
# k_h = param['k_h']
# d_r = param['d_r']
# d_w = param['d_w']

# clases = 

import os
import subprocess
from modulos.cropTIF import crop_TIF

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


