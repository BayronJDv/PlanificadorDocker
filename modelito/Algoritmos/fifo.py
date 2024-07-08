
import docker # type: ignore
from modelito.contenedores import *
from modelito.ejecucion import * 
from modelito.comando import *
import time
from copy import deepcopy


#definicion del algoitmo fifo simplemente ordena los comandos por su tiempo de llegada y los ejecuta en este orden
def aplicar_fifo(Ejecucion):
    #copia el objeto para no modificarlo durante su ejecucion
    comandos = deepcopy(Ejecucion.comandos)

    #controlador del tiempo
    tiempoActual = 0

    while comandos:
        #Se repite mientras que existen comandos y estos se filtran segun el tiempo de inicio/llegada
        comandosDisponibles = [comando for comando in comandos if comando.tiempo_inicio <= tiempoActual]

        #Si no hay comandos disponibles espera el tiempo para que lo estén
        if not comandosDisponibles:
            tiempoAux = comandos[0].tiempo_inicio
            time.sleep(tiempoAux - tiempoActual)
            tiempoActual = tiempoAux
            comandosDisponibles = [comando for comando in comandos if comando.tiempo_inicio <= tiempoActual]
        
        #determina la ejecucion del comando con menor tiempo de inicio disponible
        enEjecucion = min(comandosDisponibles, key=lambda  comando: comando.tiempo_inicio)

        print(f"ejecutando : {enEjecucion.comando}")
        iniciar_container(enEjecucion.imagen,enEjecucion.comando)
        print(f"se termino de ejecutar {enEjecucion.comando}")

        #Maneja el cambio del objeto para la base de datos
        original_comando = next(c for c in Ejecucion.comandos if c.id == enEjecucion.id)
        enEjecucion.respose = tiempoActual - enEjecucion.tiempo_inicio
        original_comando.setrespose(tiempoActual - enEjecucion.tiempo_inicio)
        tiempoActual += enEjecucion.tiempo_estimado
        enEjecucion.turnaround = tiempoActual - enEjecucion.tiempo_inicio
        original_comando.setturnaround(tiempoActual - enEjecucion.tiempo_inicio)
        
        print(f"Turnaround time: {enEjecucion.turnaround}")
        print(f"Response time: {enEjecucion.respose}")

        #Remueve el comando del ciclo
        comandos.remove(enEjecucion)