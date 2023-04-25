import unittest
import requests
import pyodbc
from datetime import datetime
from unittest.mock import Mock
from io import StringIO
import json

from main import requestInfo, storeInDataBase

direccion_servidor = '172.17.0.4'
nombre_bd = 'gasolineras'
nombre_usuario = 'sa'
password = "yourStrong(!)Password"

class TestConexionYDescarga(unittest.TestCase):

    def test_conexion_bd(self):
        try:
            conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' +
                                      direccion_servidor+' ;DATABASE='+ nombre_bd+ ' ;UID='+nombre_usuario+
                                      ' ;PWD=' + password)
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)
    
        
    def test_requestInfo(self):
        response = requestInfo()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.text)
        self.assertIsInstance(json.loads(response.text), dict)

    def test_store_in_database(self):
        # Definir datos de prueba
        test_data = {
            "ListaEESSPrecio": [{
                "C.P.": "12345",
                "Dirección": "Calle Falsa 123",
                "Horario": "L-V 8:00 - 22:00",
                "Latitud": "40.416775",
                "Localidad": "Madrid",
                "Longitud (WGS84)": "-3.703790",
                "Margen": "Normal",
                "Municipio": "Madrid",
                "Precio Biodiesel": "1.23",
                "Precio Bioetanol": "2.34",
                "Precio Gas Natural Comprimido": "3.45",
                "Precio Gas Natural Licuado": "4.56",
                "Precio Gases licuados del petróleo": "5.67",
                "Precio Gasoleo A": "6.78",
                "Precio Gasoleo B": "7.89",
                "Precio Gasoleo Premium": "8.90",
                "Precio Gasolina 95 E10": "9.01",
                "Precio Gasolina 95 E5": "10.12",
                "Precio Gasolina 95 E5 Premium": "11.23",
                "Precio Gasolina 98 E10": "12.34",
                "Precio Gasolina 98 E5": "13.45",
                "Precio Hidrogeno": "14.56",
                "Provincia": "Madrid",
                "Remisión": "DM",
                "Rótulo": "Gasolinera Falsa",
                "Tipo Venta": "Público",
                "% BioEtanol": "1.2",
                "% Éster metílico": "2.3",
                "IDEESS": "1234",
                "IDMunicipio": "5678",
                "IDProvincia": "91011",
                "IDCCAA": "12"
            }]
        }
        test_info = Mock(text=json.dumps(test_data))
        
        # Ejecutar la función y comprobar el resultado
        result = storeInDataBase(test_info)
        
        # Comprobar que la función devuelve None
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
