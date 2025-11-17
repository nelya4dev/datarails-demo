import pathlib
from typing import List, Optional
from enum import Enum

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

#: Root directory of the application (backend/)
ROOT = pathlib.Path(__file__).resolve().parent.parent


class AppMode(str, Enum):
    """Application running mode enum.

    Attributes:
        DEVELOPMENT: Development mode (enables Swagger UI, verbose errors)
        PRODUCTION: Production mode (disables docs, minimal error exposure)
    """
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
    )

    # --- Database ---
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: SecretStr

    # --- Timezone and datetime format ---
    TIMEZONE: str = "UTC"
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%fZ"  # ISO 8601 format with Z suffix for UTC

    # --- Application Settings ---
    APP_MODE: AppMode = AppMode.DEVELOPMENT

    # --- API Settings ---
    API_PATH: str = "/api/v1"

    # --- CORS Settings ---
    CORS_ALLOW_ALL_ORIGINS: bool = False
    CORS_ALLOWED_ORIGINS: str = ""

    # --- Security Settings ---
    ALLOWED_HOSTS: str = ""  # Comma-separated list of allowed hosts (e.g., "api.example.com,example.com")

    # --- File Upload Settings ---
    UPLOAD_DIR: str = "/tmp/uploads"
    UPLOAD_MAX_FILE_SIZE: int = 10485760  # 10MB in bytes

    # --- Celery / Redis Settings ---
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    # --- Config File Path ---
    CONFIG_CSV_PATH: str = "config/config.csv"

    @field_validator('DB_PORT')
    @classmethod
    def validate_db_port(cls, v: int) -> int:
        if not 1 <= v <= 65535:
            raise ValueError('DB_PORT must be between 1 and 65535')
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from string to list.

        Returns:
            List of allowed CORS origins (full URLs with protocol).
            Empty list if CORS_ALLOWED_ORIGINS not configured.

        Example:
            CORS_ALLOWED_ORIGINS="https://app.example.com,https://admin.example.com"
            → ["https://app.example.com", "https://admin.example.com"]
        """
        if not self.CORS_ALLOWED_ORIGINS:
            return []
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",") if origin.strip()]

    @property
    def allowed_hosts_list(self) -> List[str]:
        """Parse allowed hosts from string to list.

        Returns:
            List of allowed hosts (domain names only, no protocol).
            Returns ["*"] if ALLOWED_HOSTS not configured (allows all hosts).

        Note:
            In production, should be set to actual domain names for security.
            In development, can be left empty to allow all hosts.

        Example:
            ALLOWED_HOSTS="api.example.com,example.com"
            → ["api.example.com", "example.com"]

            ALLOWED_HOSTS=""
            → ["*"]  # Allow all hosts
        """
        if not self.ALLOWED_HOSTS:
            return ["*"]  # Default to allow all if not configured
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",") if host.strip()]

    @property
    def DATABASE_URL(self) -> str:
        """Generate database URL for SQLAlchemy.

        Returns:
            PostgreSQL connection URL with credentials.

        Example:
            postgresql+psycopg://user:pass@localhost:5432/dbname
        """
        pwd = self.DB_PASSWORD.get_secret_value()
        return f"postgresql+psycopg://{self.DB_USER}:{pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def is_development(self) -> bool:
        """Check if app is in development mode.

        Returns:
            True if APP_MODE is DEVELOPMENT, False otherwise.
        """
        return self.APP_MODE == AppMode.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """Check if app is in production mode.

        Returns:
            True if APP_MODE is PRODUCTION, False otherwise.
        """
        return self.APP_MODE == AppMode.PRODUCTION

    @property
    def CONFIG_CSV_ABSOLUTE_PATH(self) -> pathlib.Path:
        """Get absolute path to config.csv file.

        Returns:
            Absolute path to config.csv relative to application root.

        Example:
            /application_root/config/config.csv
        """
        # ROOT is /application_root/src/backend
        # We need /application_root/config/config.csv
        return ROOT.parent.parent / self.CONFIG_CSV_PATH

    @property
    def UPLOAD_DIR_ABSOLUTE_PATH(self) -> pathlib.Path:
        """Get absolute path to upload directory.

        Returns:
            Absolute path to upload directory.
            If UPLOAD_DIR is already absolute, returns as-is.
            If relative, resolves from application root.

        Example:
            UPLOAD_DIR="/tmp/uploads" → /tmp/uploads
            UPLOAD_DIR="uploads" → /application_root/uploads
        """
        upload_path = pathlib.Path(self.UPLOAD_DIR)

        # If already absolute, use as-is
        if upload_path.is_absolute():
            return upload_path

        # Otherwise, resolve from application root
        return ROOT.parent.parent / upload_path


#: Global settings instance loaded from environment variables and .env file.
#: Use this singleton throughout the application for configuration access.
settings = Settings()
