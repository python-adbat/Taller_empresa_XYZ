CREATE DATABASE IF NOT EXISTS EmprezaXYZ; 

USE emprezaXYZ; 
CREATE TABLE Usuario (
    id_usuario INT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    estado VARCHAR(20),
    contraseña VARCHAR(100),
    cargo VARCHAR(50),
    salario DECIMAL(10, 2),
    fecha_ingreso DATE
);

CREATE TABLE perfilesdeusuarios(
id INT PRIMARY KEY,
id_perfil INT,
id_usuario INT,
FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
FOREIGN KEY (id_perfil) REFERENCES Perfil(id_perfil)
);
CREATE TABLE Perfil (
    id_perfil INT PRIMARY KEY,
    nombre VARCHAR(50),
    fecha_vigencia DATE,
    descripcion TEXT   
);

CREATE TABLE Login (
    id_login INT PRIMARY KEY,
    id_usuario INT,
    fecha_login DATETIME,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);
CREATE TABLE Fidelizacion (
    id_fidelizacion INT PRIMARY KEY,
    id_usuario INT,
    puntos INT,
    fecha_actividad DATE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

SELECT * FROM  usuario; 
CREATE VIEW Vista_Fidelizacion AS
SELECT u.nombre, u.apellido, f.puntos, f.fecha_actividad
FROM Usuario u
JOIN Fidelizacion f ON u.id_usuario = f.id_usuario;

