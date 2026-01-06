"""
================================================================================
LESSON 8: PYSIDE6 INTRODUCTION
================================================================================

In this lesson, you'll learn the basics of PySide6 by understanding YOUR actual
code line by line.

Run this file:
    python lessons/08_pyside6_intro.py

================================================================================
WHAT IS PYSIDE6?
================================================================================

PySide6 is a Python library for creating desktop applications with windows,
buttons, forms, and more.

- Qt (pronounced "cute") is the underlying framework (written in C++)
- PySide6 is Python's official way to use Qt
- Used by professional apps like Autodesk Maya, Dropbox, and VLC

Your main_window.py uses PySide6 to create the Media Catalogue GUI.

================================================================================
STEP 1: THE IMPORTS (Your Code Lines 6-22)
================================================================================

Let's look at the imports from your main_window.py:

    from PySide6.QtWidgets import (
        QMainWindow,      # The main application window
        QWidget,          # Base class for all UI elements
        QVBoxLayout,      # Arranges widgets vertically (top to bottom)
        QHBoxLayout,      # Arranges widgets horizontally (left to right)
        QPushButton,      # A clickable button
        QTableWidget,     # A table with rows and columns
        QTableWidgetItem, # One cell in the table
        QLineEdit,        # A text input field
        QLabel,           # Displays text
        QSpinBox,         # A number input with up/down arrows
        QMessageBox,      # Popup dialogs (errors, warnings)
        QTabWidget,       # Tabs to organize content
        QFormLayout,      # Two-column layout for forms
        QHeaderView,      # Controls table headers
        QComboBox,        # Dropdown menu
    )

Each import is a WIDGET - a building block for your GUI.

WHAT EACH WIDGET DOES:
----------------------
| Widget          | What It Does                              | Example                    |
|-----------------|-------------------------------------------|----------------------------|
| QMainWindow     | The main window with title bar, menu bar  | Your entire app window     |
| QWidget         | Base container for other widgets          | Holds your form fields     |
| QVBoxLayout     | Stacks widgets top to bottom              | Form fields one below another |
| QHBoxLayout     | Puts widgets side by side                 | Filter dropdown next to Delete button |
| QPushButton     | Clickable button                          | "Add Movie" button         |
| QLineEdit       | Text input box                            | Title input                |
| QSpinBox        | Number input with arrows                  | Year selector              |
| QTableWidget    | Table of data                             | Your movie/series list     |
| QComboBox       | Dropdown selector                         | "All", "Movies Only", "TV Series Only" |
| QTabWidget      | Tabbed panels                             | "Add Movie" and "Add TV Series" tabs |
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
)


"""
================================================================================
STEP 2: CREATING A WINDOW
================================================================================

Every PySide6 app needs a WINDOW. Let's break down your window class:

    class MainWindow(QMainWindow):    # Inherit from QMainWindow
        def __init__(self):
            super().__init__()        # Call parent's __init__
            self.catalogue = MediaCatalogue()  # Your business logic
            self._setup_ui()          # Build the interface

Line by line:
1. class MainWindow(QMainWindow) - Your class inherits from QMainWindow
   (gets window features for free)
2. super().__init__() - Calls QMainWindow's setup (just like TVSeries calls
   Movie's __init__)
3. self.catalogue - Stores your MediaCatalogue (business logic separate from GUI!)
4. self._setup_ui() - Calls a method to build the visual interface
"""


# EXAMPLE 1: Create Your First Window
class MyFirstWindow(QMainWindow):
    """A simple window to demonstrate the basics."""

    def __init__(self):
        super().__init__()  # Call parent's __init__

        # Set the window title
        self.setWindowTitle("My First PySide6 Window")

        # Set minimum window size (width, height)
        self.setMinimumSize(400, 300)


"""
================================================================================
STEP 3: CENTRAL WIDGET AND LAYOUT
================================================================================

A QMainWindow needs a CENTRAL WIDGET to hold your content. From your code (lines 47-50):

    # Central widget
    central_widget = QWidget()           # Create an empty container
    self.setCentralWidget(central_widget) # Put it in the window
    main_layout = QVBoxLayout(central_widget)  # Add vertical layout to it

What's happening:
1. QWidget() - Creates an empty container (like an empty box)
2. setCentralWidget() - Puts this box in the center of your window
3. QVBoxLayout(central_widget) - Creates a vertical layout INSIDE the widget

Why layouts? Without a layout, you'd have to position every widget with exact
pixel coordinates. Layouts arrange widgets automatically!
"""


# EXAMPLE 2: Window with Central Widget and Layout
class WindowWithLayout(QMainWindow):
    """A window with a central widget and vertical layout."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window with Layout")
        self.setMinimumSize(400, 300)

        # Step 1: Create a central widget
        central_widget = QWidget()

        # Step 2: Set it as the central widget
        self.setCentralWidget(central_widget)

        # Step 3: Create a vertical layout
        layout = QVBoxLayout(central_widget)

        # Step 4: Add a label to the layout
        label = QLabel("Hello from PySide6!")
        layout.addWidget(label)


"""
================================================================================
STEP 4: ADDING WIDGETS TO A LAYOUT
================================================================================

To add widgets to a layout, use layout.addWidget():

    layout = QVBoxLayout(central_widget)
    layout.addWidget(some_label)   # Add a label
    layout.addWidget(some_button)  # Add a button below it
    layout.addWidget(some_table)   # Add a table below that

QVBoxLayout stacks them VERTICALLY (top to bottom).
QHBoxLayout puts them HORIZONTALLY (left to right).
"""


