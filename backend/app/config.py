from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    database_url: str = "sqlite:///./issuehub.db"
    secret_key: str = "super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: str = "http://localhost:5173"
    # Preferred password hashing scheme for new hashes. Set to "bcrypt" in
    # production if your environment supports the bcrypt backend. Keep
    # "pbkdf2_sha256" for CI/dev portability.
    preferred_password_scheme: str = "pbkdf2_sha256"

settings = Settings()
