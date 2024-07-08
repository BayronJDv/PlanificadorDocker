import docker # type: ignore
from modelito.contenedores import *
import time
from copy import deepcopy

def aplicar_HRRN(Ejecucion):
    comandos = deepcopy(Ejecucion.comandos)

    def ratio(comando):
        ratio = ((tiempoActual - comando.tiempo_inicio) + comando.tiempo_estimado) / comando.tiempo_estimado
        return ratio

    tiempoActual = 0
    finalizados = []
    comandos.sort(key=lambda comando: comando.tiempo_inicio)

    while comandos:
        comandosDisponibles = [comando for comando in comandos if comando.tiempo_inicio <= tiempoActual]

        if not comandosDisponibles:
            tiempoAux = comandos[0].tiempo_inicio
            time.sleep(tiempoAux - tiempoActual)
            tiempoActual = tiempoAux
            comandosDisponibles = [comando for comando in comandos if comando.tiempo_inicio <= tiempoActual]

        enEjecucion = max(comandosDisponibles, key=lambda comando: (ratio(comando), -comando.tiempo_estimado))

        original_comando = next(c for c in Ejecucion.comandos if c.id == enEjecucion.id)
        original_comando.setrespose(tiempoActual - enEjecucion.tiempo_inicio)
        enEjecucion.respose = tiempoActual - enEjecucion.tiempo_inicio
        tiempoActual += enEjecucion.tiempo_estimado
        enEjecucion.turnaround = tiempoActual - enEjecucion.tiempo_inicio
        original_comando.setturnaround(tiempoActual - enEjecucion.tiempo_inicio)
        
        finalizados.append(enEjecucion)
        comandos.remove(enEjecucion)

        print(f"ejecutando : {enEjecucion.comando}")
        iniciar_container(enEjecucion.imagen,enEjecucion.comando)
        print(f"se termino de ejecutar {enEjecucion.comando}")
        print(f"Turnaround time: {enEjecucion.turnaround}")
        print(f"Response time: {enEjecucion.respose}")