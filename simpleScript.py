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
    sumLeon = 0
    contLeon = 0
    data = json.loads(info.text)
    for value in data["ListaEESSPrecio"]:
        if(value["Municipio"] == "Benavente") or (value["Municipio"] == "León") or (value["Localidad"] == "BAÑEZA (LA)"):
            print("{} --- Precio --> {}, Direccion --> {}".format(value['Municipio'], value['Precio Gasoleo A'], value['Dirección']))
            if value["Municipio"] == "León":
                sumLeon += float(value['Precio Gasoleo A'].replace(",", "."))
                contLeon += 1
    
    print("Media León -> {:.3f}".format(sumLeon/contLeon))



def main():
    data = requestInfo()
    storeInDataBase(data)

main()

