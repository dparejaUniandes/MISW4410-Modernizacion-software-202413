from src.logica.FachadaEnForma import FachadaEnForma
from src.modelo.ejercicio import Ejercicio
from src.modelo.persona import Persona
from src.modelo.entrenamiento import DetalleEjercicio, Entrenamiento
from src.modelo.declarative_base import engine, Base, session

import re
import validators
from typing import List, Optional
from sqlalchemy import asc, insert, select, func
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import aliased
from datetime import datetime

class LogicaEnForma(FachadaEnForma):
    def __init__(self):
        Base.metadata.create_all(engine)

    def validar_crear_editar_ejercicio(self, nombre: str, descripcion: str, enlace: str, calorias: int) -> str:
        parametrosConError = []
        if(len(nombre) == 0 or len(nombre) > 200):
            parametrosConError.append('nombre')
        if(len(descripcion) == 0 or len(descripcion) > 2000):
            parametrosConError.append('descripcion')
        if( (not "youtube" in enlace) or (not validators.url(enlace)) or len(enlace) > 2000 ):
            parametrosConError.append('enlace')
        if( not isinstance(calorias, int) or calorias < 1):
            parametrosConError.append('calorias')

        respuesta = ''
        if(len(parametrosConError) > 0):
            respuesta = "Los campos " + ", ".join(parametrosConError) + " contienen error"
        return respuesta
    
    def crear_ejercicio(self, nombre: str, descripcion: str, urlVideo: str, calorias: int) -> bool:
        busqueda = session.query(Ejercicio).filter(Ejercicio.nombre == nombre).all()
        if len(busqueda) == 0:
            ejercicio = Ejercicio(nombre=nombre, descripcion=descripcion, urlVideo=urlVideo, caloriasQuemadasAproximadasPorRepeticion=calorias)
            session.add(ejercicio)
            session.commit()
            return True
        return False

    def dar_ejercicios(self) -> list:
        ejercicios = session.query(Ejercicio).order_by(asc(Ejercicio.nombre)).all()
        return ejercicios
    
    def dar_persona(self, idPersona: int) -> list:
        persona = session.query(Persona).filter(Persona.id == idPersona).first()

        respuesta = persona.__dict__.copy()
        respuesta['entrenamiento'] = persona.entrenamiento.id
        return respuesta
    
    def dar_personas(self) -> list:
        personas = session.query(Persona).order_by(asc(Persona.nombre), asc(Persona.apellido)).all()
        return personas

    def validar_crear_editar_entrenamiento(self, persona: dict, ejercicio: str, fecha: str, repeticiones: int, tiempo: str) -> str:
        parametrosConError = []
        
        if not "entrenamiento" in persona:
            parametrosConError.append('entrenamiento de persona')
        
        ejercicios = session.query(Ejercicio).filter(Ejercicio.nombre == ejercicio).all()
        if len(ejercicios) == 0:
            parametrosConError.append('ejercicio')

        fecha_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        if not fecha_pattern.match(fecha):
            parametrosConError.append('fecha')

        try:
            repeticiones = int(repeticiones)
            if repeticiones <= 0:
                parametrosConError.append('repeticiones')
        except ValueError:
            parametrosConError.append('repeticiones')

        tiempo_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
        if not tiempo_pattern.match(tiempo):
            parametrosConError.append('tiempo')

        respuesta = ''
        if(len(parametrosConError) > 0):
            respuesta = "Los campos " + ", ".join(parametrosConError) + " contienen error"
        return respuesta

    def crear_entrenamiento(self, persona: Persona, nombreEjercicio: str, fechaRealizacion: str, numeroRepeticiones: int, duracion: str) -> bool:
        try:
            # Buscar el Ejercicio por su nombre
            ejercicio = session.query(Ejercicio).filter_by(nombre=nombreEjercicio).one()

            # Crear un nuevo DetalleEjercicio
            nuevo_detalle = DetalleEjercicio(
                ejercicio=ejercicio.id,
                entrenamiento=persona['entrenamiento'],
                fechaRealizacionEjercicio=datetime.strptime(fechaRealizacion, '%Y-%m-%d').date(),
                numeroRepeticiones=numeroRepeticiones,
                duracion=duracion
            )

            # Añadir y confirmar la transacción
            session.add(nuevo_detalle)
            session.commit()

            return True

        except NoResultFound:
            # No se encontró el Entrenamiento o el Ejercicio
            return False
    
    def eliminar_entrenamiento(self, id_entrenamiento):
        detalle = session.query(DetalleEjercicio).filter_by(id=id_entrenamiento).first()

        if detalle is not None:
            session.delete(detalle)
            session.commit()
            return True
        else:
            return False

    def dar_entrenamientos(self, entrenamiento: int) -> Optional[List[DetalleEjercicio]]:
        try:
            ejercicio_alias = aliased(Ejercicio)
            
            detalles = (session.query(DetalleEjercicio, ejercicio_alias)
                    .join(ejercicio_alias, DetalleEjercicio.ejercicio == ejercicio_alias.id)
                    .filter(DetalleEjercicio.entrenamiento == entrenamiento)
                    .all())
            
            detalles_dict_list = [
                {
                    "id": detalle.id,
                    "fechaRealizacionEjercicio": detalle.fechaRealizacionEjercicio,
                    "numeroRepeticiones": detalle.numeroRepeticiones,
                    "duracion": detalle.duracion,
                    "fecha_retiro": "",
                    "ejercicio": ejercicio.nombre
                }
                for detalle, ejercicio in detalles
            ]
            
            return detalles_dict_list

        except NoResultFound:
            return []
        
    def editar_entrenamiento(self, id_entrenamiento: int, ejercicio: str, fecha: str, repeticiones: int, tiempo: str) -> bool:
        detalleEjercicio = session.query(DetalleEjercicio).filter_by(id = id_entrenamiento).first()
        if detalleEjercicio is None:
            return False
        
        ejercicio = session.query(Ejercicio).filter_by(nombre = ejercicio).first()
        if ejercicio is None:
            return False
        
        detalleEjercicio.ejercicio = ejercicio.id
        detalleEjercicio.fechaRealizacionEjercicio = datetime.strptime(fecha, '%Y-%m-%d').date()
        detalleEjercicio.numeroRepeticiones = repeticiones
        detalleEjercicio.duracion = tiempo

        session.commit()

        return True
        
    def calcular_imc(self, talla: float, peso: float) -> float:
        imc = round(peso / talla**2, 2)
        return imc

    def calcular_categoria_imc(self, calculoIMC: float) -> str:
        resultadoEsperado= ''
        if calculoIMC < 18.5:
            resultadoEsperado = "Bajo peso"
        elif calculoIMC <= 24.9:
            resultadoEsperado = "Peso saludable"
        elif calculoIMC <= 29.9:
            resultadoEsperado = "Sobrepeso"
        else:
            resultadoEsperado = "Obesidad"
        return resultadoEsperado

    def dar_reporte(self, id_persona: int) -> dict:
        busquedaPersona = session.query(Persona).filter(Persona.id == id_persona).first()
        stmt = session.query(
                DetalleEjercicio.fechaRealizacionEjercicio.label("fecha"), 
                func.sum(DetalleEjercicio.numeroRepeticiones).label("repeticiones"),
                func.sum(DetalleEjercicio.numeroRepeticiones * Ejercicio.caloriasQuemadasAproximadasPorRepeticion).label("calorias")
            ).join(
                Ejercicio
            ).group_by(
                DetalleEjercicio.fechaRealizacionEjercicio
            ).order_by(DetalleEjercicio.fechaRealizacionEjercicio.asc())

        resultados = session.execute(stmt)
        entrenamientos = []
        totalRepeticiones = 0
        totalCalorias = 0
        imc = self.calcular_imc(busquedaPersona.talla, busquedaPersona.peso)
        categoriaImc = self.calcular_categoria_imc(imc)
        for fila in resultados:

            objeto = {
                "fecha": str(fila[0]),
                "repeticiones": fila[1],
                "calorias": fila[2]              
            }
            totalRepeticiones += fila[1] 
            totalCalorias += fila[2]
            entrenamientos.append(objeto)
        reporte = {
            "persona": {
                "nombre": busquedaPersona.nombre,
                "apellido": busquedaPersona.apellido,
                "talla": busquedaPersona.talla,
                "peso": busquedaPersona.peso
            },
            "estadisticas": {
                "imc": imc,
                "clasificacion": categoriaImc,
                "entrenamientos": entrenamientos,
                "total_repeticiones": totalRepeticiones,
                "total_calorias": totalCalorias
            }
        }
        return reporte
    
    def verificar_ejercicio_existe_en_entrenamiento(self, idEjercicio: int)->bool:
        detalleEjercicio = session.query(DetalleEjercicio).filter(DetalleEjercicio.ejercicio == idEjercicio).first()
        if detalleEjercicio is None:
            return False
        return True
    
    def eliminar_ejercicio(self, idEjercicio: int)->bool:
        ejercicioExisteEnEntrenamiento = self.verificar_ejercicio_existe_en_entrenamiento(idEjercicio)
        ejercicio = session.query(Ejercicio).get(idEjercicio)
        if ejercicioExisteEnEntrenamiento or ejercicio is None:
            return False
        session.delete(ejercicio)
        session.commit()
        return True
        
    def editar_ejercicio(self, idEjercicio: int, nombre: str, descripcion: str, urlVideo: str, calorias: int) -> bool:
        busqueda = session.query(Ejercicio).filter(Ejercicio.nombre == nombre).all()
        cantidadBusqueda = len(busqueda)
        if (cantidadBusqueda == 1 and busqueda[0].id == idEjercicio) or cantidadBusqueda == 0:
            ejercicio = session.query(Ejercicio).filter(Ejercicio.id == idEjercicio).first()
            ejercicio.nombre = nombre
            ejercicio.descripcion = descripcion
            ejercicio.urlVideo = urlVideo
            ejercicio.caloriasQuemadasAproximadasPorRepeticion = calorias
            session.add(ejercicio)
            session.commit()
            return True
        return False