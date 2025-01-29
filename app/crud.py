from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas

# Valores permitidos para los campos restringidos
ALTURA_VALUES = {"1-2 m", ">3 m", "3-5 m", "> 5m"}
DIAMETRO_TRONCO_VALUES = {"1-5 cm", "5-15 cm", "> 15 cm", "Especificar"}
AMBITO_VALUES = {"Urbano", "Rural", "Otro"}
INTERFERENCIA_AEREA_VALUES = {"Línea alta", "Iluminaria y media", "Baja"}
TIPO_CABLE_VALUES = {"Preensamblado", "Cable desnudo", ""}
TIPO_INTERVENCION_VALUES = {"Poda de altura", "Poda de formación", "Poda de aclareo", "Raleo", "Aplicación de fungicida", ""}


# --- CRUD para Provincia ---
def get_provincias(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de provincias con paginación."""
    return db.query(models.Provincia).offset(skip).limit(limit).all()

def get_provincia(db: Session, provincia_id: int):
    """Obtiene una provincia específica por su ID."""
    provincia = db.query(models.Provincia).filter(models.Provincia.id_provincia == provincia_id).first()
    if not provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    return provincia

def create_provincia(db: Session, provincia: schemas.ProvinciaCreate):
    """Crea una nueva provincia en la base de datos."""
    # Normalizar nombre para evitar inconsistencias
    nombre_normalizado = provincia.nombre.strip().title()

    # Verificar si el nombre ya existe (ignorar mayúsculas/minúsculas)
    if db.query(models.Provincia).filter(models.Provincia.nombre.ilike(nombre_normalizado)).first():
        raise HTTPException(status_code=400, detail=f"La provincia '{nombre_normalizado}' ya existe.")

    # Crear la provincia
    db_provincia = models.Provincia(nombre=nombre_normalizado)
    try:
        db.add(db_provincia)
        db.commit()
        db.refresh(db_provincia)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear la provincia.")
    
    return db_provincia

def update_provincia(db: Session, provincia_id: int, provincia: schemas.ProvinciaCreate):
    """Actualiza una provincia existente por su ID."""
    db_provincia = db.query(models.Provincia).filter(models.Provincia.id_provincia == provincia_id).first()
    if not db_provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")

    # Normalizar nombre
    nombre_normalizado = provincia.nombre.strip().title()

    # Validar duplicados para otros registros
    if db.query(models.Provincia).filter(models.Provincia.nombre.ilike(nombre_normalizado), models.Provincia.id_provincia != provincia_id).first():
        raise HTTPException(status_code=400, detail=f"Ya existe otra provincia con el nombre '{nombre_normalizado}'.")

    # Actualizar la provincia
    db_provincia.nombre = nombre_normalizado
    db.commit()
    db.refresh(db_provincia)
    
    return db_provincia

def delete_provincia(db: Session, provincia_id: int):
    """Elimina una provincia si existe."""
    db_provincia = db.query(models.Provincia).filter(models.Provincia.id_provincia == provincia_id).first()
    if not db_provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")

    # Eliminar la provincia
    db.delete(db_provincia)
    db.commit()
    
    return {"detail": f"Provincia '{db_provincia.nombre}' eliminada exitosamente."}


# --- CRUD para Municipio ---
def get_municipios(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de municipios con paginación."""
    return db.query(models.Municipio).offset(skip).limit(limit).all()

def get_municipio(db: Session, municipio_id: int):
    """Obtiene un municipio específico por su ID."""
    municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == municipio_id).first()
    if not municipio:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    return municipio

def create_municipio(db: Session, municipio: schemas.MunicipioCreate):
    """Crea un nuevo municipio en la base de datos."""
    # Normalizar nombre para evitar inconsistencias
    nombre_normalizado = municipio.nombre.strip().title()

    # Verificar si el municipio ya existe en la misma provincia (ignorando mayúsculas/minúsculas)
    existing_municipio = db.query(models.Municipio).filter(
        models.Municipio.nombre.ilike(nombre_normalizado),
        models.Municipio.id_provincia == municipio.id_provincia
    ).first()
    if existing_municipio:
        raise HTTPException(status_code=400, detail=f"El municipio '{nombre_normalizado}' ya existe en esta provincia.")
    
    # Crear un nuevo municipio
    db_municipio = models.Municipio(
        id_provincia=municipio.id_provincia,
        nombre=nombre_normalizado,
        latitude=municipio.latitude,
        longitude=municipio.longitude
    )
    try:
        db.add(db_municipio)
        db.commit()
        db.refresh(db_municipio)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el municipio.")
    
    return db_municipio

def update_municipio(db: Session, municipio_id: int, municipio: schemas.MunicipioCreate):
    """Actualiza un municipio existente por su ID."""
    db_municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == municipio_id).first()
    if not db_municipio:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")

    # Normalizar nombre
    nombre_normalizado = municipio.nombre.strip().title()

    # Validar que no haya duplicados al actualizar el nombre
    existing_municipio = db.query(models.Municipio).filter(
        models.Municipio.nombre.ilike(nombre_normalizado),
        models.Municipio.id_provincia == municipio.id_provincia,
        models.Municipio.id_municipio != municipio_id
    ).first()
    if existing_municipio:
        raise HTTPException(status_code=400, detail=f"Ya existe otro municipio con el nombre '{nombre_normalizado}' en esta provincia.")
    
    # Actualizar los datos del municipio
    db_municipio.nombre = nombre_normalizado
    db_municipio.latitude = municipio.latitude
    db_municipio.longitude = municipio.longitude

    db.commit()
    db.refresh(db_municipio)
    return db_municipio

def delete_municipio(db: Session, municipio_id: int):
    """Elimina un municipio si existe."""
    db_municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == municipio_id).first()
    if not db_municipio:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    
    # Eliminar el municipio
    db.delete(db_municipio)
    db.commit()
    
    return {"detail": f"Municipio '{db_municipio.nombre}' eliminado exitosamente."}



