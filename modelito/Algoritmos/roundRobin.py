import docker # type: ignore
from modelito.contenedores import *
from copy import deepcopy

def aplicar_RoundRobin(Ejecucion):

    comandos = deepcopy(Ejecucion.comandos)

    comandos.sort(key=lambda comando: comando.tiempo_inicio)
    contenedores = []
    for comando in comandos:
        iniciarContenedor(comando.imagen, comando.comando, contenedores)
    
    tiempoActual = 0
    while contenedores:
        for i, container in enumerate(contenedores):
            comando = comandos[i]
            if comando.tiempo_inicio <= tiempoActual:
                tiempo = min(2, comando.tiempo_restante)

                if comando.tiempo_estimado == comando.tiempo_restante:
                    comando.respose = tiempoActual - comando.tiempo_inicio
                    original_comando = next(c for c in Ejecucion.comandos if c.id == comando.id)                    
                    original_comando.setrespose(tiempoActual - comando.tiempo_inicio)

                try:
                    container.unpause()
                    print(f"Contenedor despausado: {container.image}")

                except APIError as e:
                    container.start()
                    print(f"Contenedor iniciado: {container.image}")

                time.sleep(tiempo)

                try:
                    container.pause()
                    print(f"Contenedor pausado: {container.image}")
                except APIError as e:
                    print(f"Contenedor ya estaba pausado: {container.image}")             

                tiempoActual += tiempo
                comando.tiempo_restante -= tiempo

                if container.status == 'exited' or comando.tiempo_restante <= 0:
                    container.stop()
                    container.remove()                    
                    print(f"Contenedor eliminado: {container.image}")
                    print(f"El comando del mismo fue: {comando.comando}")
                    original_comando = next(c for c in Ejecucion.comandos if c.id == comando.id)
                    original_comando.setturnaround(tiempoActual - comando.tiempo_inicio)
                    comando.turnaround = tiempoActual - comando.tiempo_inicio
                    print(f"Turnaround time: {comando.turnaround}")
                    print(f"Response time: {comando.respose}")
                    contenedores.remove(container)
                    comandos.remove(comando)