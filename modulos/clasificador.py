import rasterio
import numpy as np

def clasificar(ndvi_route, ndwi_route, output):
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
    # Por ejemplo:
    classification[mascara_agua] = 0  # Clase 0: Agua
    classification[(ndvi >= 0.0) & (ndvi < 0.25)] = 1  # Clase 1: Suelo expuesto
    classification[(ndvi >= 0.25) & (ndvi < 0.4)] = 2  # Clase 2: Vegetación baja
    classification[ndvi >= 0.4] = 3  # Clase 3: Vegetación alta

    # # Guardar la clasificación en un nuevo archivo TIFF
    # with rasterio.open(output, 'w', driver='GTiff',
    #                 width=width, height=height,
    #                 count=1, dtype=classification.dtype) as dst:
    #     dst.write(classification, 1)

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

