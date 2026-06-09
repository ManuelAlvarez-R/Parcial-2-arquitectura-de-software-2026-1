from decimal import Decimal

from pydantic import BaseModel, Field


class ProductoSchema(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    precio_unitario: Decimal
    categoria: str

    class Config:
        from_attributes = True


class AlmacenSchema(BaseModel):
    id: int
    nombre: str
    direccion: str

    class Config:
        from_attributes = True


class InventarioItemResponse(BaseModel):
    producto: ProductoSchema
    cantidad: int


class InventarioPorSedeResponse(BaseModel):
    almacen: AlmacenSchema
    items: list[InventarioItemResponse]


class RegistroInventarioRequest(BaseModel):
    producto_nombre: str = Field(..., min_length=1, max_length=150)
    producto_descripcion: str | None = None
    producto_precio_unitario: Decimal = Field(..., gt=0)
    producto_categoria: str = Field(..., min_length=1, max_length=100)
    almacen_id: int = Field(..., gt=0, description="ID de la sede de almacén")
    almacen_nombre: str = Field(..., min_length=1, max_length=150)
    almacen_direccion: str = Field(..., min_length=1, max_length=255)
    cantidad_inicial: int = Field(..., ge=0)


class RegistroInventarioResponse(BaseModel):
    mensaje: str
    producto: ProductoSchema
    almacen: AlmacenSchema
    cantidad: int
