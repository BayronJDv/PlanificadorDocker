from copy import deepcopy
import os
import docker # type: ignore
import time
import msvcrt
from modelito.comando import Comando
from modelito.ejecucion import Ejecucion,crear_imagen_ubuntu
from modelito.base import Session,Base,engine
from modelito.Algoritmos.fifo import aplicar_fifo
from modelito.Algoritmos.roundRobin import aplicar_RoundRobin
from modelito.Algoritmos.SPN import aplicar_SPN
from modelito.Algoritmos.SRT import aplicar_SRT
from modelito.Algoritmos.HRRN import aplicar_HRRN

# al ser un programa por consola aunque se busco una arquitectura mvc al no haber gui se manejo
# la respuesta del programa desde el controlador en el archivo control
def esperarTecla():
    print("Presiona cualquier tecla para continuar...")
    msvcrt.getch()

def iniciar():
    Base.metadata.create_all(engine)
    while True:
        print("=========================================================")
        print("       Bienvenido al Planificador de contenedores        ")
        print("=========================================================")
        print("         ------ Digite una opcion --------              ")
        print(" 1 - Si quiere realizar una nueva ejecucion              ")
        print(" 2 - Si quiere un listado de las ejecuciones realizadas  ")
        print(" 3 - Si quiere repetir una ejecucion con otro algoritmo  ")
        print("         ----------------------------------              ")
        print("=========================================================")
        caso = int(input("opcion: "))
        os.system('clear' if os.name != 'nt' else 'cls')
        match caso:
            case 1:
                realizar_ejecucion()
            case 2:
                listar_ejecuciones()
            case 3:
                repetir_ejecucion()
            case _:
                return "ingrese una opcion valida"

# funcion encargada de realizar una nueva ejecucion
def realizar_ejecucion():
    session = Session()
    malEscrito = True
    while malEscrito:
        try:
            numero_comandos = abs(int(input("Digite el número de comandos a ejecutar: ")))
            malEscrito = False
        except ValueError:
            os.system('clear' if os.name != 'nt' else 'cls')
            print("Por favor, ingrese un número entero válido.")
    
    comandos_a_ejecutar = []
    for i in range(numero_comandos):
        comando_ingresado = input(f"Ingrese el comando nro({i+1}): \n")
        tiempo_inicio = int(input(f"Ingrese el tiempo inicio para el comando nro({i+1}):  \n"))
        tiempo_estimado = int(input(f"Ingrese el tiempo estimado para el comando nro({i+1}):  \n"))
        comando_creado = Comando(comando_ingresado, tiempo_inicio, tiempo_estimado)
        comandos_a_ejecutar.append(comando_creado)
    algoritmo = int(input("Digite el algoritmo que quiere usar para su ejecucion\n"
                          "1 _ FIFO, 2 _ Round_Robin, 3_ SPN  4 _ SRT 5 _  HRRN     "))
    # aqui se deberia programar la eleccion de un algoritmo para que la ejecucion se haga con ese algoritmo
    match algoritmo:
        case 1:
            mi_ejecucion = Ejecucion("FIFO", comandos_a_ejecutar)
            mi_ejecucion.verificar_imagenes()
            mi_ejecucion.normalizar_formato()
            aplicar_fifo(mi_ejecucion)
            mi_ejecucion.definir_response()
            mi_ejecucion.definir_turnaround()
            session.add(mi_ejecucion)
            session.commit()

            esperarTecla()
        case 2:
            mi_ejecucion = Ejecucion("RR", comandos_a_ejecutar)
            mi_ejecucion.verificar_imagenes()
            mi_ejecucion.normalizar_formato()
            aplicar_RoundRobin(mi_ejecucion)
            mi_ejecucion.definir_response()
            mi_ejecucion.definir_turnaround()
            session.add(mi_ejecucion)
            session.commit()
            esperarTecla()
        case 3:
            mi_ejecucion = Ejecucion("SPN", comandos_a_ejecutar)
            mi_ejecucion.verificar_imagenes()
            mi_ejecucion.normalizar_formato()
            aplicar_SPN(mi_ejecucion)
            mi_ejecucion.definir_response()
            mi_ejecucion.definir_turnaround()
            session.add(mi_ejecucion)
            session.commit()
            esperarTecla()
        case 4:
            mi_ejecucion = Ejecucion("SRT", comandos_a_ejecutar)
            mi_ejecucion.verificar_imagenes()
            aplicar_SRT(mi_ejecucion)
            mi_ejecucion.normalizar_formato()
            mi_ejecucion.definir_response()
            mi_ejecucion.definir_turnaround()
            session.add(mi_ejecucion)
            session.commit()
            esperarTecla()

        case 5:
            mi_ejecucion = Ejecucion("HRRN", comandos_a_ejecutar)
            mi_ejecucion.verificar_imagenes()
            mi_ejecucion.normalizar_formato()
            aplicar_HRRN(mi_ejecucion)
            mi_ejecucion.definir_response()
            mi_ejecucion.definir_turnaround()
            session.add(mi_ejecucion)
            session.commit()
            esperarTecla()
        case _:
            int(input("Digite el algoritmo que quiere usar para su ejecucion\n"
                          "1 _ FIFO, 2 _ Round_Robin, 3_ SPN  4 _ SRT 5 _  HRRN     "))

    os.system('clear' if os.name != 'nt' else 'cls')
    print("-----se a añadido la ejecucion a la base de datos-----")