# --- CRUD para Role ---
def get_roles(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de roles con paginación."""
    return db.query(models.Role).offset(skip).limit(limit).all()

def get_role(db: Session, role_id: int):
    """Obtiene un rol específico por su ID."""
    db_role = db.query(models.Role).filter(models.Role.id_role == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_role

def create_role(db: Session, role: schemas.RoleCreate):
    """Crea un nuevo rol en la base de datos."""
    # Normalizar el nombre del rol para evitar duplicados
    role_name_normalizado = role.role_name.strip().title()

    # Verificar si el rol ya existe (ignorando mayúsculas/minúsculas)
    existing_role = db.query(models.Role).filter(models.Role.role_name.ilike(role_name_normalizado)).first()
    if existing_role:
        raise HTTPException(status_code=400, detail=f"El rol '{role_name_normalizado}' ya existe.")
    
    # Crear un nuevo rol
    db_role = models.Role(
        role_name=role_name_normalizado,
        can_manage_users=role.can_manage_users,
        can_manage_all_relevamientos=role.can_manage_all_relevamientos,
        can_create_relevamientos=role.can_create_relevamientos,
        can_modify_own_relevamientos=role.can_modify_own_relevamientos,
        can_generate_reports=role.can_generate_reports
    )

    try:
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el rol.")
    
    return db_role

def update_role(db: Session, role_id: int, role: schemas.RoleCreate):
    """Actualiza un rol existente por su ID."""
    db_role = db.query(models.Role).filter(models.Role.id_role == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Normalizar nombre
    role_name_normalizado = role.role_name.strip().title()

    # Validar que no haya duplicados al actualizar el nombre del rol
    existing_role = db.query(models.Role).filter(
        models.Role.role_name.ilike(role_name_normalizado),
        models.Role.id_role != role_id
    ).first()
    if existing_role:
        raise HTTPException(status_code=400, detail=f"Ya existe otro rol con el nombre '{role_name_normalizado}'.")
    
    # Actualizar los datos del rol
    db_role.role_name = role_name_normalizado
    db_role.can_manage_users = role.can_manage_users
    db_role.can_manage_all_relevamientos = role.can_manage_all_relevamientos
    db_role.can_create_relevamientos = role.can_create_relevamientos
    db_role.can_modify_own_relevamientos = role.can_modify_own_relevamientos
    db_role.can_generate_reports = role.can_generate_reports

    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int):
    """Elimina un rol si existe."""
    db_role = db.query(models.Role).filter(models.Role.id_role == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Eliminar el rol
    db.delete(db_role)
    db.commit()
    
    return {"detail": f"Rol '{db_role.role_name}' eliminado exitosamente."}


# --- CRUD para Usuario ---
def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de usuarios con paginación."""
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def get_usuario(db: Session, usuario_id: int):
    """Obtiene un usuario específico por su ID."""
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    """Crea un nuevo usuario en la base de datos."""
    # Normalizar email y nombre
    email_normalizado = usuario.email.strip().lower()
    nombre_normalizado = usuario.nombre.strip().title()

    # Validar que el correo electrónico sea único
    existing_usuario = db.query(models.Usuario).filter(models.Usuario.email == email_normalizado).first()
    if existing_usuario:
        raise HTTPException(status_code=400, detail=f"El correo '{email_normalizado}' ya está en uso.")

    # Verificar que el municipio y el rol existen antes de asignarlos
    municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == usuario.id_municipio).first()
    role = db.query(models.Role).filter(models.Role.id_role == usuario.id_role).first()
    
    if not municipio:
        raise HTTPException(status_code=400, detail=f"El municipio con ID {usuario.id_municipio} no existe.")
    if not role:
        raise HTTPException(status_code=400, detail=f"El rol con ID {usuario.id_role} no existe.")

    # Crear el usuario
    db_usuario = models.Usuario(
        id_municipio=usuario.id_municipio,
        id_role=usuario.id_role,
        nombre=nombre_normalizado,
        email=email_normalizado,
        is_active=usuario.is_active,
        is_superuser=usuario.is_superuser,
        date_joined=usuario.date_joined,
        created_by=usuario.created_by
    )

    try:
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el usuario.")
    
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    """Actualiza un usuario existente por su ID."""
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Normalizar email y nombre
    email_normalizado = usuario.email.strip().lower()
    nombre_normalizado = usuario.nombre.strip().title()

    # Validar que no haya duplicados al actualizar el correo electrónico
    existing_usuario = db.query(models.Usuario).filter(
        models.Usuario.email == email_normalizado,
        models.Usuario.id_usuario != usuario_id
    ).first()
    if existing_usuario:
        raise HTTPException(status_code=400, detail=f"El correo '{email_normalizado}' ya está en uso por otro usuario.")

    # Validar que el municipio y rol existan si se cambian
    if usuario.id_municipio and usuario.id_municipio != db_usuario.id_municipio:
        municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == usuario.id_municipio).first()
        if not municipio:
            raise HTTPException(status_code=400, detail=f"El municipio con ID {usuario.id_municipio} no existe.")

    if usuario.id_role and usuario.id_role != db_usuario.id_role:
        role = db.query(models.Role).filter(models.Role.id_role == usuario.id_role).first()
        if not role:
            raise HTTPException(status_code=400, detail=f"El rol con ID {usuario.id_role} no existe.")

    # Actualizar los datos del usuario
    db_usuario.nombre = nombre_normalizado
    db_usuario.email = email_normalizado
    db_usuario.is_active = usuario.is_active
    db_usuario.is_superuser = usuario.is_superuser
    db_usuario.date_joined = usuario.date_joined
    db_usuario.id_municipio = usuario.id_municipio
    db_usuario.id_role = usuario.id_role
    db_usuario.created_by = usuario.created_by

    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    """Elimina un usuario si existe."""
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar el usuario
    db.delete(db_usuario)
    db.commit()
    
    return {"detail": f"Usuario '{db_usuario.email}' eliminado exitosamente."}


