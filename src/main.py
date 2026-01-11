"""Main entry point for the Task Scheduler application."""
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


def main():
    """Launch the application."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Task Scheduler")
    app.setOrganizationName("TaskScheduler")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