def listar_ejecuciones():
    session = Session()
    ejecuciones = session.query(Ejecucion).all()
    print("     Se han realizado las siguientes ejecuciones :\n")
    if ejecuciones:
        for ejecucion in ejecuciones:
            print("=====================================")
            print(f"Ejecucion ID: {ejecucion.id}")
            print(f"Algoritmo: {ejecucion.algoritmo}")
            print(f"Fecha : {ejecucion.fecha_ejecucion}")
            print(f"timearound p : {ejecucion.turnaroundp}")
            print(f"response p: {ejecucion.responsep}")
            print("=====================================")
            if ejecucion.comandos:
                print(f"    ----comandos de la ejecucion {ejecucion.id}-----    ")
                for comando in ejecucion.comandos:
                    print(
                        f" - Comando: {comando.comando}, \n"
                        f"Tiempo inicio: {comando.tiempo_inicio}, Tiempo estimado: {comando.tiempo_estimado}  "
                        f"timearound: {comando.turnaround}, response: {comando.respose},")
                print(f"    -----------------------------------    \n\n")
    else:
        print("Aun no se han registrado ejecuciones en la base de datos")

def repetir_ejecucion():
    print("Digite el id de la ejecucion a repetir :")
    print("Si no conoce el id puede encontrarlo en las pestaña ejecuciones realizadas\n"
          "digite 0 para regresar al menu principal ")
    id_buscado = int(input(" ID / 0 : "))
    if id_buscado == 0:
        return
    else:
        session = Session()
        ejecucion_pasada = session.query(Ejecucion).filter_by(id=id_buscado).first()
        if ejecucion_pasada:
            nuevo_algo = input(f"Digite el algoritmo con el que quiere ejecutar {ejecucion_pasada.id}\n")
            comandos_pasados = ejecucion_pasada.comandos
            nuevos_comandos = []
            for comando in comandos_pasados:
                nuevo_comando = Comando(
                    comando.comando,
                    comando.tiempo_inicio,
                    comando.tiempo_estimado
                )
                nuevos_comandos.append(nuevo_comando)
            nueva_ejecucion = Ejecucion(
                algoritmo=nuevo_algo,
                lista_comandos= nuevos_comandos
            )
        opcion = int(input("Digite el algoritmo que quiere usar para su ejecucion\n"
                    "1 _ FIFO, 2 _ Round_Robin, 3_ SPN  4 _ SRT 5 _  HRRN     "))    
        match opcion:
            case 1:

                nueva_ejecucion.verificar_imagenes()
                nueva_ejecucion.normalizar_formato()
                aplicar_fifo(nueva_ejecucion)
                nueva_ejecucion.definir_response()
                nueva_ejecucion.definir_turnaround()
                session.add(nueva_ejecucion)
                session.commit()

                esperarTecla()
            case 2:

                nueva_ejecucion.verificar_imagenes()
                nueva_ejecucion.normalizar_formato()
                aplicar_RoundRobin(nueva_ejecucion)
                nueva_ejecucion.definir_response()
                nueva_ejecucion.definir_turnaround()
                session.add(nueva_ejecucion)
                session.commit()
                esperarTecla()
            case 3:

                nueva_ejecucion.verificar_imagenes()
                nueva_ejecucion.normalizar_formato()
                aplicar_SPN(nueva_ejecucion)
                nueva_ejecucion.definir_response()
                nueva_ejecucion.definir_turnaround()
                session.add(nueva_ejecucion)
                session.commit()
                esperarTecla()
            case 4:

                nueva_ejecucion.verificar_imagenes()
                nueva_ejecucion.normalizar_formato()
                aplicar_SRT(nueva_ejecucion)
                nueva_ejecucion.definir_response()
                nueva_ejecucion.definir_turnaround()
                session.add(nueva_ejecucion)
                session.commit()
                esperarTecla()

            case 5:

                nueva_ejecucion.verificar_imagenes()
                nueva_ejecucion.normalizar_formato()
                aplicar_HRRN(nueva_ejecucion)
                nueva_ejecucion.definir_response()
                nueva_ejecucion.definir_turnaround()
                session.add(nueva_ejecucion)
                session.commit()
                esperarTecla()
            case _:
                int(input("Digite el algoritmo que quiere usar para su ejecucion\n"
                            "1 _ FIFO, 2 _ Round_Robin, 3_ SPN  4 _ SRT 5 _  HRRN     "))