# --- CRUD para Especie ---
def get_especies(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de especies con paginación."""
    return db.query(models.Especie).offset(skip).limit(limit).all()

def get_especie(db: Session, especie_id: int):
    """Obtiene una especie específica por su ID."""
    db_especie = db.query(models.Especie).filter(models.Especie.id_especie == especie_id).first()
    if not db_especie:
        raise HTTPException(status_code=404, detail="Especie no encontrada")
    return db_especie

def create_especie(db: Session, especie: schemas.EspecieCreate):
    """Crea una nueva especie en la base de datos."""
    # Normalizar nombres
    nombre_cientifico_normalizado = especie.nombre_cientifico.strip().capitalize()
    nombre_comun_normalizado = especie.nombre_comun.strip().title()
    origen_normalizado = especie.origen.strip().lower()

    # Validar que el nombre científico sea único
    existing_especie = db.query(models.Especie).filter(
        models.Especie.nombre_cientifico == nombre_cientifico_normalizado
    ).first()
    
    if existing_especie:
        raise HTTPException(
            status_code=400,
            detail=f"La especie con nombre científico '{nombre_cientifico_normalizado}' ya existe."
        )

    # Crear la especie
    db_especie = models.Especie(
        nombre_cientifico=nombre_cientifico_normalizado,
        nombre_comun=nombre_comun_normalizado,
        origen=origen_normalizado
    )

    try:
        db.add(db_especie)
        db.commit()
        db.refresh(db_especie)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear la especie.")
    
    return db_especie

def update_especie(db: Session, especie_id: int, especie: schemas.EspecieCreate):
    """Actualiza una especie existente por su ID."""
    db_especie = db.query(models.Especie).filter(models.Especie.id_especie == especie_id).first()
    if not db_especie:
        raise HTTPException(status_code=404, detail="Especie no encontrada")

    # Normalizar nombres
    nombre_cientifico_normalizado = especie.nombre_cientifico.strip().capitalize()
    nombre_comun_normalizado = especie.nombre_comun.strip().title()
    origen_normalizado = especie.origen.strip().lower()

    # Validar que el nombre científico no se repita al actualizar
    existing_especie = db.query(models.Especie).filter(
        models.Especie.nombre_cientifico == nombre_cientifico_normalizado,
        models.Especie.id_especie != especie_id
    ).first()
    
    if existing_especie:
        raise HTTPException(
            status_code=400,
            detail=f"El nombre científico '{nombre_cientifico_normalizado}' ya está en uso por otra especie."
        )

    # Actualizar datos de la especie
    db_especie.nombre_cientifico = nombre_cientifico_normalizado
    db_especie.nombre_comun = nombre_comun_normalizado
    db_especie.origen = origen_normalizado

    db.commit()
    db.refresh(db_especie)
    return db_especie

def delete_especie(db: Session, especie_id: int):
    """Elimina una especie si existe."""
    db_especie = db.query(models.Especie).filter(models.Especie.id_especie == especie_id).first()
    if not db_especie:
        raise HTTPException(status_code=404, detail="Especie no encontrada")

    # Eliminar la especie
    db.delete(db_especie)
    db.commit()
    
    return {"detail": f"Especie '{db_especie.nombre_cientifico}' eliminada exitosamente."}



# --- CRUD para Arbol ---
def get_arboles(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de árboles con paginación."""
    return db.query(models.Arbol).offset(skip).limit(limit).all()

def get_arbol(db: Session, arbol_id: int):
    """Obtiene un árbol específico por su ID."""
    db_arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == arbol_id).first()
    if not db_arbol:
        raise HTTPException(status_code=404, detail="Árbol no encontrado")
    return db_arbol

def create_arbol(db: Session, arbol: schemas.ArbolCreate):
    """Crea un nuevo árbol en la base de datos."""
    # Validar existencia de municipio y especie
    municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == arbol.id_municipio).first()
    especie = db.query(models.Especie).filter(models.Especie.id_especie == arbol.id_especie).first()

    if not municipio:
        raise HTTPException(status_code=400, detail=f"El municipio con ID {arbol.id_municipio} no existe.")
    if not especie:
        raise HTTPException(status_code=400, detail=f"La especie con ID {arbol.id_especie} no existe.")

    # Normalizar datos
    arbol_data = arbol.dict()
    arbol_data["calle"] = arbol_data["calle"].strip().title() if arbol_data["calle"] else None
    arbol_data["barrio"] = arbol_data["barrio"].strip().title() if arbol_data["barrio"] else None
    arbol_data["identificacion"] = arbol_data["identificacion"].strip() if arbol_data["identificacion"] else None

    # Crear el árbol
    db_arbol = models.Arbol(**arbol_data)
    try:
        db.add(db_arbol)
        db.commit()
        db.refresh(db_arbol)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el árbol.")

    return db_arbol

def update_arbol(db: Session, arbol_id: int, arbol: schemas.ArbolCreate):
    """Actualiza un árbol existente por su ID."""
    db_arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == arbol_id).first()
    if not db_arbol:
        raise HTTPException(status_code=404, detail="Árbol no encontrado")

    # Validar que el municipio y la especie existan antes de actualizar
    if arbol.id_municipio:
        municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == arbol.id_municipio).first()
        if not municipio:
            raise HTTPException(status_code=400, detail=f"El municipio con ID {arbol.id_municipio} no existe.")

    if arbol.id_especie:
        especie = db.query(models.Especie).filter(models.Especie.id_especie == arbol.id_especie).first()
        if not especie:
            raise HTTPException(status_code=400, detail=f"La especie con ID {arbol.id_especie} no existe.")

    # Normalizar datos antes de actualizar
    arbol_data = arbol.dict()
    arbol_data["calle"] = arbol_data["calle"].strip().title() if arbol_data["calle"] else None
    arbol_data["barrio"] = arbol_data["barrio"].strip().title() if arbol_data["barrio"] else None
    arbol_data["identificacion"] = arbol_data["identificacion"].strip() if arbol_data["identificacion"] else None

    # Actualizar los campos del árbol
    for key, value in arbol_data.items():
        setattr(db_arbol, key, value)
    db.commit()
    db.refresh(db_arbol)
    return db_arbol

