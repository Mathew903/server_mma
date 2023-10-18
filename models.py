from db import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String(250), index=True)
    password = Column(String(30))
    rol = Column(Integer)
    creado = Column(DateTime,default=datetime.now,onupdate=datetime.now)

class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True, unique=True)
    name = Column(String(250))
    description = Column(String)
    price = Column(Float)
    creado_por = Column(Integer, ForeignKey("user.id"))
    fecha_creacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)