from decouple import config
import os

#Directorio para los archivos csv

DIR= 'C:/Users/Jsolchaga86/Desktop'

#Llamado a los parámetros de configuración de la db
PASSWORD = config('PASSWORD',default='')
DATABASE = config('DATABASE', default='')
HOST = config('HOST', default='localhost')
USER = config('USER', default='postgres')
PORT= config('PORT', default='5432')

#Configuración del programa
DB_DEFAULT=['Museo', 'Salas_de_Cine', 'Bibliotecas_Populares']
COLUMNS_DB=['cod_localidad','id_provincia','id_departamento','categoría','provincia','localidad','nombre','domicilio','código postal','número de teléfono','mail', 'web', 'fuente']
