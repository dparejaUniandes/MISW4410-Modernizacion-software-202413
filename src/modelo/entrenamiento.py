import datetime
from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from .declarative_base import Base

class Entrenamiento(Base):
    __tablename__ = 'entrenamiento'
    id = Column(Integer, primary_key=True)
    fechaInicioEntrenamiento = Column(Date, default=datetime.datetime.utcnow)

    personaId = Column(Integer, ForeignKey('persona.id'), unique=True)
    persona = relationship('Persona', back_populates="entrenamiento")
    ejercicios = relationship('Ejercicio', secondary='detalle_ejercicio', back_populates='entrenamientos')

class DetalleEjercicio(Base):
    __tablename__ = 'detalle_ejercicio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    ejercicio = Column(
        Integer,
        ForeignKey('ejercicio.id'), nullable=False)

    entrenamiento = Column(
        Integer,
        ForeignKey('entrenamiento.id'), nullable=False)
    
    fechaRealizacionEjercicio = Column(Date)
    numeroRepeticiones = Column(Integer)
    duracion = Column(String)