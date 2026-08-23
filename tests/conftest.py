"""
tests/conftest.py — Shared pytest fixtures.

Rules:
  - Never import real broker credentials here.
  - Always use Environment.TEST to prevent accidental production access.
  - Clear settings cache between tests that need fresh config.
"""

from __future__ import annotations

import pytest

from app.config.settings import Settings, get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache() -> None:
    """
    Clear the settings LRU cache before every test.

    This ensures each test that mutates env vars gets a fresh Settings object.
    """
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture()
def test_settings(monkeypatch: pytest.MonkeyPatch) -> Settings:
    """
    Return a Settings object configured for testing.

    Overrides:
      - APP_ENV = test
      - LOG_FORMAT = console  (no JSON noise in test output)
      - LIVE_TRADING = false  (safety — always)
      - DB_URL = ""           (no real DB in unit tests)
      - REDIS_URL = ""        (no real Redis in unit tests)
    """
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("LOG_FORMAT", "console")
    monkeypatch.setenv("LIVE_TRADING", "false")
    monkeypatch.setenv("DB_URL", "")
    monkeypatch.setenv("REDIS_URL", "")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-not-for-production")

    get_settings.cache_clear()
    return get_settings()
