#!/usr/bin/env python3
"""
Markdown Editor + Viewer
A feature-rich desktop markdown editor with live preview using PySide6
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Markdown Editor")
    app.setOrganizationName("MarkdownEditor")
    
    # Create and show main window
    window = MainWindow(app)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
