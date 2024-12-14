# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Date, Text
from sqlalchemy.orm import relationship
from .database import Base

class Provincia(Base):
    __tablename__ = "provincia"
    id_provincia = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    municipios = relationship("Municipio", back_populates="provincia")

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

class Especie(Base):
    __tablename__ = "especie"
    id_especie = Column(Integer, primary_key=True, index=True)
    nombre_cientifico = Column(String, nullable=False)
    nombre_comun = Column(String, nullable=False)
    origen = Column(String, nullable=False)  # 'nativo', 'exotico'

    arboles = relationship("Arbol", back_populates="especie")

class Role(Base):
    __tablename__ = "role"
    id_role = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, nullable=False)  # 'Superuser', 'AdminMunicipio', etc.
    can_manage_users = Column(Boolean, default=False)
    can_manage_all_relevamientos = Column(Boolean, default=False)
    can_create_relevamientos = Column(Boolean, default=False)
    can_modify_own_relevamientos = Column(Boolean, default=False)
    can_generate_reports = Column(Boolean, default=False)
    can_manage_municipio_data = Column(Boolean, default=False)

    usuarios = relationship("Usuario", back_populates="role")

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

class Altura(Base):
    __tablename__ = "altura"
    id_altura = Column(Integer, primary_key=True, index=True)
    rango_altura = Column(String, nullable=False)  # '0-0.5 m', etc.

    arboles = relationship("Arbol", back_populates="altura")
    mediciones = relationship("Medicion", back_populates="altura")

class DiametroTronco(Base):
    __tablename__ = "diametrotronco"
    id_diametro = Column(Integer, primary_key=True, index=True)
    rango_diametro = Column(String, nullable=False)  # '0-10 cm', etc.

    arboles = relationship("Arbol", back_populates="diametro")
    mediciones = relationship("Medicion", back_populates="diametro")

class EstadoFitosanitario(Base):
    __tablename__ = "estadofitosanitario"
    id_estado = Column(Integer, primary_key=True, index=True)
    nombre_estado = Column(String, nullable=False)  # 'Bueno', etc.

    arboles_copa = relationship("Arbol", back_populates="estado_copa", foreign_keys='Arbol.id_estado_copa')
    arboles_tronco = relationship("Arbol", back_populates="estado_tronco", foreign_keys='Arbol.id_estado_tronco')
    arboles_base = relationship("Arbol", back_populates="estado_base", foreign_keys='Arbol.id_estado_base')
    mediciones_copa = relationship("Medicion", back_populates="estado_copa", foreign_keys='Medicion.id_estado_copa')
    mediciones_tronco = relationship("Medicion", back_populates="estado_tronco", foreign_keys='Medicion.id_estado_tronco')
    mediciones_base = relationship("Medicion", back_populates="estado_base", foreign_keys='Medicion.id_estado_base')

class CondicionesCrecimiento(Base):
    __tablename__ = "condicionescrecimiento"
    id_condicion = Column(Integer, primary_key=True, index=True)
    nombre_condicion = Column(String, nullable=False)  # 'Buena', etc.

    arboles = relationship("Arbol", back_populates="condicion")
    mediciones = relationship("Medicion", back_populates="condicion")

class TipoInterferencia(Base):
    __tablename__ = "tipointerferencia"
    id_tipo_interferencia = Column(Integer, primary_key=True, index=True)
    nombre_tipo = Column(String, nullable=False)  # 'Cableado', etc.

    interferencias = relationship("Interferencia", back_populates="tipo_interferencia")

class Arbol(Base):
    __tablename__ = "arbol"
    id_arbol = Column(Integer, primary_key=True, index=True)
    id_especie = Column(Integer, ForeignKey("especie.id_especie"), nullable=False)
    id_municipio = Column(Integer, ForeignKey("municipio.id_municipio"), nullable=False)
    ubicacion = Column(String, nullable=True)  # 'latitud, longitud'
    calle = Column(String, nullable=True)
    numero_aprox = Column(Integer, nullable=True)
    identificacion = Column(String, nullable=True)
    barrio = Column(String, nullable=True)
    id_altura = Column(Integer, ForeignKey("altura.id_altura"), nullable=True)
    id_diametro = Column(Integer, ForeignKey("diametrotronco.id_diametro"), nullable=True)
    id_estado_copa = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_estado_tronco = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_estado_base = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_condicion = Column(Integer, ForeignKey("condicionescrecimiento.id_condicion"), nullable=True)
    tratamiento_previo = Column(String, nullable=True)
    cazuela = Column(String, nullable=True)  # (estado)
    requiere_tratamiento = Column(Boolean, default=False)
    ambito = Column(String, nullable=True)  # 'urbano', 'rural'
    protegido = Column(Boolean, default=False)
    fecha_censo = Column(Date, nullable=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=True)
    interferencias = Column(Text, nullable=True)
    detalles_arbol = Column(Text, nullable=True)
    absorcion_co2 = Column(Float, nullable=True)
    edad = Column(String, nullable=True)  # 'edad del árbol'
    distancia_otros_ejemplares = Column(String, nullable=True)
    distancia_cordon = Column(String, nullable=True)

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

