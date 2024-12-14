import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Añadir el path del proyecto para permitir importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import Base  # Importar Base de tus modelos

# Obtener la configuración de Alembic
config = context.config

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

# Configurar la URL de la base de datos
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL no está configurado en el archivo .env")
config.set_main_option('sqlalchemy.url', database_url)

# Interpretar el archivo de configuración de logging de Alembic
fileConfig(config.config_file_name)

# Metadata para las migraciones
target_metadata = Base.metadata

def run_migrations_offline():
    """Ejecuta migraciones en modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Ejecuta migraciones en modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,  # Cambiar según necesidades
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
