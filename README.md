
## Endpoints Principales

- `/provincias/`: CRUD para provincias
- `/municipios/`: CRUD para municipios
- `/roles/`: CRUD para roles de usuario
- `/usuarios/`: CRUD para usuarios
- `/arboles/`: CRUD para árboles
- `/mediciones/`: CRUD para mediciones de árboles
- `/fotos/`: CRUD para fotos de árboles

Para más detalles sobre los endpoints y sus parámetros, consulta la documentación Swagger o ReDoc.

## Modelos de Datos

### Provincia
- `id_provincia`: int
- `nombre`: str

### Municipio
- `id_municipio`: int
- `id_provincia`: int
- `nombre`: str
- `latitude`: float (opcional)
- `longitude`: float (opcional)

### Role
- `id_role`: int
- `role_name`: str
- `can_manage_users`: bool
- `can_manage_all_relevamientos`: bool
- `can_create_relevamientos`: bool
- `can_modify_own_relevamientos`: bool
- `can_generate_reports`: bool

### Usuario
- `id_usuario`: int
- `id_municipio`: int
- `id_role`: int
- `nombre`: str
- `email`: str
- `hashed_password`: str
- `is_active`: bool
- `is_superuser`: bool
- `date_joined`: date
- `created_by`: int (opcional)

### Arbol
- `id_arbol`: int
- `id_especie`: int
- `id_municipio`: int
- `latitude`: float (opcional)
- `longitude`: float (opcional)
- `calle`: str (opcional)
- `numero_aprox`: int (opcional)
- `identificacion`: str (opcional)
- `barrio`: str (opcional)
- `altura`: str
- `diametro_tronco`: str
- `ambito`: str
- `distancia_entre_ejemplares`: str
- `distancia_al_cordon`: str
- `interferencia_aerea`: str
- `tipo_cable`: str (opcional)
- `requiere_intervencion`: bool
- `tipo_intervencion`: str (opcional)
- `tratamiento_previo`: str (opcional)
- `cazuela`: str (opcional)
- `protegido`: bool
- `fecha_censo`: date (opcional)
- `id_usuario`: int (opcional)

### Medicion
- `id_medicion`: int
- `id_arbol`: int
- `fecha_medicion`: date (opcional)
- `latitude`: float (opcional)
- `longitude`: float (opcional)
- `altura`: str
- `diametro_tronco`: str
- `ambito`: str
- `distancia_entre_ejemplares`: str
- `distancia_al_cordon`: str
- `interferencia_aerea`: str
- `tipo_cable`: str (opcional)
- `requiere_intervencion`: bool
- `tipo_intervencion`: str (opcional)
- `tratamiento_previo`: str (opcional)
- `cazuela`: str (opcional)
- `protegido`: bool
- `id_usuario`: int (opcional)

### Foto
- `id_foto`: int
- `id_medicion`: int
- `tipo_foto`: str
- `ruta_foto`: str

## Autenticación

La API utiliza autenticación basada en JWT. Para obtener un token, utiliza el endpoint `/token` con las credenciales de usuario.

## Desarrollo

Para contribuir al proyecto:

1. Crea una rama para tu feature: `git checkout -b feature/AmazingFeature`
2. Realiza tus cambios y haz commit: `git commit -m 'Add some AmazingFeature'`
3. Push a la rama: `git push origin feature/AmazingFeature`
4. Abre un Pull Request

## Solución de Problemas

Si encuentras problemas al iniciar el servicio de PostgreSQL o al conectarte a la base de datos, sigue estos pasos:

1. Verifica el estado del servicio: