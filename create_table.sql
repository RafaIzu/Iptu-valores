CREATE DATABASE `iptu`;

USE iptu;

CREATE TABLE iptu_valores(
ID INT NOT NULL AUTO_INCREMENT,
estado VARCHAR(10),
municipio VARCHAR(50),
regiao VARCHAR(50),
bairro VARCHAR(50),
tipo_residencia VARCHAR(50),
num_dorm VARCHAR(50),
num_vagas VARCHAR(50),
valor_m2 DECIMAL(19,4),
info varchar(500),
mes		TINYINT,
ano		INT,
CONSTRAINT iptu_valores_pk PRIMARY KEY (ID)
);

SELECT * FROM iptu_valores;

-- DELETE FROM iptu_valores;

-- DROP TABLE iptu_Valores;

