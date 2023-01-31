import requests, pyodbc
import json
import time
from datetime import datetime


# Establecemos conexion con la base de datos
direccion_servidor = '172.17.0.2'
nombre_bd = 'gasolineras'
nombre_usuario = 'sa'
password = "yourStrong(!)Password"

try:
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' +
                            direccion_servidor+' ;DATABASE='+ nombre_bd+ ' ;UID='+nombre_usuario+
                            ' ;PWD=' + password)
    print("Conexion exitosa")
except Exception as e:
    print("Ocurrio una excepcion al intentar conectar con la BBDD --> ", e)

fecha = datetime.now()
 

# informacion obtenida de datos.gob.es, pagina del gobierno
def requestInfo():
    print("Descargando datos")
    data =requests.get('https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/')
    return data


def storeInDataBase(info):
    print("Buscando datos")
    cursor = conexion.cursor()
    data = json.loads(info.text)
    for value in data["ListaEESSPrecio"]:
        cp = int(value['C.P.']) if value['C.P.'] != '' else None
        direccion = value['Dirección'] if value['Dirección'] != '' else None
        horario = value['Horario'] if value['Horario'] != '' else None
        latitud = float(value['Latitud'].replace(",", ".")) if value['Latitud'] != '' else None
        localidad = value['Localidad'] if value['Localidad'] != '' else None
        longitud = float(value['Longitud (WGS84)'].replace(",", ".")) if value['Longitud (WGS84)'] != '' else None 
        margen = value['Margen'] if value['Margen'] != '' else None
        municipio = value['Municipio'] if value['Municipio'] != '' else None
        precioBiodiesel = float(value['Precio Biodiesel'].replace(",", ".")) if value['Precio Biodiesel'] != '' else None
        precioBioetanol = float(value['Precio Bioetanol'].replace(",", ".")) if value['Precio Bioetanol'] != '' else None
        precioGasNaturalComprimido = float(value['Precio Gas Natural Comprimido'].replace(",", ".")) if value['Precio Gas Natural Comprimido'] != '' else None
        precioGasNaturalLicuado = float(value['Precio Gas Natural Licuado'].replace(",", ".")) if value['Precio Gas Natural Licuado'] != '' else None
        precioGasesLicuadosDelPetroleo = float(value['Precio Gases licuados del petróleo'].replace(",", ".")) if value['Precio Gases licuados del petróleo'] != '' else None
        precioGasoleoA = float(value['Precio Gasoleo A'].replace(",", ".")) if value['Precio Gasoleo A'] != '' else None
        precioGasoleoB = float(value['Precio Gasoleo B'].replace(",", ".")) if value['Precio Gasoleo B'] != '' else None
        precioGasoleoPremium = float(value['Precio Gasoleo Premium'].replace(",", ".")) if value['Precio Gasoleo Premium'] != '' else None
        precioGasolina95E10 = float(value['Precio Gasolina 95 E10'].replace(",", ".")) if value['Precio Gasolina 95 E10'] != '' else None
        precioGasolina95E5 = float(value['Precio Gasolina 95 E5'].replace(",", ".")) if value['Precio Gasolina 95 E5'] != '' else None
        precioGasolina95E5Premium = float(value['Precio Gasolina 95 E5 Premium'].replace(",", ".")) if value['Precio Gasolina 95 E5 Premium'] != '' else None
        precioGasolina98E10 = float(value['Precio Gasolina 98 E10'].replace(",", ".")) if value['Precio Gasolina 98 E10'] != '' else None
        precioGasolina98E5 = float(value['Precio Gasolina 98 E5'].replace(",", ".")) if value['Precio Gasolina 98 E5'] != '' else None
        precioHidrogeno = float(value['Precio Hidrogeno'].replace(",", ".")) if value['Precio Hidrogeno'] != '' else None
        provincia = value['Provincia'] if value['Provincia'] != '' else None
        remision = value['Remisión'] if value['Remisión'] != '' else None
        rotulo = value['Rótulo'] if value['Rótulo'] != '' else None
        tipoVenta =  value['Tipo Venta'] if value['Tipo Venta'] != '' else None
        porcentajeBioetanol = float(value['% BioEtanol'].replace(",", ".")) if value['% BioEtanol'] != '' else None
        porcentajeEsterMetilico = float(value['% Éster metílico'].replace(",", ".")) if value['% Éster metílico'] != '' else None
        ideess = int(value['IDEESS']) if value['IDEESS'] != '' else None
        idMunicipio = int(value['IDMunicipio']) if value['IDMunicipio'] != '' else None
        idProvincia = int(value['IDProvincia']) if value['IDProvincia'] != '' else None
        idccaa = value['IDCCAA'] if value['IDCCAA'] != '' else None
        
        # Tratamos de insertar la estacion si no existe
        try:
            count = cursor.execute("""insert into GASOLINERAS(CP, DIRECCION, HORARIO, LATITUD, LOCALIDAD, 
                                   LONGITUD, MARGEN, MUNICIPIO, ID_MUNICIPIO, ID_PROVINCIA, PROVINCIA, ROTULO, TIPO_VENTA)
                                   values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                   cp, direccion, horario, latitud, localidad, longitud, margen, municipio,
                                   idMunicipio, idProvincia,provincia, rotulo, tipoVenta)
            conexion.commit()

        except Exception as e:
            print("Estacion ya existe --> {}".format(e)) 
         
         
         
        # Obtenemos el id de la estacion para asignarselo a los registros
        try:
            count = cursor.execute("""
                                   SELECT GASOLINERAS.ID_GASOLINERA
                                   FROM GASOLINERAS
                                   WHERE GASOLINERAS.LATITUD = ? AND GASOLINERAS.LONGITUD = ?
                                   """,
                                   latitud, longitud)
            idGasolinera = cursor.fetchone()
            idGasolinera = idGasolinera[0]

        except Exception as e:
            print("Error a la hora de obtener el id de la estacion a la que pertenece {}".format(e))
        
        
        
        
        try:
            count = cursor.execute("""insert into DATA_GASOLINERAS(ID_GASOLINERA, FECHA, PRECIO_BIODIESEL, PRECIO_BIOETANOL, PRECIO_GAS_NATURAL_COMPRIMIDO, 
            PRECIO_GAS_NATURAL_LICUADO, PRECIO_GASES_LICUADOS_DEL_PETROLEO, PRECIO_GASOLEO_A, PRECIO_GASOLEO_B, PRECIO_GASOLEO_PREMIUM, PRECIO_GASOLINA_95_E10, PRECIO_GASOLINA_95_E5, 
            PRECIO_GASOLINA_95_E5_PREMIUM, PRECIO_GASOLINA_98_E10, PRECIO_GASOLINA_98_E5, PRECIO_HIDROGENO, REMISION, PORCENTAJE_BIOETANOL, PORCENTAJE_ESTER_METILICO, 
            IDEESS, IDCCAA) values(?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """,
            idGasolinera, fecha,  precioBiodiesel, precioBioetanol, 
            precioGasNaturalComprimido, precioGasNaturalLicuado, precioGasesLicuadosDelPetroleo, precioGasoleoA, 
            precioGasoleoB, precioGasoleoPremium, precioGasolina95E10, precioGasolina95E5, precioGasolina95E5Premium, 
            precioGasolina98E10, precioGasolina98E5, precioHidrogeno, remision, 
            porcentajeBioetanol, porcentajeEsterMetilico, ideess, idccaa)
            conexion.commit()
            print("Insertando datos de la consulta")
        except Exception as e:
            print("Error a la hora de insertar el registro --> {}".format(e))
            time.sleep(2)



def main():
    data = requestInfo()
    storeInDataBase(data)

main()

