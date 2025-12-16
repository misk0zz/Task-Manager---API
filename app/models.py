from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Task(Base):
    __tablename__= "tasks" ## Nombre de la tabla en SQL
    
    id = Column(Integer, primary_key=True, index=True) ## Columna ID, clave primaria
    title = Column(String, index=True) ## Columna título
    description = Column(String, index=True) ## Columna descripción
    is_completed = Column(Boolean, default=False) ## Columna para estado de completitud