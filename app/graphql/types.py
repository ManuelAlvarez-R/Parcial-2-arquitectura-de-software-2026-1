from decimal import Decimal

import strawberry

from app.models import Almacen, Inventario, Producto


@strawberry.type(name="Producto")
class ProductoType:
    id: int
    nombre: str
    descripcion: str | None
    precio_unitario: Decimal
    categoria: str

    @classmethod
    def from_model(cls, producto: Producto) -> "ProductoType":
        return cls(
            id=producto.id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio_unitario=producto.precio_unitario,
            categoria=producto.categoria,
        )


@strawberry.type(name="Almacen")
class AlmacenType:
    id: int
    nombre: str
    direccion: str

    @classmethod
    def from_model(cls, almacen: Almacen) -> "AlmacenType":
        return cls(
            id=almacen.id,
            nombre=almacen.nombre,
            direccion=almacen.direccion,
        )


@strawberry.type(name="InventarioItem")
class InventarioItemType:
    producto: ProductoType
    cantidad: int


@strawberry.type(name="InventarioPorSede")
class InventarioPorSedeType:
    almacen: AlmacenType
    items: list[InventarioItemType]


@strawberry.type(name="Inventario")
class InventarioType:
    id: int
    producto: ProductoType
    almacen: AlmacenType
    cantidad: int

    @classmethod
    def from_model(cls, inventario: Inventario) -> "InventarioType":
        return cls(
            id=inventario.id,
            producto=ProductoType.from_model(inventario.producto),
            almacen=AlmacenType.from_model(inventario.almacen),
            cantidad=inventario.cantidad,
        )


@strawberry.input(name="RegistroAlmacenInput")
class RegistroAlmacenInput:
    almacen_id: int
    nombre: str
    direccion: str


@strawberry.type(name="RegistroAlmacenResponse")
class RegistroAlmacenResult:
    mensaje: str
    almacen: AlmacenType


@strawberry.input(name="RegistroInventarioInput")
class RegistroInventarioInput:
    producto_nombre: str
    producto_descripcion: str | None = None
    producto_precio_unitario: Decimal
    producto_categoria: str
    almacen_id: int
    cantidad_inicial: int


@strawberry.type(name="RegistroInventarioResponse")
class RegistroInventarioResult:
    mensaje: str
    producto: ProductoType
    almacen: AlmacenType
    cantidad: int
