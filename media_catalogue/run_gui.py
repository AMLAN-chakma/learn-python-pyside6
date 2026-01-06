#!/usr/bin/env python3
"""
Launcher script for Media Catalogue GUI.
Can be run from anywhere - automatically handles paths and dependencies.
"""

import os
import subprocess
import sys
from pathlib import Path


def ensure_pyside6():
    """Install PySide6 and QtWebEngine if not already installed."""
    try:
        import PySide6
        return True
    except ImportError:
        print("PySide6 not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PySide6", "PySide6-WebEngine"])
        return True


def main():
    # Ensure PySide6 is installed
    ensure_pyside6()

    # CRITICAL: Set environment variables BEFORE any Qt imports
    # This prevents segfaults with QtWebEngine on macOS
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-gpu")

    # Get the directory where this script lives
    script_dir = Path(__file__).parent.resolve()

    # Add src to path so imports work
    sys.path.insert(0, str(script_dir / "src"))

    # CRITICAL: QApplication must be created BEFORE importing QWebEngineView
    # This is the #1 cause of segfaults with QtWebEngine
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    # NOW it's safe to import the main window (which imports QWebEngineView)
    from gui.main_window import MainWindow

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
