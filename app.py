from flask import Flask, jsonify, request, Response
from helpers import cargarDatosJSON, guardarDatosJSON, verificarProducto, verificarCategoria

# Creación del objeto app y configuración del ordenamiento de claves en JSON
app = Flask(__name__)
app.json.sort_keys = False

## TO-DO: Cambiar cosas aquí

def main():
    app.run(debug = True)

if __name__ == "__main__":
    main()