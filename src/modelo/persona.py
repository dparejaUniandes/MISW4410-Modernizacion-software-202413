from sqlalchemy import Column, Integer, String, Float, Boolean, event
from sqlalchemy.orm import relationship

from .declarative_base import Base, session, Session
from src.modelo.entrenamiento import Entrenamiento

class Persona(Base):
    __tablename__ = 'persona'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
    talla = Column(Float)
    peso = Column(Float)
    edad = Column(Integer)
    medidaCentimetrosBrazos = Column(Integer)
    medidaCentimetrosPecho = Column(Integer)
    medidaCentimetrosCintura = Column(Integer)
    medidaCentimetrosPiernas = Column(Integer)
    habilitadaParaEntrenar = Column(Boolean)
    entrenamiento = relationship('Entrenamiento', back_populates="persona", uselist=False)

@event.listens_for(Persona, 'after_insert')
def receive_after_insert(mapper, connection, target):
    nuevoEntrenamiento = Entrenamiento(personaId = target.id)
    Session.object_session(target).add(nuevoEntrenamiento)