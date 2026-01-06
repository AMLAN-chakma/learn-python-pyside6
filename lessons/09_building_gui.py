"""
================================================================================
LESSON 9: BUILDING FORMS AND TABLES
================================================================================

Build the actual forms and tables from YOUR main_window.py - with exercises!

Run this file:
    python lessons/09_building_gui.py

================================================================================
STEP 1: QFORMLAYOUT
================================================================================

Your code (lines 100-103):
    tab = QWidget()           # Container
    layout = QFormLayout(tab) # Two-column form layout

QFormLayout creates two columns: Labels left, inputs right.
Use addRow("Label:", widget) to add rows.

YOUR CODE - FORM FIELDS (lines 105-117):

    self.movie_title = QLineEdit()         # Text input
    self.movie_year = QSpinBox()           # Number input
    self.movie_year.setRange(1895, 2100)   # Min/max
    self.movie_year.setValue(2024)         # Default

    layout.addRow("Title:", self.movie_title)  # "Title:" | [input]
    layout.addRow("Year:", self.movie_year)    # "Year:"  | [spinner]

Why self.? So _on_add_movie() can access these later!
"""

import sys
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
    QComboBox,
    QHeaderView,
    QTabWidget,
)


# EXAMPLE 1: Building a Form with QFormLayout
class SimpleForm(QMainWindow):
    """A simple form using QFormLayout."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Form")
        self.setMinimumSize(300, 200)

        tab = QWidget()
        self.setCentralWidget(tab)
        layout = QFormLayout(tab)

        # Create input widgets
        self.name_input = QLineEdit()
        self.age_input = QSpinBox()
        self.age_input.setRange(0, 150)

        # addRow creates: "Label:" | [widget]
        layout.addRow("Name:", self.name_input)
        layout.addRow("Age:", self.age_input)

        btn = QPushButton("Submit")
        btn.clicked.connect(self.on_submit)
        layout.addRow(btn)

        self.result = QLabel("")
        layout.addRow(self.result)

    def on_submit(self):
        # .text() for QLineEdit, .value() for QSpinBox
        name = self.name_input.text()
        age = self.age_input.value()
        self.result.setText(f"{name} is {age} years old")


"""
================================================================================
STEP 2: SIGNALS - BUTTON CLICKS
================================================================================

Your code (lines 119-120):
    add_btn = QPushButton("Add Movie")
    add_btn.clicked.connect(self._on_add_movie)

Breaking it down:
- add_btn.clicked = signal (fires when clicked)
- .connect(func) = run this function when signal fires
"""


# EXAMPLE 2: Counter with Signal Connection
class Counter(QMainWindow):
    """A counter demonstrating signal/slot connection."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Counter")
        self.setMinimumSize(200, 150)

        c = QWidget()
        self.setCentralWidget(c)
        layout = QVBoxLayout(c)

        self.count = 0
        self.label = QLabel("0")
        layout.addWidget(self.label)

        btn = QPushButton("+1")
        # .connect() links the signal to a function
        btn.clicked.connect(self.add)
        layout.addWidget(btn)

    def add(self):
        self.count += 1
        self.label.setText(str(self.count))


"""
================================================================================
STEP 3: GETTING WIDGET VALUES
================================================================================

Your code (lines 163-166):
    title = self.movie_title.text()      # QLineEdit -> .text()
    year = self.movie_year.value()       # QSpinBox -> .value()

REMEMBER:
- QLineEdit.text() -> string
- QSpinBox.value() -> integer
"""


# EXAMPLE 3: The Movie Form (exactly like your code!)
class MovieForm(QMainWindow):
    """The movie form from your main_window.py."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Movie")
        self.setMinimumSize(400, 300)

        tab = QWidget()
        self.setCentralWidget(tab)
        layout = QFormLayout(tab)

        # YOUR EXACT CODE from main_window.py lines 109-116!
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

        self.result = QLabel("")
        layout.addRow(self.result)

    def _on_add_movie(self):
        # Get values - this is exactly your code pattern!
        title = self.movie_title.text()       # QLineEdit uses .text()
        year = self.movie_year.value()        # QSpinBox uses .value()
        director = self.movie_director.text()  # QLineEdit uses .text()
        duration = self.movie_duration.value()  # QSpinBox uses .value()

        self.result.setText(f"{title} ({year}) - {duration}min, {director}")


"""
================================================================================
STEP 4: TABLES (QTABLEWIDGET)
================================================================================

