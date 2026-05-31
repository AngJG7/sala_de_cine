from clases import *

#REQUERIMIENTOS IMPLEMENTADOS:
#R6- Consultar el detalle de una película
#R7- Crear un nuevo usuario en el sistema
#R8- Crear una nueva película
#R10- Crear una nueva sala de cine
#R16- Autenticar usuario y mostrar menú según perfil


class AppCine:
# Clase principal que maneja todas las demás clases y se encarga del manejo con quien requiera de esas funciones
# autores: Angela Y Samuel
# fecha: 29/04
    def __init__(self):
        self.complejo = Complejo('','')
        self.usuarios = np.empty(MAX_USUARIOS, dtype=object)
        self.peliculas = np.empty(MAX_PELICULAS, dtype=object)
        self.cant_usuarios = 0
        self.cant_peliculas = 0


        
        #Datos de ejemplo para iniciar

        self.usuarios[0] = Usuario("admin1", "1234", "administrador")
        self.usuarios[1] = Usuario("vende1", "1234", "vendedor")
        self.usuarios[2] = Usuario("cliente1", "1234", "cliente")
        self.cant_usuarios = 3
 
        self.peliculas[0] = Pelicula("El Padrino", "The Godfather", 1972, 175, "drama", "Estados Unidos", "+18")
        self.peliculas[1] = Pelicula("Intensamente 2", "Inside Out 2", 2024, 96, "infantil", "Estados Unidos", "Todo público")
        self.cant_peliculas = 2

        self.complejo.agregar_sala(Sala(1, 15000.0, 5, 8))



    def principal(self):
        
        continuar = True # para que no se cierre del todo
        while continuar == True:
                # Metodo princiapl que controla todo el flujo
                # se hace la autenticacion
            autenticado = False
            usuario_activo = None

            while autenticado == False:
                print(f'''
    ╭════════════ .✧. ════════════╮
      Bienvenido a la app de cines
    ╰════════════ .✧. ════════════╯''')
                nomb_ingresado = input('Usuario: ')
                contra_ingresada = input('Contraseña: ')

                    # secuencia de busqueda del usuario que se ingrese
                i = 0
                while i < self.cant_usuarios and autenticado == False:
                    if self.usuarios[i].nombre_usuario == nomb_ingresado:
                        if self.usuarios[i].verificar_contrasena(contra_ingresada) == True:
                                autenticado = True
                                usuario_activo = self.usuarios[i]
                    i += 1
                    
                if autenticado == False:
                    print('.✧. Usuario o contraseña incorrectos. Intente de nuevo! ')
                    
            # Mostrar menú

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
          
            salir = input("¿Desea salir del sistema? (s/n): ")
            if salir == "s":
                continuar = False

