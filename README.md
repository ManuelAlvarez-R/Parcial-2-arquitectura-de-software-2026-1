# Gestión de Inventarios de Almacén

**Equipo 4** — Parcial Práctico Arquitectura de Software

Servicio web monolítico con arquitectura **Modelo-Vista-Controlador (MVC)** desarrollado en **Python (FastAPI + Strawberry GraphQL)** y **MySQL**, desplegado en **Docker**. Incluye un frontend básico y **GraphiQL Playground** para consultar y registrar inventario.

## Requerimientos funcionales implementados

| Requerimiento | Operación GraphQL | Tipo |
|---|---|---|
| Consultar inventario por sede de almacén | `inventarioPorSede(sedeId)` | `Query` |
| Registrar producto en inventario | `registrarProducto(datos)` | `Mutation` |




## Despliegue con Docker

### Requisitos

- Docker Desktop
- Docker Compose

### Ejecutar el proyecto

```bash
docker compose up --build
```

Servicios disponibles:

| Servicio | URL |
|---|---|
| Frontend | http://localhost:8000 |
| GraphQL / GraphiQL | http://localhost:8000/graphql |
| Health check | http://localhost:8000/health |
| MySQL (host) | `localhost:3307` |

### Detener contenedores

```bash
docker compose down
```

Para eliminar también los datos persistentes:

```bash
docker compose down -v
```

### Solución de problemas

Si aparece el error `Host '...' is not allowed to connect to this MySQL server`:

```bash
docker compose down -v
docker compose up --build
```

El servicio `db-setup` reconfigura los permisos del usuario `inventario_user` en cada arranque.

## Esquema GraphQL

### Tipos

- `Producto` — nombre, descripción, precio unitario, categoría
- `Almacen` — id, nombre, dirección
- `InventarioItem` — producto + cantidad
- `InventarioPorSede` — almacén + lista de items
- `RegistroInventarioInput` — datos de entrada para la mutation
- `RegistroInventarioResponse` — resultado del registro

### Ejemplos en GraphiQL (`/graphql`)

#### 1. Query — Consultar inventario por sede

```graphql
query InventarioPorSede {
  inventarioPorSede(sedeId: 1) {
    almacen {
      id
      nombre
      direccion
    }
    items {
      cantidad
      producto {
        id
        nombre
        descripcion
        precioUnitario
        categoria
      }
    }
  }
}
```

#### 2. Mutation — Registrar producto en inventario

```graphql
mutation RegistrarProducto {
  registrarProducto(
    datos: {
      productoNombre: "Teclado mecánico"
      productoDescripcion: "Teclado RGB switch azul"
      productoPrecioUnitario: 180000
      productoCategoria: "Accesorios"
      almacenId: 1
      almacenNombre: "Almacén Central Bogotá"
      almacenDireccion: "Calle 100 # 15-20, Bogotá"
      cantidadInicial: 40
    }
  ) {
    mensaje
    cantidad
    producto {
      id
      nombre
    }
    almacen {
      id
      nombre
    }
  }
}
```

## Datos de prueba precargados

Al iniciar MySQL por primera vez se cargan:

- **Sede 1:** Almacén Central Bogotá (3 productos)
- **Sede 2:** Almacén Medellín Norte (2 productos)


## Desarrollo local (sin Docker)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Configura `.env` basándote en `.env.example` y ejecuta:

```bash
uvicorn app.main:app --reload
```

## Integrantes

Equipo 4 — Arquitectura de Software

Manuel Felipe Alvarez Rua

Luis Carlos Vanegas Zapata

Andrés Eduardo Pabón Roldán

Estefanía Garcés Pérez
