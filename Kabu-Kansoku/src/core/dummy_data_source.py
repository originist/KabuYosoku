"""Dummy data source for Kabu‑Kansoku.

This class generates synthetic quotes using a simple random walk. It is
useful for development and testing when access to a real API is not
available. Prices are stored per code in an internal dictionary and
updated on each call.
"""

from __future__ import annotations

import random
import datetime
from typing import Optional, Dict

from .data_source_base import DataSource


class DummyDataSource(DataSource):
    """Generate synthetic quote data for testing the UI and logic."""

    def __init__(self) -> None:
        # Store current synthetic price per code
        self.prices: Dict[str, float] = {}

    def login(self) -> bool:
        # Nothing to do for dummy
        return True

    def get_quote(self, code: str) -> Optional[Dict[str, object]]:
        # Initialize a random base price if not present
        base_price = self.prices.get(code)
        if base_price is None:
            base_price = random.uniform(500.0, 2000.0)
        # Random walk step
        delta = random.uniform(-10.0, 10.0)
        price = max(10.0, base_price + delta)
        self.prices[code] = price
        return {
            "code": code,
            "current_price": price,
            "high": price,
            "low": price,
            "volume": random.randint(1000, 100000),
            "timestamp": datetime.datetime.now(),
        }

    def get_base_price(self, code: str) -> Optional[float]:
        # Use the initial synthetic price as the base price
        return self.prices.get(code)