import requests
import json
import time
from datetime import datetime

def requestInfo():
    print("Descargando datos")
    data =requests.get('https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/')
    return data


def storeInDataBase(info):
    print("Buscando datos")
    data = json.loads(info.text)
    for value in data["ListaEESSPrecio"]:
        if(value["Municipio"] == "Benavente") or (value["Municipio"] == "León"):
            print("{} --- Precio --> {}".format(value['Municipio'], value['Precio Gasoleo A']))



def main():
    data = requestInfo()
    storeInDataBase(data)

main()

