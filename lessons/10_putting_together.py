"""
================================================================================
LESSON 10: PUTTING IT ALL TOGETHER
================================================================================

In this final lesson, you'll see how YOUR entire application connects - from
clicking a button to seeing data in the table.

Run this file:
    python lessons/10_putting_together.py

================================================================================
THE COMPLETE FLOW
================================================================================

When a user adds a movie, here's what happens:

    1. User clicks "Add Movie" button
              |
              v
    2. Signal fires -> _on_add_movie() runs
              |
              v
    3. Get values from form widgets
              |
              v
    4. Create Movie object (validation happens)
              |
              v
    5. Add to MediaCatalogue
              |
              v
    6. Refresh table display
              |
              v
    7. Clear form & show success

Let's trace through YOUR exact code!

================================================================================
STEP 1: THE BUTTON CLICK (SIGNAL)
================================================================================

Your code (line 120):
    add_btn.clicked.connect(self._on_add_movie)

What happens:
- User clicks button
- 'clicked' signal fires
- _on_add_movie method runs

================================================================================
STEP 2: GET VALUES FROM WIDGETS
================================================================================

Your code (lines 163-166):
    title = self.movie_title.text()       # QLineEdit -> string
    year = self.movie_year.value()        # QSpinBox -> integer
    director = self.movie_director.text() # QLineEdit -> string
    duration = self.movie_duration.value() # QSpinBox -> integer

REMEMBER:
- QLineEdit uses .text() -> returns string
- QSpinBox uses .value() -> returns integer

================================================================================
STEP 3: CREATE OBJECT & VALIDATE
================================================================================

Your code (line 169):
    movie = Movie(title, year, director, duration)

This calls your Movie class (media_catalogue.py lines 10-33):

    class Movie:
        def __init__(self, title, year, director, duration):
            # Type checks
            if not isinstance(title, str):
                raise ValueError("Title must be a string")

            # Value checks
            if not title.strip():
                raise ValueError("Title cannot be empty")
            if year < 1895:
                raise ValueError("Year must be 1895 or later")
            ...

If validation fails -> ValueError raised -> caught by except block

================================================================================
STEP 4: ADD TO CATALOGUE
================================================================================

Your code (line 172):
    self.catalogue.add(movie)

This calls MediaCatalogue.add() (media_catalogue.py lines 43-48):

    def add(self, media_item):
        if not isinstance(media_item, Movie):
            raise MediaError('Only Movie or TVSeries instances can be added', media_item)
        self.items.append(media_item)
        return media_item

================================================================================
STEP 5: REFRESH THE TABLE
================================================================================

Your code (line 175):
    self._refresh_table()

_refresh_table() (lines 209-236) does:
1. Checks current filter (All/Movies/Series)
2. Gets items from catalogue
3. Sets row count
4. Fills each cell with QTableWidgetItem

================================================================================
STEP 6: ERROR HANDLING
================================================================================

Your code (lines 179-181):
    except ValueError as e:
        self._show_error(str(e))

If anything goes wrong, the user sees a dialog - not a crash!
"""

import sys
from pathlib import Path

# Add project root to path so imports work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "media_catalogue" / "src"))

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QSpinBox,
    QFormLayout,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

# Import your actual classes!
try:
    from media_catalogue import Movie, TVSeries, MediaCatalogue, MediaError
    IMPORTS_AVAILABLE = True
except ImportError:
    IMPORTS_AVAILABLE = False
    print("Note: Could not import media_catalogue. Using simplified classes.")


# Simplified classes if imports fail
if not IMPORTS_AVAILABLE:
    class Movie:
        def __init__(self, title, year, director, duration):
            if not title.strip():
                raise ValueError("Title cannot be empty")
            if year < 1895:
                raise ValueError("Year must be 1895 or later")
            if duration <= 0:
                raise ValueError("Duration must be positive")
            self.title = title
            self.year = year
            self.director = director
            self.duration = duration

    class MediaCatalogue:
        def __init__(self):
            self.items = []

        def add(self, item):
            self.items.append(item)
            return item

        def delete(self, item):
            self.items.remove(item)
            return item


"""
================================================================================
YOUR COMPLETE _on_add_movie METHOD
================================================================================

Here's the full method from your main_window.py (lines 159-181):

    def _on_add_movie(self):
        '''Handle Add Movie button click.'''
        try:
            # Get values from UI widgets
            title = self.movie_title.text()
            year = self.movie_year.value()
            director = self.movie_director.text()
            duration = self.movie_duration.value()

            # Call movie class - all validation happens here
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
"""


