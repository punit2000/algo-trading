"""
app.strategies — Strategy engine.

BaseStrategy and concrete strategies implemented in M2.

Architecture:
    BaseStrategy
        ├── SMAStrategy     (M2)
        ├── RSIStrategy     (M5)
        ├── MomentumStrategy (M5)
        ├── MeanReversionStrategy (M5)
        └── BreakoutStrategy (M5)

A strategy receives market data and emits a Signal.
It has NO knowledge of whether it is being backtested,
paper-traded, or live-traded.
"""
