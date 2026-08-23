"""
app.config.settings — Application configuration via pydantic-settings.

All settings are loaded from environment variables (and optionally a .env file).
No secrets are hard-coded here.

Usage:
    from app.config.settings import get_settings
    settings = get_settings()
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.models import Environment


class Settings(BaseSettings):
    """
    Central configuration object.

    All fields map directly to environment variables.
    Fields with no default are *required* in production.
    Fields with a default are optional and safe to omit in development.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # silently ignore unknown env vars
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    app_name: str = Field(default="algo-trading", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    app_env: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Deployment environment",
    )

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Minimum log level",
    )
    log_format: Literal["console", "json"] = Field(
        default="console",
        description="'console' for development, 'json' for production",
    )

    # ------------------------------------------------------------------
    # ⚠️  LIVE TRADING SAFETY SWITCH
    # ------------------------------------------------------------------
    # This MUST remain False unless all M12 safety checks are passed.
    # The risk engine will hard-block any live order if this is False.
    # ------------------------------------------------------------------
    live_trading: bool = Field(
        default=False,
        description=(
            "SAFETY: enables real order submission to a broker. "
            "Must NOT be set to True until M12 readiness checks pass."
        ),
    )

    # ------------------------------------------------------------------
    # Paper Trading
    # ------------------------------------------------------------------
    paper_trading: bool = Field(
        default=False,
        description="Enable simulated paper-trading mode",
    )
    paper_initial_capital: float = Field(
        default=100_000.0,
        gt=0,
        description="Starting capital for paper-trading (₹)",
    )

    # ------------------------------------------------------------------
    # Database (PostgreSQL via asyncpg)
    # ------------------------------------------------------------------
    db_url: str = Field(
        default="",
        description=(
            "SQLAlchemy async DB URL. "
            "Example: postgresql+asyncpg://user:pass@localhost:5432/algo_trading"
        ),
    )

    # ------------------------------------------------------------------
    # Redis
    # ------------------------------------------------------------------
    redis_url: str = Field(
        default="",
        description="Redis connection URL. Example: redis://localhost:6379/0",
    )

    # ------------------------------------------------------------------
    # Security
    # ------------------------------------------------------------------
    secret_key: str = Field(
        default="",
        description=(
            "Secret key for signing tokens. "
            "Generate with: python -c \"import secrets; print(secrets.token_hex(32))\""
        ),
    )

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------
    api_host: str = Field(default="0.0.0.0", description="API server bind host")  # noqa: S104
    api_port: int = Field(default=8000, ge=1, le=65535, description="API server port")
    api_reload: bool = Field(default=False, description="Uvicorn auto-reload (dev only)")

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------

    @field_validator("live_trading", mode="before")
    @classmethod
    def validate_live_trading(cls, v: object) -> bool:
        """
        Accept common truthy string representations from env vars.
        Anything other than an explicit 'true' (case-insensitive) is False.
        """
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.strip().lower() == "true"
        return bool(v)

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def is_production(self) -> bool:
        """True when running in the production environment."""
        return self.app_env == Environment.PRODUCTION

    @property
    def is_development(self) -> bool:
        """True when running in development."""
        return self.app_env == Environment.DEVELOPMENT

    @property
    def is_test(self) -> bool:
        """True during pytest runs."""
        return self.app_env == Environment.TEST


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return the cached application settings singleton.

    Using lru_cache ensures settings are loaded once per process.
    In tests, call get_settings.cache_clear() before each test that
    needs fresh settings.
    """
    return Settings()