# EXAMPLE 1: Mini Media Catalogue (simplified version of your app)
class MiniMediaCatalogue(QMainWindow):
    """A simplified version of your Media Catalogue app."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Media Catalogue")
        self.setMinimumSize(600, 400)

        # Your business logic - separate from GUI!
        self.catalogue = MediaCatalogue()

        self._setup_ui()

    def _setup_ui(self):
        """Initialize the user interface."""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Form section
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)

        self.movie_title = QLineEdit()
        self.movie_year = QSpinBox()
        self.movie_year.setRange(1895, 2100)
        self.movie_year.setValue(2024)
        self.movie_director = QLineEdit()
        self.movie_duration = QSpinBox()
        self.movie_duration.setRange(1, 1000)
        self.movie_duration.setValue(90)

        form_layout.addRow("Title:", self.movie_title)
        form_layout.addRow("Year:", self.movie_year)
        form_layout.addRow("Director:", self.movie_director)
        form_layout.addRow("Duration (min):", self.movie_duration)

        # Add button - connects signal to slot
        add_btn = QPushButton("Add Movie")
        add_btn.clicked.connect(self._on_add_movie)
        form_layout.addRow(add_btn)

        main_layout.addWidget(form_widget)

        # Toolbar with delete button
        toolbar = QHBoxLayout()
        toolbar.addStretch()

        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self._on_delete)
        toolbar.addWidget(delete_btn)

        main_layout.addLayout(toolbar)

        # Table to display movies
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Year", "Director", "Duration"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        main_layout.addWidget(self.table)

        # Status bar
        self.statusBar().showMessage("Ready")

    def _on_add_movie(self):
        """Handle Add Movie button click - YOUR EXACT PATTERN!"""
        try:
            # STEP 1: Get values from UI widgets
            title = self.movie_title.text()
            year = self.movie_year.value()
            director = self.movie_director.text()
            duration = self.movie_duration.value()

            # STEP 2: Create Movie - validation happens here!
            movie = Movie(title, year, director, duration)

            # STEP 3: Add to MediaCatalogue
            self.catalogue.add(movie)

            # STEP 4: Update display
            self._refresh_table()
            self._clear_form()
            self._show_success(f"Added: {movie.title}")

        except ValueError as e:
            # Validation raised this error
            self._show_error(str(e))

    def _on_delete(self):
        """Handle Delete Selected button click - YOUR EXACT PATTERN!"""
        try:
            row = self.table.currentRow()
            if row < 0:
                raise ValueError("No item selected")

            # Map row index to actual data object
            item = self.catalogue.items[row]

            deleted = self.catalogue.delete(item)
            self._refresh_table()
            self._show_success(f"Deleted: {deleted.title}")

        except ValueError as e:
            self._show_error(str(e))
        except Exception as e:
            self._show_error(f"Error: {e}")

    def _refresh_table(self):
        """Refresh the table display - YOUR EXACT PATTERN!"""
        items = self.catalogue.items

        # Set number of rows
        self.table.setRowCount(len(items))

        # Fill each row
        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(item.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(item.year)))  # str()!
            self.table.setItem(row, 2, QTableWidgetItem(item.director))
            self.table.setItem(row, 3, QTableWidgetItem(f"{item.duration} min"))

    def _clear_form(self):
        """Clear the form fields."""
        self.movie_title.clear()
        self.movie_director.clear()
        self.movie_year.setValue(2024)
        self.movie_duration.setValue(90)

    def _show_error(self, message: str):
        """Display an error message dialog."""
        QMessageBox.critical(self, "Error", message)

    def _show_success(self, message: str):
        """Display a success message in the status bar."""
        self.statusBar().showMessage(message, 3000)


"""
================================================================================
KEY ARCHITECTURE PATTERNS
================================================================================

Your application follows EXCELLENT design patterns:

1. SEPARATION OF CONCERNS
   ----------------------
   media_catalogue.py  ->  Business logic (Movie, TVSeries, validation)
   main_window.py      ->  GUI only (display, user interaction)

2. THIN WRAPPER PATTERN
   ---------------------
   - GUI doesn't do validation
   - GUI calls business logic classes
   - Business logic raises exceptions
   - GUI catches and displays errors

3. SIGNAL/SLOT PATTERN
   --------------------
   - Buttons emit signals
   - Methods (slots) handle them
   - Loose coupling between components

================================================================================
SUMMARY - WHAT YOU LEARNED
================================================================================

PYTHON OOP (Lessons 1-4):
- Classes with __init__ and self
- Inheritance with super().__init__()
- Validation with isinstance() and ValueError
- Collections with list methods

TESTING (Lessons 5-7):
- Debug with print statements
- Test with pytest and assert
- Parameterize tests for efficiency

PYSIDE6 GUI (Lessons 8-10):
- QMainWindow for the window
- Layouts: QVBoxLayout, QHBoxLayout, QFormLayout
- Widgets: QLineEdit, QSpinBox, QTableWidget
- Signals: button.clicked.connect(method)
- Values: .text() for strings, .value() for numbers

================================================================================
WHAT'S NEXT?
================================================================================

Run your full app:
    python media_catalogue/run_gui.py

Run the tests:
    cd media_catalogue
    pytest -v

Explore further:
- Add new features to the app
- Write more tests
- Check out PySide6 Docs: https://doc.qt.io/qtforpython-6/

CONGRATULATIONS! You've completed the PySide6 Tutorial!
"""


def run_example(window_class):
    """Helper function to run any example window."""
    app = QApplication(sys.argv)
    window = window_class()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    print("=" * 60)
    print("LESSON 10: PUTTING IT ALL TOGETHER")
    print("=" * 60)
    print("\nThis lesson demonstrates the complete flow of your app.")
    print("Running: Mini Media Catalogue")
    print()
    print("Try these actions:")
    print("1. Add a movie (fill in all fields)")
    print("2. Try adding with empty title (see error dialog)")
    print("3. Select a row and delete it")
    print()

    run_example(MiniMediaCatalogue)