def delete_arbol(db: Session, arbol_id: int):
    """Elimina un árbol si existe."""
    db_arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == arbol_id).first()
    if not db_arbol:
        raise HTTPException(status_code=404, detail="Árbol no encontrado")

    # Eliminar el árbol
    db.delete(db_arbol)
    db.commit()
    
    return {"detail": f"Árbol con ID {arbol_id} eliminado exitosamente."}


# --- CRUD para Medición ---
def get_mediciones(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de mediciones con paginación."""
    return db.query(models.Medicion).offset(skip).limit(limit).all()

def get_medicion(db: Session, medicion_id: int):
    """Obtiene una medición específica por su ID."""
    db_medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == medicion_id).first()
    if not db_medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    return db_medicion

def create_medicion(db: Session, medicion: schemas.MedicionCreate):
    """Crea una nueva medición en la base de datos."""
    # Validar que el árbol y el usuario existan antes de crear la medición
    arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == medicion.id_arbol).first()
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == medicion.id_usuario).first()

    if not arbol:
        raise HTTPException(status_code=400, detail=f"El árbol con ID {medicion.id_arbol} no existe.")
    if not usuario:
        raise HTTPException(status_code=400, detail=f"El usuario con ID {medicion.id_usuario} no existe.")

    # Normalizar datos antes de crear la medición
    medicion_data = medicion.dict()
    medicion_data["tratamiento_previo"] = medicion_data["tratamiento_previo"].strip().title() if medicion_data["tratamiento_previo"] else None
    medicion_data["cazuela"] = medicion_data["cazuela"].strip().title() if medicion_data["cazuela"] else None

    # Crear la medición
    db_medicion = models.Medicion(**medicion_data)
    try:
        db.add(db_medicion)
        db.commit()
        db.refresh(db_medicion)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear la medición.")

    return db_medicion

def update_medicion(db: Session, medicion_id: int, medicion: schemas.MedicionCreate):
    """Actualiza una medición existente por su ID."""
    db_medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == medicion_id).first()
    if not db_medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")

    # Validar que el árbol y el usuario existan antes de actualizar
    if medicion.id_arbol:
        arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == medicion.id_arbol).first()
        if not arbol:
            raise HTTPException(status_code=400, detail=f"El árbol con ID {medicion.id_arbol} no existe.")

    if medicion.id_usuario:
        usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == medicion.id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=400, detail=f"El usuario con ID {medicion.id_usuario} no existe.")

    # Normalizar datos antes de actualizar la medición
    medicion_data = medicion.dict()
    medicion_data["tratamiento_previo"] = medicion_data["tratamiento_previo"].strip().title() if medicion_data["tratamiento_previo"] else None
    medicion_data["cazuela"] = medicion_data["cazuela"].strip().title() if medicion_data["cazuela"] else None

    # Actualizar los campos de la medición
    for key, value in medicion_data.items():
        setattr(db_medicion, key, value)
    db.commit()
    db.refresh(db_medicion)
    return db_medicion

def delete_medicion(db: Session, medicion_id: int):
    """Elimina una medición si existe."""
    db_medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == medicion_id).first()
    if not db_medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")

    # Eliminar la medición
    db.delete(db_medicion)
    db.commit()
    
    return {"detail": f"Medición con ID {medicion_id} eliminada exitosamente."}


# --- CRUD para Foto ---
def get_fotos(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de fotos con paginación."""
    return db.query(models.Foto).offset(skip).limit(limit).all()

def get_foto(db: Session, foto_id: int):
    """Obtiene una foto específica por su ID."""
    db_foto = db.query(models.Foto).filter(models.Foto.id_foto == foto_id).first()
    if not db_foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return db_foto

def create_foto(db: Session, foto: schemas.FotoCreate):
    """Crea una nueva foto asociada a una medición."""
    # Validar que la medición asociada exista
    medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == foto.id_medicion).first()
    if not medicion:
        raise HTTPException(status_code=400, detail=f"La medición con ID {foto.id_medicion} no existe.")

    # Normalizar datos antes de insertar
    foto_data = foto.dict()
    foto_data["tipo_foto"] = foto_data["tipo_foto"].strip().title()
    foto_data["ruta_foto"] = foto_data["ruta_foto"].strip()

    # Crear la foto
    db_foto = models.Foto(**foto_data)
    try:
        db.add(db_foto)
        db.commit()
        db.refresh(db_foto)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear la foto.")

    return db_foto

def update_foto(db: Session, foto_id: int, foto: schemas.FotoCreate):
    """Actualiza una foto existente por su ID."""
    db_foto = db.query(models.Foto).filter(models.Foto.id_foto == foto_id).first()
    if not db_foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    # Validar que la medición asociada exista si se cambia
    if foto.id_medicion and foto.id_medicion != db_foto.id_medicion:
        medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == foto.id_medicion).first()
        if not medicion:
            raise HTTPException(status_code=400, detail=f"La medición con ID {foto.id_medicion} no existe.")

    # Normalizar datos antes de actualizar
    foto_data = foto.dict()
    foto_data["tipo_foto"] = foto_data["tipo_foto"].strip().title()
    foto_data["ruta_foto"] = foto_data["ruta_foto"].strip()
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from . import models, schemas

