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

# CRUD para Municipio
def get_municipios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Municipio).offset(skip).limit(limit).all()

def get_municipio(db: Session, municipio_id: int):
    return db.query(models.Municipio).filter(models.Municipio.id_municipio == municipio_id).first()

def create_municipio(db: Session, municipio: schemas.MunicipioCreate):
    db_municipio = models.Municipio(**municipio.dict())
    db.add(db_municipio)
    db.commit()
    db.refresh(db_municipio)
    return db_municipio

def delete_municipio(db: Session, municipio_id: int):
    db_municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == municipio_id).first()
    if db_municipio:
        db.delete(db_municipio)
        db.commit()
    return db_municipio

def update_municipio(db: Session, municipio_id: int, municipio: schemas.MunicipioCreate):
    db_municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == municipio_id).first()
    if db_municipio:
        for key, value in municipio.dict().items():
            setattr(db_municipio, key, value)
        db.commit()
        db.refresh(db_municipio)
    return db_municipio

# CRUD para Especie
def get_especies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Especie).offset(skip).limit(limit).all()

def get_especie(db: Session, especie_id: int):
    return db.query(models.Especie).filter(models.Especie.id_especie == especie_id).first()

def create_especie(db: Session, especie: schemas.EspecieCreate):
    db_especie = models.Especie(**especie.dict())
    db.add(db_especie)
    db.commit()
    db.refresh(db_especie)
    return db_especie

def delete_especie(db: Session, especie_id: int):
    db_especie = db.query(models.Especie).filter(models.Especie.id_especie == especie_id).first()
    if db_especie:
        db.delete(db_especie)
        db.commit()
    return db_especie

def update_especie(db: Session, especie_id: int, especie: schemas.EspecieCreate):
    db_especie = db.query(models.Especie).filter(models.Especie.id_especie == especie_id).first()
    if db_especie:
        for key, value in especie.dict().items():
            setattr(db_especie, key, value)
        db.commit()
        db.refresh(db_especie)
    return db_especie

# CRUD para Usuario
def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    if db_usuario:
        for key, value in usuario.dict().items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

# CRUD para Arbol
def get_arboles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Arbol).offset(skip).limit(limit).all()

def get_arbol(db: Session, arbol_id: int):
    return db.query(models.Arbol).filter(models.Arbol.id_arbol == arbol_id).first()

def create_arbol(db: Session, arbol: schemas.ArbolCreate):
    db_arbol = models.Arbol(**arbol.dict())
    db.add(db_arbol)
    db.commit()
    db.refresh(db_arbol)
    return db_arbol

def delete_arbol(db: Session, arbol_id: int):
    db_arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == arbol_id).first()
    if db_arbol:
        db.delete(db_arbol)
        db.commit()
    return db_arbol

def update_arbol(db: Session, arbol_id: int, arbol: schemas.ArbolCreate):
    db_arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == arbol_id).first()
    if db_arbol:
        for key, value in arbol.dict().items():
            setattr(db_arbol, key, value)
        db.commit()
        db.refresh(db_arbol)
    return db_arbol

# CRUD para Medicion
def get_mediciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Medicion).offset(skip).limit(limit).all()

def get_medicion(db: Session, medicion_id: int):
    return db.query(models.Medicion).filter(models.Medicion.id_medicion == medicion_id).first()

def create_medicion(db: Session, medicion: schemas.MedicionCreate):
    db_medicion = models.Medicion(**medicion.dict())
    db.add(db_medicion)
    db.commit()
    db.refresh(db_medicion)
    return db_medicion

def delete_medicion(db: Session, medicion_id: int):
    db_medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == medicion_id).first()
    if db_medicion:
        db.delete(db_medicion)
        db.commit()
    return db_medicion

def update_medicion(db: Session, medicion_id: int, medicion: schemas.MedicionCreate):
    db_medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == medicion_id).first()
    if db_medicion:
        for key, value in medicion.dict().items():
            setattr(db_medicion, key, value)
        db.commit()
        db.refresh(db_medicion)
    return db_medicion

# CRUD para Foto
def get_fotos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Foto).offset(skip).limit(limit).all()

def get_foto(db: Session, foto_id: int):
    return db.query(models.Foto).filter(models.Foto.id_foto == foto_id).first()

def create_foto(db: Session, foto: schemas.FotoCreate):
    db_foto = models.Foto(**foto.dict())
    db.add(db_foto)
    db.commit()
    db.refresh(db_foto)
    return db_foto

def delete_foto(db: Session, foto_id: int):
    db_foto = db.query(models.Foto).filter(models.Foto.id_foto == foto_id).first()
    if db_foto:
        db.delete(db_foto)
        db.commit()
    return db_foto

def update_foto(db: Session, foto_id: int, foto: schemas.FotoCreate):
    db_foto = db.query(models.Foto).filter(models.Foto.id_foto == foto_id).first()
    if db_foto:
        for key, value in foto.dict().items():
            setattr(db_foto, key, value)
        db.commit()
        db.refresh(db_foto)
    return db_foto
