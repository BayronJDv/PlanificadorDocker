import docker # type: ignore
from docker.errors import * # type: ignore
import time

#intencion : archivo creado para funcoines de administracion de contenedores e imagenes
Client = docker.from_env()
#recibe una imagen y ejcuta un contenedor con el comando asignado (remove indica si el contenedor se borra despues de su ejecucion)
def iniciar_container(imagen, comando):
    try:
        Client.containers.run(imagen,comando,remove=True)
        print(f"se ejecutó :{comando}")
    except ContainerError as e:
        print(f"Error en el contenedor: El comando '{comando}' en la imagen '{imagen}' devolvió un estado de salida no cero.")
        print(f"Detalle del error: {e}")
    except ImageNotFound as e:
        print(f"Imagen no encontrada: {e}")
    except APIError as e:
        print(f"Error en la API de Docker: {e}")

def iniciarContenedor(imagen, comando, contenedores):
    try:
        # tecnicamente el contenedor se crea pero no se ejecuta el comando
        container = Client.containers.create(imagen, comando)
        contenedores.append(container)
        print(f"El contenedor ha sido creado con el comando: {comando}") 
    except ContainerError as e:
        print(f"Error en el contenedor: El comando '{comando}' en la imagen '{imagen}' devolvió un estado de salida no cero.")
        print(f"Detalle del error: {e}")
    except ImageNotFound as e:
        print(f"Imagen no encontrada: {e}")
    except APIError as e:
        print(f"Error en la API de Docker: {e}")

# crea una imagen con el nombre del comando (todas las imagenes tendran ubuntu como base, pero se llamaran igual que el comando que
# va a hacer uso de ellas) la funcion crea un contenedor temporal para crear la imagen con un commit
def crear_imagen_ubuntu(nombre_imagen):
    client = docker.from_env()
    base_image = "ubuntu:latest"
    container = client.containers.create(base_image)
    new_image = container.commit(repository=nombre_imagen, tag="latest")
    print(f"Imagen creada: {new_image.tags}")
    container.remove()
