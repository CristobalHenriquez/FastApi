import sqlalchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    Boolean,
    Date,
    Text,
    Index,
    CheckConstraint,
)
from sqlalchemy.orm import relationship, validates
from .database import Base


class Provincia(Base):
    __tablename__ = "provincia"

    id_provincia = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)  # Nombre único para evitar duplicados

    municipios = relationship("Municipio", back_populates="provincia")

    @validates("nombre")
    def validate_nombre(self, key, value):
        if not value.strip():
            raise ValueError("El nombre de la provincia no puede estar vacío.")
        return value.title()  # Normaliza el nombre capitalizando cada palabra


class Municipio(Base):
    __tablename__ = "municipio"

    id_municipio = Column(Integer, primary_key=True, index=True)
    id_provincia = Column(Integer, ForeignKey("provincia.id_provincia"), nullable=False)
    nombre = Column(String, nullable=False)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)

    provincia = relationship("Provincia", back_populates="municipios")
    usuarios = relationship("Usuario", back_populates="municipio")
    arboles = relationship("Arbol", back_populates="municipio")

    __table_args__ = (
        Index("ix_municipio_nombre", "nombre"),
        CheckConstraint("latitud >= -90 AND latitud <= 90", name="check_latitud"),
        CheckConstraint("longitud >= -180 AND longitud <= 180", name="check_longitud"),
    )

    @validates("nombre")
    def validate_nombre(self, key, value):
        if not value.strip():
            raise ValueError("El nombre del municipio no puede estar vacío.")
        return value.title()

    @validates("latitud")
    def validate_latitud(self, key, value):
        if value is not None and (value < -90 or value > 90):
            raise ValueError("La latitud debe estar entre -90 y 90 grados.")
        return value

    @validates("longitud")
    def validate_longitud(self, key, value):
        if value is not None and (value < -180 or value > 180):
            raise ValueError("La longitud debe estar entre -180 y 180 grados.")
        return value


class Especie(Base):
    __tablename__ = "especie"

    id_especie = Column(Integer, primary_key=True, index=True)
    nombre_cientifico = Column(String, nullable=False, unique=True)  # Nombre científico único
    nombre_comun = Column(String, nullable=False)
    origen = Column(String, nullable=False)

    arboles = relationship("Arbol", back_populates="especie")

    __table_args__ = (
        CheckConstraint("origen IN ('nativo', 'exotico')", name="check_origen"),
    )

    @validates("nombre_cientifico")
    def validate_nombre_cientifico(self, key, value):
        if not value.strip():
            raise ValueError("El nombre científico no puede estar vacío.")
        if not value.replace(" ", "").isalpha():
            raise ValueError("El nombre científico solo debe contener letras y espacios.")
        return value.capitalize()

    @validates("origen")
    def validate_origen(self, key, value):
        if value not in ("nativo", "exotico"):
            raise ValueError("El origen debe ser 'nativo' o 'exotico'.")
        return value


class Role(Base):
    __tablename__ = "role"

    id_role = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, nullable=False)  # Nombre único
    can_manage_users = Column(Boolean, default=False)
    can_manage_all_relevamientos = Column(Boolean, default=False)
    can_create_relevamientos = Column(Boolean, default=False)
    can_modify_own_relevamientos = Column(Boolean, default=False)
    can_generate_reports = Column(Boolean, default=False)
    can_manage_municipio_data = Column(Boolean, default=False)

    usuarios = relationship("Usuario", back_populates="role")

    @validates("role_name")
    def validate_role_name(self, key, value):
        if not value.strip():
            raise ValueError("El nombre del rol no puede estar vacío.")
        return value.title()  # Normaliza el nombre capitalizando cada palabra


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    id_municipio = Column(Integer, ForeignKey("municipio.id_municipio"), nullable=False)
    id_role = Column(Integer, ForeignKey("role.id_role"), nullable=False)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(Date, nullable=False)
    created_by = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=True)

    municipio = relationship("Municipio", back_populates="usuarios")
    role = relationship("Role", back_populates="usuarios")
    created_by_user = relationship("Usuario", remote_side=[id_usuario])
    created_usuarios = relationship("Usuario", back_populates="created_by_user")
    arboles = relationship("Arbol", back_populates="usuario")
    mediciones = relationship("Medicion", back_populates="usuario")

    @validates("nombre")
    def validate_nombre(self, key, value):
        if not value.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        return value.title()  # Capitaliza el nombre

    @validates("email")
    def validate_email(self, key, value):
        if not value or "@" not in value:
            raise ValueError("Debe proporcionar un email válido.")
        return value.lower()  # Normaliza el email a minúsculas

    @validates("date_joined")
    def validate_date_joined(self, key, value):
        if not value:
            raise ValueError("La fecha de registro es obligatoria.")
        return value

    @validates("is_active", "is_superuser")
    def validate_boolean_fields(self, key, value):
        if not isinstance(value, bool):
            raise ValueError(f"El campo '{key}' debe ser un valor booleano.")
        return value


