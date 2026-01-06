# Glossary

A quick reference for terms used in this tutorial. Don't worry about memorizing these. Come back here whenever you need a reminder.

## Python Basics

### Variable
A name that stores a value. Like a labeled box that holds something.
```python
name = "The Matrix"  # 'name' is a variable holding the text "The Matrix"
year = 1999          # 'year' is a variable holding the number 1999
```

### Function
A reusable block of code that does a specific task. You "call" a function to run it.
```python
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # Calling the function, prints "Hello, Alice!"
```

### Parameter / Argument
| Term | Definition |
|------|------------|
| Parameter | The variable name in a function definition |
| Argument | The actual value you pass when calling the function |

```python
def greet(name):      # 'name' is a parameter
    print(f"Hello, {name}!")

greet("Alice")        # "Alice" is an argument
```

## Object Oriented Programming (OOP)

### Class
A blueprint for creating objects. Defines what data (attributes) and actions (methods) the object will have.
```python
class Movie:
    def __init__(self, title):
        self.title = title
```

### Object / Instance
A specific thing created from a class. If `Movie` is the blueprint, then `inception` is one actual movie built from that blueprint.
```python
inception = Movie("Inception")  # 'inception' is an object/instance of Movie
```

### `__init__`
A special method that runs automatically when you create a new object. Used to set up the object's initial state.
```python
class Movie:
    def __init__(self, title, year):
        self.title = title  # Set up the title
        self.year = year    # Set up the year
```

### `self`
Refers to the current object. When you write `self.title`, you're saying "this object's title."
```python
class Movie:
    def __init__(self, title):
        self.title = title  # Store title in THIS object

    def describe(self):
        print(self.title)   # Access THIS object's title
```

### Attribute
A variable that belongs to an object. Accessed with dot notation.
```python
movie = Movie("Inception", 2010)
print(movie.title)  # 'title' is an attribute, prints "Inception"
print(movie.year)   # 'year' is an attribute, prints 2010
```

### Method
A function that belongs to a class. Called on an object using dot notation.
```python
class Movie:
    def describe(self):  # This is a method
        print(f"{self.title} ({self.year})")

movie = Movie("Inception", 2010)
movie.describe()  # Calling the method, prints "Inception (2010)"
```

### Inheritance
When one class is based on another class. The new class (child) gets all the features of the original (parent) and can add its own.
```python
class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year

class TVSeries(Movie):  # TVSeries inherits from Movie
    def __init__(self, title, year, seasons):
        super().__init__(title, year)  # Call parent's __init__
        self.seasons = seasons         # Add new attribute
```

### `super()`
Used to call a method from the parent class. Most commonly used in `__init__` to set up inherited attributes.
```python
super().__init__(title, year)  # Call parent class's __init__
```

## Error Handling

### Exception
An error that happens while the program is running. Python stops and shows an error message.
```python
x = 1 / 0  # ZeroDivisionError, can't divide by zero
```

### `raise`
Used to create an error on purpose. Useful for validation.
```python
if year < 1895:
    raise ValueError("Year must be 1895 or later")
```

### `ValueError`
An error that means "the value is wrong." Used when an argument has the right type but an inappropriate value.
```python
raise ValueError("Duration must be positive")
```

### `TypeError`
An error that means "the type is wrong." Used when an argument has the wrong type.
```python
raise TypeError("Title must be a string")
```

### `try` / `except`
A way to handle errors gracefully instead of crashing.
```python
try:
    movie = Movie("", 2020)  # This will raise an error
except ValueError as e:
    print(f"Couldn't create movie: {e}")  # Handle the error
```

## Testing

### Test
Code that checks if other code works correctly. Runs automatically to find bugs.
```python
def test_movie_has_correct_title():
    movie = Movie("Inception", 2010, "Nolan", 148)
    assert movie.title == "Inception"
```

### `assert`
A statement that checks if something is true. If false, the test fails.
```python
assert 1 + 1 == 2      # Passes, this is true
assert movie.year > 0  # Passes if year is positive
```

### pytest
A testing tool for Python. Finds and runs your test functions automatically.
```bash
pytest tests/ -v  # Run all tests with verbose output
```

### Parameterized Test
A test that runs multiple times with different inputs. Avoids writing the same test over and over.
```python
@pytest.mark.parametrize("year", [1895, 2000, 2024])
def test_valid_years(year):
    movie = Movie("Test", year, "Director", 90)
    assert movie.year == year
```

## GUI (Graphical User Interface)

### Widget
A visual element in a GUI. Buttons, text boxes, labels, and tables are all widgets.

### PySide6
A Python library for building desktop applications with a graphical interface. It's the official Python version of Qt.

### Qt
A popular framework for building GUIs. Works on Windows, macOS, and Linux. PySide6 lets you use Qt with Python.

### Signal
An event that a widget sends when something happens (like a button being clicked).
```python
button.clicked.connect(self.on_button_clicked)  # When clicked, call this method
```

### Slot
A method that responds to a signal. The function that runs when an event happens.
```python
def on_button_clicked(self):  # This is a slot
    print("Button was clicked!")
```

### Layout
A way to arrange widgets in a window. Handles positioning and resizing automatically.
```python
layout = QVBoxLayout()   # Vertical layout, widgets stack top to bottom
layout.addWidget(button)
layout.addWidget(label)
```

## Other Terms

### Virtual Environment (venv)
A separate Python installation for your project. Keeps your project's packages separate from other projects.
```bash
python -m venv .venv       # Create a virtual environment
source .venv/bin/activate  # Activate it (macOS/Linux)
```

### pip
Python's package installer. Used to download and install libraries.
```bash
pip install PySide6                  # Install the PySide6 package
pip install -r requirements.txt      # Install all packages from a file
```

### Module
A Python file that contains code you can import and use.
```python
from media_catalogue import Movie  # Import Movie from another file
```

### Package
A folder containing multiple Python modules. Has an `__init__.py` file.

## Quick Reference: Common Patterns

### Creating a class with validation
```python
class Movie:
    def __init__(self, title, year):
        if not title:
            raise ValueError("Title cannot be empty")
        if year < 1895:
            raise ValueError("Year must be 1895 or later")
        self.title = title
        self.year = year
```

### Inheritance with super()
```python
class TVSeries(Movie):
    def __init__(self, title, year, seasons):
        super().__init__(title, year)  # Parent setup
        self.seasons = seasons         # Child specific setup
```

### Basic pytest test
```python
def test_something_works():
    result = do_something()
    assert result == expected_value
```

### Basic PySide6 window
```python
from PySide6.QtWidgets import QApplication, QMainWindow
import sys

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("My App")
window.show()
app.exec()
```