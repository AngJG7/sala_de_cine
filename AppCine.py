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
        while opc != 6:         
            print(f'''
☆゜・。。・゜Menú Administrador ゜・。。・゜★
                      
    1) Crear nueva película
    2) Modificar estado película **
    3) Crear nueva sala
    4) Consultar detalle de la película
    5) Crear usuarios
    6) Cerrar sesión
                  ''')
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
                    print("Sesión cerrada. Hasta luego!")
                case _:
                    print("Opción no válida")

 
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




        


app = AppCine()
app.principal()

