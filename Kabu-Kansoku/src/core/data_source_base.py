"""Abstract base class for quote data sources.

To support multiple data sources (dummy, Tachibana API, etc.) the
application defines a common interface. Each data source must
implement the methods defined here.
"""

from __future__ import annotations

import datetime
from abc import ABC, abstractmethod
from typing import Optional, Dict


class DataSource(ABC):
    """Interface for quote providers used by the application."""

    @abstractmethod
    def login(self) -> bool:
        """Perform login or other setup. Return True if successful."""
        raise NotImplementedError

    @abstractmethod
    def get_quote(self, code: str) -> Optional[Dict[str, object]]:
        """Return the latest quote information for a stock code.

        A quote dict should contain at least:

        - 'code': str
        - 'current_price': float
        - 'high': float (optional)
        - 'low': float (optional)
        - 'volume': int (optional)
        - 'timestamp': datetime.datetime
        """
        raise NotImplementedError

    @abstractmethod
    def get_base_price(self, code: str) -> Optional[float]:
        """Return the base price used to compute limit up/down (usually the previous close)."""
        raise NotImplementedError

    def get_daily_summary(
        self, code: str, date: datetime.date
    ) -> Optional[Dict[str, object]]:
        """Return a summary of the day's trading for the given code and date.

        This method is optional and may not be implemented for all data sources.
        It should return a dict with 'high', 'low' and 'close' keys if available.
        """
        return None