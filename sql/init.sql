CREATE DATABASE IF NOT EXISTS inventario_db;
USE inventario_db;

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS almacenes (
    id INT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    almacen_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_inventario_producto FOREIGN KEY (producto_id) REFERENCES productos(id),
    CONSTRAINT fk_inventario_almacen FOREIGN KEY (almacen_id) REFERENCES almacenes(id),
    CONSTRAINT uq_producto_almacen UNIQUE (producto_id, almacen_id)
);

INSERT INTO almacenes (id, nombre, direccion) VALUES
    (1, 'Almacén Central Bogotá', 'Calle 100 # 15-20, Bogotá'),
    (2, 'Almacén Medellín Norte', 'Carrera 43A # 1-50, Medellín')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), direccion = VALUES(direccion);

INSERT INTO productos (nombre, descripcion, precio_unitario, categoria) VALUES
    ('Laptop Dell Inspiron', 'Laptop 15 pulgadas, 16GB RAM', 2899000.00, 'Tecnología'),
    ('Mouse inalámbrico', 'Mouse ergonómico con receptor USB', 45000.00, 'Accesorios'),
    ('Silla ergonómica', 'Silla de oficina con soporte lumbar', 650000.00, 'Mobiliario');

INSERT INTO inventario (producto_id, almacen_id, cantidad)
SELECT p.id, 1, v.cantidad
FROM (
    SELECT 'Laptop Dell Inspiron' AS nombre, 12 AS cantidad
    UNION ALL SELECT 'Mouse inalámbrico', 80
    UNION ALL SELECT 'Silla ergonómica', 25
) v
JOIN productos p ON p.nombre = v.nombre
ON DUPLICATE KEY UPDATE cantidad = VALUES(cantidad);

INSERT INTO inventario (producto_id, almacen_id, cantidad)
SELECT p.id, 2, v.cantidad
FROM (
    SELECT 'Laptop Dell Inspiron' AS nombre, 5 AS cantidad
    UNION ALL SELECT 'Mouse inalámbrico', 30
) v
JOIN productos p ON p.nombre = v.nombre
ON DUPLICATE KEY UPDATE cantidad = VALUES(cantidad);
