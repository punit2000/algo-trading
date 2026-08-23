"""
app.config.logging_config — Structured logging via structlog.

Two output modes:
  - console  (development): coloured, human-readable key=value pairs
  - json     (production):  one JSON object per line, machine-parseable

Usage:
    from app.config.logging_config import configure_logging
    configure_logging(log_level="INFO", log_format="console")

Every log record automatically includes:
    timestamp, level, logger, event
"""

from __future__ import annotations

import logging
import sys
from typing import Literal

import structlog


def configure_logging(
    log_level: str = "INFO",
    log_format: Literal["console", "json"] = "console",
) -> None:
    """
    Configure structlog and the standard-library logging bridge.

    Call this ONCE at application startup before any logging occurs.

    Args:
        log_level:  Standard level name (DEBUG / INFO / WARNING / ERROR / CRITICAL).
        log_format: Output format — 'console' for development, 'json' for production.
    """
    # Map string level to stdlib int
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Configure stdlib root logger (captures third-party library logs too)
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=numeric_level,
    )

    # Shared processors that run for every log record regardless of format
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
    ]

    if log_format == "json":
        # Production: machine-readable JSON
        processors: list[structlog.types.Processor] = [
            *shared_processors,
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    else:
        # Development: pretty coloured console output
        processors = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.BoundLogger:
    """
    Return a structlog bound logger.

    Args:
        name: Logger name (usually __name__ of the calling module).

    Returns:
        A structlog BoundLogger ready to use.

    Example:
        log = get_logger(__name__)
        log.info("order_submitted", order_id="abc-123", symbol="RELIANCE")
    """
    return structlog.get_logger(name)  # type: ignore[no-any-return]