# EXAMPLE 3: Multiple Widgets in a Layout
class LabelAndButton(QMainWindow):
    """A window with a label and button stacked vertically."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Label and Button")
        self.setMinimumSize(300, 200)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Add a label
        label = QLabel("Click the button below!")
        layout.addWidget(label)

        # Add a button
        button = QPushButton("Click Me")
        layout.addWidget(button)


"""
================================================================================
STEP 5: SIGNALS AND SLOTS (HOW BUTTONS WORK)
================================================================================

This is the MOST important concept in Qt!

- SIGNAL = Something that happens (button clicked, text changed)
- SLOT = A function that runs when the signal happens

From your code (line 120):
    add_btn.clicked.connect(self._on_add_movie)

Breaking it down:
- add_btn - The button widget
- .clicked - The signal (emitted when button is clicked)
- .connect() - Links the signal to a function
- self._on_add_movie - The function to run (the "slot")

In plain English: "When add_btn is clicked, run self._on_add_movie"
"""


# EXAMPLE 4: Clickable Button with Signal/Slot
class ClickableButton(QMainWindow):
    """A window with a button that counts clicks."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Click Counter")
        self.setMinimumSize(300, 200)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.count = 0

        self.label = QLabel("Count: 0")
        layout.addWidget(self.label)

        button = QPushButton("Click Me!")
        # Connect the button's clicked signal to self.on_click
        button.clicked.connect(self.on_click)
        layout.addWidget(button)

    def on_click(self):
        """This runs when the button is clicked."""
        self.count += 1
        self.label.setText(f"Count: {self.count}")


"""
================================================================================
STEP 6: TEXT INPUT WITH QLINEEDIT
================================================================================

From your code (line 105):
    self.movie_title = QLineEdit()  # Create text input

To get the text the user typed:
    title = self.movie_title.text()  # Get the text

To clear the input:
    self.movie_title.clear()  # Empty the field
"""


# EXAMPLE 5: Text Input
class GreetingApp(QMainWindow):
    """A window where you type your name and get a greeting."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Greeting App")
        self.setMinimumSize(300, 200)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(QLabel("Enter your name:"))

        self.name_input = QLineEdit()  # Text input
        layout.addWidget(self.name_input)

        button = QPushButton("Say Hello")
        button.clicked.connect(self.on_greet)
        layout.addWidget(button)

        self.result = QLabel("")
        layout.addWidget(self.result)

    def on_greet(self):
        # Get the text from name_input using .text()
        name = self.name_input.text()
        self.result.setText(f"Hello, {name}!")


"""
================================================================================
STEP 7: NUMBER INPUT WITH QSPINBOX
================================================================================

From your code (lines 106-108):
    self.movie_year = QSpinBox()       # Create number input
    self.movie_year.setRange(1895, 2100)  # Set min/max values
    self.movie_year.setValue(2024)     # Set default value

To get the number:
    year = self.movie_year.value()  # Returns an integer

NOTE: .value() for QSpinBox, .text() for QLineEdit
"""


# EXAMPLE 6: Number Input
class YearSelector(QMainWindow):
    """A window with a year selector spin box."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Year Selector")
        self.setMinimumSize(300, 200)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(QLabel("Select a year:"))

        self.year_input = QSpinBox()
        self.year_input.setRange(1895, 2100)  # Movies started in 1895
        self.year_input.setValue(2024)
        layout.addWidget(self.year_input)

        button = QPushButton("Show Year")
        button.clicked.connect(self.on_show)
        layout.addWidget(button)

        self.result = QLabel("")
        layout.addWidget(self.result)

    def on_show(self):
        # Get the value from year_input using .value()
        year = self.year_input.value()
        self.result.setText(f"Selected year: {year}")


"""
================================================================================
KEY TAKEAWAYS
================================================================================

1. QMainWindow - Your main application window
2. QWidget + Layout - Container with automatic widget arrangement
3. QVBoxLayout - Stacks widgets vertically
4. addWidget() - Adds a widget to a layout
5. Signals & Slots - button.clicked.connect(function) runs function on click
6. QLineEdit.text() - Gets text from text input
7. QSpinBox.value() - Gets number from number input

================================================================================
RUN THE EXAMPLES
================================================================================

Uncomment the example you want to run at the bottom of this file.
"""


def run_example(window_class):
    """Helper function to run any example window."""
    app = QApplication(sys.argv)
    window = window_class()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    print("=" * 60)
    print("LESSON 8: PYSIDE6 INTRODUCTION")
    print("=" * 60)
    print("\nChoose an example to run:")
    print("1. MyFirstWindow - Basic empty window")
    print("2. WindowWithLayout - Window with central widget")
    print("3. LabelAndButton - Label and button stacked")
    print("4. ClickableButton - Button that counts clicks")
    print("5. GreetingApp - Text input example")
    print("6. YearSelector - Number input example")
    print()

    choice = input("Enter number (1-6): ").strip()

    examples = {
        "1": MyFirstWindow,
        "2": WindowWithLayout,
        "3": LabelAndButton,
        "4": ClickableButton,
        "5": GreetingApp,
        "6": YearSelector,
    }

    if choice in examples:
        run_example(examples[choice])
    else:
        print("Invalid choice. Running ClickableButton as default...")
        run_example(ClickableButton)