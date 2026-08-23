"""
app.brokers — Broker adapter layer.

Implemented in M8.

Architecture:
    BaseBroker (abstract interface)
        ├── PaperBroker   — simulated fills, no real money (M7)
        └── RealBroker    — live NSE/BSE broker (M8, requires explicit activation)

The trading engine talks ONLY to BaseBroker.submit_order() etc.
It never imports a concrete broker directly.

BaseBroker interface (to be implemented):
    submit_order(order)   → broker_order_id
    cancel_order(id)      → bool
    get_order(id)         → Order
    get_positions()       → list[Position]
    get_balance()         → float
"""
