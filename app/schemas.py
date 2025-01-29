from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
from datetime import date


# 🔹 Listas de valores válidos (Evita repetir regex)
ALTURA_VALUES = {"1-2 m", ">3 m", "3-5 m", "> 5m"}
DIAMETRO_TRONCO_VALUES = {"1-5 cm", "5-15 cm", "> 15 cm", "Especificar"}
AMBITO_VALUES = {"Urbano", "Rural", "Otro"}
INTERFERENCIA_AEREA_VALUES = {"Línea alta", "Iluminaria y media", "Baja"}
TIPO_CABLE_VALUES = {"Preensamblado", "Cable desnudo"}
TIPO_INTERVENCION_VALUES = {"Poda de altura", "Poda de formación", "Poda de aclareo", "Raleo", "Aplicación de fungicida"}


# Provincia Schemas
class ProvinciaBase(BaseModel):
    nombre: str

    @validator("nombre")
    def validate_nombre(cls, value):
        if not value.strip():
            raise ValueError("El nombre de la provincia no puede estar vacío.")
        return value.title()

class ProvinciaCreate(ProvinciaBase):
    pass

class ProvinciaRead(ProvinciaBase):
    id_provincia: int

    class Config:
        from_attributes = True


# Municipio Schemas
class MunicipioBase(BaseModel):
    id_provincia: int
    nombre: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @validator("nombre")
    def validate_nombre(cls, value):
        if not value.strip():
            raise ValueError("El nombre del municipio no puede estar vacío.")
        return value.title()

class MunicipioCreate(MunicipioBase):
    pass

class MunicipioRead(MunicipioBase):
    id_municipio: int

    class Config:
        from_attributes = True


# Especie Schemas
class EspecieBase(BaseModel):
    nombre_cientifico: str
    nombre_comun: str
    origen: str

    @validator("origen")
    def validate_origen(cls, value):
        if value.lower() not in {"nativo", "exotico"}:
            raise ValueError("El origen debe ser 'nativo' o 'exotico'.")
        return value.lower()

class EspecieCreate(EspecieBase):
    pass

class EspecieRead(EspecieBase):
    id_especie: int

    class Config:
        from_attributes = True


# Role Schemas
class RoleBase(BaseModel):
    role_name: str
    can_manage_users: Optional[bool] = False
    can_manage_all_relevamientos: Optional[bool] = False
    can_create_relevamientos: Optional[bool] = False
    can_modify_own_relevamientos: Optional[bool] = False
    can_generate_reports: Optional[bool] = False

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    id_role: int

    class Config:
        from_attributes = True


# Usuario Schemas
class UsuarioBase(BaseModel):
    id_municipio: int
    id_role: int
    nombre: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    date_joined: Optional[date] = None
    created_by: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioRead(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True


# Arbol Schemas
class ArbolBase(BaseModel):
    id_especie: int
    id_municipio: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    calle: Optional[str] = None
    numero_aprox: Optional[int] = None
    identificacion: Optional[str] = None
    barrio: Optional[str] = None
    altura: str
    diametro_tronco: str
    ambito: str
    distancia_entre_ejemplares: str
    distancia_al_cordon: str
    interferencia_aerea: str
    tipo_cable: Optional[str] = None
    requiere_intervencion: bool
    tipo_intervencion: Optional[str] = None
    tratamiento_previo: Optional[str] = None
    cazuela: Optional[str] = None
    protegido: bool
    fecha_censo: Optional[date] = None
    id_usuario: Optional[int] = None

    # 🔹 Validaciones con listas en lugar de regex
    @validator("altura")
    def validar_altura(cls, value):
        if value not in ALTURA_VALUES:
            raise ValueError(f"Valor inválido para altura. Opciones: {', '.join(ALTURA_VALUES)}")
        return value

    @validator("diametro_tronco")
    def validar_diametro(cls, value):
        if value not in DIAMETRO_TRONCO_VALUES:
            raise ValueError(f"Valor inválido para diámetro. Opciones: {', '.join(DIAMETRO_TRONCO_VALUES)}")
        return value

    @validator("ambito")
    def validar_ambito(cls, value):
        if value not in AMBITO_VALUES:
            raise ValueError(f"Valor inválido para ámbito. Opciones: {', '.join(AMBITO_VALUES)}")
        return value

class ArbolCreate(ArbolBase):
    pass

class ArbolRead(ArbolBase):
    id_arbol: int

    class Config:
        from_attributes = True


# Medicion Schemas
class MedicionBase(ArbolBase):
    id_arbol: int
    fecha_medicion: Optional[date] = None

class MedicionCreate(MedicionBase):
    pass

class MedicionRead(MedicionBase):
    id_medicion: int

    class Config:
        from_attributes = True


# Foto Schemas
class FotoBase(BaseModel):
    id_medicion: int
    tipo_foto: str
    ruta_foto: str

    @validator("tipo_foto")
    def validar_tipo_foto(cls, value):
        return value.strip().title()

    @validator("ruta_foto")
    def validar_ruta_foto(cls, value):
        return value.strip()

class FotoCreate(FotoBase):
    pass

class FotoRead(FotoBase):
    id_foto: int

    class Config:
        from_attributes = True
