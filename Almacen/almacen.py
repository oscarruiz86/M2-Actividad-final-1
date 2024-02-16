import argparse
from functools import wraps
from flask import Flask, request, jsonify
from CRUDArticulos import Articulo, CRUDArticulos
from loadConfig import LoadConfig


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
        crud.actualizar_articulo(id_articulo, data['nombre'], data['unidad_disponible'], data['disponible'])
        return jsonify({'message': 'Articulo actualizado correctamente'})
    elif request.method == 'DELETE':
        crud.eliminar_articulo(id_articulo)
        return jsonify({'message': 'Articulo eliminado correctamente'}), 204
    elif request.method == 'GET':
        articulo = crud.obtener_articulos(id_articulo)
        return jsonify(vars(articulo))
    
@app.route('/articulos/<int:id_articulo>/recepcion', methods=['PUT',])
@validar_api_key
def articulo_recepcion(id_articulo):
    if request.method == 'PUT':
        data = request.json
        crud.actualizar_cantidad(id_articulo, data['cantidad'],'recepcion')
        return jsonify({'message': 'Articulo actualizado correctamente'})

@app.route('/articulos/<int:id_articulo>/salida', methods=['PUT',])
@validar_api_key
def articulo_salida(id_articulo):
    if request.method == 'PUT':
        data = request.json
        crud.actualizar_cantidad(id_articulo, data['cantidad'],'salida')
        return jsonify({'message': 'Articulo actualizado correctamente'})    

    

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































# import sqlite3

# def perro():
#     '''crear tabla'''
#     dbStructure= """
#             CREATE TABLE IF NOT EXISTS articulos (
# 	        id INTEGER PRIMARY KEY,
# 	        nombre TEXT NOT NULL,
# 	        unidad_disponible INTEGER NOT NULL,
# 	        precio REAL NOT NULL
#         );
#         """
#     '''conexion a base de datos'''
#     con = sqlite3.connect("tutorial.db")
#     # Crear un cursor
#     cursor = con.cursor()
#     cursor.execute(dbStructure)

#     # Definir la sentencia de inserción
#     sql_insert = '''INSERT INTO articulos (nombre, unidad_disponible, precio) VALUES (?, ?, ?)'''
#     datos = ('tv', '22', '8.55')
#     cursor.execute(sql_insert, datos)
#     # Guardar los cambios
#     con.commit()

#     # Definir la sentencia de actualización
#     sql_update = '''UPDATE articulos
#                     SET nombre = ?,
#                         unidad_disponible = ?,
#                         precio = ?
#                      WHERE id = ?'''
#     condicion_columna = 1
#     # Datos para la actualización
#     datos_actualizacion = ('nuevo_valor1', 'nuevo_valor2',99.99,condicion_columna)

#     # Ejecutar la sentencia de actualización
#     cursor.execute(sql_update, datos_actualizacion)
#     con.commit()
#     '''slectt''''
#     # Definir la consulta SELECT con la cláusula WHERE
#     sql_select = '''SELECT * 
#                     FROM articulos 
#                     WHERE id = ?'''

#     # Valor para la condición
#     valor_condicion = 1

#     # Ejecutar la consulta SELECT con la cláusula WHERE
#     cursor.execute(sql_select, (valor_condicion,))

#     # Obtener los resultados de la consulta
#     resultados = cursor.fetchall()

#     # Imprimir los resultados
#     for fila in resultados:
#         print(fila)

#     '''delete'''
#     sql_delete = '''DELETE FROM articulos WHERE id = ?'''

#     # Valor para la condición (opcional)
#     valor_condicion = 15

#     cursor.execute(sql_delete, (valor_condicion,))

#     # Guardar los cambios
#     con.commit()

#     # Cerrar la conexión
#     con.close()

# perro()