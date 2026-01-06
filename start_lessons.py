#!/usr/bin/env python3
"""
Start the Jupyter notebook server for the lessons.

Usage:
    python start_lessons.py
"""

import subprocess
import sys
import os
from pathlib import Path


def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.resolve()
    lessons_dir = script_dir / "lessons"

    # Check if lessons directory exists
    if not lessons_dir.exists():
        print(f"Error: Lessons directory not found at {lessons_dir}")
        sys.exit(1)

    print("=" * 50)
    print("  Starting Jupyter Notebook Server")
    print("=" * 50)
    print(f"\nLessons directory: {lessons_dir}")
    print("\nThis will open in your web browser.")
    print("To stop the server, press Ctrl+C in this terminal.\n")

    # Try to find jupyter in the virtual environment first
    venv_jupyter = script_dir / ".venv" / "bin" / "jupyter"
    if sys.platform == "win32":
        venv_jupyter = script_dir / ".venv" / "Scripts" / "jupyter.exe"

    if venv_jupyter.exists():
        jupyter_cmd = str(venv_jupyter)
        print(f"Using Jupyter from virtual environment")
    else:
        # Fall back to system jupyter
        jupyter_cmd = "jupyter"
        print(f"Using system Jupyter")

    print("-" * 50)

    try:
        # Start Jupyter notebook
        subprocess.run(
            [jupyter_cmd, "notebook", str(lessons_dir)],
            cwd=str(script_dir)
        )
    except FileNotFoundError:
        print("\nError: Jupyter is not installed!")
        print("\nTo install it, run:")
        print("  python setup.py")
        print("\nOr manually:")
        print("  pip install jupyter notebook")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nJupyter server stopped.")


if __name__ == "__main__":
    main()
