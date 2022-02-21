# -*- coding: UTF-8 -*-


# Explicacióm
# El código trabaja entrando a la seccióm del mapa culutral de la
# web del gobierno de la ciudaad, lista las bases de datos
# disponibles, y permite descargar las que se necesiten. Este enfoque
# permite independizarse de la url y siempre poder acceder a la bases
# de datos isponibles
# Funciona de dos formas:
#  1-Por default, seteando las bases de datos a descargar en
#    el módulo "settings" de manera que al iniciar el programa,
#    las tareas se ejecutan automaticamente.
#  2-Eligiendo las tablas a descargar durante la ejecución del
#    programa
# Esta seteado por dedfaut para cumplir los incisos del challenge,
# pero se puede modificar, egun se explica en el readme.txt presente en
# el repositorio.
# Una vez descrgadas las tablas, se procesan y guardan

import logging
import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import io
import os
import datetime
from collections import Counter
import urllib
from bs4 import BeautifulSoup
from decouple import config
from settings import *
import urllib.request
import urllib.parse


# Bloque 1--- DEFINICION DE CLASES -------------------------------------------------------

# Clase que define la conexión a la base de datos
# postgresql (https://www.sqlalchemy.org/)
class sql_con:

    def __init__(self, user, password, host, port, db):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db

    def get_engine(self):
        url_db = f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'
        if not database_exists(url_db):
            create_database(url_db)
        engine = create_engine(url_db, pool_size=10,
                               echo=False)
        return engine


# Clase que define métodos de descarga y normalización de las tablas
class Database:

    def __init__(self, name, description, url):
        self.name = name
        self.url = url
        self.description = description

    def dtable(self):
        url = self.url  # Obtiene la url para descargar a tba
        request = requests.get(url)  # Descrga ls tablas
        df = pd.read_csv(io.StringIO(request.content.decode('utf-8')))
        df['fecha_carga'] = datetime.date.today()
        return df  # Retorna eñ df de l tabla solicitada

    def normalized_dt(self):  # Normaliza las tablas uniformizando el name de las columnas
        df = self.dtable()
        df.columns = [df.columns[i].lower() for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'á', 'a') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'é', 'e') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'í', 'i') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'ó', 'o') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'ú', 'u') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'cod_loc', 'cod_localidad') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'idp', 'id_p') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'idd', 'id_d') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'categoria', 'categoría') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'direccion', 'domicilio') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'cp', 'código postal') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'localidad_id', 'id_localidad') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'provincia_id', 'id_provincia') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'departmento_id', 'id_dpartmnto') for i in range(len(df.columns))]
        df.columns = [df.columns[i].replace(
            'telefono', 'número de teléfono') for i in range(len(df.columns))]
        return df

# Bloque 2 -------BUSQUEDA, ELECCION, DESCARGA Y GUARADO DE LAS TABLAS-----------------------------------

# Busca en la página web, laa tablas disponibles y deveulve un df con el name
# la desripción y la url de cada una


def get_aviable_databases():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request('https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales',
                                 headers=headers)
    with urllib.request.urlopen(req) as response:
        raw = response.read()
    soup = BeautifulSoup(raw, features='html5lib')
    databases = soup.find_all(class_='pkg-container')
    titles = []
    notes = []
    urls = []
    for i in databases:
        title_i = i.find('h3').text
        title_i = title_i.replace(' ', '_')
        titles.append(title_i)
        notes.append(i.find('p').text)
        links = i.find_all('a', href=True)
        for l in links:
            if ('.csv' in l['href']):
                urls.append(l['href'])
    df = pd.DataFrame({'db': titles, 'description': notes,
                       'url': urls})
    return(df)


# A partir del df con todas las db, selecciona solo con las filas
# que corresponden a las tablas solicitadas
def select_dt(selection):
    df = get_aviable_databases()
    if (selection != []):
        for i in selection:
            df = df[df['db'].isin(selection)]
    else:
        print(df.iloc[:, 0:1])
        index_string = input(
            'ingrese los números de las tablas que desea descargar, separados por "coma"\n')
        index = index_string.split(',')
        index = map(int, index)
        df = df.iloc[index]
    return df


# La siguiente función itera entre las filas del df con las tablas elegidas. Las colunmas 'db' y 'url'
# contienen los parametros de la clase "Database", por lo que en cada iteración va definiendo un
# objeto de esta clase. Devuelve una lista con todos los objetos definidos o un objeto Database
# si se seleccionó solo una base de datos
def get_list_db(db_list):
    select_df = select_dt(db_list)
    list_db = []
    for i, j in select_df.iterrows():
        url = j['url']
        name = j['db']
        description = j['description']
        db = Database(name, description, url)
        if len(select_df) != 1:
            list_db.append(db)
            output = list_db
        else:
            output = db
    return output