# Valores permitidos para los campos restringidos
ALTURA_VALUES = {"1-2 m", ">3 m", "3-5 m", "> 5m"}
DIAMETRO_TRONCO_VALUES = {"1-5 cm", "5-15 cm", "> 15 cm", "Especificar"}
AMBITO_VALUES = {"Urbano", "Rural", "Otro"}
INTERFERENCIA_AEREA_VALUES = {"Línea alta", "Iluminaria y media", "Baja"}
TIPO_CABLE_VALUES = {"Preensamblado", "Cable desnudo", ""}
TIPO_INTERVENCION_VALUES = {"Poda de altura", "Poda de formación", "Poda de aclareo", "Raleo", "Aplicación de fungicida", ""}


# --- CRUD para Provincia ---
def get_provincias(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de provincias con paginación."""
    return db.query(models.Provincia).offset(skip).limit(limit).all()

def get_provincia(db: Session, provincia_id: int):
    """Obtiene una provincia específica por su ID."""
    provincia = db.query(models.Provincia).filter(models.Provincia.id_provincia == provincia_id).first()
    if not provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    return provincia

def create_provincia(db: Session, provincia: schemas.ProvinciaCreate):
    """Crea una nueva provincia en la base de datos."""
    # Normalizar nombre para evitar inconsistencias
    nombre_normalizado = provincia.nombre.strip().title()

    # Verificar si el nombre ya existe (ignorar mayúsculas/minúsculas)
    if db.query(models.Provincia).filter(models.Provincia.nombre.ilike(nombre_normalizado)).first():
        raise HTTPException(status_code=400, detail=f"La provincia '{nombre_normalizado}' ya existe.")

    # Crear la provincia
    db_provincia = models.Provincia(nombre=nombre_normalizado)
    try:
        db.add(db_provincia)
        db.commit()
        db.refresh(db_provincia)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear la provincia.")
    
    return db_provincia

def update_provincia(db: Session, provincia_id: int, provincia: schemas.ProvinciaCreate):
    """Actualiza una provincia existente por su ID."""
    db_provincia = db.query(models.Provincia).filter(models.Provincia.id_provincia == provincia_id).first()
    if not db_provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")

    # Normalizar nombre
    nombre_normalizado = provincia.nombre.strip().title()

    # Validar duplicados para otros registros
    if db.query(models.Provincia).filter(models.Provincia.nombre.ilike(nombre_normalizado), models.Provincia.id_provincia != provincia_id).first():
        raise HTTPException(status_code=400, detail=f"Ya existe otra provincia con el nombre '{nombre_normalizado}'.")

    # Actualizar la provincia
    db_provincia.nombre = nombre_normalizado
    db.commit()
    db.refresh(db_provincia)
    
    return db_provincia

def delete_provincia(db: Session, provincia_id: int):
    """Elimina una provincia si existe."""
    db_provincia = db.query(models.Provincia).filter(models.Provincia.id_provincia == provincia_id).first()
    if not db_provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")

    # Eliminar la provincia
    db.delete(db_provincia)
    db.commit()
    
    return {"detail": f"Provincia '{db_provincia.nombre}' eliminada exitosamente."}


# --- CRUD para Municipio ---
def get_municipios(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de municipios con paginación."""
    return db.query(models.Municipio).offset(skip).limit(limit).all()

def get_municipio(db: Session, municipio_id: int):
    """Obtiene un municipio específico por su ID."""
    municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == municipio_id).first()
    if not municipio:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    return municipio

def create_municipio(db: Session, municipio: schemas.MunicipioCreate):
    """Crea un nuevo municipio en la base de datos."""
    # Normalizar nombre para evitar inconsistencias
    nombre_normalizado = municipio.nombre.strip().title()

    # Verificar si el municipio ya existe en la misma provincia (ignorando mayúsculas/minúsculas)
    existing_municipio = db.query(models.Municipio).filter(
        models.Municipio.nombre.ilike(nombre_normalizado),
        models.Municipio.id_provincia == municipio.id_provincia
    ).first()
    if existing_municipio:
        raise HTTPException(status_code=400, detail=f"El municipio '{nombre_normalizado}' ya existe en esta provincia.")
    
    # Crear un nuevo municipio
    db_municipio = models.Municipio(
        id_provincia=municipio.id_provincia,
        nombre=nombre_normalizado,
        latitude=municipio.latitude,
        longitude=municipio.longitude
    )
    try:
        db.add(db_municipio)
        db.commit()
        db.refresh(db_municipio)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el municipio.")
    
    return db_municipio

def update_municipio(db: Session, municipio_id: int, municipio: schemas.MunicipioCreate):
    """Actualiza un municipio existente por su ID."""
    db_municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == municipio_id).first()
    if not db_municipio:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")

    # Normalizar nombre
    nombre_normalizado = municipio.nombre.strip().title()

    # Validar que no haya duplicados al actualizar el nombre
    existing_municipio = db.query(models.Municipio).filter(
        models.Municipio.nombre.ilike(nombre_normalizado),
        models.Municipio.id_provincia == municipio.id_provincia,
        models.Municipio.id_municipio != municipio_id
    ).first()
    if existing_municipio:
        raise HTTPException(status_code=400, detail=f"Ya existe otro municipio con el nombre '{nombre_normalizado}' en esta provincia.")
    
    # Actualizar los datos del municipio
    db_municipio.nombre = nombre_normalizado
    db_municipio.latitude = municipio.latitude
    db_municipio.longitude = municipio.longitude

    db.commit()
    db.refresh(db_municipio)
    return db_municipio

def delete_municipio(db: Session, municipio_id: int):
    """Elimina un municipio si existe."""
    db_municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == municipio_id).first()
    if not db_municipio:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    
    # Eliminar el municipio
    db.delete(db_municipio)
    db.commit()
    
    return {"detail": f"Municipio '{db_municipio.nombre}' eliminado exitosamente."}



