import argparse
from functools import wraps
from flask import Flask, request, jsonify
from swaggerui import swaggerui
from CRUDArticulos import Articulo, CRUDArticulos
from loadConfig import LoadConfig
from yaml import Loader, load


app = Flask(__name__)

crud = CRUDArticulos()
config = LoadConfig()

#validador de api key
def validar_api_key(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        api_key = request.headers.get('API-Key')         
        # Aquí deberías validar la API key, por ejemplo, comparándola con una lista de claves válidas
        claves_validas = config.get_api_key()
        if api_key not in claves_validas:
            return jsonify({'mensaje': 'Clave API inválida'}), 401
        
        # Si la API key es válida, ejecuta la vista protegida
        return f(*args, **kwargs)
    return decorador

# Rutas CRUD
@app.route('/articulos', methods=['GET', 'POST'])
@validar_api_key
def articulos():
    if request.method == 'GET':
        articulos = crud.obtener_articulos()
        return jsonify([vars(articulo) for articulo in articulos])
    elif request.method == 'POST':
        data = request.json
        articulo = Articulo(None, data['nombre'], data['unidad_disponible'], data['disponible'])
        crud.insertar_articulo(articulo)
        return jsonify({'message': 'Articulo creado correctamente'}), 201

@app.route('/articulos/<int:id_articulo>', methods=['PUT', 'DELETE','GET',])
@validar_api_key
def articulo(id_articulo):
    if request.method == 'PUT':
        data = request.json
        result = crud.actualizar_articulo(id_articulo, data['nombre'], data['unidad_disponible'], data['disponible'])
        if(result is None ):
             return jsonify({'message': 'No existe  artículo'}), 400
        else:
            return jsonify({'message': 'Articulo actualizado correctamente'})
    elif request.method == 'DELETE':
        result = crud.eliminar_articulo(id_articulo)
        if(result>0):
            return jsonify({'message': 'Articulo eliminado correctamente'}), 204
        else:
            return jsonify({'message': 'Acción no realizada'}), 400
    elif request.method == 'GET':
        articulo = crud.obtener_articulos(id_articulo)
        if(articulo is not None ):
            return jsonify(vars(articulo))
        else:
            return jsonify({'message': 'No existe  artículo'}), 400
    
@app.route('/articulos/<int:id_articulo>/recepcion', methods=['PUT',])
@validar_api_key
def articulo_recepcion(id_articulo):
    if request.method == 'PUT':
        data = request.json
        result = crud.actualizar_cantidad(id_articulo, data['cantidad'],'recepcion')
        if(result is None ):
             return jsonify({'message': 'No existe  artículo'}), 400
        else:
            return jsonify({'message': 'Artículo actualizado correctamente'})

@app.route('/articulos/<int:id_articulo>/salida', methods=['PUT',])
@validar_api_key
def articulo_salida(id_articulo):
    if request.method == 'PUT':
        data = request.json
        result = crud.actualizar_cantidad(id_articulo, data['cantidad'],'salida')
        if(result is None ):
             return jsonify({'message': 'No existe articulo'}), 400
        elif(result is False ):
             return jsonify({'message': 'Operacion no valida'}), 400
        else:
            return jsonify({'message': 'Artículo actualizado correctamente'})

app.register_blueprint(swaggerui())
@app.route("/services/spec")
def spec():
    swagger_yml = load(open('api_docu_Almacen.yaml', 'r', encoding='utf8'), Loader=Loader)
    return jsonify(swagger_yml)
    
def inicio(servidor,puerto,config_path):    
    cargar_configuracion = config.cargar_configuracion(config_path)
    config.set_api_key(cargar_configuracion["basedatos"]["consumidor_almacen_key"])
    crud.seleccionarBD(cargar_configuracion["basedatos"]["path"])
    crud.crear_tabla_articulos()
    app.run(host=servidor, port=puerto)

parser = argparse.ArgumentParser()
parser.add_argument("--servidor",default='localhost', help="servidor")
parser.add_argument("--puerto", default=5000, help="puerto")
parser.add_argument("config", help="config")
args = parser.parse_args()
inicio(args.servidor,args.puerto,args.config)