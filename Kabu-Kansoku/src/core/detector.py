"""Functions for determining limit hit and close conditions."""

from __future__ import annotations

from typing import Optional


def is_hit(price: Optional[float], limit_up: float, limit_down: float) -> bool:
    """Return True if the current price has reached or exceeded the limit.

    :param price: Current price (may be None)
    :param limit_up: Upper limit price
    :param limit_down: Lower limit price
    """
    if price is None:
        return False
    return price >= limit_up or price <= limit_down


def is_close(close_price: Optional[float], limit_up: float, limit_down: float) -> bool:
    """Return True if the closing price is exactly at the limit.

    :param close_price: Closing price (may be None)
    :param limit_up: Upper limit price
    :param limit_down: Lower limit price
    """
    if close_price is None:
        return False
    return close_price == limit_up or close_price == limit_down