"""
app.backtesting — Historical backtesting engine.

Implemented in M3.

Components:
  BacktestEngine       — drives the event loop over historical data
  ExecutionSimulator   — simulates fills with configurable slippage/commission
  PerformanceAnalyzer  — calculates Sharpe, Sortino, drawdown, win-rate, etc.

The same Strategy interface used here is also used in paper and live trading.
"""
