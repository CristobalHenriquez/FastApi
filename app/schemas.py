from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, List, Annotated
from datetime import date

# --- Provincia Schemas ---
class ProvinciaBase(BaseModel):
    nombre: str

    @field_validator("nombre")
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

# --- Municipio Schemas ---
class MunicipioBase(BaseModel):
    id_provincia: int
    nombre: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("nombre")
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

# --- Especie Schemas ---
class EspecieBase(BaseModel):
    nombre_cientifico: str
    nombre_comun: str
    origen: str

    @field_validator("origen")
    def validate_origen(cls, value):
        if value not in ("nativo", "exotico"):
            raise ValueError("El origen debe ser 'nativo' o 'exotico'.")
        return value.lower()

class EspecieCreate(EspecieBase):
    pass

class EspecieRead(EspecieBase):
    id_especie: int

    class Config:
        from_attributes = True

# --- Role Schemas ---
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

# --- Usuario Schemas ---
class UsuarioBase(BaseModel):
    id_municipio: int
    id_role: int
    nombre: str
    email: EmailStr
    hashed_password: str
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

# --- Arbol Schemas ---
class ArbolBase(BaseModel):
    id_especie: int
    id_municipio: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    calle: Optional[str] = None
    numero_aprox: Optional[int] = None
    identificacion: Optional[str] = None
    barrio: Optional[str] = None
    altura: Annotated[str, Field(pattern="^(1-2 m|>3 m|3-5 m|> 5m)$")]
    diametro_tronco: Annotated[str, Field(pattern="^(1-5 cm|5-15 cm|> 15 cm|Especificar)$")]
    ambito: Annotated[str, Field(pattern="^(Urbano|Rural|Otro)$")]
    distancia_entre_ejemplares: str
    distancia_al_cordon: str
    interferencia_aerea: Annotated[str, Field(pattern="^(Línea alta|Iluminaria y media|Baja)$")]
    tipo_cable: Optional[Annotated[str, Field(pattern="^(Preensamblado|Cable desnudo)?$")]] = None
    requiere_intervencion: bool
    tipo_intervencion: Optional[Annotated[str, Field(pattern="^(Poda de altura|Poda de formación|Poda de aclareo|Raleo|Aplicación de fungicida)?$")]] = None
    tratamiento_previo: Optional[str] = None
    cazuela: Optional[str] = None
    protegido: bool
    fecha_censo: Optional[date] = None
    id_usuario: Optional[int] = None

class ArbolCreate(ArbolBase):
    pass

class ArbolRead(ArbolBase):
    id_arbol: int

    class Config:
        from_attributes = True

# --- Medicion Schemas ---
class MedicionBase(BaseModel):
    id_arbol: int
    fecha_medicion: Optional[date] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altura: Annotated[str, Field(pattern="^(1-2 m|>3 m|3-5 m|> 5m)$")]
    diametro_tronco: Annotated[str, Field(pattern="^(1-5 cm|5-15 cm|> 15 cm|Especificar)$")]
    ambito: Annotated[str, Field(pattern="^(Urbano|Rural|Otro)$")]
    distancia_entre_ejemplares: str
    distancia_al_cordon: str
    interferencia_aerea: Annotated[str, Field(pattern="^(Línea alta|Iluminaria y media|Baja)$")]
    tipo_cable: Optional[Annotated[str, Field(pattern="^(Preensamblado|Cable desnudo)?$")]] = None
    requiere_intervencion: bool
    tipo_intervencion: Optional[Annotated[str, Field(pattern="^(Poda de altura|Poda de formación|Poda de aclareo|Raleo|Aplicación de fungicida)?$")]] = None
    tratamiento_previo: Optional[str] = None
    cazuela: Optional[str] = None
    protegido: bool
    id_usuario: Optional[int] = None

class MedicionCreate(MedicionBase):
    pass

class MedicionRead(MedicionBase):
    id_medicion: int

    class Config:
        from_attributes = True

# --- Foto Schemas ---
class FotoBase(BaseModel):
    id_medicion: int
    tipo_foto: str
    ruta_foto: str

class FotoCreate(FotoBase):
    pass

class FotoRead(FotoBase):
    id_foto: int

    class Config:
        from_attributes = True