"""Data models used by the application.

The dataclasses defined here represent the results of daily trading and
other domain objects. They can be extended as needed.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class DayResult:
    code: str
    date: datetime.date
    base_price: float
    limit_up: float
    limit_down: float
    high: float
    low: float
    close: float
    hit_up: bool
    hit_down: bool
    close_up: bool
    close_down: bool


@dataclass
class Event:
    ts: datetime.datetime
    code: str
    price: float
    event_type: str  # e.g. "hit_up", "hit_down"