"""Build script for creating Windows executable using PyInstaller."""
import PyInstaller.__main__
import os
import sys

# Configuration
APP_NAME = "TaskScheduler"
MAIN_SCRIPT = "src/main.py"
ICON_PATH = None  # Optional: path to .ico file

# PyInstaller arguments
args = [
    MAIN_SCRIPT,
    '--name', APP_NAME,
    '--onefile',  # Create a single executable
    '--windowed',  # No console window (GUI app)
    '--clean',  # Clean cache before building
    '--noconfirm',  # Overwrite output without asking
]

# Add icon if provided
if ICON_PATH and os.path.exists(ICON_PATH):
    args.extend(['--icon', ICON_PATH])

# Note: Data directory will be created next to executable on first run
# No need to bundle it - it's created dynamically

# Run PyInstaller
PyInstaller.__main__.run(args)

print(f"\nBuild complete! Executable is in the 'dist' folder: {APP_NAME}.exe")
