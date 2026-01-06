# Media Catalogue

A Python OOP exercise for managing a catalogue of movies and TV series with validation, custom exceptions, and a PySide6 GUI.

## Status: Complete

## Project Structure

```
media_catalogue/
├── run_gui.py                # Launcher script (auto-installs PySide6)
├── src/
│   ├── __init__.py
│   └── media_catalogue.py    # Business logic (Movie, TVSeries, MediaCatalogue)
├── gui/
│   ├── __init__.py
│   └── main_window.py        # PySide6 GUI (thin wrapper over src/)
└── tests/
    ├── conftest.py
    └── test_media_catalogue.py  # pytest tests with parameterization
```

## Features

- **Movie class** with title, year, director, duration validation
- **TVSeries class** extending Movie with seasons and episodes
- **MediaCatalogue** for managing collections with add, delete, and filtering
- **MediaError** custom exception that stores the invalid object
- **PySide6 GUI** (thin wrapper over business logic) with:
  - Tabbed forms for adding Movies and TV Series
  - Table view with row selection
  - Delete selected items
  - Filter by type (All / Movies Only / TV Series Only)
- **Comprehensive pytest suite** with parameterized tests and readable IDs

## Validation Rules

| Field    | Rules                                                                |
|----------|----------------------------------------------------------------------|
| Title    | Must be string, cannot be empty (numeric titles like "1917" allowed) |
| Year     | Must be 1895 or later                                                |
| Director | Must be string, cannot be empty, must contain at least one letter    |
| Duration | Must be positive                                                     |

## Running Tests

```bash
cd python/projects/media_catalogue
python -m pytest tests/ -v
```

## Running the GUI

```bash
# Option 1: Use the launcher (auto-installs PySide6 if needed)
python run_gui.py

# Option 2: Run directly
python -m gui.main_window
```

## Concepts Practiced

- Classes and inheritance
- Input validation with custom exceptions
- Type checking with `isinstance()`
- Separation of concerns (business logic vs GUI)
- Pytest with `@pytest.mark.parametrize`
- Test IDs with `pytest.param(..., id='readable_name')`
- Thin wrapper GUI pattern
- Path handling with `pathlib`
