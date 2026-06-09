from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Almacen(Base):
    __tablename__ = "almacenes"

    id = Column(Integer, primary_key=True, autoincrement=False)
    nombre = Column(String(150), nullable=False)
    direccion = Column(String(255), nullable=False)

    inventarios = relationship("Inventario", back_populates="almacen")