# --- CRUD para Role ---
def get_roles(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de roles con paginación."""
    return db.query(models.Role).offset(skip).limit(limit).all()

def get_role(db: Session, role_id: int):
    """Obtiene un rol específico por su ID."""
    db_role = db.query(models.Role).filter(models.Role.id_role == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_role

def create_role(db: Session, role: schemas.RoleCreate):
    """Crea un nuevo rol en la base de datos."""
    # Normalizar el nombre del rol para evitar duplicados
    role_name_normalizado = role.role_name.strip().title()

    # Verificar si el rol ya existe (ignorando mayúsculas/minúsculas)
    existing_role = db.query(models.Role).filter(models.Role.role_name.ilike(role_name_normalizado)).first()
    if existing_role:
        raise HTTPException(status_code=400, detail=f"El rol '{role_name_normalizado}' ya existe.")
    
    # Crear un nuevo rol
    db_role = models.Role(
        role_name=role_name_normalizado,
        can_manage_users=role.can_manage_users,
        can_manage_all_relevamientos=role.can_manage_all_relevamientos,
        can_create_relevamientos=role.can_create_relevamientos,
        can_modify_own_relevamientos=role.can_modify_own_relevamientos,
        can_generate_reports=role.can_generate_reports
    )

    try:
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el rol.")
    
    return db_role

def update_role(db: Session, role_id: int, role: schemas.RoleCreate):
    """Actualiza un rol existente por su ID."""
    db_role = db.query(models.Role).filter(models.Role.id_role == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Normalizar nombre
    role_name_normalizado = role.role_name.strip().title()

    # Validar que no haya duplicados al actualizar el nombre del rol
    existing_role = db.query(models.Role).filter(
        models.Role.role_name.ilike(role_name_normalizado),
        models.Role.id_role != role_id
    ).first()
    if existing_role:
        raise HTTPException(status_code=400, detail=f"Ya existe otro rol con el nombre '{role_name_normalizado}'.")
    
    # Actualizar los datos del rol
    db_role.role_name = role_name_normalizado
    db_role.can_manage_users = role.can_manage_users
    db_role.can_manage_all_relevamientos = role.can_manage_all_relevamientos
    db_role.can_create_relevamientos = role.can_create_relevamientos
    db_role.can_modify_own_relevamientos = role.can_modify_own_relevamientos
    db_role.can_generate_reports = role.can_generate_reports

    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int):
    """Elimina un rol si existe."""
    db_role = db.query(models.Role).filter(models.Role.id_role == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Eliminar el rol
    db.delete(db_role)
    db.commit()
    
    return {"detail": f"Rol '{db_role.role_name}' eliminado exitosamente."}


# --- CRUD para Usuario ---
def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de usuarios con paginación."""
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def get_usuario(db: Session, usuario_id: int):
    """Obtiene un usuario específico por su ID."""
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    """Crea un nuevo usuario en la base de datos."""
    # Normalizar email y nombre
    email_normalizado = usuario.email.strip().lower()
    nombre_normalizado = usuario.nombre.strip().title()

    # Validar que el correo electrónico sea único
    existing_usuario = db.query(models.Usuario).filter(models.Usuario.email == email_normalizado).first()
    if existing_usuario:
        raise HTTPException(status_code=400, detail=f"El correo '{email_normalizado}' ya está en uso.")

    # Verificar que el municipio y el rol existen antes de asignarlos
    municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == usuario.id_municipio).first()
    role = db.query(models.Role).filter(models.Role.id_role == usuario.id_role).first()
    
    if not municipio:
        raise HTTPException(status_code=400, detail=f"El municipio con ID {usuario.id_municipio} no existe.")
    if not role:
        raise HTTPException(status_code=400, detail=f"El rol con ID {usuario.id_role} no existe.")

    # Crear el usuario
    db_usuario = models.Usuario(
        id_municipio=usuario.id_municipio,
        id_role=usuario.id_role,
        nombre=nombre_normalizado,
        email=email_normalizado,
        is_active=usuario.is_active,
        is_superuser=usuario.is_superuser,
        date_joined=usuario.date_joined,
        created_by=usuario.created_by
    )

    try:
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el usuario.")
    
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    """Actualiza un usuario existente por su ID."""
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Normalizar email y nombre
    email_normalizado = usuario.email.strip().lower()
    nombre_normalizado = usuario.nombre.strip().title()

    # Validar que no haya duplicados al actualizar el correo electrónico
    existing_usuario = db.query(models.Usuario).filter(
        models.Usuario.email == email_normalizado,
        models.Usuario.id_usuario != usuario_id
    ).first()
    if existing_usuario:
        raise HTTPException(status_code=400, detail=f"El correo '{email_normalizado}' ya está en uso por otro usuario.")

    # Validar que el municipio y rol existan si se cambian
    if usuario.id_municipio and usuario.id_municipio != db_usuario.id_municipio:
        municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == usuario.id_municipio).first()
        if not municipio:
            raise HTTPException(status_code=400, detail=f"El municipio con ID {usuario.id_municipio} no existe.")

    if usuario.id_role and usuario.id_role != db_usuario.id_role:
        role = db.query(models.Role).filter(models.Role.id_role == usuario.id_role).first()
        if not role:
            raise HTTPException(status_code=400, detail=f"El rol con ID {usuario.id_role} no existe.")

    # Actualizar los datos del usuario
    db_usuario.nombre = nombre_normalizado
    db_usuario.email = email_normalizado
    db_usuario.is_active = usuario.is_active
    db_usuario.is_superuser = usuario.is_superuser
    db_usuario.date_joined = usuario.date_joined
    db_usuario.id_municipio = usuario.id_municipio
    db_usuario.id_role = usuario.id_role
    db_usuario.created_by = usuario.created_by

    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    """Elimina un usuario si existe."""
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar el usuario
    db.delete(db_usuario)
    db.commit()
    
    return {"detail": f"Usuario '{db_usuario.email}' eliminado exitosamente."}


