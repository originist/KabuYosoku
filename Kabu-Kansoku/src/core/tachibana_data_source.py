"""Skeleton implementation of the Tachibana Securities e‑branch API data source.

This class demonstrates the structure of a data source that authenticates
against the Tachibana API, retrieves a virtual endpoint (仮想URL), and
uses it to fetch quotes. The exact request and response formats should
follow the official API specification. At the moment, methods contain
TODO markers where integration details need to be filled in.

Usage of this data source requires the user to set environment variables
or OS keyring entries as described in the README. Sensitive credentials
should never be stored in code or committed to version control.
"""

from __future__ import annotations

import os
import datetime
from typing import Optional, Dict
import httpx
import keyring

from .data_source_base import DataSource


class TachibanaDataSource(DataSource):
    """Fetch quotes via the Tachibana Securities e‑branch API (仮想URL方式)。"""

    def __init__(self) -> None:
        self.session: Optional[httpx.Client] = None
        self.virtual_url: Optional[str] = None
        # Cache credentials from environment or keyring
        self.user_id: Optional[str] = os.getenv("TACHIBANA_USER_ID")
        self.password: Optional[str] = os.getenv("TACHIBANA_PASSWORD")
        self.second_password: Optional[str] = os.getenv("TACHIBANA_SECOND_PASSWORD")
        self.tel_pass: Optional[str] = os.getenv("TACHIBANA_TEL_PASS")
        self.account_code: Optional[str] = os.getenv("TACHIBANA_ACCOUNT_CODE")
        # If not in environment, try keyring (service names are arbitrary examples)
        if not self.user_id:
            self.user_id = keyring.get_password("tachibana", "user_id")
        if not self.password:
            self.password = keyring.get_password("tachibana", "password")
        if not self.second_password:
            self.second_password = keyring.get_password("tachibana", "second_password")
        if not self.tel_pass:
            self.tel_pass = keyring.get_password("tachibana", "tel_pass")
        if not self.account_code:
            self.account_code = keyring.get_password("tachibana", "account_code")

    def login(self) -> bool:
        """Authenticate and obtain the virtual URL for subsequent requests.

        The Tachibana API requires a login step which yields a time-limited
        virtual URL (仮想URL). The login flow may involve multi‑factor
        authentication via phone. After successful login, this method
        should store the virtual URL and initialize an HTTP client session.

        TODO: implement login according to the official API specification.
        """
        # Example stub: open a session and set a placeholder URL
        self.session = httpx.Client()
        # Here you would send a login request to the API using self.user_id etc.
        # For example:
        # response = self.session.post("https://example.com/login", data={...})
        # response.raise_for_status()
        # self.virtual_url = response.json().get("virtual_url")
        # For now we assign a dummy URL. Replace this with real login logic.
        self.virtual_url = "https://example.com/virtual"
        return True

    def get_quote(self, code: str) -> Optional[Dict[str, object]]:
        """Return the latest quote for the given code using the virtual URL.

        TODO: send a request to the Tachibana API to retrieve quote data.
        The actual path and parameters depend on the API definition. Make
        sure to handle network errors and authentication expiration.
        """
        if not self.session or not self.virtual_url:
            raise RuntimeError("Not logged in")
        # Example request (needs to be replaced with API-specific logic)
        try:
            # resp = self.session.get(f"{self.virtual_url}/price", params={"code": code})
            # resp.raise_for_status()
            # result = resp.json()
            # Parse result into dict with current_price etc.
            # Placeholder data until implemented
            now = datetime.datetime.now()
            return {
                "code": code,
                "current_price": 0.0,
                "high": 0.0,
                "low": 0.0,
                "volume": 0,
                "timestamp": now,
            }
        except Exception as ex:
            print(f"Error fetching quote for {code}: {ex}")
            return None

    def get_base_price(self, code: str) -> Optional[float]:
        """Return the base price for limit calculation.

        TODO: query the API for the previous day's close or base price.
        The Tachibana API may provide a separate endpoint or field for
        this value. Until implemented, return None so that the caller
        falls back to using the current price.
        """
        return None

    def get_daily_summary(self, code: str, date: datetime.date) -> Optional[Dict[str, object]]:
        """Return day summary (high, low, close) for the given date.

        TODO: implement this using the API's daily summary endpoint if
        available. If not implemented, return None.
        """
        return None