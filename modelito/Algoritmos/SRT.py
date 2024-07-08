import docker # type: ignore
from modelito.contenedores import *
import time

def aplicar_SRT(Ejecucion):
    comandos = Ejecucion.comandos
    tiempoActual = 0
    contenedores = []
    comandos.sort(key=lambda comando: comando.tiempo_inicio)
    
    for comando in comandos:
        iniciarContenedor(comando.imagen, comando.comando, contenedores)

    while comandos:
        comandosDisponibles = [comando for comando in comandos if comando.tiempo_inicio <= tiempoActual]

        if not comandosDisponibles:
            tiempoAux = comandos[0].tiempo_inicio
            time.sleep(tiempoAux - tiempoActual)
            tiempoActual = tiempoAux
            comandosDisponibles = [comando for comando in comandos if comando.tiempo_inicio <= tiempoActual]

        enEjecucion = min(comandosDisponibles, key=lambda comando: comando.tiempo_restante)

        # Calcula el tiempo que tarda otro comando en llegar
        tiempoOtroComando = min([comando.tiempo_inicio for comando in comandos if comando.tiempo_inicio > tiempoActual], default=float('inf'))

        # Calcula el tiempo que permite trabajar al contenedor
        tiempoDeVida = min(enEjecucion.tiempo_restante, tiempoOtroComando - tiempoActual)

        indice = comandos.index(enEjecucion)
        if enEjecucion.tiempo_estimado == enEjecucion.tiempo_restante:
            enEjecucion.respose = tiempoActual - enEjecucion.tiempo_inicio
            original_comando = next(c for c in Ejecucion.comandos if c.id == enEjecucion.id)
            original_comando.setrespose(tiempoActual - enEjecucion.tiempo_inicio)

        # Actualizar tiempo restante y tiempo actual
        enEjecucion.tiempo_restante -= tiempoDeVida
        tiempoActual += tiempoDeVida

        try:
            print(f"Despausando el contenedor para el comando: {enEjecucion.comando}")
            contenedores[indice].unpause()
                          
        except APIError as e:
            print(f"Contenedor iniciado: {contenedores[indice].image}") 
            contenedores[indice].start()

        time.sleep(tiempoDeVida)
        try:
            contenedores[indice].pause()
            print(f"Pausando el contenedor para el comando: {enEjecucion.comando}")
        except APIError as e:
            print(f"Pausando el contenedor para el comando: {enEjecucion.comando}")
        
        print(f"Tiempo ejecutado: {tiempoDeVida} Ejecutando {enEjecucion.comando}, tiempo restante: {enEjecucion.tiempo_restante}\n")

        if enEjecucion.tiempo_restante <= 0 or contenedores[indice].status == 'exited':
            enEjecucion.turnaround = tiempoActual - enEjecucion.tiempo_inicio
            original_comando = next(c for c in Ejecucion.comandos if c.id == enEjecucion.id)
            original_comando.setturnaround(tiempoActual - enEjecucion.tiempo_inicio)
            print(f"{enEjecucion.comando} ha terminado en el tiempo {tiempoActual}")
            print(f"Contenedor eliminado: {contenedores[indice].image}")
            print(f"El comando del mismo fue: {enEjecucion.comando}")
            print(f"Turnaround time: {enEjecucion.turnaround}")
            print(f"Response time: {enEjecucion.respose}")            
            comandos.remove(enEjecucion)
            contenedores[indice].remove()
            del contenedores[indice]
            