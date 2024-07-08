from copy import deepcopy
from modelito.comando import Comando
import docker
from datetime import datetime
from docker.errors import *
from sqlalchemy import Column,Integer,String,DateTime,Double
from sqlalchemy.orm import relationship
from .contenedores import *
from .Algoritmos.fifo import *
from .base import Base,Session


Client = docker.from_env()
Session = Session()

# clase que modela la ejecucion hereda de la base de datos para la tabla se cree al emepezar la ejecucion
class Ejecucion(Base):

    __tablename__ = 'ejecuciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    algoritmo = Column(String, nullable=True)
    fecha_ejecucion = Column(DateTime, nullable=True)
    comandos = relationship('Comando',backref='Ejecucion',cascade='all, delete-orphan')
    turnaroundp = Column(Double, nullable=True)
    responsep = Column(Double,nullable=True)

    def __init__(self,algoritmo, lista_comandos=None):
        self.turnaroundp= 0
        self.responsep= 0
        self.fecha_ejecucion=datetime.utcnow()
        self.algoritmo = algoritmo
        if lista_comandos is None:
            self.comandos = []
        else:
            self.comandos = lista_comandos

    # la funcion verificar imagenes consulta a la base de datos para saber si un comando ingresado ya tiene una imagen
    # si es asi asigna dicha imagen al comando de lo contrario crea y asgina una imagen con el nombre del comando
    def verificar_imagenes(self):
        # los replace se usan por que al crear una imagen no se puede pasar un texto con espacios y se pretendia que
        # las imagenes se llmaran exactamente igual que los comandos que ejecutan
        for comando in self.comandos:
            comando_actual = comando.comando
            existencia = Session.query(Comando).filter(comando_actual == Comando.comando).first()
            if existencia:
                print(f"se usarar una imagen existente para:{comando.comando}")
                comando.imagen = existencia.imagen.replace("_"," ")
            else:
                print(f"no existe la imagen para el comando: {comando.comando}")
                print("-----se va a crear una nueva imagen-----")
                imagen_nueva = comando.comando
                imagen_formato = imagen_nueva.replace(" ","_")
                comando.imagen = imagen_formato
                crear_imagen_ubuntu(imagen_formato)
                print("se creo una imagen ")
    def normalizar_formato(self):
        for comando in self.comandos:
            comando.imagen = comando.imagen.replace(" ","_")
    # funcion para calcular el turnaroundtime promedio
    def definir_turnaround(self):
        suma = 0
        for comando in self.comandos:
            suma += comando.turnaround
        p = suma/len(self.comandos)
        self.turnaroundp = p
        print("turnaround p : ",suma/len(self.comandos))
        
    #funcion para calcular el responsetime promedio
    def definir_response(self):
        suma=0
        for comando in self.comandos:
            suma+= comando.respose
        p = suma / len(self.comandos)
        self.responsep = p
        print("response p : ",suma/len(self.comandos))
    def mostrar_comandos(self):
        for comando in self.comandos:
            print(f"{comando.comando}")
    def mostrar_imagenes(self):
        for comando in self.comandos:
            print(f"{comando.imagen}")

