SET NAMES utf8mb4;

ALTER DATABASE inventario_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Garantiza que el usuario de la app pueda conectarse desde la red Docker
CREATE USER IF NOT EXISTS 'inventario_user'@'%' IDENTIFIED BY 'inventario_pass';
GRANT ALL PRIVILEGES ON inventario_db.* TO 'inventario_user'@'%';
FLUSH PRIVILEGES;
