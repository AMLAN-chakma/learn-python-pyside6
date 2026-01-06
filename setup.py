#!/usr/bin/env python3
"""
PySide6 Tutorial - Universal Setup Script

This script sets up everything you need to run the tutorial:
1. Creates a virtual environment
2. Installs all dependencies
3. Verifies the installation

Works on: Windows, macOS, Linux

Usage:
    python setup.py
"""

import subprocess
import sys
import os
from pathlib import Path


def print_step(message):
    """Print a formatted step message."""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")


def print_success(message):
    """Print a success message."""
    print(f"[OK] {message}")


def print_error(message):
    """Print an error message."""
    print(f"[ERROR] {message}")


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def get_venv_python():
    """Get the path to the Python executable in the virtual environment."""
    if sys.platform == "win32":
        return Path(".venv") / "Scripts" / "python.exe"
    else:
        return Path(".venv") / "bin" / "python"


def get_venv_pip():
    """Get the path to pip in the virtual environment."""
    if sys.platform == "win32":
        return Path(".venv") / "Scripts" / "pip.exe"
    else:
        return Path(".venv") / "bin" / "pip"


def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    print("\n" + "="*60)
    print("  PySide6 Tutorial - Setup Script")
    print("  Works on Windows, macOS, and Linux")
    print("="*60)

    # Step 1: Check Python version
    print_step("Step 1: Checking Python version")

    if sys.version_info < (3, 8):
        print_error(f"Python 3.8 or higher is required. You have Python {sys.version}")
        print("Please install a newer version of Python from https://python.org")
        sys.exit(1)

    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")

    # Step 2: Create virtual environment
    print_step("Step 2: Creating virtual environment")

    venv_path = Path(".venv")

    if venv_path.exists():
        print(f"Virtual environment already exists at: {venv_path.absolute()}")
        response = input("Do you want to recreate it? (y/N): ").strip().lower()
        if response == 'y':
            import shutil
            shutil.rmtree(venv_path)
            print("Removed existing virtual environment.")
        else:
            print("Keeping existing virtual environment.")

    if not venv_path.exists():
        success, output = run_command(
            [sys.executable, "-m", "venv", ".venv"],
            "Creating virtual environment..."
        )
        if not success:
            print_error("Failed to create virtual environment")
            print(output)
            sys.exit(1)
        print_success("Virtual environment created")

    # Step 3: Install dependencies
    print_step("Step 3: Installing dependencies")

    pip_path = get_venv_pip()

    if not pip_path.exists():
        print_error(f"Could not find pip at: {pip_path}")
        sys.exit(1)

    # Upgrade pip first
    success, output = run_command(
        [str(pip_path), "install", "--upgrade", "pip"],
        "Upgrading pip..."
    )
    if success:
        print_success("pip upgraded")

    # Install requirements
    success, output = run_command(
        [str(pip_path), "install", "-r", "requirements.txt"],
        "Installing requirements from requirements.txt..."
    )

    if not success:
        print_error("Failed to install some dependencies")
        print(output)
        print("\nYou may need to install them manually:")
        print(f"  {pip_path} install -r requirements.txt")
    else:
        print_success("All dependencies installed")

    # Step 4: Verify installation
    print_step("Step 4: Verifying installation")

    python_path = get_venv_python()

    # Check PySide6
    success, output = run_command(
        [str(python_path), "-c", "import PySide6; print(f'PySide6 version: {PySide6.__version__}')"],
        "Checking PySide6..."
    )
    if success:
        print_success(output.strip())
    else:
        print_error("PySide6 not installed correctly")

    # Check pytest
    success, output = run_command(
        [str(python_path), "-c", "import pytest; print(f'pytest version: {pytest.__version__}')"],
        "Checking pytest..."
    )
    if success:
        print_success(output.strip())
    else:
        print_error("pytest not installed correctly")

    # Check Jupyter
    success, output = run_command(
        [str(python_path), "-c", "import jupyter; print('Jupyter installed')"],
        "Checking Jupyter..."
    )
    if success:
        print_success("Jupyter installed")
    else:
        print_error("Jupyter not installed correctly")

    # Final instructions
    print_step("Setup Complete!")

    print("To activate the virtual environment:\n")

    if sys.platform == "win32":
        print("  Windows (Command Prompt):")
        print("    .venv\\Scripts\\activate")
        print("")
        print("  Windows (PowerShell):")
        print("    .venv\\Scripts\\Activate.ps1")
    else:
        print("  macOS / Linux:")
        print("    source .venv/bin/activate")

    print("\n" + "-"*60)
    print("\nNext steps:")
    print("  1. Activate the virtual environment (see above)")
    print("  2. Run the tests:")
    print("       pytest media_catalogue/tests/")
    print("  3. Start Jupyter to view the lessons:")
    print("       jupyter notebook lessons/")
    print("  4. Run the GUI application:")
    print("       python media_catalogue/run_gui.py")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
