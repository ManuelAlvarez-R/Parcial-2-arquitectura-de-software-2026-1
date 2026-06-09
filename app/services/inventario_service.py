from sqlalchemy.orm import Session

from app.exceptions import AlmacenNoEncontradoError
from app.models import Almacen, Inventario, Producto
from app.schemas.inventario import (
    InventarioItemResponse,
    InventarioPorSedeResponse,
    RegistroInventarioRequest,
    RegistroInventarioResponse,
)


class InventarioService:
    def __init__(self, db: Session):
        self.db = db

    def obtener_inventario_por_sede(self, sede_id: int) -> InventarioPorSedeResponse:
        almacen = self.db.query(Almacen).filter(Almacen.id == sede_id).first()
        if not almacen:
            raise AlmacenNoEncontradoError(sede_id)

        registros = (
            self.db.query(Inventario)
            .filter(Inventario.almacen_id == sede_id)
            .all()
        )

        items = [
            InventarioItemResponse(producto=registro.producto, cantidad=registro.cantidad)
            for registro in registros
        ]

        return InventarioPorSedeResponse(almacen=almacen, items=items)

    def registrar_producto_en_inventario(
        self, datos: RegistroInventarioRequest
    ) -> RegistroInventarioResponse:
        almacen = self.db.query(Almacen).filter(Almacen.id == datos.almacen_id).first()

        if almacen:
            almacen.nombre = datos.almacen_nombre
            almacen.direccion = datos.almacen_direccion
        else:
            almacen = Almacen(
                id=datos.almacen_id,
                nombre=datos.almacen_nombre,
                direccion=datos.almacen_direccion,
            )
            self.db.add(almacen)

        producto = Producto(
            nombre=datos.producto_nombre,
            descripcion=datos.producto_descripcion,
            precio_unitario=datos.producto_precio_unitario,
            categoria=datos.producto_categoria,
        )
        self.db.add(producto)
        self.db.flush()

        inventario_existente = (
            self.db.query(Inventario)
            .filter(
                Inventario.producto_id == producto.id,
                Inventario.almacen_id == datos.almacen_id,
            )
            .first()
        )

        if inventario_existente:
            inventario_existente.cantidad += datos.cantidad_inicial
            cantidad_final = inventario_existente.cantidad
        else:
            inventario = Inventario(
                producto_id=producto.id,
                almacen_id=datos.almacen_id,
                cantidad=datos.cantidad_inicial,
            )
            self.db.add(inventario)
            cantidad_final = datos.cantidad_inicial

        self.db.commit()
        self.db.refresh(producto)
        self.db.refresh(almacen)

        return RegistroInventarioResponse(
            mensaje="Producto registrado correctamente en el inventario",
            producto=producto,
            almacen=almacen,
            cantidad=cantidad_final,
        )
