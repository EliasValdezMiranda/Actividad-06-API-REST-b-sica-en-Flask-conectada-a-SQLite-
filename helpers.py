import json
import os
import sqlite3

from app import productoActualizado

# Nombre de la base de datos y nombre de la tabla principal 0producto'
BASE_DATOS = "inventario.db"
NOMBRE_TABLA_PRODUCTO = "producto"

# Claves y display_name's de los atributos de la tabla 'producto'.
LLAVES_PRODUCTO = {
    "id": "ID",
    "nombre": "Nombre",
    "categoria": "Categoría",
    "precioMenudeo": "Precio a menudeo",
    "precioMayoreo": "Precio a mayoreo",
    "existencias": "Existencias"}

def conexionDB():
    """
    Crea un objeto de conexión a la base de datos SQLite3.

    :return: Conexión a la base de datos
    """
    return sqlite3.connect(BASE_DATOS)

def existeTabla(nombreTabla):
    """
    Verifica si existe la tabla `producto` en la base de datos `inventario.db`
    :param nombreTabla: Nombre de la tabla cuya existencia se buscará

    :return: `True` si la tabla existe, `False` si no existe.
    """

    # Se crea una conexión a la base de datos
    # y se almacena su cursor en una variable.
    conn = conexionDB()
    cursor = conn.cursor()
    # Se ejecuta la consulta de selección para verificar la existencia
    # de la tabla producto base de datos
    tabla = cursor.execute(
        """
        SELECT name FROM sqlite_master WHERE type='table'
        AND name = ?;
        """, (nombreTabla,)).fetchone()
    # Se cierra la conexión y se devuelve True si la tabla existe.
    # De lo contrario, False.
    conn.close()
    return True if tabla is not None else False