## ** quiere decir que todavía no esta la funcion para eso

    def menu_administrador(self):
        opc = 0
        while opc != 10:         
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
    10) Cerrar sesión
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
                        print("Sesión cerrada. Hasta luego!")
                    case _:
                        print("Opción no válida")
            except ValueError:
                print("\nError. Se esperaba un número entero.")
                input("\nPresione Enter para continuar...")
 
    def menu_vendedor(self):
        opc = 0
        while opc != 4:
            print(f'''
☆゜・。。・゜Menú Vendedor ゜・。。・゜★
                      
    1) Crear un nuevo usuario
    2) Reservar boletas**
    3) Consultar detalle de una película 
    4) Cerrar Sesión
                  ''')
            opc = int(input("Seleccione una opción: "))
 
            match opc:
                case 1:
                    self.crear_usuario()
                case 2:
                    self.reservar_boletas()
                case 3:
                    self.consultar_detalle_pelicula()
                case 4:
                    print("Sesión cerrada. Hasta luego!")
                case _:
                    print("Opción no válida")

    def menu_cliente(self):
        opc = 0
        while opc != 3:
            print(f'''
☆゜・。。・゜Menú Cliente ゜・。。・゜★
                      
    1) Reservar boletas**
    2) Consultar detalles de una película
    3) Cerrar sesión
                  ''')
            opc = int(input("Seleccione una opción: "))
 
            match opc:
                case 1:
                    self.reservar_boletas()
                case 2:
                    self.consultar_detalle_pelicula()
                case 3:
                    print("Sesión cerrada. Hasta luego!")
                case _:
                    print("Opción no válida")

    def crear_usuario(self):

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
            

    def crear_pelicula(self):
        print("\n━━━━━━✧ Crear nueva película ✧━━━━━━")
        valido = True
        ne = input("Nombre en español: ")
        no = input("Nombre original: ")
        anio = int(input("Año de estreno: "))
        dur = int(input("Duración (min): "))
        gen = input("Género (drama/suspenso/terror/acción/comedia/infantil): ")
        pais = input("País de origen: ")
        cal = input("Calificación: ")
 
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

    def consultar_detalle_pelicula(self):
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

    def crear_sala(self):
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
    
    def reservar_boletas(self):             
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

        cant_boletas = int(input('Ingrese la cantidad de boletas que desea comprar: '))
        fila = int(input('Escoja la fila: '))
        silla_inicial = int(input('Escoja la silla inicial: '))

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
        
    def modificar_estado_pelicula(self):
        print("\n━━━━━━✧ Modificar estado de una película ✧━━━━━━")
        
        if self.cant_peliculas == 0:
            print("No hay películas registradas en el sistema.")
            input("\nPresione Enter para continuar...")
            return

        nombre_buscar = input("Nombre en español de la película a modificar: ")
        
        encontrada = False
        posi_pelicula = -1
        i = 0
        
        while i < self.cant_peliculas and encontrada == False:
            if self.peliculas[i].nombre_espanol.lower() == nombre_buscar.lower():
                encontrada = True
                posi_pelicula = i
            i += 1
            
        if encontrada == False:
            print("No se encontró ninguna película con ese nombre.")
            input("\nPresione Enter para continuar...")
            return

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

    def eliminar_pelicula_programacion(self):
        print("\n━━━━━━✧ Eliminar película de la programación ✧━━━━━━")
        
        try:
            id_sala_buscar = int(input("Identificador de la sala: "))
            
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
                
            if sala_encontrada.eliminar_funcion(hora_buscar) == True:
                print("Función eliminada exitosamente.")
            else:
                print("Error. No se pudo eliminar la función.")
                
        except ValueError:
            print("\nError. El identificador de la sala debe ser un número entero.")
            
        input("\nPresione Enter para regresar al menú...")


    def consultar_porcentaje_ocupacion(self):
        print("\n━━━━━━✧ Porcentaje de Ocupación por Película ✧━━━━━━")
        
        max_registros = MAX_SALAS * MAX_FUNCIONES
        
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
                
            i += 1
            
        print(f"\n{"PELÍCULA":<25} {"SALA":<8} {"HORA":<10} {"OCUPACIÓN"}")
        print("=" * 55)
        
        i = 0
        while i < cant_registros:
            print(f"{peliculas_ocup[i]:<25} {salas_ocup[i]:<8} {horas_ocup[i]:<10} {porcentajes[i]:.2f}%")
            i += 1
            
        input("\nPresione Enter para regresar al menú...")

    def consultar_recaudo_sala(self):
        print("\n━━━━━━✧ Consultar recaudo de una sala ✧━━━━━━")
        
        try:
            id_sala_buscar = int(input("Identificador de la sala: "))
            
            sala_encontrada = self.complejo.buscar_sala(id_sala_buscar)
            if sala_encontrada == None:
                print(f"No se encontró ninguna sala con ese identificador.")
                input("\nPresione Enter para continuar...")
                return
                
            total_recaudo = sala_encontrada.calcular_recaudo()
            
            print(f"\nResumen de Recaudo - Sala {id_sala_buscar}:")
            print(f"Total recaudado: ${total_recaudo:,.2f}")
            
        except ValueError:
            print("\nError. El identificador de la sala debe ser un número entero.")
            
        input("\nPresione Enter para regresar al menú...")  

    def consultar_recaudo_complejo(self):
        print("\n━━━━━━✧ Consultar recaudo del complejo ✧━━━━━━")
        
        if self.complejo.cantidad_salas == 0:
            print("No hay salas registradas en el complejo para calcular el recaudo.")
            input("\nPresione Enter para regresar al menú...")
            return
            
        print(f"\nDESGLOSE DE RECAUDO POR SALA:")
        print("─" * 45)
        
        i = 0
        while i < self.complejo.cantidad_salas:
            sala_actual = self.complejo.salas[i]
            recaudo_sala = sala_actual.calcular_recaudo()
            print(f"Sala {sala_actual.identificador:<5} | Recaudo: ${recaudo_sala:,.2f}")
            i += 1
            
        total_general = self.complejo.calcular_recaudado()
        
        print("─" * 45)
        print(f"TOTAL GENERAL DEL COMPLEJO: ${total_general:,.2f}")
            
        input("\nPresione Enter para regresar al menú...")




        


app = AppCine()
app.principal()

