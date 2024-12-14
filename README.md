# FastAPI - Gestión de Árboles Urbanos

Este proyecto es una **API REST** para la gestión de árboles urbanos, diseñada utilizando **FastAPI**. La API permite gestionar provincias, municipios, especies de árboles, usuarios y realizar operaciones relacionadas con árboles, mediciones y fotos.

---

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
   git clone https://github.com/CristobalHenriquez/FastApi.git
   cd FastApi
   ```

2. **Configurar el entorno virtual:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # macOS/Linux
   .\env\Scripts\activate   # Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:** Crear un archivo .env en la raíz del proyecto con las siguientes variables:
   ```env
   DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_base_datos
   ```

5. **Iniciar las migraciones:**
   ```bash
   alembic upgrade head
   ```

6. **Iniciar el servidor local:**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Probar la API:**
   - Documentación interactiva: http://127.0.0.1:8000/docs
   - Documentación alternativa: http://127.0.0.1:8000/redoc

## Estructura del Proyecto

```
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
```

## Rutas Disponibles

### Provincias
- GET /provincias/ - Listar todas las provincias.
- POST /provincias/ - Crear una nueva provincia.
- GET /provincias/{id} - Obtener una provincia específica.
- PUT /provincias/{id} - Actualizar una provincia existente.
- DELETE /provincias/{id} - Eliminar una provincia.

### Municipios
- GET /municipios/ - Listar todos los municipios.
- POST /municipios/ - Crear un nuevo municipio.
- GET /municipios/{id} - Obtener un municipio específico.
- PUT /municipios/{id} - Actualizar un municipio existente.
- DELETE /municipios/{id} - Eliminar un municipio.

### Especies
- GET /especies/ - Listar todas las especies.
- POST /especies/ - Crear una nueva especie.
- GET /especies/{id} - Obtener una especie específica.
- PUT /especies/{id} - Actualizar una especie existente.
- DELETE /especies/{id} - Eliminar una especie.

### Usuarios
- GET /usuarios/ - Listar todos los usuarios.
- POST /usuarios/ - Crear un nuevo usuario.
- GET /usuarios/{id} - Obtener un usuario específico.
- PUT /usuarios/{id} - Actualizar un usuario existente.
- DELETE /usuarios/{id} - Eliminar un usuario.

### Árboles
- GET /arboles/ - Listar todos los árboles.
- POST /arboles/ - Crear un nuevo árbol.
- GET /arboles/{id} - Obtener un árbol específico.
- PUT /arboles/{id} - Actualizar un árbol existente.
- DELETE /arboles/{id} - Eliminar un árbol.

### Mediciones
- GET /mediciones/ - Listar todas las mediciones.
- POST /mediciones/ - Crear una nueva medición.
- GET /mediciones/{id} - Obtener una medición específica.
- PUT /mediciones/{id} - Actualizar una medición existente.
- DELETE /mediciones/{id} - Eliminar una medición.

### Fotos
- GET /fotos/ - Listar todas las fotos.
- POST /fotos/ - Crear una nueva foto.
- GET /fotos/{id} - Obtener una foto específica.
- PUT /fotos/{id} - Actualizar una foto existente.
- DELETE /fotos/{id} - Eliminar una foto.

## Despliegue

### Preparación
1. Crear una cuenta en Render.com o Heroku.
2. Configurar la base de datos de producción.

### Pasos para Desplegar
1. Subir el código a GitHub.
2. Conectar el repositorio a Render o Heroku.
3. Configurar las variables de entorno:
   ```env
   DATABASE_URL=postgresql://usuario:contraseña@host:puerto/dbname
   ```
4. Realizar migraciones en el entorno de producción:
   ```bash
   alembic upgrade head
   ```
5. Iniciar la aplicación y probar las rutas.

## Licencia
