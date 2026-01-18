"""Utility functions for calculating daily price limits.

The Tokyo Stock Exchange defines daily price limits (値幅制限) based on
the previous day's closing price or a specified base price. This
module provides a helper to calculate the upper and lower limit
prices from the base price. The table included here is simplified
and should be updated if the official rules change.

References:
  - https://www.jpx.co.jp/english/equities/products/tp/index.html
"""

from __future__ import annotations

from typing import Tuple


# Simplified limit table: (threshold, limit)
# Rows are interpreted as: if base_price <= threshold, then the limit value is limit.
# Values are in JPY. This table should be updated according to official JPX rules.
_LIMIT_TABLE = [
    (100, 30),
    (200, 50),
    (500, 80),
    (1000, 100),
    (1500, 200),
    (2000, 300),
    (5000, 400),
    (10000, 600),
    (20000, 1000),
    (30000, 2000),
    (50000, 3000),
    (100000, 4000),
    (200000, 6000),
    (500000, 10000),
    (1_000_000, 15000),
    (float("inf"), 20000),  # default for prices above 1M
]


def calculate_limits(base_price: float) -> Tuple[float, float]:
    """Compute the daily upper and lower price limits given a base price.

    :param base_price: The base price (previous close or specified base).
    :return: (limit_up, limit_down)
    """
    limit_value = None
    for threshold, limit in _LIMIT_TABLE:
        if base_price <= threshold:
            limit_value = limit
            break
    if limit_value is None:
        limit_value = _LIMIT_TABLE[-1][1]
    limit_up = base_price + limit_value
    limit_down = max(0.0, base_price - limit_value)
    return limit_up, limit_down