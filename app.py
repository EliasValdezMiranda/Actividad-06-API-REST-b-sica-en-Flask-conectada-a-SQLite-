from flask import Flask, jsonify, request, Response
from helpers import NOMBRE_TABLA_PRODUCTO
from helpers import existeTabla, createTablaProducto, selectTablaProducto, insertTablaProducto, verificarProducto

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

# Método main
def main():
    app.run(debug = True)

if __name__ == "__main__":
    main()