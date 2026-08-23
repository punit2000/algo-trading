"""
app.main — Application entry point.

Responsibilities at M0:
  - Load configuration
  - Configure logging
  - Print startup banner
  - Expose health_check() function

The HTTP server (FastAPI / uvicorn) is NOT started here at M0.
That is added in M9 (API + Dashboard milestone).

Run:
    uv run python -m app.main
"""

from __future__ import annotations

import platform
from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.config.logging_config import configure_logging, get_logger
from app.config.settings import get_settings
from app.models import TradingMode

# Module-level logger (configured after configure_logging() is called)
log = get_logger(__name__)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@dataclass
class HealthStatus:
    """
    Snapshot of the application's current health.

    Extended in later milestones to include DB, Redis, broker connectivity.
    """

    status: str                               # "ok" | "degraded" | "error"
    timestamp: str                            # ISO-8601 UTC
    app_name: str
    app_version: str
    app_env: str
    trading_mode: str
    live_trading_enabled: bool
    python_version: str
    checks: dict[str, str] = field(default_factory=dict)


def health_check() -> HealthStatus:
    """
    Perform a lightweight application health check.

    Returns:
        HealthStatus dataclass with current status snapshot.
    """
    settings = get_settings()

    # Determine current trading mode for display purposes
    if settings.live_trading:
        mode = TradingMode.LIVE
    elif settings.paper_trading:
        mode = TradingMode.PAPER
    else:
        mode = TradingMode.BACKTEST

    checks: dict[str, str] = {
        "config": "ok",
        "logging": "ok",
    }

    # DB check (stub — actual connectivity tested in M1+)
    checks["database"] = "not_configured" if not settings.db_url else "configured"
    checks["redis"] = "not_configured" if not settings.redis_url else "configured"

    return HealthStatus(
        status="ok",
        timestamp=datetime.now(tz=UTC).isoformat(),
        app_name=settings.app_name,
        app_version=settings.app_version,
        app_env=settings.app_env.value,
        trading_mode=mode.value,
        live_trading_enabled=settings.live_trading,
        python_version=platform.python_version(),
        checks=checks,
    )


# ---------------------------------------------------------------------------
# Startup banner
# ---------------------------------------------------------------------------


def _print_banner(settings_obj: object) -> None:
    """Print a startup summary to stdout."""
    from app.config.settings import Settings  # local import to avoid circularity

    s: Settings = settings_obj  # type: ignore[assignment]

    lines = [
        "",
        "=" * 56,
        f"  {s.app_name} v{s.app_version}",
        "=" * 56,
        f"  Environment  : {s.app_env.value}",
        f"  Log Level    : {s.log_level}",
        f"  Log Format   : {s.log_format}",
        f"  Live Trading : {'[WARNING] ENABLED' if s.live_trading else '[OK] DISABLED (safe)'}",
        f"  Paper Trading: {'ENABLED' if s.paper_trading else 'DISABLED'}",
        f"  Python       : {platform.python_version()}",
        "=" * 56,
        "",
    ]
    for line in lines:
        print(line)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """
    Application bootstrap.

    1. Load settings from environment / .env
    2. Configure structured logging
    3. Print startup banner
    4. Run health check
    5. Log result
    """
    # Step 1: load settings (may raise ValidationError for bad config)
    settings = get_settings()

    # Step 2: configure logging before any structured log calls
    configure_logging(
        log_level=settings.log_level,
        log_format=settings.log_format,
    )

    # Step 3: banner (plain print — logging not yet warmed up at this point)
    _print_banner(settings)

    # Step 4: health check
    health = health_check()

    # Step 5: structured log
    log.info(
        "application_started",
        app_name=health.app_name,
        version=health.app_version,
        env=health.app_env,
        trading_mode=health.trading_mode,
        live_trading=health.live_trading_enabled,
        checks=health.checks,
    )

    if health.live_trading_enabled:
        log.warning(
            "live_trading_enabled",
            message=(
                "⚠️  LIVE TRADING IS ENABLED. "
                "Real orders may be sent to a broker. "
                "Ensure all M12 safety checks have been completed."
            ),
        )


if __name__ == "__main__":
    main()
