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
    contador = 0
    while contenedores:
        comando = comandos[contador]
        container = contenedores[contador]

        # Si el comando dictado por el contador tiene tiempo mayor al actual, pasa un segundo e incrementa el contador del tiempo
        if comando.tiempo_inicio <= tiempoActual:
            #Escoje el tiempo que vive el contenedor, si es 1 o 2 segundos segun su tiempo restante
            tiempo = min(2, comando.tiempo_restante)

            #Si es la primera ejecucion del comando se define un tiempo de respuesta
            if comando.tiempo_estimado == comando.tiempo_restante:
                comando.respose = tiempoActual - comando.tiempo_inicio
                original_comando = next(c for c in Ejecucion.comandos if c.id == comando.id)                    
                original_comando.setrespose(tiempoActual - comando.tiempo_inicio)

            try:
                container.unpause()
                print(f"Contenedor despausado: {container.image}")

            except APIError:
                container.start()
                print(f"Contenedor iniciado: {container.image}")

            #Duerme el quantum o solo 1 segundo
            time.sleep(tiempo)

            try:
                container.pause()
                print(f"Contenedor pausado: {container.image}")
            except APIError:
                #Si el contenedor no se puede pausar es debido a que ya termino
                print(f"Contenedor ya estaba pausado: {container.image}")             

            tiempoActual += tiempo
            comando.tiempo_restante -= tiempo
            contador +=1

            #Si el contador exede el indice se reinicia
            if contador == comandos.len():
                contador = 0

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
        else:
            tiempoActual += 1
            time.sleep(1)