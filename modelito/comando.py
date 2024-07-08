from sqlalchemy import Column, Integer, Double, String,ForeignKey
from .base import Base

#clase que modela  un comando hereda de la base de datos para que la tabla se cree al empezar
#la ejecucion
class Comando(Base):

    __tablename__='comandos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    comando = Column(String, nullable=False)
    tiempo_inicio = Column(Integer, nullable=False)
    tiempo_estimado = Column(Integer, nullable=False)
    tiempo_restante = Column(Integer, nullable=False)
    imagen = Column(String, nullable=True)
    turnaround = Column(Double,nullable=True)
    respose = Column(Double,nullable=True)
    ejecucion_id = Column(Integer,ForeignKey('ejecuciones.id'))

    def __init__(self, comando, tiempo_entrada, tiempo_esperado):
        self.comando = comando
        self.tiempo_inicio = tiempo_entrada
        self.tiempo_estimado = tiempo_esperado
        self.tiempo_restante = tiempo_esperado
        self.respose = 0
        self.turnaround = 0

    def setrespose(self, reponse):
        self.respose = reponse

    def setturnaround(self, turnaround):
        self.turnaround = turnaround

