# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API REST - Gestión de Árboles",
    description="API para gestionar información de árboles, municipios, especies, usuarios, etc.",
    version="1.0.0",
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rutas para Provincia
@app.post("/provincias/", response_model=schemas.ProvinciaRead)
def crear_provincia(provincia: schemas.ProvinciaCreate, db: Session = Depends(get_db)):
    return crud.create_provincia(db=db, provincia=provincia)

@app.get("/provincias/", response_model=List[schemas.ProvinciaRead])
def leer_provincias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    provincias = crud.get_provincias(db, skip=skip, limit=limit)
    return provincias

@app.get("/provincias/{provincia_id}", response_model=schemas.ProvinciaRead)
def leer_provincia(provincia_id: int, db: Session = Depends(get_db)):
    db_provincia = crud.get_provincia(db, provincia_id=provincia_id)
    if db_provincia is None:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    return db_provincia

@app.put("/provincias/{provincia_id}", response_model=schemas.ProvinciaRead)
def actualizar_provincia(provincia_id: int, provincia: schemas.ProvinciaCreate, db: Session = Depends(get_db)):
    db_provincia = crud.update_provincia(db, provincia_id=provincia_id, provincia=provincia)
    if db_provincia is None:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    return db_provincia

@app.delete("/provincias/{provincia_id}", response_model=schemas.ProvinciaRead)
def eliminar_provincia(provincia_id: int, db: Session = Depends(get_db)):
    db_provincia = crud.delete_provincia(db, provincia_id=provincia_id)
    if db_provincia is None:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    return db_provincia

# Repite rutas similares para Municipio, Especie, Role, Usuario, etc.
