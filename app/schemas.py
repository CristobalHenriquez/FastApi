# app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

# Provincia Schemas
class ProvinciaBase(BaseModel):
    nombre: str

class ProvinciaCreate(ProvinciaBase):
    pass

class ProvinciaRead(ProvinciaBase):
    id_provincia: int

    class Config:
        orm_mode = True

# Municipio Schemas
class MunicipioBase(BaseModel):
    id_provincia: int
    nombre: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class MunicipioCreate(MunicipioBase):
    pass

class MunicipioRead(MunicipioBase):
    id_municipio: int

    class Config:
        orm_mode = True

# Especie Schemas
class EspecieBase(BaseModel):
    nombre_cientifico: str
    nombre_comun: str
    origen: str  # 'nativo', 'exotico'

class EspecieCreate(EspecieBase):
    pass

class EspecieRead(EspecieBase):
    id_especie: int

    class Config:
        orm_mode = True

# Role Schemas
class RoleBase(BaseModel):
    role_name: str
    can_manage_users: Optional[bool] = False
    can_manage_all_relevamientos: Optional[bool] = False
    can_create_relevamientos: Optional[bool] = False
    can_modify_own_relevamientos: Optional[bool] = False
    can_generate_reports: Optional[bool] = False
    can_manage_municipio_data: Optional[bool] = False

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    id_role: int

    class Config:
        orm_mode = True

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
        orm_mode = True

# Altura Schemas
class AlturaBase(BaseModel):
    rango_altura: str

class AlturaCreate(AlturaBase):
    pass

class AlturaRead(AlturaBase):
    id_altura: int

    class Config:
        orm_mode = True

# DiametroTronco Schemas
class DiametroTroncoBase(BaseModel):
    rango_diametro: str

class DiametroTroncoCreate(DiametroTroncoBase):
    pass

class DiametroTroncoRead(DiametroTroncoBase):
    id_diametro: int

    class Config:
        orm_mode = True

# EstadoFitosanitario Schemas
class EstadoFitosanitarioBase(BaseModel):
    nombre_estado: str

class EstadoFitosanitarioCreate(EstadoFitosanitarioBase):
    pass

class EstadoFitosanitarioRead(EstadoFitosanitarioBase):
    id_estado: int

    class Config:
        orm_mode = True

# CondicionesCrecimiento Schemas
class CondicionesCrecimientoBase(BaseModel):
    nombre_condicion: str

class CondicionesCrecimientoCreate(CondicionesCrecimientoBase):
    pass

class CondicionesCrecimientoRead(CondicionesCrecimientoBase):
    id_condicion: int

    class Config:
        orm_mode = True

# TipoInterferencia Schemas
class TipoInterferenciaBase(BaseModel):
    nombre_tipo: str

class TipoInterferenciaCreate(TipoInterferenciaBase):
    pass

class TipoInterferenciaRead(TipoInterferenciaBase):
    id_tipo_interferencia: int

    class Config:
        orm_mode = True

# Arbol Schemas
class ArbolBase(BaseModel):
    id_especie: int
    id_municipio: int
    ubicacion: Optional[str] = None  # 'latitud, longitud'
    calle: Optional[str] = None
    numero_aprox: Optional[int] = None
    identificacion: Optional[str] = None
    barrio: Optional[str] = None
    id_altura: Optional[int] = None
    id_diametro: Optional[int] = None
    id_estado_copa: Optional[int] = None
    id_estado_tronco: Optional[int] = None
    id_estado_base: Optional[int] = None
    id_condicion: Optional[int] = None
    tratamiento_previo: Optional[str] = None
    cazuela: Optional[str] = None
    requiere_tratamiento: Optional[bool] = False
    ambito: Optional[str] = None  # 'urbano', 'rural'
    protegido: Optional[bool] = False
    fecha_censo: Optional[date] = None
    id_usuario: Optional[int] = None
    interferencias: Optional[str] = None
    detalles_arbol: Optional[str] = None
    absorcion_co2: Optional[float] = None
    edad: Optional[str] = None
    distancia_otros_ejemplares: Optional[str] = None
    distancia_cordon: Optional[str] = None

class ArbolCreate(ArbolBase):
    pass

class ArbolRead(ArbolBase):
    id_arbol: int

    class Config:
        orm_mode = True

# Interferencia Schemas
class InterferenciaBase(BaseModel):
    id_arbol: int
    id_tipo_interferencia: int
    descripcion: Optional[str] = None

class InterferenciaCreate(InterferenciaBase):
    pass

class InterferenciaRead(InterferenciaBase):
    id_interferencia: int

    class Config:
        orm_mode = True

# Medicion Schemas
class MedicionBase(BaseModel):
    id_arbol: int
    fecha_medicion: Optional[date] = None
    id_altura: Optional[int] = None
    id_diametro: Optional[int] = None
    ubicacion: Optional[str] = None  # 'latitud, longitud'
    calle: Optional[str] = None
    numero_aprox: Optional[int] = None
    barrio: Optional[str] = None
    id_estado_copa: Optional[int] = None
    id_estado_tronco: Optional[int] = None
    id_estado_base: Optional[int] = None
    id_condicion: Optional[int] = None
    tratamiento_previo: Optional[str] = None
    cazuela: Optional[str] = None  # (estado)
    requiere_tratamiento: Optional[bool] = False
    ambito: Optional[str] = None
    protegido: Optional[bool] = False
    id_usuario: Optional[int] = None
    interferencias: Optional[str] = None
    detalles_arbol: Optional[str] = None
    absorcion_co2: Optional[float] = None
    edad: Optional[str] = None  # 'edad del árbol en esta medición'
    tipo_dano: Optional[str] = None
    intervencion_programada: Optional[bool] = False
    imagen_dano: Optional[str] = None

class MedicionCreate(MedicionBase):
    pass

class MedicionRead(MedicionBase):
    id_medicion: int

    class Config:
        orm_mode = True

# Foto Schemas
class FotoBase(BaseModel):
    id_medicion: int
    tipo_foto: str  # 'censo', 'estado_fitosanitario'
    ruta_foto: str

class FotoCreate(FotoBase):
    pass

class FotoRead(FotoBase):
    id_foto: int

    class Config:
        orm_mode = True
