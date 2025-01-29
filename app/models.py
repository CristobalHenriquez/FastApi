from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Date,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship, validates
from .database import Base


# MODELOS
class Provincia(Base):
    __tablename__ = "provincia"

    id_provincia = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True, index=True)

    municipios = relationship("Municipio", back_populates="provincia", cascade="all, delete-orphan")


class Municipio(Base):
    __tablename__ = "municipio"

    id_municipio = Column(Integer, primary_key=True, index=True)
    id_provincia = Column(Integer, ForeignKey("provincia.id_provincia", ondelete="CASCADE"), nullable=False)
    nombre = Column(String, nullable=False, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    provincia = relationship("Provincia", back_populates="municipios")
    usuarios = relationship("Usuario", back_populates="municipio", cascade="all, delete-orphan")
    arboles = relationship("Arbol", back_populates="municipio", cascade="all, delete-orphan")


class Especie(Base):
    __tablename__ = "especie"

    id_especie = Column(Integer, primary_key=True, index=True)
    nombre_cientifico = Column(String, nullable=False, unique=True, index=True)
    nombre_comun = Column(String, nullable=False)
    origen = Column(String, nullable=False)

    arboles = relationship("Arbol", back_populates="especie", cascade="all, delete-orphan")


class Role(Base):
    __tablename__ = "role"

    id_role = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, nullable=False, index=True)
    can_manage_users = Column(Boolean, default=False)
    can_manage_all_relevamientos = Column(Boolean, default=False)
    can_create_relevamientos = Column(Boolean, default=False)
    can_modify_own_relevamientos = Column(Boolean, default=False)
    can_generate_reports = Column(Boolean, default=False)

    usuarios = relationship("Usuario", back_populates="role")


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True, ondelete="CASCADE")
    id_municipio = Column(Integer, ForeignKey("municipio.id_municipio", ondelete="CASCADE"), nullable=False)
    id_role = Column(Integer, ForeignKey("role.id_role", ondelete="CASCADE"), nullable=False)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)  # 🔹 Se agrega para manejar autenticación
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(Date, nullable=False)
    created_by = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="SET NULL"), nullable=True)

    municipio = relationship("Municipio", back_populates="usuarios")
    role = relationship("Role", back_populates="usuarios")
    created_by_user = relationship("Usuario", remote_side=[id_usuario])
    arboles = relationship("Arbol", back_populates="usuario", cascade="all, delete-orphan")
    mediciones = relationship("Medicion", back_populates="usuario", cascade="all, delete-orphan")




class Arbol(Base):
    __tablename__ = "arbol"

    id_arbol = Column(Integer, primary_key=True, index=True)
    id_especie = Column(Integer, ForeignKey("especie.id_especie", ondelete="CASCADE"), nullable=False)
    id_municipio = Column(Integer, ForeignKey("municipio.id_municipio", ondelete="CASCADE"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    calle = Column(String, nullable=True)
    numero_aprox = Column(Integer, nullable=True)
    identificacion = Column(String, nullable=True)
    barrio = Column(String, nullable=True)

    altura = Column(String, nullable=False, index=True)
    diametro_tronco = Column(String, nullable=False)
    ambito = Column(String, nullable=False)
    distancia_entre_ejemplares = Column(String, nullable=False)
    distancia_al_cordon = Column(String, nullable=False)
    interferencia_aerea = Column(String, nullable=False)
    tipo_cable = Column(String, nullable=True)
    requiere_intervencion = Column(Boolean, nullable=False, default=False)
    tipo_intervencion = Column(String, nullable=True)
    tratamiento_previo = Column(String, nullable=True)
    cazuela = Column(String, nullable=True)
    protegido = Column(Boolean, nullable=False, default=False)
    fecha_censo = Column(Date, nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="SET NULL"))

    especie = relationship("Especie", back_populates="arboles")
    municipio = relationship("Municipio", back_populates="arboles")
    usuario = relationship("Usuario", back_populates="arboles")
    mediciones = relationship("Medicion", back_populates="arbol", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("altura IN ('1-2 m', '>3 m', '3-5 m', '> 5m')"),
        CheckConstraint("diametro_tronco IN ('1-5 cm', '5-15 cm', '> 15 cm', 'Especificar')"),
        CheckConstraint("ambito IN ('Urbano', 'Rural', 'Otro')"),
        CheckConstraint("interferencia_aerea IN ('Línea alta', 'Iluminaria y media', 'Baja')"),

    CheckConstraint("tipo_cable IN ('Preensamblado', 'Cable desnudo')"),
    CheckConstraint("tipo_intervencion IN ('Poda de altura', 'Poda de formación', 'Poda de aclareo', 'Raleo', 'Aplicación de fungicida')"),

    )

    @validates("altura", "diametro_tronco", "ambito", "interferencia_aerea")
    def validate_enum_fields(self, key, value):
        valid_values = {
            "altura": ["1-2 m", ">3 m", "3-5 m", "> 5m"],
            "diametro_tronco": ["1-5 cm", "5-15 cm", "> 15 cm", "Especificar"],
            "ambito": ["Urbano", "Rural", "Otro"],
            "interferencia_aerea": ["Línea alta", "Iluminaria y media", "Baja"],
        }
        if key in valid_values and value not in valid_values[key]:
            raise ValueError(f"Valor inválido para {key}: {value}")
        return value


class Medicion(Base):
    __tablename__ = "medicion"

    id_medicion = Column(Integer, primary_key=True, index=True)
    id_arbol = Column(Integer, ForeignKey("arbol.id_arbol", ondelete="CASCADE"), nullable=False)
    fecha_medicion = Column(Date, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    altura = Column(String, nullable=False, index=True)
    diametro_tronco = Column(String, nullable=False)
    ambito = Column(String, nullable=False)
    distancia_entre_ejemplares = Column(String, nullable=False)
    distancia_al_cordon = Column(String, nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="SET NULL"))

    arbol = relationship("Arbol", back_populates="mediciones")
    usuario = relationship("Usuario", back_populates="mediciones")
    fotos = relationship("Foto", back_populates="medicion", cascade="all, delete-orphan")
