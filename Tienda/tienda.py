import argparse
from functools import wraps
from flask import Flask, request, jsonify

from CRUDProductos import CRUDProductos
from loadConfig import LoadConfig


app = Flask(__name__)

crud = CRUDProductos()
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
@app.route('/productos', methods=['GET', 'POST'])
@validar_api_key
def productos():
    if request.method == 'GET':
        productos = crud.obtener_productos()
        return jsonify([vars(producto) for producto in productos])
    elif request.method == 'POST':
        data = request.json
        producto = Producto(None, data['nombre'], data['unidad_disponible'], data['precio'])
        crud.insertar_producto(producto)
        return jsonify({'message': 'Producto creado correctamente'}), 201

@app.route('/productos/<int:id_producto>', methods=['PUT', 'DELETE','GET',])
@validar_api_key
def producto(id_producto):
    if request.method == 'PUT':
        data = request.json
        crud.actualizar_producto(id_producto, data['nombre'], data['unidad_disponible'], data['precio'])
        return jsonify({'message': 'Producto actualizado correctamente'})
    elif request.method == 'DELETE':
        crud.eliminar_producto(id_producto)
        return jsonify({'message': 'Producto eliminado correctamente'}), 204
    elif request.method == 'GET':
        producto = crud.obtener_productos(id_producto)
        return jsonify(vars(producto))
    
@app.route('/productos/<int:id_producto>/editar-precio', methods=['PUT',])
@validar_api_key
def producto_editar_precio(id_producto):
    if request.method == 'PUT':
        data = request.json
        crud.actualizar_precio_producto(id_producto, data['precio'])
        return jsonify({'message': 'Producto actualizado correctamente'})    
    
@app.route('/productos/<int:id_producto>/venta', methods=['PUT',])
@validar_api_key
def producto_venta(id_producto):
    if request.method == 'PUT':
        respuesta = crud.vender_producto(id_producto)
        if(respuesta):
            return jsonify({'message': 'Producto actualizado correctamente'})    
        return jsonify({'error': 'Error al vender producto'})    


def inicio(servidor,puerto,config_path,key):    
    cargar_configuracion = config.cargar_configuracion(config_path)
    config.set_api_key(key)
    crud.seleccionarBD(cargar_configuracion["basedatos"]["path"])
    crud.crear_tabla_productos()
    app.run(host=servidor, port=puerto)

parser = argparse.ArgumentParser()
parser.add_argument("--servidor",default='localhost', help="servidor")
parser.add_argument("--puerto", default=5000, help="puerto")
parser.add_argument("config", help="config")
parser.add_argument("key", help="key")
args = parser.parse_args()
inicio(args.servidor,args.puerto,args.config,args.key)































# import sqlite3

# def perro():
#     '''crear tabla'''
#     dbStructure= """
#             CREATE TABLE IF NOT EXISTS productos (
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
#     sql_insert = '''INSERT INTO productos (nombre, unidad_disponible, precio) VALUES (?, ?, ?)'''
#     datos = ('tv', '22', '8.55')
#     cursor.execute(sql_insert, datos)
#     # Guardar los cambios
#     con.commit()

#     # Definir la sentencia de actualización
#     sql_update = '''UPDATE productos
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
#                     FROM productos 
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
#     sql_delete = '''DELETE FROM productos WHERE id = ?'''

#     # Valor para la condición (opcional)
#     valor_condicion = 15

#     cursor.execute(sql_delete, (valor_condicion,))

#     # Guardar los cambios
#     con.commit()

#     # Cerrar la conexión
#     con.close()

# perro()