class Interferencia(Base):
    __tablename__ = "interferencia"
    id_interferencia = Column(Integer, primary_key=True, index=True)
    id_arbol = Column(Integer, ForeignKey("arbol.id_arbol"), nullable=False)
    id_tipo_interferencia = Column(Integer, ForeignKey("tipointerferencia.id_tipo_interferencia"), nullable=False)
    descripcion = Column(Text, nullable=True)

    arbol = relationship("Arbol", back_populates="interferencias_rel")
    tipo_interferencia = relationship("TipoInterferencia", back_populates="interferencias")

class Medicion(Base):
    __tablename__ = "medicion"
    id_medicion = Column(Integer, primary_key=True, index=True)
    id_arbol = Column(Integer, ForeignKey("arbol.id_arbol"), nullable=False)
    fecha_medicion = Column(Date, nullable=True)
    id_altura = Column(Integer, ForeignKey("altura.id_altura"), nullable=True)
    id_diametro = Column(Integer, ForeignKey("diametrotronco.id_diametro"), nullable=True)
    ubicacion = Column(String, nullable=True)  # 'latitud, longitud'
    calle = Column(String, nullable=True)
    numero_aprox = Column(Integer, nullable=True)
    barrio = Column(String, nullable=True)
    id_estado_copa = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_estado_tronco = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_estado_base = Column(Integer, ForeignKey("estadofitosanitario.id_estado"), nullable=True)
    id_condicion = Column(Integer, ForeignKey("condicionescrecimiento.id_condicion"), nullable=True)
    tratamiento_previo = Column(String, nullable=True)
    cazuela = Column(String, nullable=True)  # (estado)
    requiere_tratamiento = Column(Boolean, default=False)
    ambito = Column(String, nullable=True)  # 'urbano', 'rural'
    protegido = Column(Boolean, default=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=True)
    interferencias = Column(Text, nullable=True)
    detalles_arbol = Column(Text, nullable=True)
    absorcion_co2 = Column(Float, nullable=True)
    edad = Column(String, nullable=True)  # 'edad del árbol en esta medición'
    tipo_dano = Column(String, nullable=True)
    intervencion_programada = Column(Boolean, default=False)
    imagen_dano = Column(String, nullable=True)  # Ruta de imagen del daño

    arbol = relationship("Arbol", back_populates="mediciones")
    altura = relationship("Altura", back_populates="mediciones")
    diametro = relationship("DiametroTronco", back_populates="mediciones")
    estado_copa = relationship("EstadoFitosanitario", back_populates="mediciones_copa", foreign_keys=[id_estado_copa])
    estado_tronco = relationship("EstadoFitosanitario", back_populates="mediciones_tronco", foreign_keys=[id_estado_tronco])
    estado_base = relationship("EstadoFitosanitario", back_populates="mediciones_base", foreign_keys=[id_estado_base])
    condicion = relationship("CondicionesCrecimiento", back_populates="mediciones")
    usuario = relationship("Usuario", back_populates="mediciones")
    fotos = relationship("Foto", back_populates="medicion")

class Foto(Base):
    __tablename__ = "foto"
    id_foto = Column(Integer, primary_key=True, index=True)
    id_medicion = Column(Integer, ForeignKey("medicion.id_medicion"), nullable=False)
    tipo_foto = Column(String, nullable=False)  # 'censo', 'estado_fitosanitario'
    ruta_foto = Column(String, nullable=False)

    medicion = relationship("Medicion", back_populates="fotos")

    __table_args__ = (
        # Unique constraint en (id_medicion, tipo_foto)
        sqlalchemy.UniqueConstraint('id_medicion', 'tipo_foto', name='uix_id_medicion_tipo_foto'),
    )
