from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Inventario(Base):
    __tablename__ = "inventario"
    __table_args__ = (UniqueConstraint("producto_id", "almacen_id", name="uq_producto_almacen"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    almacen_id = Column(Integer, ForeignKey("almacenes.id"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=0)

    producto = relationship("Producto", back_populates="inventarios")
    almacen = relationship("Almacen", back_populates="inventarios")
