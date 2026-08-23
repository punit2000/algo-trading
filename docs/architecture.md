# Architecture Decision Records — M0

This document records the key architectural decisions made during M0 (Environment & Architecture).

---

## ADR-001: Package Manager — `uv` over `pip`

**Date**: M0

**Status**: Accepted

**Problem**: Python projects need a way to manage dependencies and virtual environments.
Traditional `pip + venv` is slow, fragile with lock files, and requires multiple tools.

**Options considered**:
- `pip + venv + pip-tools` — standard, familiar, slow
- `poetry` — popular, opinionated, complex dependency resolver
- `uv` — new Astral tool, extremely fast, PEP 517/621 native

**Decision**: Use `uv`.

**Reasons**:
- 10–100× faster than pip for installs
- Handles venv automatically (`uv sync` creates `.venv`)
- PEP 621 compliant — all config in `pyproject.toml`
- Lock file (`uv.lock`) is fully reproducible
- Compatible with standard `pyproject.toml` — no vendor lock-in

**Trade-offs**:
- Relatively new (2024) — some CI/CD systems may need the astral-sh/setup-uv action
- Less documentation than pip, but growing fast

---

## ADR-002: Linting & Formatting — `ruff` over `flake8 + black + isort`

**Date**: M0

**Status**: Accepted

**Problem**: Python code quality requires linting, formatting, and import sorting.
Using three tools (flake8, black, isort) is slow and has subtle conflicts.

**Options considered**:
- `flake8 + black + isort` — traditional trio, widely known
- `pylint + black + isort` — more checks, very slow
- `ruff` — single tool replacing all three

**Decision**: Use `ruff`.

**Reasons**:
- Replaces flake8, black, isort, and more in one tool
- 10–100× faster (written in Rust)
- Single `[tool.ruff]` section in `pyproject.toml`
- Compatible with black formatting style

**Trade-offs**:
- Some niche flake8 plugins not yet ported to ruff
- Newer tool — some teams unfamiliar

---

## ADR-003: Configuration — `pydantic-settings` over raw `os.environ`

**Date**: M0

**Status**: Accepted

**Problem**: The application needs typed, validated configuration from env vars.
Raw `os.environ.get("FOO", "bar")` scattered across the codebase is error-prone.

**Options considered**:
- `os.environ` + manual parsing — simple but no validation, no types
- `python-decouple` — popular but no type validation
- `dynaconf` — powerful but heavy
- `pydantic-settings` — Pydantic v2, typed, validated, `.env` support

**Decision**: Use `pydantic-settings`.

**Reasons**:
- All settings in one typed `BaseSettings` class
- Pydantic validation catches bad config at startup
- `.env` file support out of the box
- Already using Pydantic for data models (M1+) — consistent ecosystem

**Trade-offs**:
- Adds pydantic + pydantic-settings as dependencies (worth it)

---

## ADR-004: Structured Logging — `structlog` over `logging`

**Date**: M0

**Status**: Accepted

**Problem**: A trading platform needs machine-parseable logs for observability.
Standard `logging` produces unstructured text strings.

**Options considered**:
- `logging` standard library — familiar, unstructured
- `loguru` — prettier, but not JSON-native
- `structlog` — structured, key=value or JSON, highly configurable

**Decision**: Use `structlog`.

**Reasons**:
- Every log call is `log.info("event", key=value, key2=value2)`
- In development: coloured human-readable output
- In production: one JSON object per line — parseable by Prometheus, Grafana, ELK
- Context variables (`structlog.contextvars`) allow per-request log enrichment (M9+)
- No performance penalty — Rust-speed output via PrintLoggerFactory

**Trade-offs**:
- Different API from stdlib `logging` — slight learning curve

---

## ADR-005: `LIVE_TRADING=false` as a Hard Default

**Date**: M0

**Status**: Non-negotiable.

**Problem**: A trading system that accidentally sends real orders is catastrophic.

**Decision**:
- `LIVE_TRADING` defaults to `False` in `Settings`
- The validator only accepts explicit `"true"` (case-insensitive) — not `"yes"`, `"1"`, `"on"`
- Docker Compose explicitly sets `LIVE_TRADING=false` as an environment override
- CI always sets `LIVE_TRADING=false`
- The Risk Engine (M6) will hard-block any live order if `live_trading=False`

This ensures live trading requires three independent changes:
1. `.env` file change
2. Broker credentials available
3. Risk engine configured

**Trade-offs**: None. This is a safety requirement, not a trade-off.

---

## System Architecture (Target — M12)

```
                     ┌─────────────────┐
                     │    Dashboard    │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    FastAPI      │
                     └────────┬────────┘
                              │
                 ┌────────────┼────────────┐
                 │            │            │
                 ▼            ▼            ▼
           Strategy       Portfolio     Risk
            Engine         Engine       Engine
                 │            │            │
                 └────────────┼────────────┘
                              ▼
                     ┌─────────────────┐
                     │  Order Manager  │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Broker Adapter  │
                     └────────┬────────┘
                              │
                    ┌─────────┴──────────┐
                    ▼                    ▼
              PaperBroker           RealBroker
                (M7)                  (M8)
                                       │
                                  Broker API
                                       │
                                   Exchange (NSE/BSE)


Market Data ────► Market Data Service
                       │
               ┌───────┴───────┐
               ▼               ▼
            Redis          PostgreSQL
               │               │
               └───────┬───────┘
                       ▼
                 Trading Engine


           ┌──────────────────┐
           │    Prometheus    │
           └────────┬─────────┘
                    ▼
           ┌──────────────────┐
           │     Grafana      │
           └──────────────────┘
```
