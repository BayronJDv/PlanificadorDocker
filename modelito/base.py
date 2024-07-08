
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# intencion Gestionar la coneccion inicial a la base de datos

data_base_url = 'postgresql://postgres:pescado@localhost/postgres'
engine = create_engine(data_base_url)
Session = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()
