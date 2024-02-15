import requests
import yaml
from flask import Flask,request,redirect





app = Flask(__name__)

@app.route("/almacen", methods=['GET'])

def servicios_almacen():


   with open("config.yaml", "r") as archivo:
         configuracion = yaml.safe_load(archivo)
        
   # return configuracion
   print(configuracion, "la configuracion llega aqui")
 
   return redirect("http://localhost/almacen", code=302)


