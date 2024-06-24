import pandas as pd
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import subprocess

# Función gaussiana
def gaussian(x, y, x0, y0, sigma):
    """Calcula el valor de una función gaussiana bidimensional

    Args:
        x (numpy.ndarray): Coordenadas X de la matriz.
        y (numpy.ndarray): Coordenadas Y de la matriz.
        x0 (float): Coordenada X del centro de la gaussiana.
        y0 (float): Coordenada Y del centro de la gaussiana.
        sigma (float): Desviación estándar de la gaussiana.

    Returns:
        _type_: _description_
    """
    return np.exp(-((x - x0)**2 + (y - y0)**2) / (2 * sigma**2))

def obtener_densidad_inicial(tif_bg, ruta_datos):
    """Calcula un mapa de densidad de huevos utilizando una interpolación gaussiana sobre una imagen TIF de fondo.

    Args:
        tif_bg (str): Ruta al archivo TIF que se usará como fondo.
        ruta_datos (str): Ruta del archivo CSV que contiene los datos de los puntos.

    Returns:
        numpy.ndarray: Mapa de densidad calculado.
    """
    # Abrir el archivo TIF
    with rasterio.open(tif_bg) as src:
        # Leer la imagen TIF
        tif_image = src.read(1)  # Lee la banda 1 (puedes ajustar según la banda que necesites)
        # Obtener transformación y CRS (sistema de referencia de coordenadas)
        transform = src.transform
        crs = src.crs
        # Obtener límites de la imagen
        x_min, y_min, x_max, y_max = src.bounds
        # Resolución de píxeles en la imagen
        pixel_width, pixel_height = src.res

    # Cargar los datos desde el archivo CSV
    df = pd.read_csv(ruta_datos)

    # Filtrar datos por una fecha específica o cualquier otro criterio necesario
    # Ejemplo: Filtrar por una fecha específica (ajustar según tu CSV)
    df = df[df['fecha'] == '14/02/2018']

    # Obtener las columnas relevantes del CSV
    latitudes = df['y'].values
    longitudes = df['x'].values
    nro_huevos = df['nro_huevos'].values

    # Calcular la densidad de huevos por píxel interpolando con función gaussiana
    density_map = np.zeros_like(tif_image, dtype=np.float64)

    # Iterar sobre cada punto de datos y aplicar la interpolación gaussiana
    sigma = 3  # Parámetro de dispersión de la gaussiana
    for lat, lon, eggs in zip(latitudes, longitudes, nro_huevos):
        # Convertir coordenadas a índices de píxeles
        col, row = int((lon - x_min) / pixel_width), int((lat - y_min) / pixel_height)
        
        # Aplicar la función gaussiana alrededor del punto (row, col)
        y, x = np.indices(density_map.shape)
        density_map += eggs * gaussian(x, y, col, row, sigma)

    # Invertir el density_map en el eje vertical para corregir la inversión
    density_map = np.flipud(density_map)

    # Aplanar density_map para usarlo como sizes (opcional)
    sizes = 10 * nro_huevos
    
    # Crear la figura y el subplot
    fig, ax = plt.subplots(figsize=(10, 8))

    # Mostrar la imagen TIF en escala de grises
    ax.imshow(tif_image, cmap='gray', extent=[x_min, x_max, y_min, y_max])

    # Mostrar el density_map como una superposición de calor
    cbar = ax.imshow(density_map, cmap='hot', alpha=0.5, extent=[x_min, x_max, y_min, y_max])

    # Configurar colorbar sin normalización
    cbar = fig.colorbar(cbar, ax=ax, label='Número de huevos', fraction=0.046, pad=0.04)

    # Graficar puntos con tamaño proporcional a la densidad de huevos (opcional)
    ax.scatter(longitudes, latitudes, s=sizes, color='blue', alpha=0.5)

    ax.set_title('Mapa de densidad de número de huevos sobre imagen TIF (Interpolación gaussiana)')
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Latitud')
    ax.axis('off')

    # Mostrar la gráfica
    plt.show()

    return density_map
