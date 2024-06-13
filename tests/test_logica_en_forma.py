from faker import Faker
import unittest
from datetime import datetime

from src.logica.LogicaEnForma import LogicaEnForma
from src.modelo.ejercicio import Ejercicio
from src.modelo.persona import Persona
from src.modelo.entrenamiento import DetalleEjercicio, Entrenamiento
from src.modelo.declarative_base import Session, Base, engine

class LogicaEnFormaTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = LogicaEnForma()
        self.ejercicioValido = ['Brinco cruzado', 'Cruzar los brazos sobre la cabeza al saltar', 'https://www.youtube.com/watch?v=g_fsgtHXecw', 50]

        '''Abre la sesión'''
        self.session = Session()

        # Generación de datos con libreria Faker
        self.data_factory = Faker()
        # Creación de persona e información para los entrenamientos
        self.persona = Persona(
            nombre = self.data_factory.name(),
            apellido = self.data_factory.last_name(),
            talla = self.data_factory.random_int(1, 300),
            peso = self.data_factory.random_int(1, 600),
            edad = self.data_factory.random_int(1, 100),
            medidaCentimetrosBrazos = self.data_factory.random_int(10, 100),
            medidaCentimetrosPecho = self.data_factory.random_int(50, 300),
            medidaCentimetrosCintura = self.data_factory.random_int(10, 300),
            medidaCentimetrosPiernas = self.data_factory.random_int(20, 200),
            habilitadaParaEntrenar = True
        )
        self.nombreEjercicio = "Zancadas o desplantes"
        self.fechaEntrenamientoCadena = "2023-09-14"
        self.numeroRepeticiones = self.data_factory.random_int(1, 100)
        self.duracion = "01:05:21"
        self.calorias = self.data_factory.random_int(1, 100)
        self.descripcion = self.data_factory.sentence()

        self.session.add(self.persona)
        self.session.commit()

        self.entrenamientoValido =[ self.persona, self.ejercicioValido[0], self.fechaEntrenamientoCadena, self.numeroRepeticiones, self.duracion ]
        
    def tearDown(self):
        self.logica = None
        '''Abre la sesión'''
        self.session = Session()

        '''Limpiar la db'''
        Base.metadata.drop_all(bind=engine)

        self.session.close()
        
    def test_validar_crear_editar_ejercicio_validar_nombre(self):
        '''Prueba que el nombre tenga la longitud para cumplir el criterio de aceptacion 1 de la HU011'''
        ejercicioNombreMenorUno = self.ejercicioValido.copy()
        ejercicioNombreMenorUno[0] = ''
        ejercicioNombreMayorDocientos = self.ejercicioValido.copy()
        ejercicioNombreMayorDocientos[0] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis risus sed vulputate odio ut enim blandit volutpat maecenas. Mattis pellentesque id nibh tortor id aliquet lectus. Dui faucibus in ornare quam viverra orci. At varius vel pharetra vel turpis. Ac tortor dignissim convallis aenean. Risus sed vulputate odio ut. Accumsan sit amet nulla facilisi morbi tempus iaculis urna. Et ligula ullamcorper malesuada proin libero nunc consequat interdum varius."
        respuestaNombreMenorUno = self.logica.validar_crear_editar_ejercicio(*ejercicioNombreMenorUno)
        respuestaNombreMayorDocientos = self.logica.validar_crear_editar_ejercicio(*ejercicioNombreMayorDocientos)
        respuestaNombreCorrecto = self.logica.validar_crear_editar_ejercicio(*self.ejercicioValido)
        self.assertIn("nombre",  respuestaNombreMenorUno)
        self.assertIn("nombre",  respuestaNombreMayorDocientos)
        self.assertEqual("", respuestaNombreCorrecto)
    
    def test_validar_crear_editar_ejercicio_validar_descripcion(self):
        '''Prueba que la descripcion tenga la longitud para cumplir el criterio de aceptacion 2 de la HU011'''
        ejercicioDescripcionMenorUno = self.ejercicioValido.copy()
        ejercicioDescripcionMenorUno[1] = ''
        ejercicioDescripcionMayorDocientos = self.ejercicioValido.copy()
        ejercicioDescripcionMayorDocientos[1] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis risus sed vulputate odio ut enim blandit volutpat maecenas. Mattis pellentesque id nibh tortor id aliquet lectus. Dui faucibus in ornare quam viverra orci. At varius vel pharetra vel turpis. Ac tortor dignissim convallis aenean. Risus sed vulputate odio ut. Accumsan sit amet nulla facilisi morbi tempus iaculis urna. Et ligula ullamcorper malesuada proin libero nunc consequat interdum varius. Odio tempor orci dapibus ultrices in iaculis nunc sed. Risus ultricies tristique nulla aliquet enim tortor at. Morbi tristique senectus et netus et malesuada fames ac. Nunc pulvinar sapien et ligula. Dui faucibus in ornare quam viverra orci sagittis eu volutpat. Scelerisque felis imperdiet proin fermentum leo vel. Lacus vel facilisis volutpat est. Posuere sollicitudin aliquam ultrices sagittis orci. Nisl tincidunt eget nullam non nisi. Ultricies mi quis hendrerit dolor. Fames ac turpis egestas integer eget aliquet nibh praesent tristique. Turpis in eu mi bibendum neque. Pretium aenean pharetra magna ac placerat vestibulum lectus mauris. Vitae et leo duis ut. Faucibus in ornare quam viverra. Phasellus faucibus scelerisque eleifend donec. Iaculis at erat pellentesque adipiscing commodo elit at. At varius vel pharetra vel turpis nunc eget. Urna et pharetra pharetra massa massa ultricies mi quis hendrerit. Mattis aliquam faucibus purus in massa. Lectus magna fringilla urna porttitor rhoncus dolor purus non enim. Nisl condimentum id venenatis a condimentum vitae sapien pellentesque. Urna duis convallis convallis tellus id interdum. Arcu ac tortor dignissim convallis aenean et tortor at risus. Tristique sollicitudin nibh sit amet. Pretium quam vulputate dignissim suspendisse in. Urna neque viverra justo nec ultrices dui sapien. Nec ullamcorper sit amet risus nullam eget felis. Amet commodo nulla facilisi nullam vehicula ipsum a arcu cursus. Quis risus sed vulput."
        respuestaDescripcionMenorUno = self.logica.validar_crear_editar_ejercicio(*ejercicioDescripcionMenorUno)
        respuestaDescripcionMayorDosmil = self.logica.validar_crear_editar_ejercicio(*ejercicioDescripcionMayorDocientos)
        respuestaDescripcionCorrecto = self.logica.validar_crear_editar_ejercicio(*self.ejercicioValido)
        self.assertIn("descripcion",  respuestaDescripcionMenorUno)
        self.assertIn("descripcion",  respuestaDescripcionMayorDosmil)
        self.assertEqual("", respuestaDescripcionCorrecto)
    
    def test_validar_crear_editar_ejercicio_validar_enlace(self):
        '''Prueba que el enlace tenga la longitud para cumplir el criterio de aceptacion 4 de la HU011'''
        ejercicioEnlaceOtroSitio = self.ejercicioValido.copy()
        ejercicioEnlaceOtroSitio[2] = 'http://vimeo.com'
        ejercicioEnlaceLargo = self.ejercicioValido.copy()
        ejercicioEnlaceLargo[2] = "https://www.youtube.com/watch?v=VVIXSM-tQhM" + 'a'*2000
        respuestaEnlaceOtroSitio = self.logica.validar_crear_editar_ejercicio(*ejercicioEnlaceOtroSitio)
        respuestaEnlaceLargo = self.logica.validar_crear_editar_ejercicio(*ejercicioEnlaceLargo)
        respuestaCorrecto = self.logica.validar_crear_editar_ejercicio(*self.ejercicioValido)
        self.assertIn("enlace",  respuestaEnlaceOtroSitio)
        self.assertIn("enlace",  respuestaEnlaceLargo)
        self.assertEqual("", respuestaCorrecto)
    
    def test_validar_crear_editar_ejercicio_validar_calorias(self):
        '''Prueba que las calorias tengan los criterios de aceptacion para cumplir el punto 3 de la HU011'''
        ejercicioCaloriasNegativas = self.ejercicioValido.copy()
        ejercicioCaloriasNegativas[3] = -3
        ejercicioCaloriasConDecimales = self.ejercicioValido.copy()
        ejercicioCaloriasConDecimales[3] = 14.32
        respuestaCaloriasNegativas = self.logica.validar_crear_editar_ejercicio(*ejercicioCaloriasNegativas)
        respuestaCaloriasConDecimales = self.logica.validar_crear_editar_ejercicio(*ejercicioCaloriasConDecimales)
        respuestaCorrecto = self.logica.validar_crear_editar_ejercicio(*self.ejercicioValido)
        self.assertIn("calorias",  respuestaCaloriasNegativas)
        self.assertIn("calorias",  respuestaCaloriasConDecimales)
        self.assertEqual("", respuestaCorrecto)

    def test_crear_ejercicio_no_repetido(self):
        '''Prueba la adición de un ejercicio que no está repetido de la HU011'''
        resultado = self.logica.crear_ejercicio(
            nombre = self.data_factory.name(),
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            calorias = self.data_factory.random_int(1, 300)
        )
        self.assertEqual(resultado, True)

    def test_crear_ejercicio_repetido(self):
        '''Prueba la adición de un ejercicio repetido en el setup de la HU011'''
        nombre = self.data_factory.name()

        self.ejercicio1 = Ejercicio(
            nombre = nombre,
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            caloriasQuemadasAproximadasPorRepeticion = self.data_factory.random_int(1, 300)
        )
        self.session.add(self.ejercicio1)
        self.session.commit()

        resultado = self.logica.crear_ejercicio(
            nombre = nombre,
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            calorias = self.data_factory.random_int(1, 300)
        )
        self.assertFalse(resultado)

    def test_crear_ejercicio_validando_persistencia(self):
        '''Prueba la validación al crear un ejercicio con parámetros validos y su persistencia en la db de la HU011'''
        nombre = self.ejercicioValido[0]
        self.logica.crear_ejercicio(*self.ejercicioValido)
        
        busqueda = self.session.query(Ejercicio).filter(Ejercicio.nombre == nombre).first()
        self.assertEqual(nombre, busqueda.nombre)
        self.assertEqual(self.ejercicioValido[3], busqueda.caloriasQuemadasAproximadasPorRepeticion)

    def test_listar_ejercicios_sin_registros(self):
        '''Prueba devolver ejercicios sin registro en la db de la HU012'''
        resultado = self.logica.dar_ejercicios()
        self.assertEqual(0, len(resultado))

    def test_listar_ejercicios_con_registros(self):
        '''Prueba devolver ejercicios con registros en la db de la HU012 criterio de aceptación 3'''

        self.logica.crear_ejercicio(
            nombre = "Sentadillas",
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            calorias = self.data_factory.random_int(1, 300)
        )
        resultado = self.logica.dar_ejercicios()
        self.assertEqual(1, len(resultado))
        
        self.logica.crear_ejercicio(
            nombre = "Flexiones de pecho",
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            calorias = self.data_factory.random_int(1, 300)
        )
        resultado = self.logica.dar_ejercicios()
        self.assertEqual(2, len(resultado))
        
        self.assertEqual("Flexiones de pecho", resultado[0].nombre)

    def test_listar_personas_sin_registros(self):
        '''Prueba devolver personas sin registro en la db de la HU001'''
        # El setUp configura una persona inicial por defecto debemos limpiar la DB
        busquedaPersonas = self.session.query(Persona).all()
        for persona in busquedaPersonas:
            self.session.delete(persona)
        self.session.commit()

        resultado = self.logica.dar_personas()
        self.assertEqual(0, len(resultado))
    
    def test_listar_personas_con_registros(self):
        '''Prueba devolver personas con registro en la db de la HU001 criterio de aceptación 3'''

        resultado = self.logica.dar_personas()
        # El setUp configura una persona inicial por defecto
        self.assertEqual(1, len(resultado))

        persona2 = Persona(
            nombre = self.data_factory.name(),
            apellido = self.data_factory.last_name(),
            talla = self.data_factory.random_int(1, 300),
            peso = self.data_factory.random_int(1, 600),
            edad = self.data_factory.random_int(1, 100),
            medidaCentimetrosBrazos = self.data_factory.random_int(10, 100),
            medidaCentimetrosPecho = self.data_factory.random_int(50, 300),
            medidaCentimetrosCintura = self.data_factory.random_int(10, 300),
            medidaCentimetrosPiernas = self.data_factory.random_int(20, 200),
            habilitadaParaEntrenar = True
        )
        self.session.add(persona2)
        self.session.commit()
        resultado2 = self.logica.dar_personas()
        self.assertEqual(2, len(resultado2))

        persona3 = Persona(
            nombre = self.data_factory.name(),
            apellido = self.data_factory.last_name(),
            talla = self.data_factory.random_int(1, 300),
            peso = self.data_factory.random_int(1, 600),
            edad = self.data_factory.random_int(1, 100),
            medidaCentimetrosBrazos = self.data_factory.random_int(10, 100),
            medidaCentimetrosPecho = self.data_factory.random_int(50, 300),
            medidaCentimetrosCintura = self.data_factory.random_int(10, 300),
            medidaCentimetrosPiernas = self.data_factory.random_int(20, 200),
            habilitadaParaEntrenar = True
        )
        self.session.add(persona3)
        self.session.commit()
        resultado3 = self.logica.dar_personas()

        personas = [self.persona, persona2, persona3]
        personas.sort(key=lambda persona: (persona.nombre, persona.apellido))

        self.assertEqual(personas[0].nombre, resultado3[0].nombre)
        self.assertEqual(personas[0].apellido, resultado3[0].apellido)

    def test_validar_crear_editar_entrenamiento(self):
        '''Prueba validar agregar un ejercicio a una persona de la HU005'''
        self.test_crear_ejercicio_validando_persistencia()
        respuestaPersona = self.logica.dar_persona(self.entrenamientoValido[0].id)
        self.entrenamientoValido[0] = respuestaPersona
        entrenamientoValidoPersonaDict = self.entrenamientoValido.copy()
        respuestaCorrecto = self.logica.validar_crear_editar_entrenamiento(*self.entrenamientoValido)
        self.assertEqual("", respuestaCorrecto)

        '''Prueba validar agregar un ejercicio que no existe de la HU005'''
        parametrosMalos = self.entrenamientoValido.copy()
        parametrosMalos[1] = "Ejercicio Falso"
        respuestaEjercicioNoExiste = self.logica.validar_crear_editar_entrenamiento(*parametrosMalos)
        self.assertIn("ejercicio", respuestaEjercicioNoExiste)

        '''Prueba validar agregar un fecha sin patron valido al entrenamiento de la HU005'''
        parametrosMalos = self.entrenamientoValido.copy()
        parametrosMalos[2] = self.data_factory.date(pattern="%d-%m-%Y")
        respuestaEjercicioNoExiste = self.logica.validar_crear_editar_entrenamiento(*parametrosMalos)
        self.assertIn("fecha", respuestaEjercicioNoExiste)
        
        '''Prueba validar agregar repeticiones no valido al entrenamiento de la HU005'''
        parametrosMalos = self.entrenamientoValido.copy()
        parametrosMalos[3] = -1
        respuestaRepeticionesIncorrectas = self.logica.validar_crear_editar_entrenamiento(*parametrosMalos)
        self.assertIn("repeticiones", respuestaRepeticionesIncorrectas)

        '''Prueba validar agregar un tiempo incorrecto al entrenamiento  de la HU005'''
        parametrosMalos = self.entrenamientoValido.copy()
        parametrosMalos[4] = self.data_factory.time(pattern="%H-%M-%S")
        respuestaTiempoIncorrecto = self.logica.validar_crear_editar_entrenamiento(*parametrosMalos)
        self.assertIn("tiempo", respuestaTiempoIncorrecto)

        '''Prueba validar agregar un ejercicio a una persona sin entrenamiento de la HU005'''
        parametrosMalos = entrenamientoValidoPersonaDict.copy()
        del parametrosMalos[0]["entrenamiento"] 
        respuestaSinCampo = self.logica.validar_crear_editar_entrenamiento(*parametrosMalos)
        self.assertIn("entrenamiento de persona", respuestaSinCampo)

    def test_crear_ejercicio_persona_exitosamente_pero_sin_relacion_con_tablas_ejercicio_entrenamiento(self):
        '''Prueba crear en ejercicio de una persona en la db sin tener en cuenta las relaciones de la HU005'''
        self.logica.crear_ejercicio(self.nombreEjercicio, self.descripcion, "https://youtube.com", self.calorias)
        respuestaPersona = self.logica.dar_persona(self.persona.id)
        estaCreadoEjercicio = self.logica.crear_entrenamiento(respuestaPersona , self.nombreEjercicio, self.fechaEntrenamientoCadena, self.numeroRepeticiones, self.duracion)
        self.assertTrue(estaCreadoEjercicio)

    def test_crear_ejercicio_persona_exitosamente_teniendo_relacion_con_tabla_entrenamiento(self):
        '''Prueba crear en ejercicio de una persona con la relación entre detalle_ejercicio y entrenamiento en la db de la HU005'''
        self.logica.crear_ejercicio(self.nombreEjercicio, self.descripcion, "https://youtube.com", self.calorias)
        respuestaPersona = self.logica.dar_persona(self.persona.id)
        estaCreadoEjercicio = self.logica.crear_entrenamiento(respuestaPersona, self.nombreEjercicio, self.fechaEntrenamientoCadena, self.numeroRepeticiones, self.duracion)
        self.assertTrue(estaCreadoEjercicio)
    
    def test_crear_ejercicio_persona_exitosamente_teniendo_relacion_con_tablas_ejercicio_entrenamiento(self):
        '''Prueba crear en ejercicio de una persona con la relación entre detalle_ejercicio y ejercicioen la db de la HU005'''
        self.logica.crear_ejercicio(self.nombreEjercicio, self.descripcion, "https://youtube.com", self.calorias)
        respuestaPersona = self.logica.dar_persona(self.persona.id)
        estaCreadoEjercicio = self.logica.crear_entrenamiento(respuestaPersona, self.nombreEjercicio, 
                                                              self.fechaEntrenamientoCadena, self.numeroRepeticiones, self.duracion)
        self.assertTrue(estaCreadoEjercicio)

    def test_crear_ejercicio_persona_exitoso_y_prueba_datos_persistidos(self):
        '''Prueba crear en ejercicio de una persona con todos los datos persistidos en BD correctamente HU005'''
        self.logica.crear_ejercicio(self.nombreEjercicio, self.descripcion, "https://youtube.com", self.calorias)
        respuestaPersona = self.logica.dar_persona(self.persona.id)
        estaCreadoEjercicio = self.logica.crear_entrenamiento(respuestaPersona, self.nombreEjercicio, 
                                                              self.fechaEntrenamientoCadena, self.numeroRepeticiones, self.duracion)
        busquedaEntrenamiento = self.session.query(DetalleEjercicio).filter(DetalleEjercicio.entrenamiento == self.persona.entrenamiento.id).first()
        fechaResultado = busquedaEntrenamiento.fechaRealizacionEjercicio
        fechaCadena = str(fechaResultado.year) + "-0" + str(fechaResultado.month) + "-" + str(fechaResultado.day)
        self.assertTrue(estaCreadoEjercicio)
        self.assertEqual(fechaCadena, self.fechaEntrenamientoCadena)
        self.assertEqual(busquedaEntrenamiento.numeroRepeticiones, self.numeroRepeticiones)
        self.assertEqual(busquedaEntrenamiento.duracion, self.duracion)

    def test_listar_entrenamiento_sin_registros(self):
        '''Prueba devolver entrenamiento sin ejercicios en la db de la HU006'''
        resultado = self.logica.dar_entrenamientos(self.persona.entrenamiento.id)
        self.assertEqual(0, len(resultado))

    def test_listar_entrenamiento_con_registros(self):
        '''Prueba devolver entrenamiento con ejercicios en la db de la HU006'''
        self.test_crear_ejercicio_persona_exitoso_y_prueba_datos_persistidos()
        resultado = self.logica.dar_entrenamientos(self.persona.entrenamiento.id)
        self.assertEqual(1, len(resultado))

    def test_editar_entrenamiento_validacion_tipo_respuesta(self):
        '''Editar un entrenamiento a una persona, se valida el tipo de respuesta, relacionado con HU007'''
        self.test_crear_ejercicio_persona_exitoso_y_prueba_datos_persistidos()
        busquedaEntrenamiento = self.session.query(DetalleEjercicio).filter(DetalleEjercicio.entrenamiento == self.persona.entrenamiento.id).first()

        nombreNuevoEjercicio = 'Sentadillas'
        self.logica.crear_ejercicio(
            nombre = nombreNuevoEjercicio,
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            calorias = self.data_factory.random_int(1, 300)
        )

        self.assertTrue(self.logica.editar_entrenamiento(
            busquedaEntrenamiento.id,
            nombreNuevoEjercicio,
            str(busquedaEntrenamiento.fechaRealizacionEjercicio),
            157,
            busquedaEntrenamiento.duracion
        ))

    def test_editar_entrenamiento_validacion_persistencia(self):
        '''Editar un entrenamiento a una persona, se valida la persistencia, relacionado con HU008'''
        self.test_crear_ejercicio_persona_exitoso_y_prueba_datos_persistidos()
        busquedaEntrenamiento = self.session.query(DetalleEjercicio).filter(DetalleEjercicio.entrenamiento == self.persona.entrenamiento.id).first()

        nombreNuevoEjercicio = 'Sentadillas'
        self.logica.crear_ejercicio(
            nombre = nombreNuevoEjercicio,
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            calorias = self.data_factory.random_int(1, 300)
        )

        self.assertTrue(self.logica.editar_entrenamiento(
            busquedaEntrenamiento.id,
            nombreNuevoEjercicio,
            str(busquedaEntrenamiento.fechaRealizacionEjercicio),
            157,
            busquedaEntrenamiento.duracion
        ))

        busquedaPostEditar = self.logica.dar_entrenamientos(self.persona.entrenamiento.id)

        for entreno in busquedaPostEditar:
            if(entreno['id'] == busquedaEntrenamiento.id):
                self.assertEqual(nombreNuevoEjercicio, entreno['ejercicio'])
                self.assertEqual(157, entreno['numeroRepeticiones'])

    def test_eliminar_entrenamiento_validacion_tipo_respuesta(self):
        '''Eliminar un entrenamiento a una persona, se valida el tipo de respuesta, relacionado con HU008'''
        self.test_crear_ejercicio_persona_exitoso_y_prueba_datos_persistidos()
        busquedaEntrenamiento = self.session.query(DetalleEjercicio).filter(DetalleEjercicio.entrenamiento == self.persona.entrenamiento.id).first()

        resultado = self.logica.eliminar_entrenamiento(busquedaEntrenamiento.id)

        self.assertTrue(resultado)

    def test_eliminar_entrenamiento_validacion_persistencia(self):
        '''Eliminar un entrenamiento a una persona, se valida la persistencia, relacionado con HU008'''
        self.test_crear_ejercicio_persona_exitoso_y_prueba_datos_persistidos()
        busquedaEntrenamiento = self.session.query(DetalleEjercicio).filter(DetalleEjercicio.entrenamiento == self.persona.entrenamiento.id).first()

        self.assertTrue(self.logica.eliminar_entrenamiento(busquedaEntrenamiento.id))

        busquedaPostBorrado = self.logica.dar_entrenamientos(self.persona.entrenamiento.id)
        self.assertEqual(0, len(busquedaPostBorrado))

    def test_dar_reporte_sin_datos(self):
        '''Prueba generar reporte de una persona sin información HU009'''
        reporte = self.logica.dar_reporte(self.persona.id)
        self.assertTrue('persona' in reporte or reporte['persona'])
        self.assertTrue('estadisticas' in reporte or reporte['estadisticas'])
        self.assertEqual(0, len(reporte['estadisticas']['entrenamientos']))

    def test_dar_reporte_datos_persona(self):
        '''Prueba generar reporte de una persona con su talla y peso HU009'''

        reporte = self.logica.dar_reporte(self.persona.id)
        self.assertTrue('persona' in reporte or reporte['persona'])
        self.assertEqual(self.persona.talla, reporte['persona']['talla'])
        self.assertEqual(self.persona.peso, reporte['persona']['peso'])

    def test_dar_reporte_estadisticas(self):
        '''Prueba generar reporte de una persona con entrenamientos HU009'''
        fechasEntrenamiento = ["2023-09-12", "2023-09-16"]
        videoUrl = "https://www.youtube.com"
        nuevoEjercicio1 = {
            "nombre": self.data_factory.name(),
            "descripcion": self.data_factory.text(),
            "calorias": self.data_factory.random_int(1, 100),

            "numeroRepeticiones": self.data_factory.random_int(1, 100),
            "duracion": self.duracion,
        }
        nuevoEjercicio2 = {
            "nombre": self.data_factory.name(),
            "descripcion": self.data_factory.text(),
            "calorias": self.data_factory.random_int(1, 100),

            "numeroRepeticiones": self.data_factory.random_int(1, 100),
            "duracion": self.duracion,
        }
        nuevoEjercicio0 = {
            "nombre": nuevoEjercicio1['nombre'],
            "calorias": nuevoEjercicio1['calorias'],

            "numeroRepeticiones": self.numeroRepeticiones,
            "duracion": self.duracion,
        }
        self.logica.crear_ejercicio(nombre = nuevoEjercicio1['nombre'], descripcion = nuevoEjercicio1['descripcion'], urlVideo = videoUrl, calorias = nuevoEjercicio1['calorias'])
        self.logica.crear_ejercicio(nombre = nuevoEjercicio2['nombre'], descripcion = nuevoEjercicio2['descripcion'], urlVideo = videoUrl, calorias = nuevoEjercicio2['calorias'])
        
        respuestaPersona = self.logica.dar_persona(self.persona.id)
        self.logica.crear_entrenamiento(respuestaPersona, nuevoEjercicio0['nombre'], fechasEntrenamiento[0], nuevoEjercicio0['numeroRepeticiones'], nuevoEjercicio0['duracion'])
        self.logica.crear_entrenamiento(respuestaPersona, nuevoEjercicio1['nombre'], fechasEntrenamiento[1], nuevoEjercicio1['numeroRepeticiones'], nuevoEjercicio1['duracion'])
        self.logica.crear_entrenamiento(respuestaPersona, nuevoEjercicio2['nombre'], fechasEntrenamiento[1], nuevoEjercicio2['numeroRepeticiones'], nuevoEjercicio2['duracion'])
        
        reporte = self.logica.dar_reporte(self.persona.id)

        caloriasConsumidas = [(nuevoEjercicio0['numeroRepeticiones'] * nuevoEjercicio0['calorias']), (nuevoEjercicio1['numeroRepeticiones'] * nuevoEjercicio1['calorias'] + nuevoEjercicio2['numeroRepeticiones'] * nuevoEjercicio2['calorias'])]
        ejerciciosRealizados = [nuevoEjercicio0['numeroRepeticiones'], (nuevoEjercicio1['numeroRepeticiones']  + nuevoEjercicio2['numeroRepeticiones'] )]

        self.assertEqual(len(fechasEntrenamiento), len(reporte['estadisticas']['entrenamientos']))

        for index, diaDeEntrenamiento in enumerate(reporte['estadisticas']['entrenamientos']):
            self.assertEqual(fechasEntrenamiento[index], diaDeEntrenamiento['fecha'])
            self.assertEqual(ejerciciosRealizados[index], diaDeEntrenamiento['repeticiones'])
            self.assertEqual(caloriasConsumidas[index], diaDeEntrenamiento['calorias'])

        self.assertEqual(sum(ejerciciosRealizados), reporte['estadisticas']['total_repeticiones'])
        self.assertEqual(sum(caloriasConsumidas), reporte['estadisticas']['total_calorias'])

    def test_calcular_imc_validar_tipo_respuesta(self):
        '''Calcular el IMC con talla y peso de la persona se valida el tipo de respuesta, relacionado con HU009'''
        talla = self.data_factory.pyfloat(left_digits = 2, right_digits = 2, positive = True, min_value = 1)
        peso = self.data_factory.pyfloat(left_digits = 2, right_digits = 2, positive = True, min_value = 1)

        resultado = self.logica.calcular_imc(talla, peso)

        self.assertTrue(isinstance(resultado, float))
    
    def test_calcular_imc_validar_respuesta(self):
        '''Calcular el IMC con talla y peso de la persona, se valida la respuesta, relacionado con HU009'''
        talla = self.data_factory.pyfloat(left_digits = 2, right_digits = 2, positive = True, min_value = 1)
        peso = self.data_factory.pyfloat(left_digits = 2, right_digits = 2, positive = True, min_value = 1)
        imc = round(peso / talla**2, 2)

        resultado = self.logica.calcular_imc(talla, peso)

        self.assertEqual(imc, resultado)

    def test_calcular_categoria_imc_validar_tipo_respuesta(self):
        '''Calcular la categoria del IMC, se valida el tipo de respuesta, relacionado con HU009'''
        calculoIMC = self.data_factory.pyfloat(left_digits = 2, right_digits = 2, positive = True)

        resultado = self.logica.calcular_categoria_imc(calculoIMC)

        self.assertTrue(isinstance(resultado, str))
    
    def test_calcular_categoria_imc_validar_respuesta(self):
        '''Calcular la categoria del IMC, se valida la respuesta, relacionado con HU009'''
        calculoIMC = self.data_factory.pyfloat(left_digits = 2, right_digits = 2, positive = True)

        resultado = self.logica.calcular_categoria_imc(calculoIMC)
        if calculoIMC < 18.5:
            resultadoEsperado = "Bajo peso"
        elif calculoIMC <= 24.9:
            resultadoEsperado = "Peso saludable"
        elif calculoIMC <= 29.9:
            resultadoEsperado = "Sobrepeso"
        else:
            resultadoEsperado = "Obesidad"

        self.assertEqual(resultadoEsperado, resultado)
    
    def test_dar_reporte_con_imc_y_categoria_validar_tipo(self):
        '''Verificar que el reporte retorne los tipos correctos para el imc y cetegoria HU009'''
        reporte = self.logica.dar_reporte(self.persona.id)

        self.assertTrue(isinstance(reporte['estadisticas']['imc'], float))
        self.assertTrue(isinstance(reporte['estadisticas']['clasificacion'], str))

    def test_dar_reporte_con_imc_y_categoria_validar_datos_correctos(self):
        '''Verificar que el reporte retorne las estadisticas correctas para el imc y cetegoria HU009'''
        calculoIMC = self.logica.calcular_imc(self.persona.talla, self.persona.peso)
        categoria = self.logica.calcular_categoria_imc(calculoIMC)

        reporte = self.logica.dar_reporte(self.persona.id)

        self.assertEqual(calculoIMC, reporte['estadisticas']['imc'])
        self.assertEqual(categoria, reporte['estadisticas']['clasificacion'])

    def test_verificar_ejercicio_existe_en_entrenamiento_cuando_no_existe(self):
        '''Verificar que un ejercicio no esta en los entrenamientos de alguna persona, HU014'''
        idToFind = self.data_factory.random_int(1, 100)
        resultado = self.logica.verificar_ejercicio_existe_en_entrenamiento(idToFind)
        self.assertFalse(resultado)

    def test_verificar_ejercicio_existe_en_entrenamiento_cuando_existe(self):
        '''Verificar que un ejercicio esta en los entrenamientos de alguna persona, HU014'''
        ejercicio = Ejercicio(
            nombre = self.data_factory.name(),
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            caloriasQuemadasAproximadasPorRepeticion = self.data_factory.random_int(1, 300)
        )
        self.session.add(ejercicio)
        self.session.commit()
        
        detalle = DetalleEjercicio(
            ejercicio=ejercicio.id,
            entrenamiento=1,
            fechaRealizacionEjercicio=datetime.strptime(self.data_factory.date(), '%Y-%m-%d').date(),
            numeroRepeticiones=self.data_factory.random_int(1, 300),
            duracion="00:30:12"
        )
        self.session.add(detalle)
        self.session.commit()
        resultado = self.logica.verificar_ejercicio_existe_en_entrenamiento(1)
        self.assertTrue(resultado)
    
    def test_eliminar_ejercicio_cuando_el_ejercicio_no_existe(self):
        '''Eliminar un ejercicio cuando el ejericicio no existe, HU014'''
        idToFind = self.data_factory.random_int(1, 100)
        resultado = self.logica.eliminar_ejercicio(idToFind)
        self.assertFalse(resultado)
    
    def test_eliminar_ejercicio_cuando_el_ejercicio_existe_pero_no_esta_en_entrenamiento(self):
        '''Eliminar un ejercicio cuando el ejericicio existe, pero no hace parte de un entrenamiento, HU014'''
        ejercicio = Ejercicio(
            nombre = self.data_factory.name(),
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            caloriasQuemadasAproximadasPorRepeticion = self.data_factory.random_int(1, 300)
        )
        self.session.add(ejercicio)
        self.session.commit()
        resultado = self.logica.eliminar_ejercicio(1)
        ejercicios = self.session.query(Ejercicio).all()
        self.assertEqual(len(ejercicios), 0)
        self.assertTrue(resultado)
    
    def test_eliminar_ejercicio_cuando_el_ejercicio_existe_pero_esta_en_entrenamiento(self):
        '''Eliminar un ejercicio cuando el ejericicio existe y hace parte de un entrenamiento, HU014'''
        ejercicio = Ejercicio(
            nombre = self.data_factory.name(),
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            caloriasQuemadasAproximadasPorRepeticion = self.data_factory.random_int(1, 300)
        )
        self.session.add(ejercicio)
        self.session.commit()
        detalle = DetalleEjercicio(
            ejercicio=ejercicio.id,
            entrenamiento=1,
            fechaRealizacionEjercicio=datetime.strptime(self.data_factory.date(), '%Y-%m-%d').date(),
            numeroRepeticiones=self.data_factory.random_int(1, 300),
            duracion="00:30:12"
        )
        self.session.add(detalle)
        self.session.commit()
        resultado = self.logica.eliminar_ejercicio(ejercicio.id)
        ejercicios = self.session.query(Ejercicio).all()
        self.assertEqual(len(ejercicios), 1)
        self.assertFalse(resultado)

    def test_editar_ejercicio_no_repetido(self):
        '''Prueba la edicion de un ejercicio que no está repetido, HU013'''
        ejercicio = Ejercicio(
            nombre = self.data_factory.name(),
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            caloriasQuemadasAproximadasPorRepeticion = self.data_factory.random_int(1, 300)
        )
        self.session.add(ejercicio)
        self.session.commit()
        resultado = self.logica.editar_ejercicio(
            ejercicio.id,
            nombre = self.data_factory.name(),
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            calorias = self.data_factory.random_int(1, 300)
        )
        self.assertTrue(resultado)

    def test_editar_ejercicio_repetido(self):
        '''Prueba la edicion de un ejercicio repetido, HU013'''

        ejercicioEditar = Ejercicio(
            nombre = self.data_factory.name(),
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            caloriasQuemadasAproximadasPorRepeticion = self.data_factory.random_int(1, 300)
        )
        self.session.add(ejercicioEditar)
        self.session.commit()

        nombre = self.data_factory.name()
        ejercicioDiferenteAEditado = Ejercicio(
            nombre = nombre,
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            caloriasQuemadasAproximadasPorRepeticion = self.data_factory.random_int(1, 300)
        )
        self.session.add(ejercicioDiferenteAEditado)
        self.session.commit()

        resultado = self.logica.editar_ejercicio(
            ejercicioEditar.id,
            nombre = nombre,
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            calorias = self.data_factory.random_int(1, 300)
        )
        self.assertFalse(resultado)
    
    def test_editar_ejercicio_validando_persistencia(self):
        '''Prueba la persistencia en la db de un ejercicio editado, HU013'''
        nombre = self.data_factory.name()
        r = self.logica.crear_ejercicio(
            nombre = nombre,
            descripcion = self.data_factory.text(),
            urlVideo = "https://www.youtube.com",
            calorias = self.data_factory.random_int(1, 300)
        )

        ejercicioEditar = self.session.query(Ejercicio).filter(Ejercicio.nombre == nombre).first()

        nombre = self.data_factory.name()
        descripcion = self.data_factory.text()
        calorias = self.data_factory.random_int(1, 300)
        resultado = self.logica.editar_ejercicio(
            idEjercicio = ejercicioEditar.id,
            nombre = nombre,
            descripcion = descripcion,
            urlVideo = "https://www.youtube.com",
            calorias = calorias)
        
        busqueda = self.session.query(Ejercicio).filter(Ejercicio.id == ejercicioEditar.id).first()
        self.session.refresh(ejercicioEditar)
        self.assertTrue(resultado)
        self.assertEqual(nombre, busqueda.nombre)
        self.assertEqual(descripcion, busqueda.descripcion)
        self.assertEqual(calorias, busqueda.caloriasQuemadasAproximadasPorRepeticion)