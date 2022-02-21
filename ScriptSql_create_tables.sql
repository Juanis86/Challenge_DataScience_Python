CREATE TABLE museos(
	cod_localidad VARCHAR(50),
	id_provincia VARCHAR(50),
	id_departamento VARCHAR(50),
	categoria VARCHAR(50),
	provincia VARCHAR(50),
	localidad VARCHAR(50),
	nombre VARCHAR(50),
	domicilio VARCHAR(50),
	codigo_postal VARCHAR(50),
	numero_de_telefono VARCHAR(50),
	mil VARCHAR(50),
	web VARCHAR(50),
	fuente VARCHAR(50),	
	fecha_carga DATE
);
CREATE TABLE cines (
	cod_localidad VARCHAR(50),
	id_provincia VARCHAR(50),
	id_departamento VARCHAR(50),
	categoria VARCHAR(50),
	provincia VARCHAR(50),
	localidad VARCHAR(50),
	nombre VARCHAR(50),
	domicilio VARCHAR(50),
	codigo_postal VARCHAR(50),
	numero_de_telefono VARCHAR(50),
	mil VARCHAR(50),
	web VARCHAR(50),
	fuente VARCHAR(50),	
	fecha_carga DATE	
);
CREATE TABLE bibliotecas(
	cod_localidad VARCHAR(50),
	id_provincia VARCHAR(50),
	id_departamento VARCHAR(50),
	categoria VARCHAR(50),
	provincia VARCHAR(50),
	localidad VARCHAR(50),
	nombre VARCHAR(50),
	domicilio VARCHAR(50),
	codigo_postal VARCHAR(50),
	numero_de_telefono VARCHAR(50),
	mil VARCHAR(50),
	web VARCHAR(50),
	fuente VARCHAR(50),	
	fecha_carga DATE	
);
CREATE TABLE tot_data(
	cod_localidad VARCHAR(50),
	id_provincia VARCHAR(50),
	id_departamento VARCHAR(50),
	categoria VARCHAR(50),
	provincia VARCHAR(50),
	localidad VARCHAR(50),
	nombre VARCHAR(50),
	domicilio VARCHAR(50),
	codigo_postal VARCHAR(50),
	numero_de_telefono VARCHAR(50),
	mil VARCHAR(50),
	web VARCHAR(50),
	fuente VARCHAR(50),	
	fecha_carga DATE
);
CREATE TABLE cines_count(
	provincia VARCHAR(50),
	pantallas INT,
	butacas INT,
	espacio_INCAA INT,
	fecha_carga DATE
);
CREATE TABLE regisros(
	registro VARCHAR(100),
	total INT
);

--CREATE TABLE NOMBRE_DE_TU_NUEVA TBLA(
--	COLUMNA_1 VAR_TYPE(50),
--	COLUMNA_2 VAR_TYPE(50),
--	COLUMNA_3 VAR_TYPE(50),
--	COLUMNA_4 VAR_TYPE(50),
--	COLUMNA_5 VAR_TYPE(50),

--COLUMNA_n Es el nombre que pondras a tu nueva tabla
--VAR_TYPE es el tipo de variable que almacenará la colimna