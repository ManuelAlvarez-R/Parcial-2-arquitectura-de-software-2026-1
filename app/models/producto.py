from sqlalchemy import Column, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(100), nullable=False)

    inventarios = relationship("Inventario", back_populates="producto")
