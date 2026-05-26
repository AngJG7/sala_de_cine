import numpy as np

MAX_USUARIOS = 20
MAX_PELICULAS = 20
MAX_SALAS = 12
MAX_FUNCIONES = 5

class Usuario:
# representa a un usuario del sistema con un perfil asignado (cliente, vendedor o administrador), cada perfil tiene acceso a un menu diferente
# autor: samuel arcila
# fecha: 23/04

    def __init__(self, nombre_usuario, contrasena, perfil):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.perfil = perfil
    
    def verificar_contrasena(self, c) -> bool:
        return self.contrasena == c
    
    def get_perfil(self) -> str:
        return self.perfil

class Pelicula:
# representa una película del catálogo con todos sus datos. Una película puede estar activa (puede ser programada) o inactiva (no programable)
# autor: samuel arcila
# fecha: 23/04
    def __init__(self, ne, no, anio, dur, gen, pais, cal):
        self.nombre_espanol = ne
        self.nombre_original = no
        self.anio_estreno = anio
        self.duracion_min = dur
        self.genero = gen
        self.pais_origen = pais
        self.calificacion = cal

        self.activa = True
            
    def get_activa(self) -> bool:
        return self.activa
    
    def set_activo(self, activa) ->  bool:
        self.activa = activa
    
    def mostrar_detalles(self):
        estado = ""
        if self.activa == True:
            estado = "Activa"
        else:
            estado = "Inactiva"
    
        print(f'''
Nombre:             {self.nombre_espanol}
Original:           {self.nombre_original}
Año estreno:        {str(self.anio_estreno)}
Duración:           {str(self.duracion_min)} minutos
Género:             {self.genero}
País origen:        {self.pais_origen}
Calificación:       {self.calificacion}
Estado:             {estado}''')

class Funcion:
# representa la proyección de una película a una hora específica en una sala
# autor: samuel arcila
# fecha: 25/04

    def __init__(self, pelicula, hora, num_filas, sillas_por_fila):
        self.pelicula = pelicula
        self.hora = hora
        self.num_filas = num_filas
        self.sillas_por_fila = sillas_por_fila
        self.sillas = np.zeros((num_filas, sillas_por_fila), dtype=bool)
    
    def mostrar_mapa(self):
        print(f'''
━━━━━━✧ Mapa de Sillas ✧━━━━━━
Pelicula: {self.pelicula}
Hora: {self.hora}

      ━━━━━━ PANTALLA ━━━━━━
              ''')
        i = 0
        # ciclo while para mostrar numero de columnas
        while i < self.sillas_por_fila:
            print(f'{i+1:3d} ', end='')
            i = i+1
        print('')
        # nro filas
        f = 0
        while f < self.num_filas:
            print(f'F{f+1:2d} ', end='') #Marcar el inicio de fila#
            i = 0
            while i < self.sillas_por_fila: #recorre las sillas de las filas#
                if self.sillas[f, i] == True: # se decide si esta ocupada o no#
                    print('  X', end='')
                else:
                    print('  _', end='')
                i += 1
            print('')
            f += 1
        print('X = OCUPADA, _= LIBRE')

    def get_pelicula(self):
        None
    def reservar_sillas(self):
        None

class Sala:
# Se refiere a una sala del complejo, con un identificador único, valor, dimensiones, numero de filas y silla por cada fila.
# autor: Angela Jurado
# fecha: 25/04

    def __init__(self, identificador, valor_boleta, num_filas, silla_por_fila):
        self.identificador = identificador
        self.valor_boleta = valor_boleta
        self.num_filas = num_filas
        self.silla_por_fila = silla_por_fila

        self.programacion = np.empty(MAX_FUNCIONES, dtype=object)
        self.cantidad_funciones = 0

   
class Complejo:
# Contiene el arreglo de salas y se refiere al complejo que le pertenece a la empresa
# autor: Angela Jurado
# fecha: 29/04
    def __init__(self, nombre, direccion):
        self.nombre = nombre
        self.direccion = direccion
        self.salas = np.empty(MAX_SALAS, dtype=object)
        self.cantidad_salas = 0
 
    def agregar_sala(self, s):
        if self.cantidad_salas >= MAX_SALAS:
            return False
 
        self.salas[self.cantidad_salas] = s
        self.cantidad_salas = self.cantidad_salas + 1
        return True

class Boleta: 
    def __init__(self, fecha, comp, sala, peli, hora, pre, cal):
        self.fecha_venta = fecha
        self.nombre_complejo = comp
        self.identificador_sala = sala
        self.nombre_pelicula = peli
        self.hora_funcion = hora
        self.precio_total = pre
        self.calificacion_pelicula = cal
        self.sillas_reservadas = np.array([])
    
    def mostrar_boleta(self):
        print(f'''
    ╭══════════ .✧. ══════════╮
               BOLETA
    Fecha: {self.fecha_venta}
    Complejo: {self.nombre_complejo}
    Sala: {self.identificador_sala}
    Película: {self.nombre_pelicula}
    Hora Función: {self.hora_funcion}
    Calificación: {self.calificacion_pelicula}
    Sillas Reservadas: {self.sillas_reservadas}
    Precio Total: {self.precio_total}
              
    ╰══════════ .✧. ══════════╯''')