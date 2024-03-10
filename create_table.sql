CREATE DATABASE `iptu`;


CREATE TABLE iptu_valores(
ID INT NOT NULL AUTO_INCREMENT,
estado VARCHAR(10),
municipio VARCHAR(50),
regiao VARCHAR(50),
bairro VARCHAR(50),
valor_m2 DECIMAL(19,4),
mes		TINYINT,
ano		INT,
CONSTRAINT iptu_valores_pk PRIMARY KEY (ID)
);

DROP TABLE iptu_Valores;

