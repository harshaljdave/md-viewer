"""
Theme management for light/dark mode
"""

from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt, QSettings


class ThemeManager:
    """Manages application themes (light/dark mode)."""
    
    def __init__(self, app):
        self.app = app
        self.settings = QSettings("MarkdownEditor", "Preferences")
        self.current_theme = self.settings.value("ui_theme", "light")
        
        # Create palettes
        self.light_palette = self._create_light_palette()
        self.dark_palette = self._create_dark_palette()
    
    def _create_light_palette(self):
        """Create light theme palette."""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(0, 102, 204))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        return palette
    
    def _create_dark_palette(self):
        """Create dark theme palette."""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        return palette
    
    def apply_theme(self, theme_name):
        """
        Apply a theme to the application.
        
        Args:
            theme_name: 'light' or 'dark'
        """
        self.current_theme = theme_name
        
        if theme_name == 'dark':
            self.app.setPalette(self.dark_palette)
        else:
            self.app.setPalette(self.light_palette)
        
        # Save preference
        self.settings.setValue("ui_theme", theme_name)
    
    def get_current_theme(self):
        """Get current theme name."""
        return self.current_theme
    
    def is_dark_mode(self):
        """Check if dark mode is active."""
        return self.current_theme == 'dark'
    
    def get_preview_theme_name(self):
        """Get appropriate preview theme name based on UI theme."""
        return 'github-dark' if self.is_dark_mode() else 'github-light'
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme(new_theme)
        return new_theme
