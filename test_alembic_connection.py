from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:Ramcc202323@localhost:5432/app_arbolado_fastapi"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Conexión exitosa desde Alembic")
except Exception as e:
    print(f"Error en la conexión desde Alembic: {e}")
