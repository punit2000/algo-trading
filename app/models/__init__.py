"""
app.models — Shared domain models, enums, and type aliases.

These are imported by every other module.  They have NO external dependencies
(no DB, no broker, no strategy logic) so there are no circular imports.
"""

from __future__ import annotations

from enum import StrEnum

# ---------------------------------------------------------------------------
# Market / Instrument
# ---------------------------------------------------------------------------


class Exchange(StrEnum):
    """Supported Indian exchanges."""

    NSE = "NSE"
    BSE = "BSE"
    NFO = "NFO"   # NSE Futures & Options
    BFO = "BFO"   # BSE Futures & Options
    MCX = "MCX"   # Multi Commodity Exchange


class InstrumentType(StrEnum):
    """Broad classification of tradeable instruments."""

    EQUITY = "EQUITY"
    FUTURES = "FUTURES"
    OPTIONS = "OPTIONS"
    ETF = "ETF"
    INDEX = "INDEX"
    CURRENCY = "CURRENCY"
    COMMODITY = "COMMODITY"


# ---------------------------------------------------------------------------
# Orders
# ---------------------------------------------------------------------------


class Side(StrEnum):
    """Order direction."""

    BUY = "BUY"
    SELL = "SELL"


class OrderType(StrEnum):
    """How the order should be executed."""

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"


class OrderValidity(StrEnum):
    """Time-in-force / validity types common in NSE/BSE."""

    DAY = "DAY"      # Cancel at end of trading session
    IOC = "IOC"      # Immediate-or-Cancel
    GTC = "GTC"      # Good-Till-Cancelled (not all brokers support)


class OrderStatus(StrEnum):
    """Full lifecycle of an internal order."""

    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    OPEN = "OPEN"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------


class SignalType(StrEnum):
    """What a strategy wants to do."""

    ENTER_LONG = "ENTER_LONG"
    EXIT_LONG = "EXIT_LONG"
    ENTER_SHORT = "ENTER_SHORT"
    EXIT_SHORT = "EXIT_SHORT"
    HOLD = "HOLD"


# ---------------------------------------------------------------------------
# Portfolio / Positions
# ---------------------------------------------------------------------------


class PositionSide(StrEnum):
    """Direction of an open position."""

    LONG = "LONG"
    SHORT = "SHORT"


# ---------------------------------------------------------------------------
# System / Environment
# ---------------------------------------------------------------------------


class Environment(StrEnum):
    """Deployment environment."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class TradingMode(StrEnum):
    """
    Current operating mode of the trading engine.

    BACKTEST     — running against historical data only
    PAPER        — simulated execution against live market data
    LIVE         — real orders sent to a broker
                   (requires explicit LIVE_TRADING=true)
    """

    BACKTEST = "BACKTEST"
    PAPER = "PAPER"
    LIVE = "LIVE"


# ---------------------------------------------------------------------------
# Risk events
# ---------------------------------------------------------------------------


class RiskViolation(StrEnum):
    """Reasons a risk manager may reject or modify an order."""

    MAX_POSITION_SIZE = "MAX_POSITION_SIZE"
    MAX_PORTFOLIO_EXPOSURE = "MAX_PORTFOLIO_EXPOSURE"
    MAX_DAILY_LOSS = "MAX_DAILY_LOSS"
    MAX_OPEN_POSITIONS = "MAX_OPEN_POSITIONS"
    MAX_ORDER_VALUE = "MAX_ORDER_VALUE"
    LIVE_TRADING_DISABLED = "LIVE_TRADING_DISABLED"
    KILL_SWITCH_ACTIVE = "KILL_SWITCH_ACTIVE"


__all__ = [
    "Environment",
    "Exchange",
    "InstrumentType",
    "OrderStatus",
    "OrderType",
    "OrderValidity",
    "PositionSide",
    "RiskViolation",
    "Side",
    "SignalType",
    "TradingMode",
]
