"""
app.execution — Order execution pipeline.

Implemented in M3 (simulated) and M8 (live broker).

Responsibilities:
  - Accept orders from the Order Management System
  - Route to the appropriate broker (PaperBroker or RealBroker)
  - Track fill events and update Portfolio

Never directly modify Portfolio state — publish fill events instead.
"""
