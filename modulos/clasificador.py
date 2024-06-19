import rasterio
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import subprocess
import os
from matplotlib.colors import ListedColormap

def clasificar_clases(ndvi_route, ndwi_route, output):
    """Clasifica clases de cobertura del suelo basadas en valores de NDVI y NDWI de archivos raster.

    Args:
        ndvi_route (str): Ruta al archiv raster del Índice Normalizado de Diferencia de Vegetación (NDVI).
        ndwi_route (str): Ruta al archivo raster del Índice Normalizado de Diferencia de Agua (NDWI).
        output (str): Ruta donde se guardará el archivo raster resultante de la clasificación.
    
    Descripción:
    -----------
    Esta función clasifica diferentes clases de cobertura del suelo utilizando los valores de NDVI y NDWI:
    - Clase 0: Agua (según el umbral definido en NDWI).
    - Clase 1: Suelo expuesto (NDVI entre 0.0 y 0.25).
    - Clase 2: Vegetación baja (NDVI entre 0.25 y 0.4).
    - Clase 3: Vegetación alta (NDVI mayor o igual a 0.4).

    La función abre los archivos raster de NDVI y NDWI usando rasterio, calcula máscaras para cada clase basadas en estos índices,
    asigna los píxeles correspondientes a cada clase en un array de clasificación, y guarda el resultado en un archivo raster
    especificado por `output`
    """
    with rasterio.open(ndwi_route) as src:
        ndwi = src.read(1)
        width = src.width
        height = src.height

    with rasterio.open(ndvi_route) as src:
        ndvi = src.read(1)

    umbral_agua = 0.0

    mascara_agua = ndwi > umbral_agua

    # Crear un array para la clasificación final
    classification = np.zeros_like(ndvi, dtype=np.uint8)

    # Asignar las clases según las máscaras
    classification[mascara_agua] = 0  # Clase 0: Agua
    classification[(ndvi >= 0.0) & (ndvi < 0.25)] = 1  # Clase 1: Suelo expuesto
    classification[(ndvi >= 0.25) & (ndvi < 0.4)] = 2  # Clase 2: Vegetación baja
    classification[ndvi >= 0.4] = 3  # Clase 3: Vegetación alta

    # # Guardar la clasificación en un nuevo archivo TIFF
    with rasterio.open(ndvi_route) as src:
            profile = src.profile

            # Actualizar perfil para el archivo de clasificación
            profile.update(
                dtype=rasterio.uint8,
                count=1
            )

            # Guardar la clasificación en un archivo TIFF
            with rasterio.open(output, 'w', **profile) as dst:
                dst.write(classification, 1)

def clasificar_urbanizacion(ndbi_route, ndbai_route, ndmi_route, ndvi_route):
    """
    Realiza la clasificación de zonas de urbanización utilizando índices espectrales y K-means clustering.

    Args:
        ndbi_route (str): Ruta al archivo raster del Índice de Diferencia Normalizada de Edificación (NDBI).
        ndbai_route (str): Ruta al archivo raster del Índice Normalizado de Diferencia de Bareness y Albedo Integrado (NDBaI).
        ndmi_route (str): Ruta al archivo raster del Índice de Diferencia Normalizada de Humedad (NDMI).
        ndvi_route (str): Ruta al archivo raster del Índice de Vegetación de Diferencia Normalizada (NDVI).

    Returns:
        numpy.ndarray: Matriz booleana donde True representa zonas clasificadas como urbanas y False como no urbanas.

    Descripción:
    ------------
    Esta función utiliza los índices espectrales NDBI, NDBaI, NDMI y NDVI para clasificar zonas de urbanización mediante K-means clustering.
    Primero, aplica máscaras basadas en el NDVI para filtrar áreas de vegetación. Luego, crea un DataFrame con los valores de índices
    filtrados y aplica K-means con 2 clusters para identificar áreas urbanas y no urbanas. El usuario selecciona manualmente y en base a su conocimiento del área el label que
    representa las zonas urbanas, y se devuelve una matriz booleana que indica las zonas clasificadas como urbanas.
    """
    with rasterio.open(ndbi_route) as bandNdvi:
        ndbi = bandNdvi.read(1).astype('float32')

    with rasterio.open(ndbai_route) as bandNdbai:
        ndbai = bandNdbai.read(1).astype('float32')

    with rasterio.open(ndmi_route) as bandNimi:
        nimi = bandNimi.read(1).astype('float32')

    with rasterio.open(ndvi_route) as bandNdvi:
        ndvi = bandNdvi.read(1).astype('float32')


    # Creamos una máscara para valores de ndvi que representen vegetacion
    mascara_vegetacion = ndvi > 0.3

    # Aplicar las máscaras a los índices espectrales
    masked_ndbi = np.where((mascara_vegetacion) & (ndbi > 0), np.nan, ndbi)
    masked_ndbai = np.where(mascara_vegetacion, np.nan, ndbai)
    masked_nimi = np.where(mascara_vegetacion, np.nan, nimi)

    # Crear un DataFrame con los índices calculados
    data = {
        'masked_NDBI': masked_ndbi.flatten(),
        'masked_NDBaI': masked_ndbai.flatten(),
        'masked_NIMI': masked_nimi.flatten(),
    }

    df = pd.DataFrame(data).dropna()

    # Aplicar K-means
    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans.fit(df)

    # Obtener las etiquetas de los clusters
    clusters = kmeans.labels_

    # Crear una matriz de clusters completa para visualización
    clusters_full = np.full(masked_ndbi.shape, np.nan)
    # clusters_full[mascara_vegetacion] = clusters
    clusters_full[~(mascara_vegetacion)] = clusters

    # Definir colores para cada cluster
    colors = ['red', 'blue']  # Cambiar según los colores deseados para cada cluster

    # Crear un colormap personalizado
    cmap_custom = ListedColormap(colors)

    # Obtener las dimensiones del gráfico
    height, width = clusters_full.shape

    # Visualizar los clusters con colormap personalizado
    plt.imshow(clusters_full, cmap=cmap_custom)
    plt.colorbar(ticks=[0, 1], boundaries=[-0.5, 0.5, 1.5], label='Clusters')
    plt.title('K-means Clustering with 2 Clusters (Masked)')
    plt.axis('off')
    # Agregar el texto al plot
    plt.text(1, height - 0.5, 'Recuerde el label de la clase que cree que es urbanización', 
            fontsize=12, color='white', backgroundcolor='black', 
            bbox=dict(facecolor='black', alpha=0.8))
    plt.show()

    label_urbano = input("\t\tIngrese el label correspondiente a la zona urbana: ")

    while(not int(label_urbano) in [0, 1]):
        label_urbano = input("\tIngrese un label válido (0 o 1): ")

    label_urbano = int(label_urbano)

    plt.close()

    clusters_full[np.isnan(clusters_full)] = not label_urbano

    clusters_full = np.where(clusters_full == label_urbano, True, False)

    return clusters_full



