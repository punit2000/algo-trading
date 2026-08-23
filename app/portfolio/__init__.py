"""
app.portfolio — Portfolio and position management.

Implemented in M3.

Responsibilities:
  - Track cash balance
  - Track open positions (symbol, quantity, average entry price)
  - Calculate realized P&L (on close)
  - Calculate unrealized P&L (mark-to-market)
  - Calculate total portfolio value
  - Track exposure and allocation

The Portfolio is the single source of truth for financial state.
"""
