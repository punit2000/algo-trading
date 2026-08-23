"""
tests/unit/test_models.py — Unit tests for domain enums and models.
"""

from __future__ import annotations

from app.models import (
    Exchange,
    OrderStatus,
    RiskViolation,
    Side,
    TradingMode,
)


class TestSideEnum:
    def test_buy_value(self) -> None:
        assert Side.BUY.value == "BUY"

    def test_sell_value(self) -> None:
        assert Side.SELL.value == "SELL"

    def test_from_string(self) -> None:
        assert Side("BUY") == Side.BUY


class TestOrderStatusEnum:
    def test_all_statuses_defined(self) -> None:
        statuses = {s.value for s in OrderStatus}
        assert "CREATED" in statuses
        assert "SUBMITTED" in statuses
        assert "FILLED" in statuses
        assert "CANCELLED" in statuses
        assert "REJECTED" in statuses


class TestTradingModeEnum:
    def test_live_trading_mode_exists(self) -> None:
        assert TradingMode.LIVE.value == "LIVE"

    def test_backtest_mode_exists(self) -> None:
        assert TradingMode.BACKTEST.value == "BACKTEST"

    def test_paper_mode_exists(self) -> None:
        assert TradingMode.PAPER.value == "PAPER"


class TestExchangeEnum:
    def test_nse_exists(self) -> None:
        assert Exchange.NSE.value == "NSE"

    def test_bse_exists(self) -> None:
        assert Exchange.BSE.value == "BSE"

    def test_nfo_exists(self) -> None:
        assert Exchange.NFO.value == "NFO"


class TestRiskViolationEnum:
    def test_live_trading_disabled_violation(self) -> None:
        assert RiskViolation.LIVE_TRADING_DISABLED.value == "LIVE_TRADING_DISABLED"

    def test_kill_switch_violation(self) -> None:
        assert RiskViolation.KILL_SWITCH_ACTIVE.value == "KILL_SWITCH_ACTIVE"
