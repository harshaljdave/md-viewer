#!/usr/bin/env python3
"""
Simple Markdown Editor + Viewer
A desktop markdown editor with live preview using PySide6
"""

import sys
import os
import hashlib
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSplitter,
    QTextEdit, QVBoxLayout, QFileDialog, QMessageBox
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QFont, QAction

import markdown
from pygments.formatters import HtmlFormatter


class MarkdownEditor(QMainWindow):
    """Main application window for the markdown editor."""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.is_modified = False
        self.last_hash = None
        
        # Initialize markdown processor with extensions
        self.md = markdown.Markdown(
            extensions=['extra', 'codehilite', 'toc', 'sane_lists', 'smarty'],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'guess_lang': False,  # Performance optimization
                    'use_pygments': True,
                    'noclasses': False
                }
            }
        )
        
        # Generate CSS for syntax highlighting (cache it)
        self.syntax_css = HtmlFormatter(style='monokai').get_style_defs('.highlight')
        
        # Setup debounce timer for preview updates
        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.setInterval(300)  # 300ms delay
        self.preview_timer.timeout.connect(self.update_preview)
        
        self.init_ui()
        self.update_title()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Markdown Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create horizontal splitter for editor and preview
        splitter = QSplitter(Qt.Horizontal)
        
        # Create editor (left pane)
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Enter your markdown here...")
        self.editor.setFont(QFont("Monospace", 11))
        self.editor.textChanged.connect(self.on_text_changed)
        
        # Create preview (right pane)
        self.preview = QWebEngineView()
        
        # Add widgets to splitter
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)
        
        # Set initial splitter sizes (50/50 split)
        splitter.setSizes([600, 600])
        
        layout.addWidget(splitter)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Initial preview update
        self.update_preview()
    
    def create_menu_bar(self):
        """Create the menu bar with File menu."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # New action
        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        # Open action
        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Save action
        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # Save As action
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def on_text_changed(self):
        """Handle text changes in the editor."""
        self.is_modified = True
        self.update_title()
        # Restart debounce timer
        self.preview_timer.start()
    
    def update_preview(self):
        """Update the preview pane with rendered markdown."""
        text = self.editor.toPlainText()
        
        # Hash check for caching - skip if content unchanged
        text_hash = hashlib.md5(text.encode()).hexdigest()
        if text_hash == self.last_hash:
            return
        
        self.last_hash = text_hash
        
        # Convert markdown to HTML
        html_body = self.md.convert(text)
        self.md.reset()  # Important: reset for next conversion
        
        # Wrap in full HTML with CSS
        full_html = self.wrap_with_style(html_body)
        
        # Set base URL for relative paths (if file is open)
        if self.current_file:
            base_url = QUrl.fromLocalFile(str(Path(self.current_file).parent) + os.sep)
        else:
            base_url = QUrl()
        
        self.preview.setHtml(full_html, base_url)
    
    def wrap_with_style(self, content):
        """Wrap HTML content with CSS styling."""
        return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{self.syntax_css}

body {{
    margin: 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 900px;
}}

h1, h2, h3, h4, h5, h6 {{
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
}}

h1 {{ font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
h2 {{ font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
h3 {{ font-size: 1.25em; }}

code {{
    background: #f6f8fa;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: "Monaco", "Menlo", "Consolas", monospace;
    font-size: 0.9em;
}}

pre {{
    background: #272822;
    padding: 16px;
    border-radius: 6px;
    overflow-x: auto;
    line-height: 1.45;
}}

pre code {{
    background: transparent;
    padding: 0;
}}

blockquote {{
    border-left: 4px solid #dfe2e5;
    padding-left: 16px;
    color: #6a737d;
    margin: 0;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
}}

table th, table td {{
    border: 1px solid #dfe2e5;
    padding: 8px 13px;
}}

table th {{
    background: #f6f8fa;
    font-weight: 600;
}}

a {{
    color: #0366d6;
    text-decoration: none;
}}

a:hover {{
    text-decoration: underline;
}}

img {{
    max-width: 100%;
    height: auto;
}}

hr {{
    border: 0;
    border-top: 2px solid #eaecef;
    margin: 24px 0;
}}
</style>
</head>
<body>
{content}
</body>
</html>'''
    
    def new_file(self):
        """Create a new file."""
        if not self.check_save_changes():
            return
        
        self.editor.clear()
        self.current_file = None
        self.is_modified = False
        self.update_title()
    
    def open_file(self):
        """Open a markdown file."""
        if not self.check_save_changes():
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            "",
            "Markdown Files (*.md *.markdown *.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.editor.setPlainText(content)
                self.current_file = file_path
                self.is_modified = False
                self.update_title()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Could not open file:\n{str(e)}"
                )
    
    def save_file(self):
        """Save the current file."""
        if self.current_file:
            return self.save_to_file(self.current_file)
        else:
            return self.save_file_as()
    
    def save_file_as(self):
        """Save the current file with a new name."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Markdown File",
            "",
            "Markdown Files (*.md);;All Files (*)"
        )
        
        if file_path:
            return self.save_to_file(file_path)
        return False
    
    def save_to_file(self, file_path):
        """Save content to the specified file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            
            self.current_file = file_path
            self.is_modified = False
            self.update_title()
            return True
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not save file:\n{str(e)}"
            )
            return False
    
    def check_save_changes(self):
        """Check if there are unsaved changes and prompt user."""
        if not self.is_modified:
            return True
        
        reply = QMessageBox.question(
            self,
            "Unsaved Changes",
            "You have unsaved changes. Do you want to save them?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Save
        )
        
        if reply == QMessageBox.Save:
            return self.save_file()
        elif reply == QMessageBox.Discard:
            return True
        else:
            return False
    
    def update_title(self):
        """Update the window title."""
        if self.current_file:
            filename = Path(self.current_file).name
        else:
            filename = "Untitled"
        
        modified_marker = " *" if self.is_modified else ""
        self.setWindowTitle(f"{filename}{modified_marker} - Markdown Editor")
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.check_save_changes():
            event.accept()
        else:
            event.ignore()


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Markdown Editor")
    
    editor = MarkdownEditor()
    editor.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
