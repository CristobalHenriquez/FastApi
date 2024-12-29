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
    description="API para gestionar información de árboles, municipios, especies, usuarios, y más.",
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
    return crud.get_provincias(db, skip=skip, limit=limit)

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

@app.delete("/provincias/{provincia_id}", status_code=204)
def eliminar_provincia(provincia_id: int, db: Session = Depends(get_db)):
    # Intentar eliminar la provincia
    eliminado = crud.delete_provincia(db, provincia_id=provincia_id)
    if not eliminado:
        # Si no existe, devolver 404
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    # Si se elimina con éxito, no retornamos contenido
    return


# Rutas para Municipio
@app.post("/municipios/", response_model=schemas.MunicipioRead)
def crear_municipio(municipio: schemas.MunicipioCreate, db: Session = Depends(get_db)):
    return crud.create_municipio(db=db, municipio=municipio)

@app.get("/municipios/", response_model=List[schemas.MunicipioRead])
def leer_municipios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_municipios(db, skip=skip, limit=limit)

@app.get("/municipios/{municipio_id}", response_model=schemas.MunicipioRead)
def leer_municipio(municipio_id: int, db: Session = Depends(get_db)):
    db_municipio = crud.get_municipio(db, municipio_id=municipio_id)
    if db_municipio is None:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    return db_municipio

@app.put("/municipios/{municipio_id}", response_model=schemas.MunicipioRead)
def actualizar_municipio(municipio_id: int, municipio: schemas.MunicipioCreate, db: Session = Depends(get_db)):
    db_municipio = crud.update_municipio(db, municipio_id=municipio_id, municipio=municipio)
    if db_municipio is None:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    return db_municipio

@app.delete("/municipios/{municipio_id}", status_code=204)
def eliminar_municipio(municipio_id: int, db: Session = Depends(get_db)):
    # Intentar eliminar el municipio
    eliminado = crud.delete_municipio(db, municipio_id=municipio_id)
    if not eliminado:
        # Si no se encuentra el municipio, devolver 404
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    # Si se elimina con éxito, no retornamos contenido
    return


# Rutas para Especie
@app.post("/especies/", response_model=schemas.EspecieRead)
def crear_especie(especie: schemas.EspecieCreate, db: Session = Depends(get_db)):
    return crud.create_especie(db=db, especie=especie)

@app.get("/especies/", response_model=List[schemas.EspecieRead])
def leer_especies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_especies(db, skip=skip, limit=limit)

@app.get("/especies/{especie_id}", response_model=schemas.EspecieRead)
def leer_especie(especie_id: int, db: Session = Depends(get_db)):
    db_especie = crud.get_especie(db, especie_id=especie_id)
    if db_especie is None:
        raise HTTPException(status_code=404, detail="Especie no encontrada")
    return db_especie

@app.put("/especies/{especie_id}", response_model=schemas.EspecieRead)
def actualizar_especie(especie_id: int, especie: schemas.EspecieCreate, db: Session = Depends(get_db)):
    db_especie = crud.update_especie(db, especie_id=especie_id, especie=especie)
    if db_especie is None:
        raise HTTPException(status_code=404, detail="Especie no encontrada")
    return db_especie

@app.delete("/especies/{especie_id}", status_code=204)
def eliminar_especie(especie_id: int, db: Session = Depends(get_db)):
    # Intentar eliminar la especie
    eliminado = crud.delete_especie(db, especie_id=especie_id)
    if not eliminado:
        # Si no se encuentra la especie, devolver 404
        raise HTTPException(status_code=404, detail="Especie no encontrada")
    # Si se elimina con éxito, no retornamos contenido
    return


# Rutas para Usuario
@app.post("/usuarios/", response_model=schemas.UsuarioRead)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db=db, usuario=usuario)

@app.get("/usuarios/", response_model=List[schemas.UsuarioRead])
def leer_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_usuarios(db, skip=skip, limit=limit)