class Altura(Base):
    __tablename__ = "altura"

    id_altura = Column(Integer, primary_key=True, index=True)
    rango_altura = Column(String, nullable=False)  # Debe contener un rango válido, ej. "5-10 m"

    arboles = relationship("Arbol", back_populates="altura")
    mediciones = relationship("Medicion", back_populates="altura")

    @validates("rango_altura")
    def validate_rango_altura(self, key, value):
        if not value.strip():
            raise ValueError("El rango de altura no puede estar vacío.")
        if "-" not in value or not all(part.strip().isdigit() for part in value.split("-")):
            raise ValueError("El rango de altura debe estar en el formato 'X-Y m'.")
        return value


class DiametroTronco(Base):
    __tablename__ = "diametrotronco"

    id_diametro = Column(Integer, primary_key=True, index=True)
    rango_diametro = Column(String, nullable=False)  # Ejemplo: "20-30 cm"

    arboles = relationship("Arbol", back_populates="diametro")
    mediciones = relationship("Medicion", back_populates="diametro")

    @validates("rango_diametro")
    def validate_rango_diametro(self, key, value):
        if not value.strip():
            raise ValueError("El rango de diámetro no puede estar vacío.")
        if "-" not in value or not all(part.strip().isdigit() for part in value.split("-")):
            raise ValueError("El rango de diámetro debe estar en el formato 'X-Y cm'.")
        return value


class EstadoFitosanitario(Base):
    __tablename__ = "estadofitosanitario"

    id_estado = Column(Integer, primary_key=True, index=True)
    nombre_estado = Column(String, nullable=True)  # Puede ser `NULL` si no se define

    arboles_copa = relationship("Arbol", back_populates="estado_copa", foreign_keys="Arbol.id_estado_copa")
    arboles_tronco = relationship("Arbol", back_populates="estado_tronco", foreign_keys="Arbol.id_estado_tronco")
    arboles_base = relationship("Arbol", back_populates="estado_base", foreign_keys="Arbol.id_estado_base")
    mediciones_copa = relationship("Medicion", back_populates="estado_copa", foreign_keys="Medicion.id_estado_copa")
    mediciones_tronco = relationship("Medicion", back_populates="estado_tronco", foreign_keys="Medicion.id_estado_tronco")
    mediciones_base = relationship("Medicion", back_populates="estado_base", foreign_keys="Medicion.id_estado_base")

    @validates("nombre_estado")
    def validate_nombre_estado(self, key, value):
        if value is not None and not value.strip():
            raise ValueError("El nombre del estado fitosanitario no puede ser vacío.")
        return value.title() if value else value


class CondicionesCrecimiento(Base):
    __tablename__ = "condicionescrecimiento"
    
    id_condicion = Column(Integer, primary_key=True, index=True)
    nombre_condicion = Column(String, nullable=False, unique=True)  # Se agrega unique para evitar duplicados

    arboles = relationship("Arbol", back_populates="condicion")
    mediciones = relationship("Medicion", back_populates="condicion")

    @validates("nombre_condicion")
    def validate_nombre_condicion(self, key, value):
        if not value or not value.strip():
            raise ValueError("El nombre de la condición de crecimiento no puede estar vacío.")
        return value.title()  # Convierte a formato título


class TipoInterferencia(Base):
    __tablename__ = "tipointerferencia"
    
    id_tipo_interferencia = Column(Integer, primary_key=True, index=True)
    nombre_tipo = Column(String, nullable=False, unique=True)  # Evita duplicados

    interferencias = relationship("Interferencia", back_populates="tipo_interferencia")

    @validates("nombre_tipo")
    def validate_nombre_tipo(self, key, value):
        if not value or not value.strip():
            raise ValueError("El nombre del tipo de interferencia no puede estar vacío.")
        return value.title()  # Convierte a formato título



