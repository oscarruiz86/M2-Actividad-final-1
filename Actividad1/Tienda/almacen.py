import requests

from CRUDProductos import CRUDProductos, Producto

class Almacen:

    
    def cargarInvetarioInicial(self,almacen):
        listado = almacen.obtener_productos()
        url = 'http://localhost:5002/'
        headers  = {'API-Key': 'Almacen'}
        if(len(listado) == 0):
            ##iniciar cargar inventario inicial
            response = requests.get(url+'articulos',headers =headers )
            # Verificar si la petición fue exitosa (código de estado 200)
            if response.status_code == 200:
                data = response.json()
                for articulo in data:
                    cantidad = 2
                    responseSalida = requests.put(url+'articulos/'+str(articulo['id_articulo'])+'/salida',json={"cantidad":cantidad},headers = headers)
                    if responseSalida.status_code == 200:
                        producto = Producto(
                                                id_producto=None,
                                                nombre= articulo['nombre'],
                                                unidad_disponible=cantidad,
                                                precio=0,
                                                id_articulo=articulo['id_articulo'],
                                                unidad_vendida= 0)
                        almacen.insertar_producto(producto)                
                    else:
                        # Imprimir un mensaje de error en caso de que la petición falle
                        print(f'Error al hacer la petición salida almacen: {responseSalida.status_code}')
                    
            else:
                # Imprimir un mensaje de error en caso de que la petición falle
                print(f'Error al hacer la petición: {response.status_code}')

    def trasladoTiendo(self,tienda,id_producto,cantidad):

        url = 'http://127.0.0.1:5000/'
        headers  = {'API-Key': 'Almacen'}

        ##iniciar cargar inventario inicial
        response = requests.get(url+'articulos/'+str(id_producto),headers =headers )
        # Verificar si la petición fue exitosa (código de estado 200)
        if response.status_code == 200:
            articulo = response.json()
            if(articulo['unidad_disponible'] >= cantidad):
                responseSalida = requests.put(f'{url}articulos/{str(articulo["id_articulo"])}/salida',json={"cantidad":cantidad},headers = headers)
                if responseSalida.status_code == 200:
                    articuloTienda = tienda.obtener_productos(id_producto)
                    cantidad = articuloTienda.unidad_disponible+cantidad
                    tienda.actualizar_producto(id_producto, articuloTienda.nombre, cantidad, articuloTienda.precio)    
                    return True           
                else:
                    # Imprimir un mensaje de error en caso de que la petición falle
                    print(f'Error al hacer la petición salida almacen: {responseSalida.status_code}') 
            else:
                    # Imprimir un mensaje de error en caso de que la petición falle
                    print(f'sin stock suficiente')                                               
        else:
            # Imprimir un mensaje de error en caso de que la petición falle
            print(f'Error al hacer la petición: {response.status_code}')
        return False