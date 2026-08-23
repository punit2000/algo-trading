"""
tests/unit/test_health.py — Unit tests for the health check.
"""

from __future__ import annotations

from app.config.settings import Settings
from app.main import HealthStatus, health_check


class TestHealthCheck:
    def test_health_check_returns_ok(self, test_settings: Settings) -> None:
        result = health_check()
        assert isinstance(result, HealthStatus)
        assert result.status == "ok"

    def test_health_check_live_trading_disabled(self, test_settings: Settings) -> None:
        result = health_check()
        assert result.live_trading_enabled is False

    def test_health_check_has_timestamp(self, test_settings: Settings) -> None:
        result = health_check()
        assert result.timestamp  # non-empty string
        assert "T" in result.timestamp  # ISO-8601 format

    def test_health_check_includes_config_check(self, test_settings: Settings) -> None:
        result = health_check()
        assert result.checks.get("config") == "ok"

    def test_health_check_includes_logging_check(self, test_settings: Settings) -> None:
        result = health_check()
        assert result.checks.get("logging") == "ok"

    def test_health_check_db_not_configured(self, test_settings: Settings) -> None:
        result = health_check()
        assert result.checks.get("database") == "not_configured"

    def test_health_check_redis_not_configured(self, test_settings: Settings) -> None:
        result = health_check()
        assert result.checks.get("redis") == "not_configured"
