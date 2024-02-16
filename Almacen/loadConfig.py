import yaml

class LoadConfig:
    def cargar_configuracion(self,path):
        with open(path, 'r') as archivo:
            configuracion = yaml.safe_load(archivo)
        return configuracion
    def set_api_key(self,key):
        self.api_key = [key]
    def get_api_key(self):
        return self.api_key