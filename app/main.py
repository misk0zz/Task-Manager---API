from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

## Importamos nuestros archivos locales
from . import models, schemas, database

## Creamos las tablas en la base de datos automáticamente
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Task Manager API", version="1.0.1")

## Nos da una sesión de base de datos para cada petición
## y la cierra al finaliza. Asi no saturamos el servidor.
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
## RUTAS (Endpoints) ##
@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)): ## Creamos el objeto del Modelo con los datos del Esquema
    db_task = models.Task(title=task.title, description=task.description, is_completed=task.is_completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# GET - Leer todas
@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return tasks

# GET - Leer una
@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

# PUT - Actualizar
@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # Actualizamos los campos
    task.title = task_update.title # type: ignore
    task.description = task_update.description # type: ignore
    task.is_completed = task_update.is_completed # type: ignore
    
    db.commit()
    db.refresh(task)
    return task

# DELETE - Borrar
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    db.delete(task)
    db.commit()
    return {"message": "Tarea eliminada correctamente"}