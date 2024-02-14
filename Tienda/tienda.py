from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

class Producto:
    def __init__(self, id_producto, nombre, unidad_disponible, precio,unidad_vendida=0):
        self.id_producto = id_producto
        self.nombre = nombre
        self.unidad_disponible = unidad_disponible        
        self.precio = precio
        self.unidad_vendida = unidad_vendida

class CRUDProductos:
    def __init__(self, nombre_base_datos):
        self.nombre_base_datos = nombre_base_datos

    def crear_tabla_productos(self):
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                            id INTEGER PRIMARY KEY,
                            nombre TEXT,
                            unidad_disponible INTEGER DEFAULT 0,
                            precio REAL,
                            unidad_vendida INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()

    def insertar_producto(self, producto):
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO productos (nombre, unidad_disponible, precio) VALUES (?, ?, ?)''',
                       (producto.nombre, producto.unidad_disponible, producto.precio))
        conn.commit()
        conn.close()

    def obtener_productos(self,id_producto=None):
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()        
        if(id_producto is not None):
            select='''SELECT * FROM productos WHERE id = ?'''
            cursor.execute(select, (id_producto,))         
            data = Producto(*cursor.fetchone())
        else:
            select = '''SELECT * FROM productos'''
            cursor.execute(select)
            filas = cursor.fetchall()
            data = []
            for fila in filas:
                data.append(Producto(*fila))
        conn.close()
        return data

    def actualizar_producto(self, id_producto, nombre, unidad_disponible, precio):
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()
        cursor.execute('''UPDATE productos SET nombre=?, unidad_disponible=?, precio=? WHERE id=?''',
                       (nombre, unidad_disponible, precio, id_producto))
        conn.commit()
        conn.close()

    def vender_producto(self, id_producto):
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()
        producto_tienda = self.obtener_productos(id_producto)

        unidad_vendida = producto_tienda.unidad_vendida+1
        unidad_disponible = producto_tienda.unidad_disponible-1

        if(unidad_disponible >= 0 and producto_tienda.precio>0):
            cursor.execute('''UPDATE productos SET unidad_vendida=?, unidad_disponible=? WHERE id=?''',
                        (unidad_vendida, unidad_disponible, id_producto))
            conn.commit()
            conn.close()
            return True
        return False

    def actualizar_precio_producto(self, id_producto, precio):
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()
        cursor.execute('''UPDATE productos SET precio=? WHERE id=?''',
                       (precio, id_producto))
        conn.commit()
        conn.close()

    def eliminar_producto(self, id_producto):
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM productos WHERE id=?''', (id_producto,))
        conn.commit()
        conn.close()

# Rutas CRUD

crud = CRUDProductos('productos.db')
crud.crear_tabla_productos()

@app.route('/productos', methods=['GET', 'POST'])
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
def producto_editar_precio(id_producto):
    if request.method == 'PUT':
        data = request.json
        crud.actualizar_precio_producto(id_producto, data['precio'])
        return jsonify({'message': 'Producto actualizado correctamente'})    
    
@app.route('/productos/<int:id_producto>/venta', methods=['PUT',])
def producto_venta(id_producto):
    if request.method == 'PUT':
        respuesta = crud.vender_producto(id_producto)
        if(respuesta):
            return jsonify({'message': 'Producto actualizado correctamente'})    
        return jsonify({'error': 'Error al vender producto'})    

if __name__ == '__main__':
    app.run(debug=True)




































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