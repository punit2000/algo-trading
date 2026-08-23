# algo-trading

> Production-quality algorithmic trading platform for NSE/BSE Indian markets.

---

## ⚠️ Safety Notice

**Live trading is disabled by default** and must remain so until all [M12 readiness checks](#m12-live-trading-readiness) are completed.

```
LIVE_TRADING=false   ← always the default
```

---

## Project Roadmap

| Milestone | Description | Status |
|-----------|-------------|--------|
| **M0** | Environment & Architecture | ✅ Complete |
| **M1** | Market Data (OHLCV, validation, storage) | 🔲 Upcoming |
| **M2** | Strategy Engine (BaseStrategy, SMA) | 🔲 |
| **M3** | Backtesting Engine | 🔲 |
| **M4** | Realistic Backtesting (commission, slippage) | 🔲 |
| **M5** | Multiple Strategies (RSI, Momentum, etc.) | 🔲 |
| **M6** | Risk Engine (position limits, kill switch) | 🔲 |
| **M7** | Paper Trading | 🔲 |
| **M8** | Broker Integration (NSE/BSE) | 🔲 |
| **M9** | REST API + Web Dashboard | 🔲 |
| **M10** | Observability (Prometheus + Grafana) | 🔲 |
| **M11** | Production Infrastructure (Docker, K8s, CI/CD) | 🔲 |
| **M12** | Live Trading Readiness | 🔲 |

---

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (package manager)

### Setup

```bash
# Clone
git clone <your-repo-url>
cd algo-trading

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --dev

# Copy and configure environment
cp .env.example .env
# Edit .env with your settings — leave LIVE_TRADING=false

# Run the application
uv run python -m app.main

# Run health check
uv run python scripts/health_check.py
```

### Development Commands

```bash
# Lint
uv run ruff check app/ tests/

# Format
uv run ruff format app/ tests/

# Type check
uv run mypy app/

# Tests
uv run pytest tests/ -v

# Tests with coverage
uv run pytest tests/ --cov=app --cov-report=term-missing
```

### Docker

```bash
# Build
docker build -f docker/Dockerfile -t algo-trading:latest .

# Run with Docker Compose (requires .env)
cd docker
docker compose up
```

---

## Architecture

```
algo-trading/
│
├── app/
│   ├── main.py              # Entry point, health check
│   ├── config/
│   │   ├── settings.py      # Pydantic-settings (env vars → typed config)
│   │   └── logging_config.py # Structlog (console/JSON)
│   ├── models/              # Domain enums: Side, OrderStatus, Exchange…
│   ├── strategies/          # Strategy interface + implementations (M2+)
│   ├── market_data/         # OHLCV data loading & validation (M1+)
│   ├── backtesting/         # Backtest engine, execution simulator (M3+)
│   ├── portfolio/           # Portfolio, positions, P&L (M3+)
│   ├── risk/                # Risk engine, limits, kill switch (M6+)
│   ├── execution/           # Order execution pipeline (M3+)
│   ├── brokers/             # Broker abstraction: Paper + Real (M7+, M8+)
│   ├── database/            # SQLAlchemy async engine (M1+)
│   └── api/                 # FastAPI routes (M9+)
│
├── tests/
│   ├── unit/                # Fast, isolated — no external services
│   ├── integration/         # Requires DB, Redis (M1+)
│   └── regression/          # Backtest must produce exact known results (M3+)
│
├── scripts/                 # Operational scripts
├── data/                    # Local OHLCV CSV files (never committed)
├── migrations/              # Alembic DB migrations (M1+)
├── docker/                  # Dockerfile + docker-compose.yml
├── helm/                    # Kubernetes Helm charts (M11+)
├── docs/                    # Architecture Decision Records
└── .github/workflows/       # GitHub Actions CI
```

### Data & Trading Flow

```
Strategy
    ↓
Signal
    ↓
Risk Manager
    ↓
Order
    ↓
Execution (Paper / Live Broker)
    ↓
Position
    ↓
Portfolio
    ↓
P&L
```

### Environment Progression

```
Backtesting (historical data)
    ↓
Paper Trading (live data, simulated fills)
    ↓
Live Trading (only after M12 checks pass)
```

The **same strategy code** runs unchanged across all three environments.

---

## Configuration

All configuration is loaded from environment variables (and `.env`).

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `development` | `development` / `staging` / `production` / `test` |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `LOG_FORMAT` | `console` | `console` (dev) / `json` (production) |
| `LIVE_TRADING` | **`false`** | ⚠️ Only `true` after M12 checks |
| `PAPER_TRADING` | `false` | Enable paper trading mode |
| `DB_URL` | _(empty)_ | PostgreSQL async URL (M1+) |
| `REDIS_URL` | _(empty)_ | Redis URL (M7+) |
| `SECRET_KEY` | _(empty)_ | Token signing key (M9+) |

See `.env.example` for the full list.

---

## Agent Handoff Protocol

Any AI agent working on this project must:

1. **Inspect before modifying** — read existing code, tests, and this README first
2. **Preserve module boundaries** — Strategy / Risk / Execution / Portfolio are separate
3. **Never enable live trading** — `LIVE_TRADING=false` is always the default
4. **Never hard-code secrets** — use env vars only
5. **Run tests after every change** — `pytest tests/ -v`
6. **No look-ahead bias** — strategies must never use future data
7. **Document assumptions** — every backtest must state dataset, period, commission, slippage

---

## M12 Live Trading Readiness

Before live trading can be considered:

- [ ] Backtests validated on out-of-sample data
- [ ] Paper trading completed successfully
- [ ] Risk limits tested and confirmed working
- [ ] Kill switch tested
- [ ] Broker reconciliation tested
- [ ] Duplicate-order protection verified
- [ ] Failure recovery tested
- [ ] Monitoring (Prometheus + Grafana) operational
- [ ] Alerts configured
- [ ] Secrets secured (no keys in Git)
- [ ] Audit logging operational
- [ ] Capital limits configured

---

## License

MIT