@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioRead)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioRead)
def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.update_usuario(db, usuario_id=usuario_id, usuario=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@app.delete("/usuarios/{usuario_id}", status_code=204)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    # Intentar eliminar el usuario
    eliminado = crud.delete_usuario(db, usuario_id=usuario_id)
    if not eliminado:
        # Si no se encuentra el usuario, devolver 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Si se elimina con éxito, no retornamos contenido
    return


# Rutas para Arbol
@app.post("/arboles/", response_model=schemas.ArbolRead)
def crear_arbol(arbol: schemas.ArbolCreate, db: Session = Depends(get_db)):
    # Validación: Si hay interferencia aérea, se deben especificar detalles.
    if arbol.interferencia_aerea and not arbol.especificaciones_interferencia:
        raise HTTPException(
            status_code=400,
            detail="Debe especificar detalles de la interferencia aérea si esta existe.",
        )
    return crud.create_arbol(db=db, arbol=arbol)

@app.get("/arboles/", response_model=List[schemas.ArbolRead])
def leer_arboles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_arboles(db, skip=skip, limit=limit)

@app.get("/arboles/{arbol_id}", response_model=schemas.ArbolRead)
def leer_arbol(arbol_id: int, db: Session = Depends(get_db)):
    db_arbol = crud.get_arbol(db, arbol_id=arbol_id)
    if db_arbol is None:
        raise HTTPException(status_code=404, detail="Árbol no encontrado")
    return db_arbol

@app.put("/arboles/{arbol_id}", response_model=schemas.ArbolRead)
def actualizar_arbol(arbol_id: int, arbol: schemas.ArbolCreate, db: Session = Depends(get_db)):
    # Validación: Si hay interferencia aérea, se deben especificar detalles.
    if arbol.interferencia_aerea and not arbol.especificaciones_interferencia:
        raise HTTPException(
            status_code=400,
            detail="Debe especificar detalles de la interferencia aérea si esta existe.",
        )
    db_arbol = crud.update_arbol(db, arbol_id=arbol_id, arbol=arbol)
    if db_arbol is None:
        raise HTTPException(status_code=404, detail="Árbol no encontrado")
    return db_arbol

@app.delete("/arboles/{arbol_id}", status_code=204)
def eliminar_arbol(arbol_id: int, db: Session = Depends(get_db)):
    # Intentar eliminar el árbol
    eliminado = crud.delete_arbol(db, arbol_id=arbol_id)
    if not eliminado:
        # Si no se encuentra el árbol, devolver 404
        raise HTTPException(status_code=404, detail="Árbol no encontrado")
    # Si se elimina con éxito, no retornamos contenido
    return


# Rutas para Medicion
@app.post("/mediciones/", response_model=schemas.MedicionRead)
def crear_medicion(medicion: schemas.MedicionCreate, db: Session = Depends(get_db)):
    # Validación: Si hay interferencia aérea, se deben especificar detalles.
    if medicion.interferencia_aerea and not medicion.especificaciones_interferencia:
        raise HTTPException(
            status_code=400,
            detail="Debe especificar detalles de la interferencia aérea si esta existe.",
        )
    return crud.create_medicion(db=db, medicion=medicion)

@app.get("/mediciones/", response_model=List[schemas.MedicionRead])
def leer_mediciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_mediciones(db, skip=skip, limit=limit)

@app.get("/mediciones/{medicion_id}", response_model=schemas.MedicionRead)
def leer_medicion(medicion_id: int, db: Session = Depends(get_db)):
    db_medicion = crud.get_medicion(db, medicion_id=medicion_id)
    if db_medicion is None:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    return db_medicion

@app.put("/mediciones/{medicion_id}", response_model=schemas.MedicionRead)
def actualizar_medicion(medicion_id: int, medicion: schemas.MedicionCreate, db: Session = Depends(get_db)):
    # Validación: Si hay interferencia aérea, se deben especificar detalles.
    if medicion.interferencia_aerea and not medicion.especificaciones_interferencia:
        raise HTTPException(
            status_code=400,
            detail="Debe especificar detalles de la interferencia aérea si esta existe.",
        )
    db_medicion = crud.update_medicion(db, medicion_id=medicion_id, medicion=medicion)
    if db_medicion is None:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    return db_medicion

@app.delete("/mediciones/{medicion_id}", status_code=204)
def eliminar_medicion(medicion_id: int, db: Session = Depends(get_db)):
    # Intentar eliminar la medición
    eliminado = crud.delete_medicion(db, medicion_id=medicion_id)
    if not eliminado:
        # Si no se encuentra la medición, devolver 404
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    # Si se elimina con éxito, no retornamos contenido
    return


# Rutas para Foto
@app.post("/fotos/", response_model=schemas.FotoRead, status_code=201)
def crear_foto(foto: schemas.FotoCreate, db: Session = Depends(get_db)):
    # Crear la foto
    try:
        return crud.create_foto(db=db, foto=foto)
    except Exception:
        raise HTTPException(status_code=409, detail="Conflicto al crear la foto.")

@app.get("/fotos/", response_model=List[schemas.FotoRead])
def leer_fotos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_fotos(db, skip=skip, limit=limit)

@app.get("/fotos/{foto_id}", response_model=schemas.FotoRead)
def leer_foto(foto_id: int, db: Session = Depends(get_db)):
    db_foto = crud.get_foto(db, foto_id=foto_id)
    if db_foto is None:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return db_foto

@app.put("/fotos/{foto_id}", response_model=schemas.FotoRead)
def actualizar_foto(foto_id: int, foto: schemas.FotoCreate, db: Session = Depends(get_db)):
    db_foto = crud.update_foto(db, foto_id=foto_id, foto=foto)
    if db_foto is None:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return db_foto

@app.delete("/fotos/{foto_id}", status_code=204)
def eliminar_foto(foto_id: int, db: Session = Depends(get_db)):
    # Intentar eliminar la foto
    eliminado = crud.delete_foto(db, foto_id=foto_id)
    if not eliminado:
        # Si no se encuentra la foto, devolver 404
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    # Si se elimina con éxito, no retornamos contenido
    return