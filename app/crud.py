# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

# CRUD para Provincia
def get_provincias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Provincia).offset(skip).limit(limit).all()

def get_provincia(db: Session, provincia_id: int):
    return db.query(models.Provincia).filter(models.Provincia.id_provincia == provincia_id).first()

def create_provincia(db: Session, provincia: schemas.ProvinciaCreate):
    db_provincia = models.Provincia(nombre=provincia.nombre)
    db.add(db_provincia)
    db.commit()
    db.refresh(db_provincia)
    return db_provincia

def delete_provincia(db: Session, provincia_id: int):
    db_provincia = db.query(models.Provincia).filter(models.Provincia.id_provincia == provincia_id).first()
    if db_provincia:
        db.delete(db_provincia)
        db.commit()
    return db_provincia

def update_provincia(db: Session, provincia_id: int, provincia: schemas.ProvinciaCreate):
    db_provincia = db.query(models.Provincia).filter(models.Provincia.id_provincia == provincia_id).first()
    if db_provincia:
        db_provincia.nombre = provincia.nombre
        db.commit()
        db.refresh(db_provincia)
    return db_provincia

# Repite funciones similares para Municipio, Especie, Role, Usuario, etc.
