from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

DATABASE_URL = "postgresql+psycopg2://postgres:Ramcc202323@localhost:5432/app_arbolado_fastapi"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("Conexión exitosa con SQLAlchemy")
except OperationalError as e:
    print(f"Error al conectar: {e}")