def save_df(df, name, engine, sql=False, csv=False):
    current_date = datetime.datetime.now()
    path1 = DIR+'/'+name
    path2 = DIR+'/'+name+'/'+current_date.strftime('%Y-%B')
    if not os.path.exists(path1):
        os.mkdir(path1)
    if not os.path.exists(path2):
        os.mkdir(path2)
    if sql == True:
        print('Guardando '+name+' en '+DATABASE)
        df.to_sql(name, if_exists='replace', schema='public', con=engine)
    if csv == True:
        print('Guardando '+name+'.csv'+' en '+path2)
        df.to_csv(path2+'/'+name+'_'+current_date.strftime('%d-%m-%Y')+'.csv')


# -- Bloque 3---------- PROCESAMIENTO DE DATOS---------------------------------------------------

# La siguinte función crea la tabla general requerida en el challenge, a partir
# de las tablas que se hayan seleccionado. Toma como i,put la lista con los objetos
# Database
def create_tot_table(tot_table_col):
    list = get_list_db(DB_DEFAULT)
    df_tot = pd.DataFrame([])
    for i in list:
        df_norm = i.normalized_dt()
        df_tot = pd.concat([df_tot, df_norm], axis=0,
                           ignore_index=True, sort=False)
    df_tot = df_tot[tot_table_col]
    df_tot['fecha_carga'] = datetime.date.today()
    return df_tot

# Funció que procesa los datos de la forma requerida
# Primero obtiene conteoos por registro en las variables
# indicadas, y finalmente lo une en un df total


def get_registros_dt(total_table):
    list = get_list_db(DB_DEFAULT)
    total_table = create_tot_table(COLUMNS_DB)
    categorias = (Counter(total_table['categoría']))
    by_categorias = pd.DataFrame.from_dict(categorias,
                                           orient='index').reset_index()
    by_categorias.columns = ['registro', 'cantidad']

    fuentes = (Counter(total_table['fuente']))
    by_fuentes = pd.DataFrame.from_dict(fuentes,
                                        orient='index').reset_index()
    by_fuentes.columns = ['registro', 'cantidad']

    by_prov_cat = (total_table.groupby(['provincia',
                                        'categoría'])).size()
    df_prov_cat = by_prov_cat.to_frame(name='size').reset_index()
    df_prov_cat['registro'] = df_prov_cat['provincia'] + \
        '-'+df_prov_cat['categoría']
    df_prov_cat = df_prov_cat[['registro', 'size']]
    df_prov_cat.columns = ['registro', 'cantidad']

    registros = pd.concat([by_categorias, by_fuentes, df_prov_cat], axis=0)
    registros['fecha_carga'] = datetime.date.today()
    return registros


def counter_cines_features(db_name):
    cines_Databas_obj = get_list_db(db_name)
    cines_norm_df = cines_Databas_obj.normalized_dt()
    cines_resume = cines_norm_df.groupby('provincia').agg({'pantallas': 'sum', 'butacas': 'sum',
                                                           'espacio_incaa': 'count'})
    cines_resume['fecha_carga'] = datetime.date.today()
    return cines_resume


def main():

    # --seteo el registro de logs desde el nivel WARNING y los registro en el archivo indicado
    logging.basicConfig(level=logging.WARNING, filename=DIR+'logs_challenge_app.log',
                        format='%(asctime)s %(levelname)s:%(message)s')

    # --------- BLOQUE 1 ---------------------------
    engine = sql_con(user=USER, password=PASSWORD,
                     host=HOST, port=PORT, db=DATABASE)
    engine = engine.get_engine()
    # --------- BLOQUE 2 ---------------------------
    list_of_df = get_list_db(DB_DEFAULT)
    for df in list_of_df:
        save_df(df.dtable(), df.name, engine=2, sql=False, csv=True)
    # --------- BLOQUE 3 ---------------------------
    # Tabla total
    Espacios_culturales = create_tot_table(COLUMNS_DB)
    save_df(Espacios_culturales, 'tot_data', engine=2, sql=False, csv=True)
    # Tabla registros
    tablas_registros = get_registros_dt(Espacios_culturales)
    save_df(tablas_registros, 'registros', engine, sql=True, csv=False)
    # Tabla cines
    cines = counter_cines_features(['Salas_de_Cine'])
    save_df(cines, 'cines_count', engine, sql=True, csv=False)


if __name__ == '__main__':
    main()
