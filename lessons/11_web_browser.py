"""
================================================================================
LESSON 11: EMBEDDING A WEB BROWSER (BONUS)
================================================================================

Load websites inside your PySide6 app using QWebEngineView.

This is a bonus lesson showing how to embed web content in desktop apps.

Run this file:
    python lessons/11_web_browser.py

================================================================================
WHY SOME SITES MAY NOT LOAD
================================================================================

Some websites may show a blank page or error when embedded. This is not a bug.

Websites can set security headers that block embedding inside other apps.
This is a security feature to prevent attacks like clickjacking.

If a site doesn't load, try a different one.

================================================================================
IMPORTANT: QWEBENGINEVIEW SETUP
================================================================================

CRITICAL: QWebEngineView must be imported AFTER QApplication is created!

    # WRONG - will cause segfault:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    app = QApplication(sys.argv)

    # CORRECT - create QApplication first:
    app = QApplication(sys.argv)
    from PySide6.QtWebEngineWidgets import QWebEngineView

This is why the Jupyter notebook version didn't work well!

================================================================================
BASIC WEB VIEW
================================================================================

    from PySide6.QtWebEngineWidgets import QWebEngineView
    from PySide6.QtCore import QUrl

    browser = QWebEngineView()
    browser.setUrl(QUrl("https://www.google.com"))
    browser.show()

Key points:
- Use QUrl() to wrap URL strings
- setUrl() loads a webpage
- The browser widget is just like any other widget

================================================================================
USEFUL SIGNALS
================================================================================

QWebEngineView provides these signals:

    browser.urlChanged.connect(on_url_changed)      # URL changed
    browser.loadFinished.connect(on_load_finished)  # Page loaded
    browser.loadProgress.connect(on_progress)       # Loading progress (0-100)

================================================================================
NAVIGATION METHODS
================================================================================

    browser.setUrl(QUrl("https://example.com"))  # Go to URL
    browser.back()                                # Go back
    browser.forward()                             # Go forward
    browser.reload()                              # Reload page
    browser.stop()                                # Stop loading
"""

import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QProgressBar,
)
from PySide6.QtCore import QUrl


# EXAMPLE 1: Simple Web Browser
class SimpleBrowser(QMainWindow):
    """The simplest possible web browser."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Browser")
        self.setMinimumSize(800, 600)

        # Import QWebEngineView AFTER QApplication exists
        from PySide6.QtWebEngineWidgets import QWebEngineView

        # Create web view as central widget
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Load a URL
        self.browser.setUrl(QUrl("https://www.google.com"))


# EXAMPLE 2: Browser with URL Bar
class BrowserWithUrlBar(QMainWindow):
    """A browser with a URL bar for navigation."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser with URL Bar")
        self.setMinimumSize(900, 700)

        # Import QWebEngineView AFTER QApplication exists
        from PySide6.QtWebEngineWidgets import QWebEngineView

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # URL bar
        nav_bar = QHBoxLayout()

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL...")
        # returnPressed fires when user presses Enter
        self.url_bar.returnPressed.connect(self.navigate)
        nav_bar.addWidget(self.url_bar)

        go_btn = QPushButton("Go")
        go_btn.clicked.connect(self.navigate)
        nav_bar.addWidget(go_btn)

        layout.addLayout(nav_bar)

        # Web view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        # Update URL bar when URL changes
        self.browser.urlChanged.connect(self.update_url_bar)
        layout.addWidget(self.browser)

    def navigate(self):
        """Navigate to the URL in the URL bar."""
        url = self.url_bar.text()
        # Add https:// if not present
        if not url.startswith("http"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, url):
        """Update URL bar when browser navigates."""
        self.url_bar.setText(url.toString())


# EXAMPLE 3: Full Browser with Navigation Buttons
class FullBrowser(QMainWindow):
    """A more complete browser with back, forward, reload buttons."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Browser")
        self.setMinimumSize(1000, 700)

        # Import QWebEngineView AFTER QApplication exists
        from PySide6.QtWebEngineWidgets import QWebEngineView

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Navigation bar
        nav_bar = QHBoxLayout()

        # Back button
        back_btn = QPushButton("<")
        back_btn.setFixedWidth(30)
        back_btn.clicked.connect(lambda: self.browser.back())
        nav_bar.addWidget(back_btn)

        # Forward button
        forward_btn = QPushButton(">")
        forward_btn.setFixedWidth(30)
        forward_btn.clicked.connect(lambda: self.browser.forward())
        nav_bar.addWidget(forward_btn)

        # Reload button
        reload_btn = QPushButton("R")
        reload_btn.setFixedWidth(30)
        reload_btn.clicked.connect(lambda: self.browser.reload())
        nav_bar.addWidget(reload_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL...")
        self.url_bar.returnPressed.connect(self.navigate)
        nav_bar.addWidget(self.url_bar)

        # Go button
        go_btn = QPushButton("Go")
        go_btn.clicked.connect(self.navigate)
        nav_bar.addWidget(go_btn)

        layout.addLayout(nav_bar)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximumHeight(5)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)

        # Web view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        # Connect signals
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadProgress.connect(self.update_progress)
        self.browser.loadFinished.connect(self.on_load_finished)

        layout.addWidget(self.browser)

        # Status bar
        self.statusBar().showMessage("Ready")

    def navigate(self):
        """Navigate to the URL in the URL bar."""
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, url):
        """Update URL bar when browser navigates."""
        self.url_bar.setText(url.toString())
        self.statusBar().showMessage(f"Loading: {url.toString()}")

    def update_progress(self, progress):
        """Update progress bar during page load."""
        self.progress.setValue(progress)

    def on_load_finished(self, ok):
        """Called when page finishes loading."""
        if ok:
            self.statusBar().showMessage("Done", 2000)
        else:
            self.statusBar().showMessage("Failed to load", 2000)


"""
================================================================================
KEY POINTS
================================================================================

1. Create QApplication FIRST - before importing QWebEngineView
2. Use QUrl() - Wrap URLs with QUrl("https://...")
3. Signals available:
   - urlChanged - fires when URL changes
   - loadFinished - fires when page loads
   - loadProgress - fires during loading (0-100)
4. Navigation methods:
   - setUrl(QUrl) - go to URL
   - back() - go back
   - forward() - go forward
   - reload() - reload page

================================================================================
RUN THE EXAMPLES
================================================================================
"""


def run_example(window_class):
    """Helper function to run any example window."""
    # QApplication must be created BEFORE QWebEngineView is used
    app = QApplication(sys.argv)
    window = window_class()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    print("=" * 60)
    print("LESSON 11: EMBEDDING A WEB BROWSER")
    print("=" * 60)
    print("\nChoose an example to run:")
    print("1. SimpleBrowser - Just a web view")
    print("2. BrowserWithUrlBar - Web view + URL bar")
    print("3. FullBrowser - Back/Forward/Reload + progress bar")
    print()

    choice = input("Enter number (1-3): ").strip()

    examples = {
        "1": SimpleBrowser,
        "2": BrowserWithUrlBar,
        "3": FullBrowser,
    }

    if choice in examples:
        run_example(examples[choice])
    else:
        print("Invalid choice. Running FullBrowser as default...")
        run_example(FullBrowser)