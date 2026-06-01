from unittest import case
import numpy as np
from clases import *
import os

class AppCine:
# Clase principal que maneja todas las demás clases y se encarga del manejo con quien requiera de esas funciones
# autores: Angela, Yulisa y Sebastian
# fecha: 15/05
    def __init__(self):
        '''
        Este es el método constructor de la clase
        AUTORES: Angela y Sebastian
        PARAM: No aplica
        Return: No aplica
        '''
        self.complejo = Complejo('','')
        self.usuarios = np.empty(MAX_USUARIOS, dtype=object)
        self.peliculas = np.empty(MAX_PELICULAS, dtype=object)
        self.cant_usuarios = 0
        self.cant_peliculas = 0

        if os.path.exists("datos_complejo.npy"):
            try:
                arreglo_comp = np.load("datos_complejo.npy", allow_pickle=True)
                self.complejo = arreglo_comp[0] 
            except (OSError, IndexError, EOFError):
                self.complejo = Complejo("","")
        else:
            self.complejo = Complejo("","")
        
        self.usuarios, self.cant_usuarios = self.cargar_datos("datos_usuarios.npy", MAX_USUARIOS)

        self.peliculas, self.cant_peliculas = self.cargar_datos("datos_peliculas.npy", MAX_PELICULAS)

    def principal(self):
        '''
        FECHA: 30/05/2026
        AUTORES: Angela y Yulisa
        Este método permite la autenticación de los usuarios y su verificación de existencia en el sistema
        PARAM: No aplica
        RETURN: Un menú correspondiente al perfil del usuario registrado en caso de poder hacerse el registro
        Un mensaje que indique que no se pudo realizar el registtro
        '''
        try:
            continuar = True 
            
            while continuar == True:
                autenticado = False
                usuario_activo = None
    
                while autenticado == False:
                    self.limpiar_pantalla()
                    print(f'''
        ╭════════════ .✧. ════════════╮
          Bienvenido a la app de cines
        ╰════════════ .✧. ════════════╯''')
                    nomb_ingresado = input('Usuario: ')
                    contra_ingresada = input('Contraseña: ')
    
                    # secuencia de busqueda del usuario que se ingrese
                    i = 0
                    while i < self.cant_usuarios and autenticado == False:
                        # ══ FILTRO DE SEGURIDAD ══
                        # Verificamos que la casilla NO sea None antes de evaluar sus atributos
                        if self.usuarios[i] is not None:
                            if self.usuarios[i].nombre_usuario == nomb_ingresado:
                                if self.usuarios[i].verificar_contrasena(contra_ingresada) == True:
                                    autenticado = True
                                    usuario_activo = self.usuarios[i]
                        i += 1
                        
                    if autenticado == False:
                        print('\n.✧. Usuario o contraseña incorrectos. Intente de nuevo! ')
                
                # Mostrar menú (Alineado perfectamente con el 'while' de arriba)
                print(f'''
        ・‥…━━━☆ ¡Bienvenido {usuario_activo.nombre_usuario}!
        (Perfil: {usuario_activo.get_perfil()})''')
                
                match (usuario_activo.get_perfil()):
                    case 'administrador':
                        self.menu_administrador()
                    case 'vendedor':
                        self.menu_vendedor()
                    case 'cliente':
                        self.menu_cliente()
                  
                salir = input("\n¿Desea cerrar sesión o salir del sistema? (s/n): ")
                if salir.lower() == "s":
                    continuar = False
        except ValueError:
                print("\nERROR. Entrada de datos inválida. Se esperaba un formato diferente.")
                input("\nPresione Enter para continuar...")
                continuar = False

    def mostrar_programacion_sala(self):
        '''
        Este método permite mostrar todas las programaciones que tiene una sala
        FECHA: 29/05/2026
        AUTORES: Yulisa Otero
        PARAM: No aplica
        RETURN: La programación completa de la sala esperada en caso de encontrarla
        Un mensaje que indique que no se encontró la sala
        '''
        print("\n━━━━━━✧ Consultar programación de una sala ✧━━━━━━")
        
        cant_salas = self.complejo.cantidad_salas 
        
        if cant_salas == 0:
            print("El complejo no tiene salas registradas actualmente.")
            input("\nPresione Enter para regresar...")
            return
            
        print("\nSalas disponibles en el complejo:")
        print("─" * 45)
        s = 0
        while s < cant_salas:
            sala_disp = self.complejo.salas[s]
            print(f" • Sala ID: {sala_disp.identificador:<5} | Valor boleta: ${sala_disp.valor_boleta:,.2f}")
            s += 1
        print("─" * 45)

        id_sala_buscar = None
        while id_sala_buscar is None:
            try:
                entrada = input("\nIngrese el identificador de la sala que desea consultar: ").strip()
                if not entrada: # Si está vacío, lo ignora y vuelve a pedir
                    continue
                id_sala_buscar = int(entrada) 
            except ValueError:
                print("\nError. El identificador de la sala debe ser un número entero.")
                input("\nPresione Enter para intentar de nuevo...")
                return

        encontrada = False 
        i = 0 
        while i < cant_salas and encontrada == False:
            sala_actual:Sala
            sala_actual = self.complejo.salas[i] 
            if sala_actual.identificador == id_sala_buscar: 
                encontrada = True 
                # Solo llamamos a mostrar_programacion si encontramos la sala real elegida
                sala_actual.mostrar_programacion()
            i += 1
            
        if encontrada == False:
            print(f"\nNo se encontró ninguna sala con el identificador {id_sala_buscar}.")
        
        input("\nPresione Enter para continuar...")

    def menu_administrador(self):
        '''
        Este método es el que permite  acceder al perfil de administrador a todas sus funciones por medio de un menú
        AUTORES: Angela y Yulisa
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: No aplica
        '''
        self.limpiar_pantalla()
        opc = 0
        while opc != 12:
            print(f'''
☆゜・。。・゜Menú Administrador ゜・。。・゜★

    1) Crear nueva película
    2) Modificar estado película
    3) Crear nueva sala
    4) Consultar detalle de la película
    5) Crear usuarios
    6) Eliminar película de la programación
    7) Consultar porcentaje de ocupación
    8) Consultar recaudo de una sala
    9) Consultar recaudo del complejo
    10) Consultar programación
    11) Agregar funcion
    12) Cerrar sesión
                  ''')
            try:
                opc = int(input("Seleccione una opción: "))
                match opc:
                    case 1:
                        self.crear_pelicula()
                    case 2:
                        self.modificar_estado_pelicula()
                    case 3:
                        self.crear_sala()
                    case 4:
                        self.consultar_detalle_pelicula()
                    case 5:
                        self.crear_usuario()
                    case 6:
                        self.eliminar_pelicula_programacion()
                    case 7:
                        self.consultar_porcentaje_ocupacion()
                    case 8:
                        self.consultar_recaudo_sala()
                    case 9:
                        self.consultar_recaudo_complejo()
                    case 10:
                        print(f'''
☆゜・。。・゜Programación ゜・。。・゜★
                      
    1) Consultar programación completa del complejo
    2) Consultar programación por película
    3) Consultar programación  por Sala
    4) Cerrar sesión
                  ''')
                        opc=0
                        opc2 = int(input("Seleccione una opción: "))
                        match(opc2):
                            case 1:
                                self.complejo.mostrar_programacion()
                            case 2:
                                self.mostrar_programacion_pelicula()
                            case 3:
                                self.mostrar_programacion_sala()
                    case 11:
                        self.agregar_funcion()
                    case 12:
                        print("Sesión cerrada. Hasta luego!")
                    case _:
                        print("Opción no válida")
            except ValueError:
                print("\nError. Se esperaba un número entero.")
                input("\nPresione Enter para continuar...")
 
    def menu_vendedor(self):
        '''
        Este método es el que permite  acceder al perfil de vendedor a todas sus funciones por medio de un menú
        AUTORES: Angela y Yulisa
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: No aplica
        '''
        self.limpiar_pantalla()
        opc = 0
        while opc != 5:
            print(f'''
☆゜・。。・゜Menú Vendedor ゜・。。・゜★
                      
    1) Crear un nuevo usuario
    2) Reservar boletas
    3) Consultar detalle de una película 
    4) Consultar programación
    5) Cerrar Sesión
                  ''')
            try:
                opc = int(input("Seleccione una opción: "))
     
                match opc:
                    case 1:
                        self.crear_usuario()
                    case 2:
                        self.reservar_boletas()
                    case 3:
                        self.consultar_detalle_pelicula()
                    case 4:
                        print(f'''
☆゜・。。・゜Programación ゜・。。・゜★
                      
    1) Consultar programación completa del complejo
    2) Consultar programación por película
    3) Consultar programación  por Sala
    4) Cerrar sesión
                  ''')
                        opc2 = int(input("Seleccione una opción: "))
                        match(opc2):
                            case 1:
                                self.complejo.mostrar_programacion()
                            case 2:
                                self.mostrar_programacion_pelicula()
                            case 3:
                               self.mostrar_programacion_sala()
                        print("Sesión cerrada. Hasta luego!")
                    case _:
                        print("Opción no válida")
            except (EOFError, KeyboardInterrupt):
                print("\n\n[INFO]: Se interrumpió la lectura de datos por consola.")
                input("\nPresione Enter para regresar al menú...")

    def menu_cliente(self):
        '''
        Este método es el que permite  acceder al perfil de cliente a todas sus funciones por medio de un menú
        AUTORES: Angela y Yulisa
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: No aplica
        '''
        self.limpiar_pantalla()
        opc = 0
        opc2=0
        while opc != 3:
            print(f'''
☆゜・。。・゜Menú Cliente ゜・。。・゜★
                      
    1) Reservar boletas
    2) Consultar detalles de una película
    3) Consultar programación 
    4) Cerrar sesión
                  ''')
            opc = int(input("Seleccione una opción: "))
 
            match opc:
                case 1:
                    self.reservar_boletas()
                case 2:
                    self.consultar_detalle_pelicula()
                case 3:
                    while opc2 != 3:
                        print(f'''
☆゜・。。・゜Programación ゜・。。・゜★
                      
    1) Consultar programación completa del complejo
    2) Consultar programación por película
    3) Consultar programación  por Sala
    4) Cerrar sesión
                  ''')
                        opc2 = int(input("Seleccione una opción: "))
                        match(opc2):
                            case 1:
                                self.complejo.mostrar_programacion()
                            case 2:
                                self.mostrar_programacion_pelicula()
                            case 3:
                                self.mostrar_programacion_sala()
                                
                case 4:
                    print("Sesión cerrada. Hasta luego!")
                case _:
                    print("Opción no válida")

    def crear_usuario(self):
        '''
        Este método permite el registro de usuarios de cualquiera de los 3 perfiles en el sistema
        AUTORES: Angela
        FECHA: 5/05/2026
        PARAM: No aplica
        RETURN: Un mensaje que indicando que se registró el usuario de manera exitosa
        Un mensaje que indique que no se pudo registrar el usuario
        '''
        print("\n━━━━━━✧ Crear nuevo usuario ✧━━━━━━")
        valido = True
        ya_existe = False
        perfil_texto = ""
 
        nuevo_nomb = input("Nombre de usuario: ")
        nueva_contra = input("Contraseña: ")
        nuevo_perfil = int(input("Perfil (1=cliente, 2=vendedor, 3=administrador): "))
 
        #Validar que los campos no esten vacios
        if nuevo_nomb == "" or nueva_contra == "":
            valido = False
            print("Error: el nombre y la contraseña no pueden estar vacíos")
 
        # convertir nro a cadena
        match nuevo_perfil:
            case 1:
                perfil_texto = "cliente"
            case 2:
                perfil_texto = "vendedor"
            case 3:
                perfil_texto = "administrador"
            case _:
                valido = False
                print("Error: perfil no válido")
 
        # verificar nombre usuario que no exista ya
        i = 0
        while i < self.cant_usuarios and ya_existe == False:
            if self.usuarios[i].nombre_usuario == nuevo_nomb:
                ya_existe = True
                print("Ya existe un usuario con ese nombre!")
            i = i + 1
 
        # verificar cupo
        if self.cant_usuarios >= MAX_USUARIOS:
            valido = False
            print("Error: se alcanzó el máximo de usuarios!!")
 
        # con todas las validaciones entonces se crea el usuario
        if valido == True and ya_existe == False:
            self.usuarios[self.cant_usuarios] = Usuario(nuevo_nomb, nueva_contra, perfil_texto)
            self.cant_usuarios = self.cant_usuarios + 1
            print("Usuario creado exitosamente!!! :)")
        input("\nPresione Enter para continuar...")
        self.guardar_todo()

        self.menu_externo() # volver al menu externo para que el nuevo usuario pueda autenticarse
            

    def crear_pelicula(self):
        '''
        Este método permite el registro de películas en el sistema
        AUTORES: Angela
        FECHA: 5/05/2026
        PARAM: No aplica
        RETURN: Un mensaje que indique que se registró exitosamente en el sistema en caso de hacerlo.
        Un mensaje que indique que no se pudo registrar la película
        '''
        print("\n━━━━━━✧ Crear nueva película ✧━━━━━━")
        try:
            valido = True
            ne = input("Nombre en español: ")
            no = input("Nombre original: ")
            anio = int(input("Año de estreno: "))
            dur = int(input("Duración (min): "))
            gen = input("Género (drama/suspenso/terror/acción/comedia/infantil): ")
            pais = input("País de origen: ")
            cal = input("Calificación: ")
        except ValueError:
            print("\nERROR. Se esperaba un número entero. Intente de nuevo.")
 
        # validar campos no esten vacios
        if ne == "" or no == "" or pais == "":
            valido = False
            print("Error: el nombre y el país no pueden estar vacíos")
 
        # año y duracion sean positivos 
        if anio <= 0 or dur <= 0:
            valido = False
            print("Error: el año y la duración deben ser mayores a 0")
 
        # el genero sea valido
        if (gen != "drama" and gen != "suspenso" and gen != "terror" and
            gen != "acción" and gen != "comedia" and gen != "infantil"):
            valido = False
            print("Error: género no válido.")
 
        # verificar cupo
        if self.cant_peliculas >= MAX_PELICULAS:
            valido = False
            print("Error: se alcanzó el máximo de películas")
 
        # si pasa todas las anteriores se crea
        if valido == True:
            self.peliculas[self.cant_peliculas] = Pelicula(ne, no, anio, dur, gen, pais, cal)
            self.cant_peliculas = self.cant_peliculas + 1
            print("Película creada exitosamente!")
        input("\nPresione Enter para continuar...")
        self.guardar_todo()

    def consultar_detalle_pelicula(self):
        '''
        Este método muestra los datos de una película en específico.
        AUTOR: Angela Jurado
        FECHA: 24/04
        PARAM: No aplica.
        RETURN: No aplica.
        '''
        print("\n━━━━━━✧ Consultar detalle de película ✧━━━━━━")
        encontrada = False
        nombre_buscar = input("Nombre en español de la película: ")
 
        # buscar peli
        i = 0
        while i < self.cant_peliculas and encontrada == False:
            if self.peliculas[i].nombre_espanol == nombre_buscar:
                encontrada = True
                print("")
                self.peliculas[i].mostrar_detalles()
            i = i + 1
 
        if encontrada == False:
            print("No se encontró ninguna película con ese nombre")
        input("\nPresione Enter para continuar...")

    def crear_sala(self):
        '''
        Este método permite la creación de salas en el complejo.
        AUTOR: Angela Jurado
        FECHA: 24/04
        PARAM: No aplica.
        RETURN: Un mensaje indicando que secreó exitosamente la sala en el sistema.
        Un mensaje que indique que no se pudo crear la salao que esta ya existe.
        '''
        print("\n━━━━━━✧ Crear nueva sala ✧━━━━━━")
        valido = True
        id_sala = int(input("Identificador de la sala: "))
        val_boleta = float(input("Valor de la boleta: "))
        filas = int(input("Número de filas: "))
        sillas = int(input("Sillas por fila: "))

        # que id sea positivo
        if id_sala <= 0:
            valido = False
            print("Error: el identificador debe ser mayor a 0.")

        # que los valores sean positivos
        if val_boleta <= 0 or filas <= 0 or sillas <= 0:
            valido = False
            print("Error: el valor, las filas y las sillas deben ser mayores a 0.")

        # crearla o no dependiendo si se pasa de la cantidad limite
        if valido == True:
            nueva_sala = Sala(id_sala, val_boleta, filas, sillas)
            if self.complejo.agregar_sala(nueva_sala) == True:
                print("Sala creada exitosamente!")
            else:
                print("El complejo ya tiene el máximo de salas permitidas (12).")

        input("\nPresione Enter para continuar...")
        self.guardar_todo()
    
    def reservar_boletas(self):
        '''
        Este método permite la reservación de boletas disponibles en el sistema
        AUTORES: Angela
        FECHA: 5/05/2026
        PARAM: No aplica
        RETURN: Un mensaje que indique que se realizó la reserva de manera exitosa
        Un mensaje que indique que no se pudo realizar la reserva
        '''
        print(f'''
━━━━━━✧  Reservar boletas ✧━━━━━━''')
        id_sala_buscar = int(input('Ingresa el identificador de la sala:')) # Buscar por id
        sala_selecc = self.complejo.buscar_sala(id_sala_buscar)
        if sala_selecc is None:
            print(f'No se ha encontrado ninguna sala con el id {id_sala_buscar}')
            return
        
        hora_buscar = input('Hora de la función: ') # Buscar por funcion
        funcion_selecc = sala_selecc.buscar_funcion(hora_buscar)
        if funcion_selecc is None:
            print(f'No se ha encontrado ninguna función a la hora {hora_buscar}')
            return
        
        funcion_selecc.mostrar_mapa()
        
        try:
            cant_boletas = int(input('Ingrese la cantidad de boletas que desea comprar: '))
            fila = int(input('Escoja la fila: '))
            silla_inicial = int(input('Escoja la silla inicial: '))
        except ValueError:
            print("\nERROR. Se esperaba un número entero. Intente de nuevo.")

        # validar la cantidad
        if cant_boletas < 1:
            print('Error: se debe reservar al menos una boleta!')
            return
        # reserva con datos dados 
        reserva = funcion_selecc.reservar_sillas(fila, silla_inicial, cant_boletas)
        if reserva == False:
            print('La reserva no fue posible. Verifique si la fila es invalida, las sillas no caben o están ocupadas')
            return
        
        # si si se reserva, se construye el arreglo
        sillas_reservadas = np.empty(cant_boletas, dtype=object)
        i = 0
        while i < cant_boletas:
            sillas_reservadas[i] = f'F{fila}-S{silla_inicial+i}'  # dar una mini codigo para identificar facilmente la posicion de cada silla
            i += 1
        
        # calcular precio total
        precio_total = cant_boletas * sala_selecc.valor_boleta
        fecha = input('Fecha de la venta (dd/mm/aaaa): ')

        boleta = Boleta(fecha, self.complejo.nombre, sala_selecc.identificador, funcion_selecc.get_pelicula().nombre_espanol, funcion_selecc.get_hora(), precio_total, funcion_selecc.get_pelicula().calificacion, sillas_reservadas)
        boleta.mostrar_boleta()
        input("\nPresione Enter para continuar...")
        self.guardar_todo()
        
    def modificar_estado_pelicula(self):
        '''
        Este método le permite al administrador editar el estado en el que se encuentra una película indicando si hay funciones habilitadas o no 
        AUTORES: Sebastian Murillo
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: Un mensaje que indique que no hay peliculas en caso de no encontrar ninguna registrada.
        Un mensaje que indique que el cambio de estado fue exitoso  en caso de hacerlo.
        Un mensaje que indique que no se pudo realizar el cambio de estado.
        '''
        print("\n━━━━━━✧ Modificar estado de una película ✧━━━━━━")
        #se verifica si hay peliculas registradas
        if self.cant_peliculas == 0:
            print("No hay películas registradas en el sistema.")
            input("\nPresione Enter para continuar...")
            return

        nombre_buscar = input("Nombre en español de la película a modificar: ")
        
        encontrada = False
        posi_pelicula = -1
        i = 0
        #se recorre el arreglo para buscar la pelicula
        while i < self.cant_peliculas and encontrada == False:
            if self.peliculas[i].nombre_espanol.lower() == nombre_buscar.lower():
                encontrada = True
                posi_pelicula = i
            i += 1
            
        if encontrada == False:
            print("No se encontró ninguna película con ese nombre.")
            input("\nPresione Enter para continuar...")
            return
        #se cambia el estaod en el que este
        pelicula_seleccionada = self.peliculas[posi_pelicula]
        estado_actual_bool = pelicula_seleccionada.get_activa()
        estado_actual_texto = "Activa" if estado_actual_bool else "Inactiva"
        
        print(f"\nPelícula encontrada: {pelicula_seleccionada.nombre_espanol}")
        print(f"Estado actual: {estado_actual_texto}")
        
        try:
            print("\nSeleccione el nuevo estado:")
            print("1 = Activa")
            print("2 = Inactiva")
            nuevo_estado = int(input("Opción: "))
            
            if nuevo_estado == 1:
                if estado_actual_bool == True:
                    print("La película ya se encuentra en estado Activa. No se realizaron cambios.")
                else:
                    pelicula_seleccionada.set_activo(True)
                    print("Película marcada como Activa.")
            #se verifica que no se cambie el estado al mismo     
            elif nuevo_estado == 2:
                if estado_actual_bool == False:
                    print("La película ya se encuentra en estado Inactiva. No se realizaron cambios.")
                else:
                    tiene_funciones = False
                    j = 0
                    while j < self.complejo.cantidad_salas and tiene_funciones == False:
                        sala_actual = self.complejo.salas[j]
                        f = 0
                        while f < sala_actual.cantidad_funciones and tiene_funciones == False:
                            if sala_actual.programacion[f].get_pelicula().nombre_espanol == pelicula_seleccionada.nombre_espanol:
                                tiene_funciones = True
                            f += 1
                        j += 1
                    
                    if tiene_funciones == True:
                        print("Error. No se puede inactivar la película porque actualmente tiene funciones en cartelera")
                    else:
                        pelicula_seleccionada.set_activo(False)
                        print("Película marcada como Inactiva.")
            else:
                print("Error, debe seleccionar 1 o 2.")
                
        except ValueError:
            print("\nError. Se esperaba un número entero. Volviendo al menú principal sin realizar cambios.")
            
        input("\nPresione Enter para regresar al menú...")
        self.guardar_todo()

    def eliminar_pelicula_programacion(self):
        '''
        Este método permite la eliminación de películas de la programación del complejo
        AUTORES: Sebastian Murillo
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: Un mensaje que indique que que no se encontró la película si no está dentro de la programación.
        Un mensaje que indique que la película se eliminó correctamente.
        Un mensaje que indique que no se pudo eliminar la película.
        '''
        print("\n━━━━━━✧ Eliminar película de la programación ✧━━━━━━")
        
        try:
            id_sala_buscar = int(input("Identificador de la sala: "))
            #se busca la pelicula que se quiere eliminar
            sala_encontrada = self.complejo.buscar_sala(id_sala_buscar)
            if sala_encontrada == None:
                print(f"Error. No se encontró ninguna sala con el ID {id_sala_buscar}")
                input("\nPresione Enter para continuar...")
                return
                
            hora_buscar = input("Hora de la función a eliminar: ")
            
            funcion_encontrada = sala_encontrada.buscar_funcion(hora_buscar)
            if funcion_encontrada == None:
                print(f"Error. No se encontró ninguna función a las {hora_buscar} en la Sala {id_sala_buscar}")
                input("\nPresione Enter para continuar...")
                return
              #se llama el metodo de otra clase para elimanr la funcion  
            if sala_encontrada.eliminar_funcion(hora_buscar) == True:
                print("Función eliminada exitosamente.")
            else:
                print("Error. No se pudo eliminar la función.")
                
        except ValueError:
            print("\nError. El identificador de la sala debe ser un número entero.")
            
        input("\nPresione Enter para regresar al menú...")
        self.guardar_todo()


    def consultar_porcentaje_ocupacion(self):
        '''
        Este método le permite al administrador ver qué tan ocupada está una sala en una función definida
        AUTORES: Sebastian Murillo
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: Un mensaje que indique que no hay funciones disponibles para generar el reporte.
        Un mensaje que indique con los reportes del porcentaje de ocupación de la sala.
        '''
        print("\n━━━━━━✧ Porcentaje de Ocupación por Película ✧━━━━━━")
        
        max_registros = MAX_SALAS * MAX_FUNCIONES
        #se declaran los sigeunte arreglos 
        peliculas_ocup = np.empty(max_registros, dtype=object)
        salas_ocup = np.empty(max_registros, dtype=int)
        horas_ocup = np.empty(max_registros, dtype=object)
        porcentajes = np.zeros(max_registros, dtype=float)
        
        cant_registros = 0
        
        i = 0
        while i < self.complejo.cantidad_salas:
            sala_actual = self.complejo.salas[i]
            
            j = 0
            while j < sala_actual.cantidad_funciones:
                func_actual = sala_actual.programacion[j]
                
                peliculas_ocup[cant_registros] = func_actual.get_pelicula().nombre_espanol
                salas_ocup[cant_registros] = sala_actual.identificador
                horas_ocup[cant_registros] = func_actual.get_hora()
                porcentajes[cant_registros] = func_actual.calcular_ocupacion()
                #se llaman a los siguente metodos
                cant_registros += 1
                j += 1
            i += 1
            
        if cant_registros == 0:
            print("No hay funciones programadas en ninguna sala para generar el reporte.")
            input("\nPresione Enter para regresar al menú...")
            return
            
        i = 0
        while i < cant_registros - 1:
            p = i
            j = i + 1
            while j < cant_registros:
                if porcentajes[j] > porcentajes[p]:
                    p = j
                j += 1
                
            if p != i:
                aux_porc = porcentajes[i]
                porcentajes[i] = porcentajes[p]
                porcentajes[p] = aux_porc
                
                aux_peli = peliculas_ocup[i]
                peliculas_ocup[i] = peliculas_ocup[p]
                peliculas_ocup[p] = aux_peli
                
                aux_sala = salas_ocup[i]
                salas_ocup[i] = salas_ocup[p]
                salas_ocup[p] = aux_sala
                
                aux_hora = horas_ocup[i]
                horas_ocup[i] = horas_ocup[p]
                horas_ocup[p] = aux_hora
                #se ordenan los arreglos ya que son paralelos
            i += 1
            
        print(f"\n{"PELÍCULA":<25} {"SALA":<8} {"HORA":<10} {"OCUPACIÓN"}")
        print("=" * 55)
        
        i = 0
        while i < cant_registros:
            print(f"{peliculas_ocup[i]:<25} {salas_ocup[i]:<8} {horas_ocup[i]:<10} {porcentajes[i]:.2f}%")
            i += 1
            
        input("\nPresione Enter para regresar al menú...")

    def consultar_recaudo_sala(self):
        '''
        Este método permite calcular el porcentaje  recaudado por sala
        AUTORES: Sebastian Murillo
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: Un mensaje que indique que no se encontró la sala buscada.
        Un mensaje con el total recaudado si la sala sí se encontró.
        '''
        print("\n━━━━━━✧ Consultar recaudo de una sala ✧━━━━━━")
        
        try:
            id_sala_buscar = int(input("Identificador de la sala: "))
            #se busca la sala
            sala_encontrada = self.complejo.buscar_sala(id_sala_buscar)
            if sala_encontrada == None:
                print(f"No se encontró ninguna sala con ese identificador.")
                input("\nPresione Enter para continuar...")
                return
                
            total_recaudo = sala_encontrada.calcular_recaudo()
            #se llama al metodo para calcular el recaudo
            print(f"\nResumen de Recaudo - Sala {id_sala_buscar}:")
            print(f"Total recaudado: ${total_recaudo:,.2f}")
            
        except ValueError:
            print("\nError. El identificador de la sala debe ser un número entero.")
            
        input("\nPresione Enter para regresar al menú...")  


    def consultar_recaudo_complejo(self):
        '''
        Este método permite consultar el recaudo total de todas las salas del complejo
        AUTORES: Sebastian Murillo
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: Un mensaje que indique que no hay salas registradas y por  ende no se puede calcular el recaudo
        Un mensaje que indique la suma del recaudo de todas las salas del complejo
        '''
        print("\n━━━━━━✧ Consultar recaudo del complejo ✧━━━━━━")
        
        if self.complejo.cantidad_salas == 0:
            print("No hay salas registradas en el complejo para calcular el recaudo.")
            input("\nPresione Enter para regresar al menú...")
            return
            #se verifica que haya salas activas 
        print(f"\nDESGLOSE DE RECAUDO POR SALA:")
        print("─" * 45)
        
        i = 0
        while i < self.complejo.cantidad_salas:
            sala_actual = self.complejo.salas[i]
            recaudo_sala = sala_actual.calcular_recaudo()
            print(f"Sala {sala_actual.identificador:<5} | Recaudo: ${recaudo_sala:,.2f}")
            i += 1
            #se calcula el recaudo total del complejo llamando el metodo de la clase Complejo
        total_general = self.complejo.calcular_recaudado()
        
        print("─" * 45)
        print(f"TOTAL GENERAL DEL COMPLEJO: ${total_general:,.2f}")
            
        input("\nPresione Enter para regresar al menú...")
        
    def mostrar_programacion_pelicula(self):
        '''
        Este método permite mostrar todas las programaciones que tiene una película
        AUTORES: Yulisa Otero
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: Un mensaje que indique que no hay películas registradas en el sistema
        La programación de la película en caso de encontrarla en el sistema
        '''
        print("\n━━━━━━✧ Consultar horarios de una película ✧━━━━━━")
        
        # Validación inicial: verificar si hay películas en el sistema
        try:
            if self.cant_peliculas == 0:
                print("No hay películas registradas en el sistema actualmente.")
                input("\nPresione Enter para regresar...")
                return
                
            # Mostrar todas las películas disponibles antes de elegir
            print("\nPelículas registradas en el sistema:")
            print("─" * 45)
            p = 0
            while p < self.cant_peliculas:
                # Mostramos el nombre y si está activa o no
                estado = "Activa" if self.peliculas[p].get_activa() else "Inactiva"
                print(f" • {self.peliculas[p].nombre_espanol:<30} ({estado})")
                p += 1
            print("─" * 45)
    
            nombre_buscar = input("\nIngrese el nombre en español de la película que desea buscar: ") 
            
            # Validar entrada vacía
            if nombre_buscar.strip() == "":
                print("Error: El nombre de la película no puede estar vacío.")
                input("\nPresione Enter para regresar...")
                return
    
            encontrada = False
            cant_salas = self.complejo.cantidad_salas 
            
            i = 0 
            while i < cant_salas: 
                sala_actual = self.complejo.salas[i] 
                
                j = 0 
                while j < sala_actual.cantidad_funciones: 
                    funcion = sala_actual.programacion[j] 
                    
                    # Comparamos ignorando mayúsculas/minúsculas para mejorar la experiencia del usuario
                    if funcion.get_pelicula().nombre_espanol.lower() == nombre_buscar.lower(): 
                        if encontrada == False:
                            print(f"\n=====================================================")
                            print(f" Horarios y funciones disponibles para:")
                            print(f" '{funcion.get_pelicula().nombre_espanol}'")
                            print(f"=====================================================")
                            print(f"   {'SALA':<10} | {'HORA'}")
                            print(f"   {'─'*10}─┼─{'─'*10}")
                        
                        # alinea el identificador de la sala de forma uniforme
                        print(f"   • Sala {sala_actual.identificador:<5} | {funcion.get_hora()}")
                        encontrada = True
                    j += 1
                i += 1
                
            if encontrada == False:
                print(f"\nLa película '{nombre_buscar}' no se encuentra programada en ninguna sala actual.")

            input("\nPresione Enter para continuar...")

        except Exception as e:
            print(f"\nError inesperado: {e}")
            input("\nPresione Enter para continuar...")

    def menu_externo(self) -> None:
            '''
            Este es el menú principal y permite que los usuarios se autentiquen en el sistema.
            AUTORES: Yulisa Otero
            FECHA: 5/05/2026
            PARAM: No aplica
            RETURN: No aplica
            '''
            self.limpiar_pantalla()
            try:
                x:int
                x=0
                x=int(input("\n━━━━━━✧ Autentica tu usuario ✧━━━━━━ \n\n1. Iniciar Sesión \n\n2. Registrarse \n\n3. Salir \n"))
                match (x):
                    case 1: 
                        if self.cant_usuarios == 0:
                            print("\n[SISTEMA]: No hay usuarios en la base de datos.")
                            self.menu_externo()
                        else:
                            self.principal()
                    case 2:
                        self.crear_usuario()
                    case 3:
                        print("Gracias por usar la app de cines. Hasta luego!")
                    case _:
                        print("Opción no válida")
            except (EOFError, KeyboardInterrupt):
                print("\n Se interrumpió la lectura de datos por consola.")
                input("\nPresione Enter para regresar al menú...")

    def cargar_datos(self, archivo: str, num_max_datos: int) -> tuple[np.ndarray, int]:
        '''
        Este método permite la creación de los archivos para que el programa no inicie desde cero cada vez que se ejecute.
        AUTORES: Sebastian Murillo
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: No aplica
        '''
        try:
            if os.path.exists(archivo):
                arreglo_de_datos = np.load(archivo, allow_pickle=True)
                tam_arreglo = len(arreglo_de_datos)
                i = 0
                while i < tam_arreglo and arreglo_de_datos[i] != None:
                    i += 1
                return arreglo_de_datos, i
            else:
                return np.full((num_max_datos), fill_value=None, dtype=object), 0
        except (FileNotFoundError, EOFError, IndexError, OSError):
            return np.full((num_max_datos), fill_value=None, dtype=object), 0

    def guardar_datos(self, arreglo_de_datos: np.ndarray, archivo: str) -> bool:
        '''
        Este método guarda los datos de los archivos ya creados para que el programa no inicie desde cero cada vez que se ejecute.
        AUTORES: Sebastian Murillo
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: No aplica
        '''
        try:
            np.save(archivo, arreglo_de_datos, allow_pickle=True)
            return True 
        except OSError:
            print(f"Error: No se pudo escribir en el archivo {archivo}.")
            return False

    def guardar_todo(self) -> None:
        '''
        Este método guarda los datos de todos los archivos ya creados para que el programa no inicie desde cero cada vez que se ejecute.
        AUTORES: Sebastian Murillo
        FECHA: 30/05/2026
        PARAM: No aplica
        RETURN: No aplica
        '''
        """ Centraliza el guardado utilizando los strings fijos de los archivos """
        print("\nGuardando datos del sistema...")
        
        self.guardar_datos(self.usuarios, "datos_usuarios.npy")
        
        self.guardar_datos(self.peliculas, "datos_peliculas.npy")
        
        self.guardar_datos(np.array([self.complejo], dtype=object), "datos_complejo.npy")
        
        print("Datos guardados correctamente.")
    def limpiar_pantalla(self) -> None:
        '''
        Este método limpia la pantalla después de ejecutado el programa.
        AUTOR: Sebastian Murillo
        FECHA: 31/05
        PARAM: No aplica.
        RETURN: No aplica.
        '''
        """ Limpia la consola de comandos según el sistema operativo """
        try:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        except OSError:   
            pass

    def agregar_funcion(self):
        print("\n━━━━━━✧ Agregar función a programación ✧━━━━━━")

        # verificar validez del input
        try:
            id_sala_buscar = int(input("Identificador de la sala: "))
        except ValueError:
            print("\nError. El identificador de la sala debe ser un número entero.")
            input("\nPresione Enter para regresar al menú...")
            return

        sala_seleccionada = self.complejo.buscar_sala(id_sala_buscar)
        if sala_seleccionada is None:
            print("No se encontró ninguna sala con ese identificador.")
            input("\nPresione Enter para regresar al menú...")
            return

        # verificar que la sala no tenga ya 5 funciones
        if sala_seleccionada.cantidad_funciones >= MAX_FUNCIONES:
            print("La sala ya tiene el máximo de funciones programadas (5).")
            input("\nPresione Enter para regresar al menú...")
            return

        # buscar la película
        nombre_buscar = input("Nombre en español de la película: ")
        pelicula_seleccionada = None
        i = 0
        while i < self.cant_peliculas and pelicula_seleccionada is None:
            if self.peliculas[i].nombre_espanol == nombre_buscar:
                pelicula_seleccionada = self.peliculas[i]
            i = i + 1

        if pelicula_seleccionada is None:
            print("No se encontró ninguna película con ese nombre.")
            input("\nPresione Enter para regresar al menú...")
            return
        if pelicula_seleccionada.get_activa() == False:
            print("La película está inactiva, no se puede programar.")
            input("\nPresione Enter para regresar al menú...")
            return

        hora = input("Hora de la función (00:00): ")

        # crear la función con las dimensiones de la sala y agregarla
        nueva_funcion = Funcion(pelicula_seleccionada, hora,
                                sala_seleccionada.num_filas,
                                sala_seleccionada.sillas_por_fila)
        exito = sala_seleccionada.agregar_funcion(nueva_funcion)
        if exito == True:
            print("Función agregada exitosamente!")
            self.guardar_todo()
        else:
            print("Error: ya existe una función a esa hora en la sala.")

        input("\nPresione Enter para regresar al menú...")

        
    
app = AppCine()
app.menu_externo()
