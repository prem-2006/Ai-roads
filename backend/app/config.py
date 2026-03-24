from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    databricks_server_hostname: str = ""
    databricks_http_path: str = ""
    databricks_access_token: str = ""
    backend_cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins(self) -> list[str]:
        return [v.strip() for v in self.backend_cors_origins.split(",") if v.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