Your code (lines 84-88):
    self.table = QTableWidget()
    self.table.setColumnCount(6)
    self.table.setHorizontalHeaderLabels([
        "Type", "Title", "Year", "Director", "Duration", "Details"
    ])
"""


# EXAMPLE 4: Creating a Table
class TableDemo(QMainWindow):
    """A simple table demonstration."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Demo")
        self.setMinimumSize(400, 200)

        c = QWidget()
        self.setCentralWidget(c)
        layout = QVBoxLayout(c)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        # setHorizontalHeaderLabels sets the column headers
        self.table.setHorizontalHeaderLabels(["Title", "Year", "Director"])
        layout.addWidget(self.table)


"""
================================================================================
STEP 5: ADDING DATA TO TABLE
================================================================================

Your code (lines 220-227):
    self.table.setRowCount(len(items))
    for row, item in enumerate(items):
        self.table.setItem(row, 0, QTableWidgetItem(item.title))
        self.table.setItem(row, 1, QTableWidgetItem(str(item.year)))

NOTE: QTableWidgetItem needs STRING - use str(year)!
"""


# EXAMPLE 5: Table with Data
class FilledTable(QMainWindow):
    """A table filled with movie data."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movies Table")
        self.setMinimumSize(500, 300)

        c = QWidget()
        self.setCentralWidget(c)
        layout = QVBoxLayout(c)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Title", "Year", "Director"])
        # Make columns stretch to fill width
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Sample movie data
        movies = [
            ("The Matrix", 1999, "Wachowskis"),
            ("Inception", 2010, "Christopher Nolan"),
            ("Interstellar", 2014, "Christopher Nolan"),
        ]

        # Set number of rows
        self.table.setRowCount(len(movies))

        # Fill the table
        for row, (title, year, director) in enumerate(movies):
            # setItem(row, column, QTableWidgetItem)
            self.table.setItem(row, 0, QTableWidgetItem(title))
            self.table.setItem(row, 1, QTableWidgetItem(str(year)))  # str() needed!
            self.table.setItem(row, 2, QTableWidgetItem(director))


"""
================================================================================
STEP 6: ERROR DIALOGS
================================================================================

Your code (lines 254-256):
    def _show_error(self, message: str):
        QMessageBox.critical(self, "Error", message)

QMessageBox types:
- QMessageBox.critical() - Error (red X icon)
- QMessageBox.warning() - Warning (yellow ! icon)
- QMessageBox.information() - Info (blue i icon)
"""


# EXAMPLE 6: Form with Validation and Error Dialog
class ValidatedForm(QMainWindow):
    """A form that shows an error if title is empty."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Validated Form")
        self.setMinimumSize(300, 150)

        c = QWidget()
        self.setCentralWidget(c)
        layout = QFormLayout(c)

        self.title_input = QLineEdit()
        layout.addRow("Title:", self.title_input)

        btn = QPushButton("Submit")
        btn.clicked.connect(self.submit)
        layout.addRow(btn)

        self.result = QLabel("")
        layout.addRow(self.result)

    def submit(self):
        title = self.title_input.text()
        if not title.strip():
            # Show error dialog - exactly like your _show_error method!
            QMessageBox.critical(self, "Error", "Title cannot be empty!")
            return
        self.result.setText(f"OK: {title}")


"""
================================================================================
STEP 7: DROPDOWN WITH QCOMBOBOX
================================================================================

Your code (lines 73-76):
    self.filter_combo = QComboBox()
    self.filter_combo.addItems(["All", "Movies Only", "TV Series Only"])
    self.filter_combo.currentTextChanged.connect(self._on_filter_changed)

To get the selected value:
    filter_text = self.filter_combo.currentText()
"""


# EXAMPLE 7: Dropdown Filter
class DropdownDemo(QMainWindow):
    """A dropdown that filters a label."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dropdown Demo")
        self.setMinimumSize(300, 150)

        c = QWidget()
        self.setCentralWidget(c)
        layout = QVBoxLayout(c)

        # Create dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Movies Only", "TV Series Only"])
        # currentTextChanged fires when selection changes
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        layout.addWidget(self.filter_combo)

        self.result = QLabel("Filter: All")
        layout.addWidget(self.result)

    def on_filter_changed(self):
        # .currentText() gets the selected option
        filter_text = self.filter_combo.currentText()
        self.result.setText(f"Filter: {filter_text}")


"""
================================================================================
STEP 8: TABS WITH QTABWIDGET
================================================================================

