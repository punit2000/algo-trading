#!/usr/bin/env python
"""
scripts/health_check.py — Standalone health check CLI.

Exits with code 0 if healthy, 1 otherwise.

Usage:
    uv run python scripts/health_check.py
    uv run python scripts/health_check.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict


def main() -> None:
    parser = argparse.ArgumentParser(description="algo-trading health check")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output health status as JSON",
    )
    args = parser.parse_args()

    # Import here so the module path is available
    from app.config.logging_config import configure_logging
    from app.config.settings import get_settings
    from app.main import health_check

    settings = get_settings()
    configure_logging(log_level=settings.log_level, log_format=settings.log_format)

    health = health_check()

    if args.json:
        print(json.dumps(asdict(health), indent=2))
    else:
        print(f"\n{'='*54}")
        print(f"  Status          : {health.status.upper()}")
        print(f"  App             : {health.app_name} v{health.app_version}")
        print(f"  Environment     : {health.app_env}")
        print(f"  Trading Mode    : {health.trading_mode}")
        live_status = "⚠️  ENABLED" if health.live_trading_enabled else "✅ DISABLED"
        print(f"  Live Trading    : {live_status}")
        print(f"  Python          : {health.python_version}")
        print(f"  Timestamp       : {health.timestamp}")
        print(f"{'='*54}")
        for check, result in health.checks.items():
            icon = "✅" if result == "ok" else "⚠️ "
            print(f"  {icon} {check:<20} {result}")
        print(f"{'='*54}\n")

    sys.exit(0 if health.status == "ok" else 1)


if __name__ == "__main__":
    main()
