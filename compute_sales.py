"""Este módulo calcula el costo total de las ventas a partir de un
catálogo de precios y un registro de ventas."""

import json
import sys
import time
import logging

# Configuración del logger
logging.basicConfig(filename='computeSales.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def buscar_producto(catalogo_, producto):
    """Busca un producto en el catálogo y devuelve su precio.

    Args:
        catalogo (list): Lista de diccionarios con la información de los productos.
        producto (str): Nombre del producto a buscar.

    Returns:
        float: El precio del producto si se encuentra, None en caso contrario.
    """
    for item in catalogo_:
        if producto == item["title"]:
            return item["price"]
    return None  # Devuelve None si el producto no se encuentra


def calcular_costo_total(catalogo_, ventas_):
    """Calcula el costo total de las ventas.

    Args:
        catalogo (list): Lista de diccionarios con la información de los productos.
        ventas (list): Lista de diccionarios con la información de las ventas.

    Returns:
        float: El costo total de las ventas.
    """
    costo_total_ = 0

    for venta in ventas_:
        for item in venta.get('items', []):  # Maneja la posible falta de 'items'
            try:
                producto = item['Product']
                cantidad = item['Quantity']
                precio = buscar_producto(catalogo_, producto)

                if precio is None:
                    logging.error("Producto no encontrado en el catálogo: %s", producto)
                    print(f"Error: Producto no encontrado en el catálogo: {producto}")
                    continue

                costo_total_ += precio * cantidad
            except KeyError as e:
                logging.error("Falta la clave %s en el item: %s", e, item)
                print(f"Error: Datos de venta inválidos (falta clave {e}): {item}")
            except TypeError as e:
                logging.error("Error de tipo al calcular el costo: %s. Item: %s", e, item)
                print(f"Error: Datos de venta inválidos (error de tipo): {item}")
    return costo_total_


def escribir_resultados(costo, tiempo):
    """Escribe los resultados en un archivo y en la consola.

    Args:
        costo (float): El costo total de las ventas.
        tiempo (float): El tiempo de ejecución en segundos.
    """

    resultados = f"Costo total de las ventas: ${costo:.2f}\n"
    resultados += f"Tiempo de ejecución: {tiempo:.6f} segundos\n"

    print(resultados)

    with open("SalesResults.txt", "w", encoding="utf-8") as archivo:
        archivo.write(resultados)


def cargar_datos(nombre_archivo):
    """Carga datos desde un archivo JSON.

    Args:
        nombre_archivo (str): El nombre del archivo JSON.

    Returns:
        list o dict: Los datos cargados desde el archivo JSON.
            Sale del programa con código 1 si hay un error.
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        logging.error("Archivo no encontrado: %s", nombre_archivo)
        print(f"Error: Archivo no encontrado: {nombre_archivo}")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.error("Error al decodificar JSON en: %s", nombre_archivo)
        print(f"Error: Archivo JSON inválido: {nombre_archivo}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python computeSales.py priceCatalogue.json salesRecord.json")
        sys.exit(1)

    catalogo_archivo = sys.argv[1]
    registro_archivo = sys.argv[2]

    tiempo_inicio = time.time()

    catalogo = cargar_datos(catalogo_archivo)
    ventas = cargar_datos(registro_archivo)

    costo_total = calcular_costo_total(catalogo, ventas)

    tiempo_fin = time.time()
    tiempo_transcurrido = tiempo_fin - tiempo_inicio
    escribir_resultados(costo_total, tiempo_transcurrido)