# --- CRUD para Especie ---
def get_especies(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de especies con paginación."""
    return db.query(models.Especie).offset(skip).limit(limit).all()

def get_especie(db: Session, especie_id: int):
    """Obtiene una especie específica por su ID."""
    db_especie = db.query(models.Especie).filter(models.Especie.id_especie == especie_id).first()
    if not db_especie:
        raise HTTPException(status_code=404, detail="Especie no encontrada")
    return db_especie

def create_especie(db: Session, especie: schemas.EspecieCreate):
    """Crea una nueva especie en la base de datos."""
    # Normalizar nombres
    nombre_cientifico_normalizado = especie.nombre_cientifico.strip().capitalize()
    nombre_comun_normalizado = especie.nombre_comun.strip().title()
    origen_normalizado = especie.origen.strip().lower()

    # Validar que el nombre científico sea único
    existing_especie = db.query(models.Especie).filter(
        models.Especie.nombre_cientifico == nombre_cientifico_normalizado
    ).first()
    
    if existing_especie:
        raise HTTPException(
            status_code=400,
            detail=f"La especie con nombre científico '{nombre_cientifico_normalizado}' ya existe."
        )

    # Crear la especie
    db_especie = models.Especie(
        nombre_cientifico=nombre_cientifico_normalizado,
        nombre_comun=nombre_comun_normalizado,
        origen=origen_normalizado
    )

    try:
        db.add(db_especie)
        db.commit()
        db.refresh(db_especie)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear la especie.")
    
    return db_especie

def update_especie(db: Session, especie_id: int, especie: schemas.EspecieCreate):
    """Actualiza una especie existente por su ID."""
    db_especie = db.query(models.Especie).filter(models.Especie.id_especie == especie_id).first()
    if not db_especie:
        raise HTTPException(status_code=404, detail="Especie no encontrada")

    # Normalizar nombres
    nombre_cientifico_normalizado = especie.nombre_cientifico.strip().capitalize()
    nombre_comun_normalizado = especie.nombre_comun.strip().title()
    origen_normalizado = especie.origen.strip().lower()

    # Validar que el nombre científico no se repita al actualizar
    existing_especie = db.query(models.Especie).filter(
        models.Especie.nombre_cientifico == nombre_cientifico_normalizado,
        models.Especie.id_especie != especie_id
    ).first()
    
    if existing_especie:
        raise HTTPException(
            status_code=400,
            detail=f"El nombre científico '{nombre_cientifico_normalizado}' ya está en uso por otra especie."
        )

    # Actualizar datos de la especie
    db_especie.nombre_cientifico = nombre_cientifico_normalizado
    db_especie.nombre_comun = nombre_comun_normalizado
    db_especie.origen = origen_normalizado

    db.commit()
    db.refresh(db_especie)
    return db_especie

def delete_especie(db: Session, especie_id: int):
    """Elimina una especie si existe."""
    db_especie = db.query(models.Especie).filter(models.Especie.id_especie == especie_id).first()
    if not db_especie:
        raise HTTPException(status_code=404, detail="Especie no encontrada")

    # Eliminar la especie
    db.delete(db_especie)
    db.commit()
    
    return {"detail": f"Especie '{db_especie.nombre_cientifico}' eliminada exitosamente."}



# --- CRUD para Arbol ---
def get_arboles(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de árboles con paginación."""
    return db.query(models.Arbol).offset(skip).limit(limit).all()

def get_arbol(db: Session, arbol_id: int):
    """Obtiene un árbol específico por su ID."""
    db_arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == arbol_id).first()
    if not db_arbol:
        raise HTTPException(status_code=404, detail="Árbol no encontrado")
    return db_arbol

def create_arbol(db: Session, arbol: schemas.ArbolCreate):
    """Crea un nuevo árbol en la base de datos."""
    # Validar existencia de municipio y especie
    municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == arbol.id_municipio).first()
    especie = db.query(models.Especie).filter(models.Especie.id_especie == arbol.id_especie).first()

    if not municipio:
        raise HTTPException(status_code=400, detail=f"El municipio con ID {arbol.id_municipio} no existe.")
    if not especie:
        raise HTTPException(status_code=400, detail=f"La especie con ID {arbol.id_especie} no existe.")

    # Normalizar datos
    arbol_data = arbol.dict()
    arbol_data["calle"] = arbol_data["calle"].strip().title() if arbol_data["calle"] else None
    arbol_data["barrio"] = arbol_data["barrio"].strip().title() if arbol_data["barrio"] else None
    arbol_data["identificacion"] = arbol_data["identificacion"].strip() if arbol_data["identificacion"] else None

    # Crear el árbol
    db_arbol = models.Arbol(**arbol_data)
    try:
        db.add(db_arbol)
        db.commit()
        db.refresh(db_arbol)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el árbol.")

    return db_arbol

def update_arbol(db: Session, arbol_id: int, arbol: schemas.ArbolCreate):
    """Actualiza un árbol existente por su ID."""
    db_arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == arbol_id).first()
    if not db_arbol:
        raise HTTPException(status_code=404, detail="Árbol no encontrado")

    # Validar que el municipio y la especie existan antes de actualizar
    if arbol.id_municipio:
        municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == arbol.id_municipio).first()
        if not municipio:
            raise HTTPException(status_code=400, detail=f"El municipio con ID {arbol.id_municipio} no existe.")

    if arbol.id_especie:
        especie = db.query(models.Especie).filter(models.Especie.id_especie == arbol.id_especie).first()
        if not especie:
            raise HTTPException(status_code=400, detail=f"La especie con ID {arbol.id_especie} no existe.")

    # Normalizar datos antes de actualizar
    arbol_data = arbol.dict()
    arbol_data["calle"] = arbol_data["calle"].strip().title() if arbol_data["calle"] else None
    arbol_data["barrio"] = arbol_data["barrio"].strip().title() if arbol_data["barrio"] else None
    arbol_data["identificacion"] = arbol_data["identificacion"].strip() if arbol_data["identificacion"] else None

    # Actualizar los campos del árbol
    for key, value in arbol_data.items():
        setattr(db_arbol, key, value)
    db.commit()
    db.refresh(db_arbol)
    return db_arbol

