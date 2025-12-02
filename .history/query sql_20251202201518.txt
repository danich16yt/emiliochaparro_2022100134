CREATE DATABASE IF NOT EXISTS emilio_chaparro_2022100134 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE emilio_chaparro_2022100134;

CREATE TABLE consultas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    celular VARCHAR(20) NOT NULL,
    horario_llamada VARCHAR(50) NOT NULL,
    fecha_consulta DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_fecha (fecha_consulta),
    INDEX idx_nombre (nombre_apellido)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