Your code (lines 57-66):
    self.tab_widget = QTabWidget()
    main_layout.addWidget(self.tab_widget)

    movie_tab = self._create_movie_tab()
    self.tab_widget.addTab(movie_tab, "Add Movie")

    series_tab = self._create_series_tab()
    self.tab_widget.addTab(series_tab, "Add TV Series")

How it works:
1. Create QTabWidget()
2. Create each tab as a QWidget with its own layout
3. Use addTab(widget, "Tab Name") to add tabs
"""


# EXAMPLE 8: Tabbed Interface (exactly like your app!)
class TabbedApp(QMainWindow):
    """A window with tabs, just like your Media Catalogue."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabbed App")
        self.setMinimumSize(400, 300)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Create the tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create and add tabs
        movie_tab = self._create_movie_tab()
        self.tab_widget.addTab(movie_tab, "Add Movie")

        series_tab = self._create_series_tab()
        self.tab_widget.addTab(series_tab, "Add TV Series")

        # Result label below tabs
        self.result = QLabel("")
        main_layout.addWidget(self.result)

    def _create_movie_tab(self):
        """Create the movie form tab."""
        tab = QWidget()
        layout = QFormLayout(tab)

        self.movie_title = QLineEdit()
        self.movie_year = QSpinBox()
        self.movie_year.setRange(1895, 2100)
        self.movie_year.setValue(2024)

        layout.addRow("Title:", self.movie_title)
        layout.addRow("Year:", self.movie_year)

        btn = QPushButton("Add Movie")
        btn.clicked.connect(self._on_add_movie)
        layout.addRow(btn)

        return tab

    def _create_series_tab(self):
        """Create the TV series form tab."""
        tab = QWidget()
        layout = QFormLayout(tab)

        self.series_title = QLineEdit()
        self.series_seasons = QSpinBox()
        self.series_seasons.setRange(1, 100)
        self.series_seasons.setValue(1)

        layout.addRow("Title:", self.series_title)
        layout.addRow("Seasons:", self.series_seasons)

        btn = QPushButton("Add TV Series")
        btn.clicked.connect(self._on_add_series)
        layout.addRow(btn)

        return tab

    def _on_add_movie(self):
        title = self.movie_title.text()
        year = self.movie_year.value()
        self.result.setText(f"Added movie: {title} ({year})")

    def _on_add_series(self):
        title = self.series_title.text()
        seasons = self.series_seasons.value()
        self.result.setText(f"Added series: {title} ({seasons} seasons)")


"""
================================================================================
KEY METHODS SUMMARY
================================================================================

| Widget          | Get Value         | Notes                |
|-----------------|-------------------|----------------------|
| QLineEdit       | .text()           | Returns string       |
| QSpinBox        | .value()          | Returns int          |
| QComboBox       | .currentText()    | Selected option      |
| QTableWidget    | .setItem(r,c,item)| Fill cells           |
| QTableWidget    | .currentRow()     | Selected row index   |

================================================================================
RUN THE EXAMPLES
================================================================================
"""


def run_example(window_class):
    """Helper function to run any example window."""
    app = QApplication(sys.argv)
    window = window_class()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    print("=" * 60)
    print("LESSON 9: BUILDING FORMS AND TABLES")
    print("=" * 60)
    print("\nChoose an example to run:")
    print("1. SimpleForm - Basic QFormLayout")
    print("2. Counter - Signal/Slot connection")
    print("3. MovieForm - Your exact movie form!")
    print("4. TableDemo - Empty table with headers")
    print("5. FilledTable - Table with movie data")
    print("6. ValidatedForm - Form with error dialog")
    print("7. DropdownDemo - QComboBox filter")
    print("8. TabbedApp - Tabs like your Media Catalogue!")
    print()

    choice = input("Enter number (1-8): ").strip()

    examples = {
        "1": SimpleForm,
        "2": Counter,
        "3": MovieForm,
        "4": TableDemo,
        "5": FilledTable,
        "6": ValidatedForm,
        "7": DropdownDemo,
        "8": TabbedApp,
    }

    if choice in examples:
        run_example(examples[choice])
    else:
        print("Invalid choice. Running TabbedApp as default...")
        run_example(TabbedApp)