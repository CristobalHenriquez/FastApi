from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv
from app.database import Base  # Asegúrate de importar Base desde tu proyecto FastAPI
import app.models  # Asegúrate de importar tus modelos

# Cargar variables del archivo .env
load_dotenv()

# Cargar configuración de Alembic
config = context.config

# Leer la URL desde las variables de entorno
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL no está definida en el archivo .env")

# Sobrescribir la URL en el archivo de configuración
config.set_main_option("sqlalchemy.url", database_url)

# Configuración del logger
fileConfig(config.config_file_name)

# MetaData para 'autogenerate'
target_metadata = Base.metadata

def run_migrations_offline():
    """Ejecuta las migraciones en modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Ejecuta las migraciones en modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
