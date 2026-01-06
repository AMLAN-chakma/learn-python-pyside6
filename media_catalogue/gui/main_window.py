"""
Stubbed PySide6 GUI for Media Catalogue.
This is a thin wrapper over the MediaCatalogue business logic.
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QLabel,
    QSpinBox,
    QMessageBox,
    QTabWidget,
    QFormLayout,
    QHeaderView,
    QComboBox,
)
from PySide6.QtCore import QUrl

# CRITICAL: QWebEngineView import is deferred - must happen AFTER QApplication exists
# Do NOT import at module level or you WILL get segfaults

import sys
from pathlib import Path

# Add project root to path so imports work from anywhere
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from media_catalogue import MediaCatalogue, Movie, TVSeries, MediaError


class MainWindow(QMainWindow):
    """Main window for the Media Catalogue application."""

    def __init__(self):
        super().__init__()
        self.catalogue = MediaCatalogue()
        self._setup_ui()

    def _setup_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Media Catalogue")
        self.setMinimumSize(800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Tab widget for Movie and TV Series forms
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Add Movie tab
        movie_tab = self._create_movie_tab()
        self.tab_widget.addTab(movie_tab, "Add Movie")

        # Add TV Series tab
        series_tab = self._create_series_tab()
        self.tab_widget.addTab(series_tab, "Add TV Series")

        # Toolbar with filter and delete
        toolbar = QHBoxLayout()

        # Filter dropdown
        toolbar.addWidget(QLabel("Filter:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Movies Only", "TV Series Only"])
        self.filter_combo.currentTextChanged.connect(self._on_filter_changed)
        toolbar.addWidget(self.filter_combo)

        toolbar.addStretch()  # Push delete button to the right

        # Delete button
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self._on_delete)
        toolbar.addWidget(self.delete_btn)

        main_layout.addLayout(toolbar)

        # Catalogue table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Type", "Title", "Year", "Director", "Duration", "Details"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        main_layout.addWidget(self.table)

        # Track which items are currently displayed (for filtering)
        self._displayed_items = []

        # Status bar
        self.statusBar().showMessage("Ready")

    def _create_movie_tab(self) -> QWidget:
        """Create the Add Movie form tab."""
        tab = QWidget()
        layout = QFormLayout(tab)

        self.movie_title = QLineEdit()
        self.movie_year = QSpinBox()
        self.movie_year.setRange(1895, 2100)
        self.movie_year.setValue(2024)
        self.movie_director = QLineEdit()
        self.movie_duration = QSpinBox()
        self.movie_duration.setRange(1, 1000)
        self.movie_duration.setValue(90)

        layout.addRow("Title:", self.movie_title)
        layout.addRow("Year:", self.movie_year)
        layout.addRow("Director:", self.movie_director)
        layout.addRow("Duration (min):", self.movie_duration)

        add_btn = QPushButton("Add Movie")
        add_btn.clicked.connect(self._on_add_movie)
        layout.addRow(add_btn)

        return tab

    def _create_series_tab(self) -> QWidget:
        """Create the Add TV Series form tab."""
        tab = QWidget()
        layout = QFormLayout(tab)


        self.series_title = QLineEdit()
        self.series_year = QSpinBox()
        self.series_year.setRange(1895, 2100)
        self.series_year.setValue(2024)
        self.series_director = QLineEdit()
        self.series_duration = QSpinBox()
        self.series_duration.setRange(1, 1000)
        self.series_duration.setValue(45)
        self.series_seasons = QSpinBox()
        self.series_seasons.setRange(1, 100)
        self.series_seasons.setValue(1)
        self.series_episodes = QSpinBox()
        self.series_episodes.setRange(1, 1000)
        self.series_episodes.setValue(10)

        layout.addRow("Title:", self.series_title)
        layout.addRow("Year:", self.series_year)
        layout.addRow("Director:", self.series_director)
        layout.addRow("Avg Duration (min):", self.series_duration)
        layout.addRow("Seasons:", self.series_seasons)
        layout.addRow("Total Episodes:", self.series_episodes)

        add_btn = QPushButton("Add TV Series")
        add_btn.clicked.connect(self._on_add_series)
        layout.addRow(add_btn)

        return tab

    def _on_add_movie(self):
        """Handle Add Movie button click."""
        try:
            # Get values from UI widgets
            title = self.movie_title.text()
            year = self.movie_year.value()
            director = self.movie_director.text()
            duration = self.movie_duration.value()

            # Call movie class all validation happens here
            movie = Movie(title, year, director, duration)

            # Add to MediaCatalogue
            self.catalogue.add(movie)

            # Update display
            self._refresh_table()
            self._clear_movie_form()
            self._show_success(f"Added: {movie.title}")

        except ValueError as e:
            # validation raised this error
            self._show_error(str(e))

    def _on_add_series(self):
        """Handle Add TV Series button click."""
        try:
            # Get values from UI widgets
            title = self.series_title.text()
            year = self.series_year.value()
            director = self.series_director.text()
            duration = self.series_duration.value()
            seasons = self.series_seasons.value()
            episodes = self.series_episodes.value()

            # CallTVSeries class all validation happens there
            series = TVSeries(title, year, director, duration, seasons, episodes)

            # Add to MediaCatalogue
            self.catalogue.add(series)

            # Update display
            self._refresh_table()
            self._clear_series_form()
            self._show_success(f"Added: {series.title}")

        except ValueError as e:
            # validation raised this error
            self._show_error(str(e))

    def _refresh_table(self):
        """Refresh the catalogue table display based on current filter."""
        # Determine which items to display based on filter
        filter_text = self.filter_combo.currentText()
        if filter_text == "Movies Only":
            self._displayed_items = self.catalogue.get_movies()
        elif filter_text == "TV Series Only":
            self._displayed_items = self.catalogue.get_tv_series()
        else:
            self._displayed_items = self.catalogue.items.copy()

        self.table.setRowCount(len(self._displayed_items))

        for row, item in enumerate(self._displayed_items):
            # Determine type
            item_type = "TV Series" if isinstance(item, TVSeries) else "Movie"
            self.table.setItem(row, 0, QTableWidgetItem(item_type))
            self.table.setItem(row, 1, QTableWidgetItem(item.title))
            self.table.setItem(row, 2, QTableWidgetItem(str(item.year)))
            self.table.setItem(row, 3, QTableWidgetItem(item.director))
            self.table.setItem(row, 4, QTableWidgetItem(f"{item.duration} min"))

            # Details column
            if isinstance(item, TVSeries):
                details = f"{item.seasons} seasons, {item.total_episodes} episodes"
            else:
                details = "-"
            self.table.setItem(row, 5, QTableWidgetItem(details))

    def _clear_movie_form(self):
        """Clear the movie form fields."""
        self.movie_title.clear()
        self.movie_director.clear()
        self.movie_year.setValue(2024)
        self.movie_duration.setValue(90)

    def _clear_series_form(self):
        """Clear the series form fields."""
        self.series_title.clear()
        self.series_director.clear()
        self.series_year.setValue(2024)
        self.series_duration.setValue(45)
        self.series_seasons.setValue(1)
        self.series_episodes.setValue(10)

    def _show_error(self, message: str):
        """Display an error message dialog."""
        QMessageBox.critical(self, "Error", message)

    def _show_success(self, message: str):
        """Display a success message in the status bar."""
        self.statusBar().showMessage(message, 3000)

    def _on_filter_changed(self):
        """Handle filter dropdown change."""
        self._refresh_table()

    def _on_delete(self):
        """Handle Delete Selected button click."""
        try:
            row = self.table.currentRow()
            if row < 0:
                raise ValueError("No item selected")

            # Map row index to actual data object
            item = self._displayed_items[row]

            deleted = self.catalogue.delete(item)
            self._refresh_table()
            self._show_success(f"Deleted: {deleted.title}")

        except ValueError as e:
            self._show_error(str(e))
        except MediaError as e:
            self._show_error(f"Error deleting item: {e}")


def run_app():
    """Entry point to run the GUI application."""
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
