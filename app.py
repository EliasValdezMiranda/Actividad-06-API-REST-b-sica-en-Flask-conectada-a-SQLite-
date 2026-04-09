from flask import Flask, jsonify, request, Response
from helpers import NOMBRE_TABLA_PRODUCTO
from helpers import existeTabla, createTablaProducto, selectTablaProducto, insertTablaProducto, verificarProducto, eliminarTablaProducto, actualizarTablaProducto

# Creación del objeto app y configuración del ordenamiento de claves en JSON
app = Flask(__name__)
app.json.sort_keys = False

# Métodos GET y POST
@app.route("/productos", methods=['GET', 'POST'])
def productoSingular():
    # Si no existe la tabla 'producto':
    # - Se devuelve un error en caso de que el método sea GET
    # - Se crea la tabla si el método es POST
    if not existeTabla(NOMBRE_TABLA_PRODUCTO):
        if request.method == 'GET':
            return jsonify({"Error": "No existen registros de productos (Crear con POST)"}), 404
        elif request.method == 'POST':
            createTablaProducto()
    # Si la tabla 'producto' existe:
    # - Se devuelven las entradas en esta si el método es GET
    # - Se toman los valores de la solicitud y se crea una nueva entrada si estos son válidos
    #   en caso de trabajar con un método POST
    if request.method == 'GET':
        return jsonify(selectTablaProducto()), 200
    elif request.method == 'POST':
        solicitud = request.get_json()
        resultado = verificarProducto(solicitud, False)
        # Si se obtiene un resultado diferente de None, se obtuvo un mensaje de error y se regresa en formato JSON.
        if resultado is not None:
            return jsonify(resultado), 400
        # Si no se encontraron errores, se crea una entrada a la base de datos y se informa al usuario del éxito.
        idCreado = insertTablaProducto(solicitud["nombre"],solicitud["categoria"],solicitud["precioMenudeo"],solicitud["precioMayoreo"],solicitud["existencias"])
        return jsonify({"Mensaje": f"Producto creado con ID #{idCreado}"}), 201

# Método PUT por ID
@app.route("/productos/<int:id>", methods=['PUT'])
def actualizarProducto(id):
    # Si no existe la tabla 'producto':
    # - Se devuelve un error
    if not existeTabla(NOMBRE_TABLA_PRODUCTO):
        return jsonify({'Error': 'No existen registros de productos (Crear con POST).'}), 404

    # Se intenta actualizar el producto con el ID proporcionado
    productoActualizado = actualizarTablaProducto(id)
    # Si el producto fue actualizado correctamente, se devuelve un mensaje de éxito
    if productoActualizado:
        return jsonify({"Mensaje": f"Producto  con ID #{id} actualizado exitosamente"}), 200
    # Si el producto no se pudo actualizar, devuelve un mensaje de error
    else:
        return jsonify({"Error": f"No se pudo actualizar el producto con #{id}"}), 404

# Método DELETE por ID
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminarProducto(id):
    # Si no existe la tabla 'producto':
    # - Se devuelve un error
    if not existeTabla(NOMBRE_TABLA_PRODUCTO):
        return jsonify({'Error': 'No existen registros de productos (Crear con POST).'}), 404
    
    # Se intenta eliminar el producto con el ID proporcionado
    productoEliminado = eliminarTablaProducto(id)
    
    # Si el producto fue eliminado exitosamente, se devuelve un mensaje de éxito
    if productoEliminado:
        return jsonify({"Mensaje": f"Producto con ID #{id} eliminado exitosamente"}), 200
    # Si el producto no existe, se devuelve un error 404
    else:
        return jsonify({"Error": f"No existe un producto con ID #{id}"}), 404
    

# Método main
def main():
    app.run(debug = True)

if __name__ == "__main__":
    main()