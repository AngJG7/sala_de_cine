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

    def get_pelicula(self):
        return self.pelicula
    
    def get_hora(self):
        return self.hora
    
    def reservar_sillas(self, fila, silla_inicial, cantidad) -> bool:
        disponibles = True
        i = 0
        # validar que la fila dada si sea real
        if fila < 1 or fila > self.num_filas:
            return False
        # Ver que si quepan
        if silla_inicial < 1 or (silla_inicial + cantidad) > self.sillas_por_fila:
            return False
        # Ver si si están libres, no recorriendo todas sino parando cuando una es False
        while i < cantidad and disponibles == True:
            if self.sillas[fila - 1, (silla_inicial -1) + i] == True: # El ususario las va mostrar desde 1 entonces resto 1
                disponibles = False
            i += 1
        # Si esta ocupada entonces no se reserva
        if disponibles == False:
            return False
        # Si se reserva, marcarlas como ocupadas
        i = 0
        while i < cantidad:
            self.sillas[fila-1, (silla_inicial-1) + i] = True
            i += 1
        return True
        
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
        

    def calcular_ocupacion(self):#hace un recorrido por las filas y columnas de las sillas para contar cuales estan acupadas y dar el porcentaje de ocupación
         sillas_ocupadas = 0
        total_sillas = self.num_filas * self.sillas_por_fila
        
        if total_sillas == 0:
            return 0.0
            
        i = 0
        while i < self.num_filas:
            j = 0
            while j < self.sillas_por_fila:
                if self.sillas[i, j] == True:
                    sillas_ocupadas += 1
                j += 1
            i += 1
            
        return (sillas_ocupadas / total_sillas) * 100.0

class Sala:
# Se refiere a una sala del complejo, con un identificador único, valor, dimensiones, numero de filas y silla por cada fila.
# autor: Angela Jurado
# fecha: 25/04

    def __init__(self, id, val, filas, sillas):
        self.identificador = id
        self.valor_boleta = val
        self.num_filas = filas
        self.sillas_por_fila = sillas

        self.programacion = np.empty(MAX_FUNCIONES, dtype=object)
        self.cantidad_funciones = 0
    
    def agregar_funcion(self, f) -> bool:
        # verificar cupo
        if self.cantidad_funciones >= MAX_FUNCIONES:
            return False
        # verificar que no haya otra funcion a la misma hora
        i = 0
        while i < self.cantidad_funciones:
            if self.programacion[i].get_hora() == f.get_hora():
                return False
            i = i + 1
        # agregar al final
        self.programacion[self.cantidad_funciones] = f
        self.cantidad_funciones = self.cantidad_funciones + 1
        return True
    
    def eliminar_funcion(self, hora_buscar):
        # buscar la posición de la función a eliminar
        pos_funcion = -1
        i = 0
        while i < self.cantidad_funciones and pos_funcion == -1:
            if self.programacion[i].get_hora() == hora_buscar:
                pos_funcion = i
            i = i + 1
        if pos_funcion == -1:
            return False
        
        # desplazar todos los elementos desde pos funcion hacia atrás
        j = pos_funcion
        while j < self.cantidad_funciones - 1:
            self.programacion[j] = self.programacion[j + 1]
            j = j + 1

        # limpio la última posición y resto uno al contador
        self.programacion[self.cantidad_funciones - 1] = None
        self.cantidad_funciones = self.cantidad_funciones - 1
        return True
    
    def mostrar_mapa(self, hora_buscar):  # muestra el mapa de sillas de la función que está a la hora indicada
        funcion = self.buscar_funcion(hora_buscar)
        if funcion is None:
            print("No se encontró ninguna función a esa hora en esa sala!")
        else:
            funcion.mostrar_mapa()

    def calcular_recaudo(self):#hace un recorrido por las filas y columnas de las sillas vendidas y calcula el recaudo de estas
        sillas_vendidas = 0
        
        i = 0
        while i < self.num_filas:
            j = 0
            while j < self.sillas_por_fila:
                if self.sillas[i, j] == True:
                    sillas_vendidas += 1
                j += 1
            i += 1
            
        return sillas_vendidas * precio_boleta
        
    def calcular_ocupacion(self):
        None


    def buscar_funcion(self, hora_buscar): # BUSQUEDA POR HORA AGREGAR AL DIAGRAMA#  se usa dos veces entonces mejor funcion
        encontrada = None
        i = 0
        while i < self.cantidad_funciones and encontrada is None:
            if self.programacion[i].get_hora() == hora_buscar:
                encontrada = self.programacion[i]
            i += 1
        return encontrada

    def mostrar_programacion(self): # IMPRIMIR FUNCIONES DE LA SALA AGREGAR AL DIAGRAMA # se usa dos veces entonces mejor funcion
        print(f"\nSala {self.identificador} (Valor boleta: ${self.valor_boleta})")
        if self.cantidad_funciones == 0:
            print("---Sin funciones programadas")
        else:
            i = 0
            while i < self.cantidad_funciones:
                f = self.programacion[i]  # funcion concreta en el arreglo
                print(f"  - {f.get_pelicula().nombre_espanol} a las {f.get_hora()}")
                i =+ 1
   
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
    
    def buscar_sala(self, id_sala):
        encontrada = None
        i = 0
        while i < self.cantidad_salas and encontrada is None: # busqueda secuencial por id
            if self.salas[i].identificador == id_sala:
                encontrada = self.salas[i]
            i = i + 1
        return encontrada
    
    def consultar_programacion(self):
        None

    def calcular_recaudado(self):
        None

class Boleta: 
    def __init__(self, fecha, comp, sala, peli, hora, pre, cal, sillas):
        self.fecha_venta = fecha
        self.nombre_complejo = comp
        self.identificador_sala = sala
        self.nombre_pelicula = peli
        self.hora_funcion = hora
        self.precio_total = pre
        self.calificacion_pelicula = cal
        self.sillas_reservadas = sillas
    
    def mostrar_boleta(self):
        print(f'''
    ╭══════════ .✧. ══════════╮
               BOLETA
    Fecha: {self.fecha_venta}
    Complejo: {self.nombre_complejo}
    Sala: {self.identificador_sala}
    Película: {self.nombre_pelicula}
    Hora Función: {self.hora_funcion}
    Calificación: {self.calificacion_pelicula} ''')
        print(f'''
    Sillas Reservadas: ''', end='')
        i = 0
        while i < len(self.sillas_reservadas):
            print(self.sillas_reservadas[i], end=' ')
            i += 1
              
        print(f'''
    Precio Total: {self.precio_total}

    ╰══════════ .✧. ══════════╯''')
