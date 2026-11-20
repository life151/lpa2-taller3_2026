from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "API de Música"
    app_version: str = "1.0.0"
    environment: str = "development"
    database_url: str = "sqlite:///./musica.db"
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True
    cors_origins: list[str] = ["*"]
    secret_key: str = "cambia-esta-clave-en-produccion"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL no puede estar vacío")
        return v


settings = Settings()


class DevelopmentSettings(Settings):
    debug: bool = True


class TestingSettings(Settings):
    database_url: str = "sqlite:///./test_musica.db"


class ProductionSettings(Settings):
    debug: bool = False
    database_url: str = "sqlite:///./musica_prod.db"


def get_settings() -> Settings:
    env = settings.environment.lower()
    if env == "testing":
        return TestingSettings()
    elif env == "production":
        return ProductionSettings()
    return DevelopmentSettings()


def validate_settings():
    for campo in ["database_url", "app_name"]:
        if not getattr(settings, campo, None):
            raise ValueError(f"Configuración requerida no encontrada: {campo}")