def delete_arbol(db: Session, arbol_id: int):
    """Elimina un árbol si existe."""
    db_arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == arbol_id).first()
    if not db_arbol:
        raise HTTPException(status_code=404, detail="Árbol no encontrado")

    # Eliminar el árbol
    db.delete(db_arbol)
    db.commit()
    
    return {"detail": f"Árbol con ID {arbol_id} eliminado exitosamente."}


# --- CRUD para Medición ---
def get_mediciones(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de mediciones con paginación."""
    return db.query(models.Medicion).offset(skip).limit(limit).all()

def get_medicion(db: Session, medicion_id: int):
    """Obtiene una medición específica por su ID."""
    db_medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == medicion_id).first()
    if not db_medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    return db_medicion

def create_medicion(db: Session, medicion: schemas.MedicionCreate):
    """Crea una nueva medición en la base de datos."""
    # Validar que el árbol y el usuario existan antes de crear la medición
    arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == medicion.id_arbol).first()
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == medicion.id_usuario).first()

    if not arbol:
        raise HTTPException(status_code=400, detail=f"El árbol con ID {medicion.id_arbol} no existe.")
    if not usuario:
        raise HTTPException(status_code=400, detail=f"El usuario con ID {medicion.id_usuario} no existe.")

    # Normalizar datos antes de crear la medición
    medicion_data = medicion.dict()
    medicion_data["tratamiento_previo"] = medicion_data["tratamiento_previo"].strip().title() if medicion_data["tratamiento_previo"] else None
    medicion_data["cazuela"] = medicion_data["cazuela"].strip().title() if medicion_data["cazuela"] else None

    # Crear la medición
    db_medicion = models.Medicion(**medicion_data)
    try:
        db.add(db_medicion)
        db.commit()
        db.refresh(db_medicion)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear la medición.")

    return db_medicion

def update_medicion(db: Session, medicion_id: int, medicion: schemas.MedicionCreate):
    """Actualiza una medición existente por su ID."""
    db_medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == medicion_id).first()
    if not db_medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")

    # Validar que el árbol y el usuario existan antes de actualizar
    if medicion.id_arbol:
        arbol = db.query(models.Arbol).filter(models.Arbol.id_arbol == medicion.id_arbol).first()
        if not arbol:
            raise HTTPException(status_code=400, detail=f"El árbol con ID {medicion.id_arbol} no existe.")

    if medicion.id_usuario:
        usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == medicion.id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=400, detail=f"El usuario con ID {medicion.id_usuario} no existe.")

    # Normalizar datos antes de actualizar la medición
    medicion_data = medicion.dict()
    medicion_data["tratamiento_previo"] = medicion_data["tratamiento_previo"].strip().title() if medicion_data["tratamiento_previo"] else None
    medicion_data["cazuela"] = medicion_data["cazuela"].strip().title() if medicion_data["cazuela"] else None

    # Actualizar los campos de la medición
    for key, value in medicion_data.items():
        setattr(db_medicion, key, value)
    db.commit()
    db.refresh(db_medicion)
    return db_medicion

def delete_medicion(db: Session, medicion_id: int):
    """Elimina una medición si existe."""
    db_medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == medicion_id).first()
    if not db_medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")

    # Eliminar la medición
    db.delete(db_medicion)
    db.commit()
    
    return {"detail": f"Medición con ID {medicion_id} eliminada exitosamente."}


# --- CRUD para Foto ---
def get_fotos(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de fotos con paginación."""
    return db.query(models.Foto).offset(skip).limit(limit).all()

def get_foto(db: Session, foto_id: int):
    """Obtiene una foto específica por su ID."""
    db_foto = db.query(models.Foto).filter(models.Foto.id_foto == foto_id).first()
    if not db_foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return db_foto

def create_foto(db: Session, foto: schemas.FotoCreate):
    """Crea una nueva foto asociada a una medición."""
    # Validar que la medición asociada exista
    medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == foto.id_medicion).first()
    if not medicion:
        raise HTTPException(status_code=400, detail=f"La medición con ID {foto.id_medicion} no existe.")

    # Normalizar datos antes de insertar
    foto_data = foto.dict()
    foto_data["tipo_foto"] = foto_data["tipo_foto"].strip().title()
    foto_data["ruta_foto"] = foto_data["ruta_foto"].strip()

    # Crear la foto
    db_foto = models.Foto(**foto_data)
    try:
        db.add(db_foto)
        db.commit()
        db.refresh(db_foto)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear la foto.")

    return db_foto

def update_foto(db: Session, foto_id: int, foto: schemas.FotoCreate):
    """Actualiza una foto existente por su ID."""
    db_foto = db.query(models.Foto).filter(models.Foto.id_foto == foto_id).first()
    if not db_foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    # Validar que la medición asociada exista si se cambia
    if foto.id_medicion and foto.id_medicion != db_foto.id_medicion:
        medicion = db.query(models.Medicion).filter(models.Medicion.id_medicion == foto.id_medicion).first()
        if not medicion:
            raise HTTPException(status_code=400, detail=f"La medición con ID {foto.id_medicion} no existe.")

    # Normalizar datos antes de actualizar
    foto_data = foto.dict()
    foto_data["tipo_foto"] = foto_data["tipo_foto"].strip().title()
    foto_data["ruta_foto"] = foto_data["ruta_foto"].strip()

    # Actualizar los campos de la foto
    for key, value in foto_data.items():
        setattr(db_foto, key, value)
    db.commit()
    db.refresh(db_foto)
    return db_foto

def delete_foto(db: Session, foto_id: int):
    """Elimina una foto si existe."""
    db_foto = db.query(models.Foto).filter(models.Foto.id_foto == foto_id).first()
    if not db_foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    # Eliminar la foto
    db.delete(db_foto)
    db.commit()
    
    return {"detail": f"Foto con ID {foto_id} eliminada exitosamente."}

def get_user_by_email(db: Session, email: str):
    """Obtiene un usuario específico por su email."""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()