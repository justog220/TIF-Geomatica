import subprocess

def crop_TIF(input_TIF, output_TIF, cutline_shapefile="poligono.shp"):
    # Construir el comando gdalwarp
    comando_gdalwarp = [
        "gdalwarp",
        "-cutline", cutline_shapefile,
        "-crop_to_cutline",
        input_TIF,
        output_TIF
    ]

    # Ejecutar el comando gdalwarp
    try:
        subprocess.run(comando_gdalwarp, check=True)
        print("El comando gdalwarp se ejecutó correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar gdalwarp: {e}")