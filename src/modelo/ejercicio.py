from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Ejercicio(Base):
    __tablename__ = 'ejercicio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    caloriasQuemadasAproximadasPorRepeticion = Column(Integer, nullable=False)
    urlVideo = Column(String, nullable=False)
    entrenamientos = relationship('Entrenamiento', secondary='detalle_ejercicio')