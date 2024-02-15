import sqlite3

class Producto:
    def __init__(self, id_producto, nombre, unidad_disponible, precio,unidad_vendida=0):
        self.id_producto = id_producto
        self.nombre = nombre
        self.unidad_disponible = unidad_disponible        
        self.precio = precio
        self.unidad_vendida = unidad_vendida

class CRUDProductos:
    # def __init__(self, nombre_base_datos):
    #     self.nombre_base_datos = nombre_base_datos
    def seleccionarBD(self, nombre_base_datos):
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
