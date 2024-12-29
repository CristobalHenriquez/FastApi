from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import date

# Provincia Schemas
class ProvinciaBase(BaseModel):
    nombre: str

    @validator("nombre")
    def validate_nombre(cls, value):
        if not value.strip():
            raise ValueError("El nombre de la provincia no puede estar vacío.")
        return value.title()  # Capitaliza el nombre

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
    latitud: Optional[float] = None
    longitud: Optional[float] = None

    @validator("nombre")
    def validate_nombre(cls, value):
        if not value.strip():
            raise ValueError("El nombre del municipio no puede estar vacío.")
        return value.title()  # Capitaliza el nombre

    @validator("latitud")
    def validate_latitud(cls, value):
        if value is not None and (value < -90 or value > 90):
            raise ValueError("La latitud debe estar entre -90 y 90 grados.")
        return value

    @validator("longitud")
    def validate_longitud(cls, value):
        if value is not None and (value < -180 or value > 180):
            raise ValueError("La longitud debe estar entre -180 y 180 grados.")
        return value

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
    origen: str  # 'nativo', 'exotico'

    @validator("nombre_cientifico")
    def validate_nombre_cientifico(cls, value):
        if not value.strip():
            raise ValueError("El nombre científico no puede estar vacío.")
        if not value.replace(" ", "").isalpha():
            raise ValueError("El nombre científico solo debe contener letras y espacios.")
        return value.capitalize()  # Capitaliza el primer carácter

    @validator("origen")
    def validate_origen(cls, value):
        if value not in ("nativo", "exotico"):
            raise ValueError("El origen debe ser 'nativo' o 'exotico'.")
        return value.lower()  # Normaliza el valor a minúsculas

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
    can_manage_municipio_data: Optional[bool] = False

    @validator("role_name")
    def validate_role_name(cls, value):
        if not value.strip():
            raise ValueError("El nombre del rol no puede estar vacío.")
        return value.title()  # Normaliza el nombre capitalizando cada palabra

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

    @validator("nombre")
    def validate_nombre(cls, value):
        if not value.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        return value.title()  # Capitaliza el nombre

    @validator("email")
    def validate_email(cls, value):
        if not value or "@" not in value:
            raise ValueError("Debe proporcionar un email válido.")
        return value.lower()  # Normaliza el email a minúsculas

    @validator("date_joined")
    def validate_date_joined(cls, value):
        if value and value > date.today():
            raise ValueError("La fecha de registro no puede estar en el futuro.")
        return value

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioRead(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True


# Altura Schemas
class AlturaBase(BaseModel):
    rango_altura: str  # Ejemplo de formato esperado: "5-10 m"

    @validator("rango_altura")
    def validate_rango_altura(cls, value):
        if not value.strip():
            raise ValueError("El rango de altura no puede estar vacío.")
        if "-" not in value or not all(part.strip().isdigit() for part in value.replace("m", "").split("-")):
            raise ValueError("El rango de altura debe estar en el formato 'X-Y m'.")
        return value

class AlturaCreate(AlturaBase):
    pass

class AlturaRead(AlturaBase):
    id_altura: int

    class Config:
        from_attributes = True


# DiametroTronco Schemas
class DiametroTroncoBase(BaseModel):
    rango_diametro: str  # Ejemplo de formato esperado: "20-30 cm"

    @validator("rango_diametro")
    def validate_rango_diametro(cls, value):
        if not value.strip():
            raise ValueError("El rango de diámetro no puede estar vacío.")
        if "-" not in value or not all(part.strip().isdigit() for part in value.replace("cm", "").split("-")):
            raise ValueError("El rango de diámetro debe estar en el formato 'X-Y cm'.")
        return value

class DiametroTroncoCreate(DiametroTroncoBase):
    pass

class DiametroTroncoRead(DiametroTroncoBase):
    id_diametro: int

    class Config:
        from_attributes = True


# EstadoFitosanitario Schemas
class EstadoFitosanitarioBase(BaseModel):
    nombre_estado: Optional[str] = None  # Permitimos valores nulos o vacíos

    @validator("nombre_estado")
    def validate_nombre_estado(cls, value):
        if value is not None and not value.strip():
            raise ValueError("El nombre del estado fitosanitario no puede ser una cadena vacía.")
        return value.title() if value else value

class EstadoFitosanitarioCreate(EstadoFitosanitarioBase):
    pass

class EstadoFitosanitarioRead(EstadoFitosanitarioBase):
    id_estado: int

    class Config:
        from_attributes = True


# CondicionesCrecimiento Schemas
class CondicionesCrecimientoBase(BaseModel):
    nombre_condicion: str

    @validator("nombre_condicion")
    def validate_nombre_condicion(cls, value):
        if not value.strip():
            raise ValueError("El nombre de la condición de crecimiento no puede estar vacío.")
        return value.title()  # Convierte a formato título para uniformidad

class CondicionesCrecimientoCreate(CondicionesCrecimientoBase):
    pass

class CondicionesCrecimientoRead(CondicionesCrecimientoBase):
    id_condicion: int

    class Config:
        from_attributes = True


# TipoInterferencia Schemas
class TipoInterferenciaBase(BaseModel):
    nombre_tipo: str

    @validator("nombre_tipo")
    def validate_nombre_tipo(cls, value):
        if not value.strip():
            raise ValueError("El nombre del tipo de interferencia no puede estar vacío.")
        return value.title()  # Convierte a formato título para uniformidad

class TipoInterferenciaCreate(TipoInterferenciaBase):
    pass

class TipoInterferenciaRead(TipoInterferenciaBase):
    id_tipo_interferencia: int

    class Config:
        from_attributes = True


# Arbol Schemas
class ArbolBase(BaseModel):
    id_especie: int
    id_municipio: int
    ubicacion: Optional[str] = None
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
    ambito: Optional[str] = None
    protegido: Optional[bool] = False
    fecha_censo: Optional[date] = None
    id_usuario: Optional[int] = None
    interferencias: Optional[str] = None
    detalles_arbol: Optional[str] = None
    absorcion_co2: Optional[float] = None
    edad: Optional[int] = None
    distancia_otros_ejemplares: Optional[str] = None
    distancia_cordon: Optional[str] = None

    # Nuevos campos
    ancho_vereda: Optional[float] = None
    interferencia_aerea: Optional[bool] = False
    especificaciones_interferencia: Optional[str] = None

    # Validadores
    @validator("ancho_vereda")
    def validate_ancho_vereda(cls, value):
        if value is not None and value < 0:
            raise ValueError("El ancho de la vereda no puede ser negativo.")
        return value

    @validator("especificaciones_interferencia")
    def validate_especificaciones_interferencia(cls, value, values):
        if values.get("interferencia_aerea") and not value:
            raise ValueError("Las especificaciones de interferencia son requeridas si hay interferencia aérea.")
        if not values.get("interferencia_aerea") and value:
            raise ValueError("No puede haber especificaciones de interferencia si no hay interferencia aérea.")
        return value.strip() if value else value

    @validator("identificacion")
    def validate_identificacion(cls, value):
        if value and len(value) > 50:
            raise ValueError("La identificación no puede exceder los 50 caracteres.")
        return value.strip() if value else value

class ArbolCreate(ArbolBase):
    pass

class ArbolRead(ArbolBase):
    id_arbol: int

    class Config:
        from_attributes = True


# Interferencia Schemas
class InterferenciaBase(BaseModel):
    id_arbol: int
    id_tipo_interferencia: int
    descripcion: Optional[str] = None

    # Validadores
    @validator("descripcion")
    def validate_descripcion(cls, value):
        if value and len(value) > 500:
            raise ValueError("La descripción no puede exceder los 500 caracteres.")
        return value.strip() if value else value

class InterferenciaCreate(InterferenciaBase):
    pass

class InterferenciaRead(InterferenciaBase):
    id_interferencia: int

    class Config:
        from_attributes = True

class MedicionBase(BaseModel):
    id_arbol: int
    fecha_medicion: Optional[date] = None
    id_altura: Optional[int] = None
    id_diametro: Optional[int] = None
    ubicacion: Optional[str] = None
    calle: Optional[str] = None
    numero_aprox: Optional[int] = None
    barrio: Optional[str] = None
    id_estado_copa: Optional[int] = None
    id_estado_tronco: Optional[int] = None
    id_estado_base: Optional[int] = None
    id_condicion: Optional[int] = None
    tratamiento_previo: Optional[str] = None
    cazuela: Optional[str] = None
    requiere_tratamiento: Optional[bool] = False
    ambito: Optional[str] = None
    protegido: Optional[bool] = False
    id_usuario: Optional[int] = None
    interferencias: Optional[str] = None
    detalles_arbol: Optional[str] = None
    absorcion_co2: Optional[float] = None
    edad: Optional[int] = None
    tipo_dano: Optional[str] = None
    intervencion_programada: Optional[bool] = False
    imagen_dano: Optional[str] = None

    # Nuevos campos
    ancho_vereda: Optional[float] = None
    interferencia_aerea: Optional[bool] = False
    especificaciones_interferencia: Optional[str] = None

    # Validadores
    @validator("ancho_vereda")
    def validate_ancho_vereda(cls, value):
        if value is not None and value < 0:
            raise ValueError("El ancho de la vereda no puede ser negativo.")
        return value

    @validator("especificaciones_interferencia")
    def validate_especificaciones_interferencia(cls, value, values):
        interferencia_aerea = values.get("interferencia_aerea", False)
        if interferencia_aerea and not value:
            raise ValueError("Especificaciones de interferencia son requeridas si hay interferencia aérea.")
        if not interferencia_aerea and value:
            raise ValueError("No puede haber especificaciones si no hay interferencia aérea.")
        return value.strip() if value else value

    @validator("tipo_dano")
    def validate_tipo_dano(cls, value):
        if value and len(value) > 100:
            raise ValueError("El tipo de daño no puede exceder los 100 caracteres.")
        return value.strip() if value else value

class MedicionCreate(MedicionBase):
    pass

class MedicionRead(MedicionBase):
    id_medicion: int

    class Config:
        from_attributes = True


class FotoBase(BaseModel):
    id_medicion: int
    tipo_foto: str
    ruta_foto: str

    # Validadores
    @validator("tipo_foto")
    def validate_tipo_foto(cls, value):
        valid_tipos = ["censo", "estado_fitosanitario"]
        if value not in valid_tipos:
            raise ValueError(f"El tipo de foto debe ser uno de los siguientes: {', '.join(valid_tipos)}.")
        return value.strip()

    @validator("ruta_foto")
    def validate_ruta_foto(cls, value):
        if not value:
            raise ValueError("La ruta de la foto es obligatoria.")
        if len(value) > 255:
            raise ValueError("La ruta de la foto no puede exceder los 255 caracteres.")
        return value.strip()

class FotoCreate(FotoBase):
    pass

class FotoRead(FotoBase):
    id_foto: int

    class Config:
        from_attributes = True
