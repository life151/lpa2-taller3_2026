import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from musica_api.config import settings
from musica_api.database import create_db_and_tables, engine
from musica_api.routers import canciones, favoritos, usuarios

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    logger.info("App iniciada")
    yield
    logger.info("Cerrando aplicación...")
    engine.dispose()


app = FastAPI(
    title="API de Música",
    description="API RESTful para gestionar usuarios, canciones y favoritos. FastAPI + SQLModel + Pydantic.",
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Lina Fernanda Chamorro Diaz",
        "email": "lina.chamorro.0604@miremington.edu.co",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {time.time() - start:.4f}s")
    return response


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Recurso no encontrado", "path": str(request.url.path)},
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Error interno: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})


app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(canciones.router, prefix="/api/canciones", tags=["Canciones"])
app.include_router(favoritos.router, prefix="/api/favoritos", tags=["Favoritos"])


@app.get("/", tags=["Root"])
async def root():
    return {
        "mensaje": "Bienvenido a la API de Música",
        "version": "1.0.0",
        "autora": "Lina Fernanda Chamorro Diaz",
        "documentacion": "/docs",
        "endpoints": {
            "usuarios": "/api/usuarios",
            "canciones": "/api/canciones",
            "favoritos": "/api/favoritos",
        },
    }


@app.get("/health", tags=["Health"])
async def health_check():
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        db_status = "conectada"
    except Exception as e:
        logger.error(f"Error BD: {e}")
        return JSONResponse(status_code=503, content={"status": "unhealthy", "database": "error"})
    return {
        "status": "healthy",
        "database": db_status,
        "version": "1.0.0",
        "entorno": settings.environment,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
