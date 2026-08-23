"""
app.risk — Risk management engine.

Implemented in M6.

Pipeline:
    Strategy Signal
        ↓
    RiskManager.evaluate(signal)
        ↓
    ALLOWED / REJECTED / MODIFIED
        ↓
    Order

Hard limits enforced:
    MAX_POSITION_SIZE
    MAX_PORTFOLIO_EXPOSURE
    MAX_DAILY_LOSS
    MAX_OPEN_POSITIONS
    MAX_ORDER_VALUE
    LIVE_TRADING_DISABLED (if settings.live_trading is False)
    KILL_SWITCH_ACTIVE

The Risk Engine is independent of the Strategy.
"""
