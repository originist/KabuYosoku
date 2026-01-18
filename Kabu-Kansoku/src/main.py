"""Entry point for the Kabu‑Kansoku application.

This module sets up the Qt application, constructs the main window and
integrates the chosen data source. It intentionally avoids any API
credentials or sensitive information. To use the real Tachibana API,
configure environment variables or OS keyring as described in the README.
"""

import sys
import datetime
from typing import List, Optional

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTabWidget,
    QTextEdit,
    QMessageBox,
)

from core.data_source_base import DataSource
from core.dummy_data_source import DummyDataSource
from core.limit_rules import calculate_limits


class MainWindow(QMainWindow):
    """Main window containing dashboard, history and settings tabs."""

    def __init__(self, data_source: DataSource, update_interval: int = 30) -> None:
        super().__init__()
        self.data_source = data_source
        self.update_interval = update_interval  # seconds
        self.watchlist: List[str] = []
        self.init_ui()
        # Timer for periodic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_quotes)
        self.timer.start(self.update_interval * 1000)

    def init_ui(self) -> None:
        self.setWindowTitle("Kabu‑Kansoku")
        tabs = QTabWidget(self)

        # Dashboard tab
        dashboard = QWidget()
        dashboard_layout = QVBoxLayout(dashboard)
        splitter = QSplitter(Qt.Horizontal)
        # Table: code, price, limit up, limit down, distance, hit, updated
        self.table = QTableWidget(0, 7, splitter)
        self.table.setHorizontalHeaderLabels([
            "Code",
            "Price",
            "Limit Up",
            "Limit Down",
            "Distance",
            "Hit",
            "Updated",
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.cellClicked.connect(self.on_table_select)
        splitter.addWidget(self.table)

        # Detail panel
        self.detail = QTextEdit(splitter)
        self.detail.setReadOnly(True)
        splitter.addWidget(self.detail)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        dashboard_layout.addWidget(splitter)
        tabs.addTab(dashboard, "Dashboard")

        # History tab (placeholder)
        history = QWidget()
        history_layout = QVBoxLayout(history)
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Date",
            "Code",
            "High",
            "Low",
            "Close",
            "Result",
        ])
        history_layout.addWidget(self.history_table)
        tabs.addTab(history, "History")

        # Settings tab (placeholder)
        settings = QWidget()
        settings_layout = QVBoxLayout(settings)
        settings_layout.addWidget(QLabel("Settings (coming soon)"))
        tabs.addTab(settings, "Settings")

        self.setCentralWidget(tabs)

    def add_code(self, code: str) -> None:
        """Add a stock code to the watchlist and table."""
        if code in self.watchlist:
            return
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col in range(self.table.columnCount()):
            self.table.setItem(row, col, QTableWidgetItem(""))
        self.table.item(row, 0).setText(code)
        self.watchlist.append(code)

    def update_quotes(self) -> None:
        """Fetch and update quote information for all watched codes."""
        for row, code in enumerate(self.watchlist):
            try:
                quote = self.data_source.get_quote(code)
            except Exception as ex:
                QMessageBox.warning(self, "Data error", f"Failed to fetch data for {code}: {ex}")
                continue
            if not quote:
                continue
            price = quote.get("current_price")
            base = self.data_source.get_base_price(code) or price
            limit_up, limit_down = calculate_limits(base)
            # Distance to nearest limit
            dist = min(limit_up - price, price - limit_down)
            hit = "Yes" if (price >= limit_up or price <= limit_down) else ""  # simple flag
            # Update table cells
            self.table.item(row, 1).setText(f"{price:.2f}")
            self.table.item(row, 2).setText(f"{limit_up:.2f}")
            self.table.item(row, 3).setText(f"{limit_down:.2f}")
            self.table.item(row, 4).setText(f"{dist:.2f}")
            self.table.item(row, 5).setText(hit)
            self.table.item(row, 6).setText(datetime.datetime.now().strftime("%H:%M:%S"))

    def on_table_select(self, row: int, column: int) -> None:
        """Display details for the selected code."""
        code = self.table.item(row, 0).text()
        self.detail.setPlainText(f"Details for {code}\n\n(Detail view not yet implemented)")


def main() -> int:
    # Choose data source. In the future this could be set via CLI or config.
    data_source: DataSource = DummyDataSource()
    data_source.login()
    app = QApplication(sys.argv)
    window = MainWindow(data_source)
    # Example: prepopulate with a few codes
    window.add_code("7203")  # Toyota Motor
    window.add_code("6758")  # Sony Group
    window.add_code("9984")  # SoftBank Group
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())