"""
app.market_data — Market data ingestion and management.

Implemented in M1.

Responsibilities:
  - Load historical OHLCV data (CSV → pandas → DB)
  - Validate data quality (missing timestamps, bad prices, etc.)
  - Eventually: live WebSocket feed from broker (M7+)
"""
