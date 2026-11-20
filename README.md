# API de Música

API RESTful para gestionar usuarios, canciones y favoritos. Hecha con FastAPI, SQLModel y Pydantic.

## Datos del estudiante

- Nombre: Lina Fernanda Chamorro Diaz
- Correo: lina.chamorro.0604@miremington.edu.co
- Asignatura: Lenguaje de Programación Avanzado 2
- Docente: Diego Fernando  Marin lozano
- Repositorio: lpa2-taller3_2026

## Descripción

Esta API permite administrar:

- Usuarios: crear y gestionar perfiles de usuarios.
- Canciones: agregar, actualizar y eliminar canciones.
- Favoritos: gestionar las canciones favoritas de cada usuario.

El proyecto incluye documentación interactiva generada automáticamente con Swagger, disponible en el endpoint /docs.

## Estructura del Proyecto
lpa2-taller3_2026
├── .env                 # Variables de entorno
├── .gitignore           # Archivos que ignora Git
├── .pre-commit-config.yaml # Configuración de pre-commit
├── README.md            # Documentación del proyecto
├── main.py              # Archivo principal para ejecutar la aplicación
├── musica.db            # Base de datos
├── pyproject.toml       # Configuración del proyecto
├── pytest.ini           # Configuración de pytest
├── requirements.txt     # Dependencias del proyecto
├── seed.py              # Script para cargar datos de ejemplo
├── utils.py             # Funciones de utilidad
├── .github
│   └── workflows
│       └── ci.yml       # Workflow de GitHub Actions
├── musica_api
│   ├── __init__.py      # Inicialización del módulo
│   ├── config.py        # Configuración
│   ├── database.py      # Conexión a la base de datos
│   ├── models.py        # Modelos de la base de datos
│   ├── schemas.py       # Esquemas de validación con Pydantic
│   └── routers
│       ├── __init__.py  # Inicialización de routers
│       ├── canciones.py # Endpoints de canciones
│       ├── favoritos.py # Endpoints de favoritos
│       └── usuarios.py  # Endpoints de usuarios
└── tests
    └── test_api.py      # Pruebas unitarias
    
## Modelo de Datos

Usuario:
- id: Identificador único
- nombre: Nombre del usuario
- correo: Correo electrónico (único)
- fecha_registro: Fecha de registro

Canción:
- id: Identificador único
- titulo: Título de la canción
- artista: Artista o intérprete
- album: Álbum al que pertenece
- duracion: Duración en segundos
- año: Año de lanzamiento
- genero: Género musical
- fecha_creacion: Fecha de creación del registro

Favorito:
- id: Identificador único
- id_usuario: ID del usuario (clave foránea)
- id_cancion: ID de la canción (clave foránea)
- fecha_marcado: Fecha en que se marcó como favorito

## INSTALACION

## 1_Clonar el repositorio:
git clone https://github.com/UR-CC/lpa2-taller3.git
cd lpa2-taller3_2026

## 2_Crear y activar el entorno virtual:
python -m venv .venv
source .venv/bin/activate


## 3_Instalar las dependencias:
pip install -r requirements.txt

## Ejecución

## 1_Ejecutar la aplicación:

uvicorn main:app --reload


## Acceder a:

- API: http://127.0.0.1:8000/
- Documentación Swagger UI: http://127.0.0.1:8000/docs
- Documentación ReDoc: http://127.0.0.1:8000/redoc

## Uso de la API

Usuarios
- Listar usuarios: GET /api/usuarios
- Crear usuario: POST /api/usuarios
- Obtener usuario: GET /api/usuarios/{id}
- Actualizar usuario: PUT /api/usuarios/{id}
- Eliminar usuario: DELETE /api/usuarios/{id}

Canciones
- Listar canciones: GET /api/canciones
- Crear canción: POST /api/canciones
- Obtener canción: GET /api/canciones/{id}
- Actualizar canción: PUT /api/canciones/{id}
- Eliminar canción: DELETE /api/canciones/{id}
- Buscar canciones: GET /api/canciones/buscar?titulo=value&artista=value&genero=value

Favoritos
- Listar favoritos: GET /api/favoritos
- Marcar favorito: POST /api/favoritos
- Obtener favorito: GET /api/favoritos/{id}
- Eliminar favorito: DELETE /api/favoritos/{id}
- Listar favoritos de usuario: GET /api/usuarios/{id}/favoritos
- Marcar favorito específico: POST /api/usuarios/{id_usuario}/favoritos/{id_cancion}
- Eliminar favorito específico: DELETE /api/usuarios/{id_usuario}/favoritos/{id_cancion}

## Desarrollo del Taller

1. Ajustar README con los datos del estudiante
Listo. Los datos quedaron en la parte de arriba de este archivo.

2. Datos en DBeaver
Se agregaron directo en las tablas con DBeaver:
- 5 usuarios en la tabla usuario
- 10 canciones en la tabla cancion

3. Pre-commit y GitHub Actions
Se agregó el archivo .pre-commit-config.yaml y el workflow en .github/workflows/ci.yml para correr ruff (linter y formatter) y pytest en cada push y pull request.

## Para correrlo en local:
pre-commit run --all-files
ruff check .
ruff format .
pytest -v


4. Validación con Pydantic
Se usan schemas en musica_api/schemas.py, por ejemplo CancionCreate y CancionUpdate, con model_dump() para validar los datos antes de guardarlos en la base de datos.

5. Prueba en Swagger UI / ReDoc
Se probó el funcionamiento en /docs. Se probó crear un favorito, listar canciones y usuarios. También se verificó el error cuando se intenta crear un favorito duplicado y el código 201 al crear.

6. Pruebas automatizadas
Están en tests/test_api.py con pytest y TestClient. Verifican crear usuario, crear canción, crear favorito, que no se pueda repetir un favorito, la paginación y el health check.

pytest -v


## Sugerencias de Mejora

Para este taller se implementaron 2:

1. Paginación
En GET /api/canciones/, GET /api/usuarios/ y GET /api/favoritos/ se puede usar skip y limit:

GET /api/canciones/?skip=0&limit=10
GET /api/canciones/?skip=10&limit=10

Se hizo con Query(0, ge=0) y Query(10, ge=1, le=100) para no traer toda la tabla de una vez.

2. Registro (logging)
En main.py se agregó un middleware con logging que registra el método, la ruta, el status y el tiempo de cada petición, además de los errores de base de datos y los errores 500.

Otras sugerencias que no se implementaron en este taller:
- Autenticación y autorización con JWT o OAuth2
- Base de datos en producción como PostgreSQL o MySQL
- Docker
- Caché
- Estadísticas de uso
- Subida de archivos de audio a S3