class Arbol(Base):
    __tablename__ = "arbol"
    
    id_arbol = Column(Integer, primary_key=True, index=True)
    id_especie = Column(Integer, ForeignKey("especie.id_especie"), nullable=False)
    id_municipio = Column(Integer, ForeignKey("municipio.id_municipio"), nullable=False)
    ubicacion = Column(String, nullable=True)
    calle = Column(String, nullable=True)
    numero_aprox = Column(Integer, nullable=True)
    identificacion = Column(String, nullable=True, unique=True)  # Identificación única si está presente
    barrio = Column(String, nullable=True)
    id_altura = Column(Integer, ForeignKey("altura.id_altura"), nullable=True)
    id_diametro = Column(Integer, ForeignKey("diametrotronco.id_diametro"), nullable=True)
    id_estado_copa = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_estado_tronco = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_estado_base = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_condicion = Column(Integer, ForeignKey("condicionescrecimiento.id_condicion"), nullable=True)
    tratamiento_previo = Column(String, nullable=True)
    cazuela = Column(String, nullable=True)
    requiere_tratamiento = Column(Boolean, default=False)
    ambito = Column(String, nullable=True)
    protegido = Column(Boolean, default=False)
    fecha_censo = Column(Date, nullable=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=True)
    interferencias = Column(Text, nullable=True)
    detalles_arbol = Column(Text, nullable=True)
    absorcion_co2 = Column(Float, nullable=True)
    edad = Column(Integer, nullable=True)
    distancia_otros_ejemplares = Column(String, nullable=True)
    distancia_cordon = Column(String, nullable=True)

    # Nuevos campos
    ancho_vereda = Column(Float, nullable=True)  # Ancho de la vereda en metros
    interferencia_aerea = Column(Boolean, default=False)  # True si hay interferencia aérea
    especificaciones_interferencia = Column(String, nullable=True)  # Detalles de la interferencia aérea

    # Relaciones
    especie = relationship("Especie", back_populates="arboles")
    municipio = relationship("Municipio", back_populates="arboles")
    altura = relationship("Altura", back_populates="arboles")
    diametro = relationship("DiametroTronco", back_populates="arboles")
    estado_copa = relationship("EstadoFitosanitario", back_populates="arboles_copa", foreign_keys=[id_estado_copa])
    estado_tronco = relationship("EstadoFitosanitario", back_populates="arboles_tronco", foreign_keys=[id_estado_tronco])
    estado_base = relationship("EstadoFitosanitario", back_populates="arboles_base", foreign_keys=[id_estado_base])
    condicion = relationship("CondicionesCrecimiento", back_populates="arboles")
    usuario = relationship("Usuario", back_populates="arboles")
    interferencias_rel = relationship("Interferencia", back_populates="arbol")
    mediciones = relationship("Medicion", back_populates="arbol")

    @validates("ancho_vereda")
    def validate_ancho_vereda(self, key, value):
        if value is not None and value < 0:
            raise ValueError("El ancho de la vereda no puede ser negativo.")
        return value

    @validates("especificaciones_interferencia")
    def validate_especificaciones_interferencia(self, key, value):
        if self.interferencia_aerea and not value:
            raise ValueError("Especificaciones de interferencia son obligatorias si hay interferencia aérea.")
        if not self.interferencia_aerea and value:
            raise ValueError("No puede haber especificaciones si no hay interferencia aérea.")
        return value.strip() if value else value


class Interferencia(Base):
    __tablename__ = "interferencia"

    id_interferencia = Column(Integer, primary_key=True, index=True)
    id_arbol = Column(Integer, ForeignKey("arbol.id_arbol"), nullable=False)
    id_tipo_interferencia = Column(Integer, ForeignKey("tipointerferencia.id_tipo_interferencia"), nullable=False)
    descripcion = Column(Text, nullable=True)

    # Relaciones
    arbol = relationship("Arbol", back_populates="interferencias_rel")
    tipo_interferencia = relationship("TipoInterferencia", back_populates="interferencias")

    @validates("descripcion")
    def validate_descripcion(self, key, value):
        if value and len(value.strip()) == 0:
            raise ValueError("La descripción no puede estar vacía si se proporciona.")
        if value and len(value) > 500:
            raise ValueError("La descripción no puede exceder los 500 caracteres.")
        return value.strip() if value else value

    @validates("id_tipo_interferencia")
    def validate_id_tipo_interferencia(self, key, value):
        if value is None:
            raise ValueError("El tipo de interferencia es obligatorio.")
        return value



class Medicion(Base):
    __tablename__ = "medicion"

    id_medicion = Column(Integer, primary_key=True, index=True)
    id_arbol = Column(Integer, ForeignKey("arbol.id_arbol"), nullable=False)
    fecha_medicion = Column(Date, nullable=True)
    id_altura = Column(Integer, ForeignKey("altura.id_altura"), nullable=True)
    id_diametro = Column(Integer, ForeignKey("diametrotronco.id_diametro"), nullable=True)
    ubicacion = Column(String, nullable=True)
    calle = Column(String, nullable=True)
    numero_aprox = Column(Integer, nullable=True)
    barrio = Column(String, nullable=True)
    id_estado_copa = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_estado_tronco = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_estado_base = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_condicion = Column(Integer, ForeignKey("condicionescrecimiento.id_condicion"), nullable=True)
    tratamiento_previo = Column(String, nullable=True)
    cazuela = Column(String, nullable=True)
    requiere_tratamiento = Column(Boolean, default=False)
    ambito = Column(String, nullable=True)
    protegido = Column(Boolean, default=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=True)
    interferencias = Column(Text, nullable=True)
    detalles_arbol = Column(Text, nullable=True)
    absorcion_co2 = Column(Float, nullable=True)
    edad = Column(Integer, nullable=True)
    tipo_dano = Column(String, nullable=True)
    intervencion_programada = Column(Boolean, default=False)
    imagen_dano = Column(String, nullable=True)

    # Nuevos campos
    ancho_vereda = Column(Float, nullable=True)
    interferencia_aerea = Column(Boolean, default=False)
    especificaciones_interferencia = Column(String, nullable=True)

    # Relaciones
    arbol = relationship("Arbol", back_populates="mediciones")
    altura = relationship("Altura", back_populates="mediciones")
    diametro = relationship("DiametroTronco", back_populates="mediciones")
    estado_copa = relationship("EstadoFitosanitario", back_populates="mediciones_copa", foreign_keys=[id_estado_copa])
    estado_tronco = relationship("EstadoFitosanitario", back_populates="mediciones_tronco", foreign_keys=[id_estado_tronco])
    estado_base = relationship("EstadoFitosanitario", back_populates="mediciones_base", foreign_keys=[id_estado_base])
    condicion = relationship("CondicionesCrecimiento", back_populates="mediciones")
    usuario = relationship("Usuario", back_populates="mediciones")
    fotos = relationship("Foto", back_populates="medicion")

    # Validaciones
    @validates("ancho_vereda")
    def validate_ancho_vereda(self, key, value):
        if value is not None and value < 0:
            raise ValueError("El ancho de la vereda no puede ser negativo.")
        return value

    @validates("especificaciones_interferencia")
    def validate_especificaciones_interferencia(self, key, value):
        if self.interferencia_aerea and not value:
            raise ValueError("Especificaciones de interferencia son requeridas si hay interferencia aérea.")
        if not self.interferencia_aerea and value:
            raise ValueError("No puede haber especificaciones si no hay interferencia aérea.")
        return value.strip() if value else value

    @validates("tipo_dano")
    def validate_tipo_dano(self, key, value):
        if value and len(value) > 100:
            raise ValueError("El tipo de daño no puede exceder los 100 caracteres.")
        return value

    @validates("intervencion_programada")
    def validate_intervencion_programada(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("El campo 'intervención programada' debe ser un booleano.")
        return value

class Foto(Base):
    __tablename__ = "foto"

    id_foto = Column(Integer, primary_key=True, index=True)
    id_medicion = Column(Integer, ForeignKey("medicion.id_medicion"), nullable=False)
    tipo_foto = Column(String, nullable=False)
    ruta_foto = Column(String, nullable=False)

    # Relaciones
    medicion = relationship("Medicion", back_populates="fotos")

    __table_args__ = (
        sqlalchemy.UniqueConstraint("id_medicion", "tipo_foto", name="uix_id_medicion_tipo_foto"),
        CheckConstraint("tipo_foto IN ('censo', 'estado_fitosanitario')", name="check_tipo_foto"),
    )

    # Validaciones
    @validates("tipo_foto")
    def validate_tipo_foto(self, key, value):
        valid_tipos = ["censo", "estado_fitosanitario"]
        if value not in valid_tipos:
            raise ValueError(f"El tipo de foto debe ser uno de los siguientes: {', '.join(valid_tipos)}.")
        return value.strip()

    @validates("ruta_foto")
    def validate_ruta_foto(self, key, value):
        if not value:
            raise ValueError("La ruta de la foto es obligatoria.")
        if len(value) > 255:
            raise ValueError("La ruta de la foto no puede exceder los 255 caracteres.")
        return value.strip()
