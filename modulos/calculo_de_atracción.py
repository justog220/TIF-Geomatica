import numpy as np
import matplotlib.pyplot as plt

def calculo_campo_atraccion(viviendas):
    """Calcula y visualiza el campo de atracción basado en la proximidad de viviendas

    Args:
        viviendas (numpy.ndarray): Matriz binaria donde cada elemento indica la presencia o no de una vivienda.

    Returns:
        numpy.ndarray: Matriz que representa el nivel de atracción de cada posición basado en la proximidad de otras viviendas.


    Descripción:
    ------------
    Esta función calcula el campo de atracción para una matriz de viviendas dada. Utiliza una ventana de tamaño 3x3
    alrededor de cada píxel para contar cuántas viviendas están presentes en esa vecindad. Luego, asigna un valor
    de atracción proporcional al número de viviendas vecinas.

    La función tambien genera un mapa de calor (heatmap) que visualiza el campo de atracción calculado. Este mapa
    se guarda como 'campoDeAtraccion.png' en el directorio de trabajo actual y se muestra en pantalla.
    """
    # Tamaño de la ventana (3 píxeles alrededor de cada píxel)
    ventana_size = 3

    # Crear un arreglo de atracción inicializado con ceros
    atraccion = np.zeros_like(viviendas, dtype=float)

    # Obtener dimensiones del arreglo de viviendas
    filas, columnas = viviendas.shape

    # Iterar sobre cada píxel del arreglo de viviendas
    for i in range(filas):
        for j in range(columnas):
            # Si el píxel contiene una vivienda, verificar la ventana 90x90
            viviendas_vecinas = 0
            vecinas = 0
            for di in range(-ventana_size, ventana_size + 1):
                for dj in range(-ventana_size, ventana_size + 1):
                    ni, nj = i + di, j + dj
                    # Verificar límites del arreglo
                    if 0 <= ni < filas and 0 <= nj < columnas:
                        vecinas += 1
                        if viviendas[ni, nj]:
                            viviendas_vecinas += 1
            
            atraccion[i, j] = 1 * (viviendas_vecinas/vecinas)


    # Crear un heatmap de atracción
    plt.figure(figsize=(8, 6))
    plt.imshow(atraccion, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Atracción')
    plt.title('Campo de atracción')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('campoDeAtraccion.png')
    plt.show()

    return atraccion