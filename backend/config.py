import os
from pathlib import Path
from pydantic_settings import BaseSettings

# .env lives at the project root (parent of this file's directory)
_HERE = Path(__file__).parent
_ENV_PATHS = [_HERE / ".env", _HERE.parent / ".env"]
_ENV_FILE = next((str(p) for p in _ENV_PATHS if p.exists()), ".env")


class Settings(BaseSettings):
    mongodb_uri: str
    db_name: str = "healthcare_demo"
    voyage_api_key: str
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    cors_origin: str = "http://localhost:5173"

    class Config:
        env_file = _ENV_FILE
        env_file_encoding = "utf-8"
        extra = "ignore"  # allow .env to carry keys used only by shell scripts (e.g. FRONTEND_PORT)


settings = Settings()
