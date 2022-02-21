Hola!
A continuación, encontraras las indicaciones necesarias para el correcto funcionamiento del programa.


Entorno:
El primer paso será la creación de un ambiente virtual en el que alojar los archivos involucrados.Para eso es necesario
el módulo virtualenv. Los pasos a seguir son los siguientes:

1- pip install virtualenv
2- En el terminal, nos posicionamos en la carpeta en donde nos interesa ubicar el entorno
y escribimos: virtulenv -nombre- 
3- A continuación, lo activamos mediante el comando /venv/Scripts/activate (en el caso de linux será source /venv/Scripts/activate)
4- Finalmente, instalamos los paquetes necesarios. Estos se encuentran en el archivo requirements.txt y se instalan
mediante el comando pip install -r requirements.txt


Claves y credenciales:
1- Configurar las credenciales de la base de datos:
    Abre el archivo .env y completa los datos de acceso a la base de datos postgresql

Creación de las tablas en la base de datos pgsql:
1- Ejecute Execute_sql_Script. Ese archivo ejecutará el archivo ScriptSql_create_tables.sql y creará las tablas necesarias. Al final del archivo ScriptSql_create_tables
    se encuentra un 'template' que podrá usar si quiere agregar nuevas tablas

Settings:
    Hay dos formas de correr el programa:
    1- Explorando las bases de datos disponibles y eligiendo durante la ejecución cuales trabajar. Esto se hace, entrando al archivo settings.py
        y dejando una lista vacía en DB_DEFAULT
    2- Seteando en settings los nombres de las bases de datos que se quieren descargar. Esto es hace agregando los nombres en forma de lista de strings
        ['database_a', database_b'] a la variable DB_DEFAULT. El programa corrrerá de principio a fin sin interrupcion

3- Tabla total:
    Como entre las funciones del programa está la de hacer una tabla general a partir de las tablas descargadas, 
    también se puede setear en settings.py una lista con los nombres de las columnas que se quieran conservar en la tabla final.
    Esto se hace en la variable COLUMNS_DB 



