from pydantic import BaseModel
from typing import Optional

## Esquema base para una tarea
class TaskBase(BaseModel):
    title: str ## Título de la tarea
    description: Optional[str] = None ## Descripción de la tarea (opcional)
    is_completed: bool = False ## Estado de completitud (por defecto es False)
    
## Modelo para CREAR tareas (el usuario no proporciona el ID)
class TaskCreate(TaskBase):
    pass

## Modelo para LEER tareas (incluye el ID que genera la DB)
class Task(TaskBase):
    id: int ## ID de la tarea
    
    class Config:
        from_attribute = True ## Permite a Pydantic leer datos de SQLAlchemy