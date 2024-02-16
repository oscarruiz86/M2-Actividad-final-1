import yaml
import argparse
import sqlite3

"""Leemos el fichero yaml"""
def cargar_configuracion(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        configuracion = yaml.safe_load(archivo)
    return configuracion

config = cargar_configuracion('config.yaml')

if config == config:
    # Conectar a la base de datos (se crea si no existe)
    conexion = sqlite3.connect('database/almacen')

    # Crear un cursor para ejecutar consultas SQL
    cursor = conexion.cursor()

    # Crear una tabla
    cursor.execute('''CREATE TABLE IF NOT EXISTS zapatillas (
                    id INTEGER PRIMARY KEY,
                    marca TEXT NOT NULL,
                    modelo TEXT NOT NULL,
                    stock INTEGER
                )''')

    # Insertar datos
    cursor.execute("INSERT INTO zapatillas (marca, modelo, stock) VALUES (?, ?, ?)", ('Nike','Vaporfly', 30))
    cursor.execute("INSERT INTO zapatillas (marca, modelo, stock) VALUES (?, ?, ?)", ('Adidas','Adios', 25))
    cursor.execute("INSERT INTO zapatillas (marca, modelo, stock) VALUES (?, ?, ?)", ('Hoka', 'Rocket',35))

    # Guardar los cambios
    conexion.commit()

    # Realizar una consulta
    cursor.execute("SELECT * FROM zapatillas")
    filas = cursor.fetchall()

    # Imprimir los resultados
    for fila in filas:
        print(fila)

    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()



if __name__ == "__main__":

        parser = argparse.ArgumentParser(description='Parámetros de la aplicación')
        parser.add_argument('--config', help=config, required=True)

        args = parser.parse_args()

 #      cargar_configuracion(args.ruta_archivo)
        
print(config)
print(config['database']['host'])