def createTablaProducto():
    """
    Crea la tabla `producto` en la base de datos `inventario.db`

    """

    # Se crea una conexión a la base de datos
    # y se almacena su cursor en una variable.
    conn = conexionDB()
    cursor = conn.cursor()
    # Se ejecuta la instrucción de creación de la base de datos.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            categoria TEXT,
            precioMenudeo REAL,
            precioMayoreo REAL,
            existencias INTEGER
        );
        """
    )
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()


def selectTablaProducto():
    """
    Maneja la instrucción de selección de la tabla `producto` de la base de datos.

    :return: Lista de diccionarios donde cada diccionario corresponde a una fila de la tabla `producto`
    """
    # Se crea una conexión a la base de datos
    # y se almacena su cursor en una variable.
    conn = conexionDB()
    cursor = conn.cursor()
    # Se ejecuta la consulta de selección.
    cursor.execute(
        """
        SELECT
            id, 
            nombre,
            categoria,
            precioMenudeo,
            precioMayoreo,
            existencias
        FROM producto;
        """
    )
    # Se extraen las filas del cursor y se agregan
    # a una lista en forma de diccionarios.
    datos = cursor.fetchall()
    productos = []
    for fila in datos:
        productos.append({
            "id": fila[0],
            "nombre": fila[1],
            "categoria": fila[2],
            "precioMenudeo": fila[3],
            "precioMayoreo": fila[4],
            "existencias": fila[5]
        })
    # Se cierra la conexión y se devuelven la lista de filas.
    conn.close()
    return productos


def insertTablaProducto(nombre, categoria, precioMenudeo, precioMayoreo, existencias):
    """
    Maneja la instrucción de inserción a la tabla `producto` de la base de datos.

    :param nombre: Nombre del producto por registrar.
    :param categoria: Nombre de la categoría en la que se encontrará el producto.
    :param precioMenudeo: Valor numérico correspondiente al precio a menudeo del producto.
    :param precioMayoreo: Valor numérico correspondiente al precio a mayoreo del producto.
    :param existencias: Valor numérico entero correspondiente a la cantidad de existencias del producto.
    :return: ID correspondiente al producto recien creado.
    """
    # Se crea una conexión a la base de datos.
    conn = conexionDB()
    # Se ejecuta una consulta de inserción tomando los valores de los parámetros.
    cursor = conn.execute(
        """
        INSERT INTO producto(nombre, categoria, precioMenudeo, precioMayoreo, existencias)
        VALUES (?,?,?,?,?)
        """
        ,(nombre,categoria,precioMenudeo,precioMayoreo,existencias)
    )
    # Se obtiene el ID de la fila recién creada.
    idCreado = cursor.lastrowid
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()
    # Se regresa el ID de la fila creada.
    return idCreado

def actualizarTablaProducto(nombre, categoria, precioMenudeo, precioMayoreo, existencias):
    """
    Maneja la instrucción de actualización en la tabla `producto` de la base de datos.

    :param nombre: Nombre del producto por registrar.
    :param categoria: Nombre de la categoría en la que se encontrará el producto.
    :param precioMenudeo: Valor numérico correspondiente al precio a menudeo del producto.
    :param precioMayoreo: Valor numérico correspondiente al precio a mayoreo del producto.
    :param existencias: Valor numérico entero correspondiente a la cantidad de existencias del producto.
    :return: ID correspondiente al producto recien actualizado.
    """

    # Se crea una conexión a la base de datos
    conn = conexionDB()

    # Se ejecuta el comando de actualización en la tabla 'productos' de la base de datos
    # Toma como referencia la id provista en la ruta
    cursor = conn.execute("""
                 UPDATE productos
                 SET nombre = ?,
                     categoria = ?,
                     precioMenudeo  = ?,
                     precioMayoreo = ?,
                     existencias = ?
                 WHERE id = ?
                 """, (nombre, categoria, precioMenudeo, precioMayoreo, existencias, id))

    # Se verifica si la fila fue eliminada exitosamente
    # (rowcount > 0 indica que se actualizó al menos una fila).
    productoActualizado = cursor.rowcount > 0

    # Se confirma la modificación sobre la base de datos, se cierra la conexión y
    # se devuelve True si se actualizó, False de lo contrario
    conn.commit()
    conn.close()

    # Se regresa True si el producto fue actualizado, False de lo contrario
    return productoActualizado

def eliminarTablaProducto(id):
    """
    Maneja la instrucción de eliminación en la tabla `producto` de la base de datos.
    
    :param id: ID del producto a eliminar.
    :return: `True` si el producto fue eliminado exitosamente, `False` si el producto no existe.
    """
    # Se crea una conexión a la base de datos.
    conn = conexionDB()
    
    # Se ejecuta una consulta de eliminación utilizando el ID como parámetro.
    cursor = conn.execute(
        """
        DELETE FROM producto
        WHERE id = ?;
        """
        ,(id,)
    )
    # Se verifica si la fila fue eliminada exitosamente
    # (rowcount > 0 indica que se eliminó al menos una fila).
    productoEliminado = cursor.rowcount > 0
    
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()
    
    # Se regresa True si el producto fue eliminado, False de lo contrario.
    return productoEliminado

def verificarProducto(diccionarioProducto, incluirID):
    """
    Verifica que un diccionario otorgado cuente con las claves esperadas
    de un producto de acuerdo a la especificación en este programa.

    :param diccionarioProducto: Diccionario de producto por analizar.
    :para incluirID: Valor booleano que indica si se eliminará la clave `id` del set de referencia.
    :return: El resultado de `verificarEntradas()` si el diccionario cumple con la estructura esperada por el programa, de lo contrario, un diccionario con un mensaje de error.
    """
    # Se crea un set de las claves del diccionario LLAVES_PRODUCTO
    # y otro set del diccionario correspondiente al producto por verificar.
    referencia = set(LLAVES_PRODUCTO)
    setDiccionario = set(diccionarioProducto)
    # Se elimina la ID para la verificación de solicitudes POST y PUT del usuario
    if not incluirID:
        referencia.remove("id")
    # Si las claves de ambos diccionarios coinciden, se pasa a la validación de entradas
    # numéricas
    if setDiccionario == referencia:
        return verificarEntradas(diccionarioProducto)
    # Si las claves de ambos diccionarios no coinciden, se busca la clave que no se encuentra
    # en el diccionario otorgado por el usuario.
    else:
        if incluirID and "id" not in setDiccionario:
            return {"Error": "ID no incluída en la solicitud JSON"}
        # Se utiliza el display_name del diccionario LLAVES_PRODUCTO para expresar
        # el mensaje de forma más clara.
        for clave, display_name in LLAVES_PRODUCTO.items():
            if clave not in setDiccionario and clave != "id":
                return {"Error": f"{display_name} no incluído en la solicitud JSON"}
        # Si, en un caso inusual, no se encuentra una clave con la que asociar la falla, se 
        # imprime un mensaje de error genérico.
        return {"Error": "La estructura de la solicitud no coincide con la solicitud esperada"}


def verificarEntradas(diccionarioProducto):
    """
    Verifica que las entradas numéricas de un diccionario correspondiente a un producto
    sean válidas

    :param diccionarioProducto: Diccionario de producto por analizar.
    :para incluirID: Valor booleano que indica si se eliminará la clave `id` del set de referencia.
    :return: `None` si el diccionario cumple con la estructura esperada por el programa, de lo contrario, un diccionario con un mensaje de error.
    """
    # Se evalúan las diferentes condiciones que podrían causar problemas con la inserción a la base de datos:
    # precioMenudeo
    if not verificarNumero(diccionarioProducto["precioMenudeo"], min = 0, isFloat = True):
        return {"Error": "El precio a menudeo debe ser un número real mayor a 0"}
    # precioMayoreo
    elif not verificarNumero(diccionarioProducto["precioMayoreo"], min = 0, isFloat = True):
        return {"Error": "El precio a mayoreo debe ser un número real mayor a 0"}
    elif diccionarioProducto["precioMayoreo"] > diccionarioProducto["precioMenudeo"]:
        return {"Error": "El precio a mayoreo no puede ser mayor al precio a menudeo"}
    # existencias
    elif not verificarNumero(diccionarioProducto["existencias"], min=0, isFloat = False):
        return {"Error": "Las existencias deben ser un número entero mayor o igual a 0"}
    else:
        return None


def verificarNumero(numero, min=None, isFloat=True):
    """
    Verifica que una entrada numérica cumpla con las características deseadas.

    :param numero: Valor numérico por analizar.
    :para min: Valor numérico opcional que indica el mínimo inclusivo con el que deberá cumplir la función.
    :param isFloat: Valor booleano que indica si el número que se espera es de punto flotante o no.
    :return: `True` si el número es válido, `False` de lo contrario.
    """
    # Se almacena el tipo de entradas que se aceptarán de acuerdo a si el número será entero o flotante.
    tipoNumero = (float, int) if isFloat else int
    # Si el número otorgado no pertenece a los tipos de entradas aceptado, se devuelve False.
    if not isinstance(numero, tipoNumero):
        return False
    # Si el número es mayor o igual al mínimo, se regresa True. De lo contrario, False.
    return numero >= min