# FastAPI - Gestión de Árboles Urbanos

Este proyecto es una **API REST** para la gestión de árboles urbanos, diseñada utilizando **FastAPI**. La API permite gestionar provincias, municipios, especies de árboles, usuarios y realizar operaciones relacionadas con árboles, mediciones y fotos.

## Características

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Migraciones de base de datos**: Alembic
- **Soporte para desarrollo local y despliegue en producción.**
- **Rutas CRUD completas** para todas las entidades del modelo.
- **Validación de datos** y documentación automática mediante Pydantic.
- **Servidor ASGI** utilizando Uvicorn.

---

## Requisitos Previos

- **Python**: Versión 3.8 o superior.
- **Base de datos**: PostgreSQL (recomendado para producción), SQLite (para desarrollo local).
- **Entorno virtual**: Se recomienda utilizar `venv` o `virtualenv`.
- **Herramientas de Migración**: Alembic.

---

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
Configurar el entorno virtual:

bash
Copiar código
python3 -m venv env
source env/bin/activate  # macOS/Linux
.\env\Scripts\activate   # Windows
Instalar dependencias:

bash
Copiar código
pip install -r requirements.txt
Configurar las variables de entorno: Crear un archivo .env en la raíz del proyecto con las siguientes variables:

env
Copiar código
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_base_datos
Iniciar las migraciones:

bash
Copiar código
alembic upgrade head
Iniciar el servidor local:

bash
Copiar código
uvicorn app.main:app --reload
Probar la API:

Documentación interactiva: http://127.0.0.1:8000/docs
Documentación alternativa: http://127.0.0.1:8000/redoc
Estructura del Proyecto
plaintext
Copiar código
FastAPI/
├── alembic/                # Configuración y migraciones de Alembic
│   ├── env.py              # Configuración de migraciones
│   └── versions/           # Archivos de migraciones generados
├── app/                    # Código principal de la aplicación
│   ├── __init__.py
│   ├── crud.py             # Funciones CRUD para las entidades
│   ├── database.py         # Configuración de la base de datos
│   ├── main.py             # Punto de entrada de la aplicación
│   ├── models.py           # Definición de modelos SQLAlchemy
│   └── schemas.py          # Validación de datos con Pydantic
├── .env                    # Variables de entorno (no incluir en el repositorio)
├── .gitignore              # Archivos y carpetas ignorados por Git
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación del proyecto
Rutas Disponibles
Provincias
GET /provincias/ - Listar todas las provincias.
POST /provincias/ - Crear una nueva provincia.
GET /provincias/{id} - Obtener una provincia específica.
PUT /provincias/{id} - Actualizar una provincia existente.
DELETE /provincias/{id} - Eliminar una provincia.
Municipios
GET /municipios/ - Listar todos los municipios.
POST /municipios/ - Crear un nuevo municipio.
GET /municipios/{id} - Obtener un municipio específico.
PUT /municipios/{id} - Actualizar un municipio existente.
DELETE /municipios/{id} - Eliminar un municipio.
Especies
GET /especies/ - Listar todas las especies.
POST /especies/ - Crear una nueva especie.
GET /especies/{id} - Obtener una especie específica.
PUT /especies/{id} - Actualizar una especie existente.
DELETE /especies/{id} - Eliminar una especie.
Usuarios
GET /usuarios/ - Listar todos los usuarios.
POST /usuarios/ - Crear un nuevo usuario.
GET /usuarios/{id} - Obtener un usuario específico.
PUT /usuarios/{id} - Actualizar un usuario existente.
DELETE /usuarios/{id} - Eliminar un usuario.
Árboles
GET /arboles/ - Listar todos los árboles.
POST /arboles/ - Crear un nuevo árbol.
GET /arboles/{id} - Obtener un árbol específico.
PUT /arboles/{id} - Actualizar un árbol existente.
DELETE /arboles/{id} - Eliminar un árbol.
Mediciones
GET /mediciones/ - Listar todas las mediciones.
POST /mediciones/ - Crear una nueva medición.
GET /mediciones/{id} - Obtener una medición específica.
PUT /mediciones/{id} - Actualizar una medición existente.
DELETE /mediciones/{id} - Eliminar una medición.
Fotos
GET /fotos/ - Listar todas las fotos.
POST /fotos/ - Crear una nueva foto.
GET /fotos/{id} - Obtener una foto específica.
PUT /fotos/{id} - Actualizar una foto existente.
DELETE /fotos/{id} - Eliminar una foto.
Despliegue
Preparación
Crear una cuenta en Render.com o Heroku.
Configurar la base de datos de producción.
Pasos para Desplegar
Subir el código a GitHub.
Conectar el repositorio a Render o Heroku.
Configurar las variables de entorno:
DATABASE_URL
Realizar migraciones en el entorno de producción:
bash
Copiar código
alembic upgrade head
Iniciar la aplicación y probar las rutas.
Licencia
Este proyecto está licenciado bajo la Licencia MIT.

yaml
Copiar código

---

### Características del `README.md`:
- **Bien estructurado:** Presenta las secciones esenciales como instalación, rutas y despliegue.
- **Claro y profesional:** Facilita la comprensión para cualquier desarrollador.
- **Directo al uso:** Los comandos están listos para copiar y ejecutar.

Si necesitas personalizar algo más, ¡avísame! 😊