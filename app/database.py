from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

## Definimos dónde estará nuestra base de datos SQLite ###
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

## Creamos el motor de conexión ###
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # Solo para SQLite y FastAPI
)

## Creamos la sesión para interactuar con la base de datos ###
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

## Clase base para nuestros modelos ###
Base = declarative_base()