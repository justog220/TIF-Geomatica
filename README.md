<div align="center">

# Análisis de Densidad de Mosquitos con Datos de Ovitrampas y Landsat 8

[Descripción](#️-descripción) • [Estructura de Directorios](#-estructura-de-directorios) • [Links de Interés](#paperclip-links-de-interés) • [Contacto](#-contacto) • [Referencias](#-referencias)



<div style="text-align: center;">
    <div style="display: inline-flex; align-items: center;">
        <img src="imgs/logouner.png" alt="Logo UNER" style="height: 50px;">
    </div>
</div>

</div>

## 🛰️ Descripción

Este proyecto tiene como objetivo analizar la densidad de mosquitos en la región de Oro Verde, Entre Ríos, Argentina, utilizando datos recolectados con ovitrampas y combinándolos con imágenes satelitales del Landsat 8. 

Surge a partir de los trabajos propuestos por Rotela (2012), quien desarrolló una metodología para el análisis de la densidad de mosquitos en otras regiones. Nuestro objetivo es adaptar y aplicar esta metodología a una nueva área de interés, evaluando su eficacia y aportando nuevas perspectivas y datos específicos de la región de Oro Verde. Con esto, buscamos contribuir al control de vectores y mejorar las estrategias de prevención de enfermedades transmitidas por mosquitos.

## 📂 Estructura de directorios

- ***Imagenes/***: Directorio con imágenes Landsat para el Path y Row decidido que luego serán recortadas al área de interés.
- ***Informe/***: Directorio con los archivos utilizados para crear el informe.
- ***data/***: Datos utilizados a lo largo del proceso.
- ***imgs/***: Imágenes utilizadas en este README.
- ***modulos/***: Módulos desarrollados para el flujo de trabajo implementado y pruebas realizadas con ellos.
	- calculo_de_atraccion.py: Funciones para calcular y visualizar el campo de atracción basándose en la proximidad de viviendas.
	- calculo_indices.py: Implementación del cálculo de diversos índices a partir de bandas de Landsat 8.
	- clasificador.py: Funciones para clasificar clases de suelo y la presencia de viviendas en base a índices concretos y algoritmos de clustering no supervisado.
	- cropTIF.py: Funciones utilizadas para recortar un archivo TIF utilizando un shapefile de línea de corte y gdalwarp.
	- obtener_densidad_inicial.py: Funciones utilizadas para calcular el mapa de densidad de huevos utilizando datos de ovitrampas e interpolación gaussiana.
	- *.ipynb: Notebooks varios utilizados para probar alternativas de implementación de los módulos descritos previamente, además se incluyen funcionalidades para el procesamiento de archivos, como la reproyección al crs de las imágenes TIF de datos de ovitrampas y ka visualización de las mismas.
- Informe.pdf: Informe académico del trabajo realizado.
- main.py: Flujo de trabajo que implementa la utilización de los módulos para extraer características necesarias para el modelo a partir de las imágenes TIF.

### 📬 Contacto

- Alumno a cargo del proyecto:
	- justo.garcia@ingenieria.uner.edu.ar
- Docente a cargo de la materia:
	- walter.elias@uner.edu.ar

### 📚 Referencias

