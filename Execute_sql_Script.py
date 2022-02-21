from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from settings import *

# Acceso a la b

def get_engine(user, password, host, port, db):
    url=f'postgresql://{user}:{password}@{host}:{port}/{db}'
    if not database_exists(url):
        create_database(url)
    engine= create_engine(url, pool_size=10, echo= False)
    return engine

def execute_sql(path, engine):
    file = open(path)
    escaped_sql = sqlalchemy.text(file.read())
    engine.execute(escaped_sql)

def main():
    engine= get_engine(USER, PASSWORD, HOST,PORT, DATABASE)
    execute_sql('./ScriptSql_create_tables', engine)

if __name__== '__main__':
    main()

