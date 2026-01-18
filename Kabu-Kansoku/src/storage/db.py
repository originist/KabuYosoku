"""SQLite storage for Kabu‑Kansoku.

This module defines a simple database wrapper around SQLite. It
initializes the necessary tables and provides functions to insert
daily results and events. For more complex use cases you may wish to
use a higher‑level ORM such as SQLAlchemy, but SQLite's builtin
support is sufficient here.
"""

from __future__ import annotations

import sqlite3
import datetime
from typing import Iterable

from core.models import DayResult, Event


class Database:
    def __init__(self, path: str = "kabu.db") -> None:
        self.conn = sqlite3.connect(path)
        # store timestamps as ISO strings
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._init_tables()

    def _init_tables(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_results (
                date TEXT NOT NULL,
                code TEXT NOT NULL,
                base_price REAL,
                limit_up REAL,
                limit_down REAL,
                high REAL,
                low REAL,
                close REAL,
                hit_up INTEGER,
                hit_down INTEGER,
                close_up INTEGER,
                close_down INTEGER,
                PRIMARY KEY (date, code)
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                ts TEXT NOT NULL,
                code TEXT NOT NULL,
                price REAL,
                event_type TEXT
            );
            """
        )
        self.conn.commit()

    def save_daily(self, result: DayResult) -> None:
        """Insert or replace a daily result."""
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT OR REPLACE INTO daily_results (
                date, code, base_price, limit_up, limit_down, high, low, close,
                hit_up, hit_down, close_up, close_down
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                result.date.isoformat(),
                result.code,
                result.base_price,
                result.limit_up,
                result.limit_down,
                result.high,
                result.low,
                result.close,
                int(result.hit_up),
                int(result.hit_down),
                int(result.close_up),
                int(result.close_down),
            ),
        )
        self.conn.commit()

    def save_events(self, events: Iterable[Event]) -> None:
        """Bulk insert events."""
        cur = self.conn.cursor()
        cur.executemany(
            """
            INSERT INTO events (ts, code, price, event_type)
            VALUES (?, ?, ?, ?);
            """,
            [
                (e.ts.isoformat(), e.code, e.price, e.event_type)
                for e in events
            ],
        )
        self.conn.commit()

    def fetch_daily_results(self, limit: int = 100) -> Iterable[DayResult]:
        """Yield the most recent daily results, ordered by date descending."""
        cur = self.conn.cursor()
        for row in cur.execute(
            """
            SELECT date, code, base_price, limit_up, limit_down, high, low, close,
                   hit_up, hit_down, close_up, close_down
            FROM daily_results
            ORDER BY date DESC
            LIMIT ?;
            """,
            (limit,),
        ):
            yield DayResult(
                code=row[1],
                date=datetime.date.fromisoformat(row[0]),
                base_price=row[2],
                limit_up=row[3],
                limit_down=row[4],
                high=row[5],
                low=row[6],
                close=row[7],
                hit_up=bool(row[8]),
                hit_down=bool(row[9]),
                close_up=bool(row[10]),
                close_down=bool(row[11]),
            )