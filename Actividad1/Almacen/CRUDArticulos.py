import sqlite3

class Articulo:
    def __init__(self, id_articulo, nombre, unidad_disponible,disponible=True):
        self.id_articulo = id_articulo
        self.nombre = nombre
        self.unidad_disponible = unidad_disponible        
        self.disponible = disponible

class CRUDArticulos:

    def seleccionarBD(self, nombre_base_datos):
        self.nombre_base_datos = nombre_base_datos

    def crear_tabla_articulos(self):
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS articulos (
                            id INTEGER PRIMARY KEY,
                            nombre TEXT,
                            unidad_disponible INTEGER DEFAULT 0,
                            disponible boolean DEFAULT 0)''')
        conn.commit()
        conn.close()

    def insertar_articulo(self, articulo):
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO articulos (nombre, unidad_disponible,disponible) VALUES (?, ?, ?)''',
                       (articulo.nombre, articulo.unidad_disponible, articulo.disponible))
        conn.commit()
        conn.close()

    def obtener_articulos(self,id_articulo=None):
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor() 
        data=None      
        if(id_articulo is not None):
            select='''SELECT * FROM articulos WHERE id = ?'''
            cursor.execute(select, (id_articulo,)) 
            result = cursor.fetchone()
            if(result is not None):
                data = Articulo(*result)
        else:
            select = '''SELECT * FROM articulos'''
            cursor.execute(select)
            filas = cursor.fetchall()
            data = []
            for fila in filas:
                data.append(Articulo(*fila))
        conn.close()
        return data

    def eliminar_articulo(self, id_articulo):
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM articulos WHERE id=?''', (id_articulo,))
        result = cursor.rowcount
        conn.commit()
        conn.close()
        return result
    def actualizar_articulo(self, id_articulo,nombre, cantidad,disponible):
        # //data['nombre'], data['unidad_disponible'], data['disponible']    
        articulo = self.obtener_articulos(id_articulo)
        if(articulo is None):
            return None
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()
        cursor.execute('''UPDATE articulos SET nombre = ?, unidad_disponible=?, disponible=? WHERE id=?''',
                       (nombre,cantidad,disponible, id_articulo))
        conn.commit()
        conn.close()
        return True
    def actualizar_cantidad(self, id_articulo, cantidad, accion):
        articulo = self.obtener_articulos(id_articulo)
        if(articulo is None):
            return None
        if (accion == 'recepcion'):
            cantidad = cantidad+articulo.unidad_disponible
        if (accion == 'salida'):
            cantidad = articulo.unidad_disponible-cantidad
        if(cantidad<0):
            return False
        conn = sqlite3.connect(self.nombre_base_datos)
        cursor = conn.cursor()
        cursor.execute('''UPDATE articulos SET unidad_disponible=? WHERE id=?''',
                       (cantidad, id_articulo))
        conn.commit()
        conn.close()
        return True