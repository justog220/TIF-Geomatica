from qgis.core import QgsApplication, QgsProject, QgsRasterCalculator, QgsRasterLayer
import os
import os
import glob


RUTA_IMAGENES = "../Imagenes/"

# Iniciar la aplicación QGIS
qgs = QgsApplication([], False)
qgs.initQgis()

# Rutas a los archivos de las bandas roja e infrarroja
# ruta_banda_roja = '/ruta/a/tu/banda_roja.tif'
ruta_banda_roja = glob.glob(os.path.join(RUTA_IMAGENES, '*B4*'))
# ruta_banda_infrarroja = '/ruta/a/tu/banda_infrarroja.tif'
ruta_banda_infrarroja = glob.glob(os.path.join(RUTA_IMAGENES, '*B5*'))

# Agregar las bandas como capas raster al proyecto de QGIS
banda_roja_layer = QgsRasterLayer(ruta_banda_roja, 'Banda Roja')
banda_infrarroja_layer = QgsRasterLayer(ruta_banda_infrarroja, 'Banda Infrarroja')

# Comprobar si las capas se cargaron correctamente
if not banda_roja_layer.isValid() or not banda_infrarroja_layer.isValid():
    print('Error: No se pudo cargar una o ambas capas.')
else:
    # Agregar las capas al proyecto de QGIS
    QgsProject.instance().addMapLayer(banda_roja_layer)
    QgsProject.instance().addMapLayer(banda_infrarroja_layer)

    # Cálculo del NDVI
    ndvi_expresion = '(B@1 - A@1) / (B@1 + A@1)'
    ndvi_calculadora = QgsRasterCalculator(
        ndvi_expresion,
        {'A': banda_roja_layer, 'B': banda_infrarroja_layer},
        'GTiff',
        banda_roja_layer.extent(),
        banda_roja_layer.width(),
        banda_roja_layer.height(),
    )
    ndvi_resultado = ndvi_calculadora.processCalculation()

    # Guardar el resultado en un archivo raster
    ruta_ndvi_resultado = '/ruta/donde/guardar/ndvi_resultado.tif'
    QgsRasterLayer.exportRasterLayer(ndvi_resultado, ruta_ndvi_resultado, 'GTiff')

# Cerrar la aplicación QGIS
qgs.exitQgis()
