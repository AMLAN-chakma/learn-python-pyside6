# PySide6 Tutorial: Build Your First Desktop App

Learn Python best practices, testing, and GUI development by building a real Media Catalogue application.

## Table of Contents

1. [What You'll Learn](#what-youll-learn)
2. [Who Is This For](#who-is-this-for)
3. [The Project You'll Build](#the-project-youll-build)
4. [Quick Start](#quick-start)
5. [Lesson Index](#lesson-index)
6. [Try the Finished Application](#try-the-finished-application)
7. [Recommended Learning Path](#recommended-learning-path)
8. [Project Structure](#project-structure)
9. [Running Tests](#running-tests)
10. [Need Help](#need-help)

## What You'll Learn

This tutorial covers three main areas:

### 1. Python Object Oriented Programming (OOP)

You'll learn how to organize your code using classes, the building blocks of real applications.

| Topic                 | Description                                                                               |
|-----------------------|-------------------------------------------------------------------------------------------|
| Classes and Objects   | How to create blueprints (`class Movie`) and make things from them (`movie = Movie(...)`) |
| The `__init__` method | How objects get set up when you create them                                               |
| `self`                | Why every method needs it and what it means                                               |
| Inheritance           | How to build new classes based on existing ones (like `TVSeries` extending `Movie`)       |
| `super()`             | How child classes use their parent's code                                                 |
| Validation            | How to check that data is correct before using it                                         |
| Custom Errors         | How to create your own error types with helpful messages                                  |

### 2. Testing with pytest

Most tutorials skip testing. We don't. You'll learn why testing matters and how to do it properly.

| Topic                        | Description                                       |
|------------------------------|---------------------------------------------------|
| Why test?                    | How tests save you hours of debugging             |
| Debug printing vs real tests | We'll show you both and why tests are better      |
| pytest basics                | How to write and run tests                        |
| Assertions                   | How to check if your code does what you expect    |
| Parameterized tests          | How to test many cases without repeating yourself |
| Test organization            | How to structure your test files                  |

### 3. GUI Development with PySide6

You'll build a real desktop application that runs on Windows, macOS, and Linux.

| Topic                    | Description                                                  |
|--------------------------|--------------------------------------------------------------|
| What is Qt/PySide6?      | The framework behind many professional apps                  |
| Windows and Widgets      | Buttons, text boxes, tables, and more                        |
| Layouts                  | How to arrange widgets so they resize properly               |
| Signals and Slots        | How buttons know what to do when clicked                     |
| The thin wrapper pattern | How to keep your GUI code clean and separate from your logic |
| Putting it all together  | Building the complete Media Catalogue app                    |

## Who Is This For

This tutorial is for Python beginners to intermediate learners who:

| Requirement        | Description                                |
|--------------------|--------------------------------------------|
| Know the basics    | Variables, functions, loops, if statements |
| Want to learn      | How to build real applications             |
| Are curious        | About GUI programming                      |
| Want to understand | Testing and best practices                 |

You don't need to know:

| Topic                       | i'll teach you!   |
|-----------------------------|-------------------|
| Object oriented programming | Covered in Part 1 |
| Testing frameworks          | Covered in Part 2 |
| GUI development             | Covered in Part 3 |

See the [Glossary](resources/glossary.md) for definitions of any terms you don't recognize.

See [External Resources](resources/external_resources.md) for links to FreeCodeCamp, documentation, and more help.

## The Project You'll Build

Throughout this tutorial, you'll build a Media Catalogue application, a desktop app for tracking your movies and TV series.

### The Business Logic (Python)

You'll create these classes:

```
Movie
    title (string)
    year (number, 1895 or later)
    director (string)
    duration (minutes)

TVSeries (extends Movie)
    Everything from Movie, plus:
    seasons (number)
    total_episodes (number)

MediaCatalogue
    add()            Add a movie or series
    delete()         Remove an item
    get_movies()     Get only movies
    get_tv_series()  Get only series
```

### The GUI (PySide6)

You'll build a window with:

| Feature         | Description                |
|-----------------|----------------------------|
| Tabs            | To add movies or TV series |
| Form inputs     | With validation            |
| Table           | Showing your collection    |
| Filter dropdown | All / Movies / Series      |
| Delete button   | Remove items               |

### The Tests (pytest)

You'll write tests that:

| Test Type           | What It Checks                          |
|---------------------|-----------------------------------------|
| Creation tests      | Verify movies are created correctly     |
| Validation tests    | Check that validation catches bad input |
| Filter tests        | Ensure the catalogue filters work       |
| Parameterized tests | Cover edge cases automatically          |

By the end, you'll have 71 passing tests and a fully working application!

## Quick Start

### Step 1: Clone or Download This Project

```bash
git clone <repository-url>
cd pyside_tutorial
```

### Step 2: Run the Setup Script

This works on Windows, macOS, and Linux:

```bash
python setup.py
```

The script will:
1. Create a virtual environment
2. Install all dependencies (PySide6, pytest, Jupyter)
3. Verify everything is working

### Step 3: Activate the Virtual Environment

macOS / Linux:
```bash
source .venv/bin/activate
```

Windows (Command Prompt):
```bash
.venv\Scripts\activate
```

Windows (PowerShell):
```bash
.venv\Scripts\Activate.ps1
```

### Step 4: Start the Lessons

```bash
jupyter notebook lessons/
```

This opens the lessons in your web browser. Start with `00_introduction.ipynb`.

## Lesson Index

### Part 1: Python OOP (Jupyter Notebooks)

| Lesson | File                      | Topic                 | What You'll Build                                      |
|--------|---------------------------|-----------------------|--------------------------------------------------------|
| 00     | `00_introduction.ipynb`   | Introduction          | Getting set up and understanding the learning approach |
| 01     | `01_python_classes.ipynb` | Python Classes        | Build the `Movie` class from scratch                   |
| 02     | `02_inheritance.ipynb`    | Inheritance           | Build `TVSeries` that extends `Movie`                  |
| 03     | `03_validation.ipynb`     | Validation and Errors | Add input validation and custom `MediaError`           |
| 04     | `04_collections.ipynb`    | Collections           | Build the `MediaCatalogue` to store and filter items   |

### Part 2: Testing (Jupyter Notebooks)

| Lesson | File                      | Topic               | What You'll Learn                                  |
|--------|---------------------------|---------------------|----------------------------------------------------|
| 05     | `05_debugging.ipynb`      | Debugging           | Using print statements and debug flags effectively |
| 06     | `06_testing_basics.ipynb` | Testing Basics      | Write your first pytest tests for the Movie class  |
| 07     | `07_parameterized.ipynb`  | Parameterized Tests | Test many cases without repeating yourself         |

### Part 3: GUI Development (Python Files)

**Note:** The GUI lessons are Python files, not Jupyter notebooks. PySide6 does not work properly in Jupyter.

| Lesson | File                     | Topic               | What You'll Build                          |
|--------|--------------------------|---------------------|--------------------------------------------|
| 08     | `08_pyside6_intro.py`    | PySide6 Intro       | Your first window with buttons and signals |
| 09     | `09_building_gui.py`     | Building the GUI    | Forms, tables, and validation dialogs      |
| 10     | `10_putting_together.py` | Putting It Together | The complete Media Catalogue interface     |

To run the GUI lessons:
```bash
python lessons/08_pyside6_intro.py
python lessons/09_building_gui.py
python lessons/10_putting_together.py
```

### Bonus: Embedding Web Content

| Lesson | File                | Topic       | What You'll Learn                |
|--------|---------------------|-------------|----------------------------------|
| 11     | `11_web_browser.py` | Web Browser | Embed web pages in a PySide6 app |

```bash
python lessons/11_web_browser.py
```

**Note:** Some sites may not load due to security settings. This is normal.

## Try the Finished Application

Want to see what you'll build? Run the completed GUI:

```bash
python media_catalogue/run_gui.py
```

This opens the Media Catalogue application where you can:

| Action | Description                |
|--------|----------------------------|
| Add    | Movies and TV series       |
| View   | Your collection in a table |
| Filter | By movies or series        |
| Delete | Remove items               |

## Recommended Learning Path

### Option A: Complete the FreeCodeCamp Workshop First (Recommended)

1. Complete the [FreeCodeCamp Media Catalogue Workshop](https://www.freecodecamp.org/learn/python-v9/workshop-media-catalogue/step-1) first
2. This builds the initial Media Catalogue code so you understand how it works
3. Then come back here to learn testing and GUI development

### Option B: Learn Everything Here

1. Start with Lesson 00 and work through each lesson in order
2. Each lesson has explanations, examples, and exercises
3. Take your time, there's no rush

## Project Structure

```
pyside_tutorial/
    README.md               You are here
    setup.py                Run this to set up your environment
    requirements.txt        List of dependencies

    lessons/                Lesson files (start here!)
        00_introduction.ipynb
        01_python_classes.ipynb
        02_inheritance.ipynb
        03_validation.ipynb
        04_collections.ipynb
        05_debugging.ipynb
        06_testing_basics.ipynb
        07_parameterized.ipynb
        08_pyside6_intro.py      (Python file)
        09_building_gui.py       (Python file)
        10_putting_together.py   (Python file)
        11_web_browser.py        (Python file)

    media_catalogue/        The application we're building
        src/                Business logic (Python classes)
        gui/                GUI code (PySide6)
        tests/              Test files (pytest)
        run_gui.py          Run the application

    resources/              Extra learning materials
        glossary.md         Definitions of terms
        external_resources.md   Helpful links
```

## Running Tests

To run the test suite:

```bash
pytest media_catalogue/tests/ -v
```

You should see all 71 tests pass. As you go through the lessons, you'll learn how these tests work and even write some yourself!

## Need Help

| Resource                                              | Description                      |
|-------------------------------------------------------|----------------------------------|
| [Glossary](resources/glossary.md)                     | Definitions of programming terms |
| [External Resources](resources/external_resources.md) | Links to more learning materials |
| GitHub Issues                                         | Found a bug? Open an issue       |

## Philosophy

> Don't try to memorize everything. Focus on understanding.

This tutorial is designed so you can:

| Goal                 | How                 |
|----------------------|---------------------|
| Learn by doing       | Not just reading    |
| Make mistakes        | And learn from them |
| Build something real | That actually works |
| Reference later      | Come back anytime   |

Take your time. Programming is a skill that gets better with practice.

## License

This tutorial is open source and free to use for learning.
