"""
tests/unit/test_config.py — Unit tests for configuration loading.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.config.settings import Settings, get_settings
from app.models import Environment


class TestSettingsDefaults:
    """Verify that default values are safe and correct."""

    def test_live_trading_defaults_to_false(self, test_settings: Settings) -> None:
        """LIVE_TRADING must default to False — critical safety requirement."""
        assert test_settings.live_trading is False

    def test_paper_trading_defaults_to_false(self, test_settings: Settings) -> None:
        assert test_settings.paper_trading is False

    def test_app_env_defaults_to_test_in_test_settings(
        self, test_settings: Settings
    ) -> None:
        assert test_settings.app_env == Environment.TEST

    def test_log_level_default(self, test_settings: Settings) -> None:
        assert test_settings.log_level == "INFO"

    def test_paper_initial_capital_positive(self, test_settings: Settings) -> None:
        assert test_settings.paper_initial_capital > 0

    def test_api_port_in_valid_range(self, test_settings: Settings) -> None:
        assert 1 <= test_settings.api_port <= 65535


class TestLiveTradingValidator:
    """Verify that LIVE_TRADING env var is parsed safely."""

    def test_live_trading_false_from_string_false(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LIVE_TRADING", "false")
        get_settings.cache_clear()
        s = get_settings()
        assert s.live_trading is False

    def test_live_trading_false_from_string_zero(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LIVE_TRADING", "0")
        get_settings.cache_clear()
        s = get_settings()
        assert s.live_trading is False

    def test_live_trading_false_from_empty_string(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LIVE_TRADING", "")
        get_settings.cache_clear()
        s = get_settings()
        assert s.live_trading is False

    def test_live_trading_true_only_from_explicit_true(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LIVE_TRADING", "true")
        get_settings.cache_clear()
        s = get_settings()
        assert s.live_trading is True

    def test_live_trading_true_case_insensitive(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LIVE_TRADING", "TRUE")
        get_settings.cache_clear()
        s = get_settings()
        assert s.live_trading is True

    def test_live_trading_random_string_is_false(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LIVE_TRADING", "yes")
        get_settings.cache_clear()
        s = get_settings()
        # Only "true" should enable live trading
        assert s.live_trading is False


class TestSettingsFromEnv:
    """Verify env vars are read correctly."""

    def test_app_name_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("APP_NAME", "my-trading-platform")
        get_settings.cache_clear()
        s = get_settings()
        assert s.app_name == "my-trading-platform"

    def test_log_level_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        get_settings.cache_clear()
        s = get_settings()
        assert s.log_level == "DEBUG"

    def test_invalid_app_env_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("APP_ENV", "invalid_env")
        get_settings.cache_clear()
        with pytest.raises(ValidationError):
            get_settings()

    def test_invalid_log_level_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("LOG_LEVEL", "VERBOSE")
        get_settings.cache_clear()
        with pytest.raises(ValidationError):
            get_settings()


class TestSettingsProperties:
    """Verify computed properties."""

    def test_is_test_true_in_test_mode(self, test_settings: Settings) -> None:
        assert test_settings.is_test is True

    def test_is_production_false_in_test_mode(self, test_settings: Settings) -> None:
        assert test_settings.is_production is False

    def test_is_development_false_in_test_mode(self, test_settings: Settings) -> None:
        assert test_settings.is_development is False

    def test_is_production_true(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("APP_ENV", "production")
        get_settings.cache_clear()
        s = get_settings()
        assert s.is_production is True


class TestSettingsCacheSingleton:
    """Verify settings are cached (same object returned)."""

    def test_get_settings_returns_same_instance(self) -> None:
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2
