"""
Main window with all features integrated
"""

import os
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QTextEdit, QVBoxLayout,
    QFileDialog, QMessageBox, QLabel, QMenu, QInputDialog
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QFont, QAction, QTextCursor, QActionGroup

from core.markdown_processor import MarkdownProcessor
from core.theme_manager import ThemeManager
from core.spell_checker import SpellCheckHighlighter, ENCHANT_AVAILABLE
from utils.file_manager import FileManager
from utils.statistics import Statistics
from ui.find_replace_dialog import FindReplaceDialog
from ui.toolbar import MarkdownToolbar
from themes.css_themes import get_theme_names


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, app):
        super().__init__()
        
        # Core components
        self.app = app
        self.current_file = None
        self.is_modified = False
        
        # Managers
        self.theme_manager = ThemeManager(app)
        self.file_manager = FileManager()
        self.markdown_processor = MarkdownProcessor()
        self.statistics = Statistics()
        
        # Dialogs (lazy loading)
        self._find_dialog = None
        
        # Spell checker
        self.spell_checker = None
        self.spell_check_enabled = False
        
        # Synchronized scrolling
        self.sync_scroll_enabled = False
        
        # Preview update timer (debouncing)
        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.setInterval(300)
        self.preview_timer.timeout.connect(self.update_preview)
        
        # Auto-save timer
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.autosave)
        autosave_interval = self.file_manager.get_autosave_interval() * 1000
        self.autosave_timer.start(autosave_interval)
        
        # Initialize UI
        self.init_ui()
        
        # Apply saved theme
        self.theme_manager.apply_theme(self.theme_manager.get_current_theme())
        self.update_preview_theme()
        
        # Cleanup old autosaves
        self.file_manager.cleanup_old_autosaves()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Markdown Editor")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Create editor (left pane)
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Enter your markdown here...")
        self.editor.setFont(QFont("Monospace", 11))
        self.editor.textChanged.connect(self.on_text_changed)
        
        # Create preview (right pane)
        self.preview = QWebEngineView()
        self._configure_webengine()
        
        # Add widgets to splitter
        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.preview)
        
        # Set initial sizes (50/50 split)
        self.splitter.setSizes([700, 700])
        
        layout.addWidget(self.splitter)
        
        # Create menus and toolbar
        self.create_menu_bar()
        self.create_toolbar()
        
        # Create status bar
        self.create_status_bar()
        
        # Initial preview
        self.update_preview()
    
    def _configure_webengine(self):
        """Configure QWebEngineView settings for better performance and security."""
        settings = self.preview.settings()
        # Performance settings
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        
        # SECURITY: Disable potentially dangerous features
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, False)
        settings.setAttribute(QWebEngineSettings.AllowGeolocationOnInsecureOrigins, False)
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Recent files submenu
        self.recent_menu = file_menu.addMenu("Recent Files")
        self.update_recent_files_menu()
        
        file_menu.addSeparator()
        
        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Export submenu
        export_menu = file_menu.addMenu("Export")
        
        export_html_action = QAction("Export as HTML...", self)
        export_html_action.triggered.connect(self.export_html)
        export_menu.addAction(export_html_action)
        
        export_pdf_action = QAction("Export as PDF...", self)
        export_pdf_action.triggered.connect(self.export_pdf)
        export_menu.addAction(export_pdf_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        find_action = QAction("&Find and Replace", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.show_find_dialog)
        edit_menu.addAction(find_action)
        
        edit_menu.addSeparator()
        
        # Spell check toggle
        if ENCHANT_AVAILABLE:
            self.spell_check_action = QAction("Enable &Spell Check", self)
            self.spell_check_action.setCheckable(True)
            self.spell_check_action.triggered.connect(self.toggle_spell_check)
            edit_menu.addAction(self.spell_check_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        # Theme submenu
        theme_menu = view_menu.addMenu("UI Theme")
        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)
        
        light_theme_action = QAction("Light", self, checkable=True)
        light_theme_action.setChecked(not self.theme_manager.is_dark_mode())
        light_theme_action.triggered.connect(lambda: self.change_ui_theme('light'))
        theme_group.addAction(light_theme_action)
        theme_menu.addAction(light_theme_action)
        
        dark_theme_action = QAction("Dark", self, checkable=True)
        dark_theme_action.setChecked(self.theme_manager.is_dark_mode())
        dark_theme_action.triggered.connect(lambda: self.change_ui_theme('dark'))
        theme_group.addAction(dark_theme_action)
        theme_menu.addAction(dark_theme_action)
        
        # Preview theme submenu
        preview_theme_menu = view_menu.addMenu("Preview Theme")
        preview_theme_group = QActionGroup(self)
        preview_theme_group.setExclusive(True)
        
        for theme_name in get_theme_names():
            action = QAction(theme_name.replace('-', ' ').title(), self, checkable=True)
            action.setData(theme_name)
            if theme_name == 'github-light':
                action.setChecked(True)
            action.triggered.connect(lambda checked, tn=theme_name: self.change_preview_theme(tn))
            preview_theme_group.addAction(action)
            preview_theme_menu.addAction(action)
        
        view_menu.addSeparator()
        
        # Split mode submenu
        split_menu = view_menu.addMenu("Split Mode")
        split_group = QActionGroup(self)
        split_group.setExclusive(True)
        
        horizontal_action = QAction("Horizontal", self, checkable=True)
        horizontal_action.setChecked(True)
        horizontal_action.triggered.connect(self.set_horizontal_split)
        split_group.addAction(horizontal_action)
        split_menu.addAction(horizontal_action)
        
        vertical_action = QAction("Vertical", self, checkable=True)
        vertical_action.triggered.connect(self.set_vertical_split)
        split_group.addAction(vertical_action)
        split_menu.addAction(vertical_action)
        
        split_menu.addSeparator()
        
        # View mode
        view_mode_group = QActionGroup(self)
        view_mode_group.setExclusive(True)
        
        both_action = QAction("Both Panes", self, checkable=True)
        both_action.setChecked(True)
        both_action.triggered.connect(lambda: self.set_view_mode('both'))
        view_mode_group.addAction(both_action)
        split_menu.addAction(both_action)
        
        editor_only_action = QAction("Editor Only", self, checkable=True)
        editor_only_action.setShortcut("F11")
        editor_only_action.triggered.connect(lambda: self.set_view_mode('editor'))
        view_mode_group.addAction(editor_only_action)
        split_menu.addAction(editor_only_action)
        
        preview_only_action = QAction("Preview Only", self, checkable=True)
        preview_only_action.setShortcut("F12")
        preview_only_action.triggered.connect(lambda: self.set_view_mode('preview'))
        view_mode_group.addAction(preview_only_action)
        split_menu.addAction(preview_only_action)
        
        view_menu.addSeparator()
        
        # Synchronized scrolling
        self.sync_scroll_action = QAction("Synchronized Scrolling", self)
        self.sync_scroll_action.setCheckable(True)
        self.sync_scroll_action.triggered.connect(self.toggle_sync_scroll)
        view_menu.addAction(self.sync_scroll_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        stats_action = QAction("Show &Statistics", self)
        stats_action.setShortcut("Ctrl+Shift+S")
        stats_action.triggered.connect(self.show_statistics_dialog)
        tools_menu.addAction(stats_action)
    
    def create_toolbar(self):
        """Create the toolbar."""
        toolbar_manager = MarkdownToolbar(self, self.editor)
        toolbar = toolbar_manager.create_toolbar()
        self.addToolBar(toolbar)
    
    def create_status_bar(self):
        """Create the status bar."""
        self.stats_label = QLabel()
        self.statusBar().addPermanentWidget(self.stats_label)
        self.update_statistics()
    
    # File operations
    
    def new_file(self):
        """Create a new file."""
        if not self.check_save_changes():
            return
        
        self.editor.clear()
        self.current_file = None
        self.is_modified = False
        self.update_title()
    
    def open_file(self):
        """Open a file."""
        if not self.check_save_changes():
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            "",
            "Markdown Files (*.md *.markdown *.txt);;All Files (*)"
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """Load a file into the editor."""
        try:
            # SECURITY: Validate file path
            file_path = os.path.abspath(file_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not os.path.isfile(file_path):
                raise ValueError(f"Not a file: {file_path}")
            
            # SECURITY: Check file size (10MB limit)
            file_size = os.path.getsize(file_path)
            max_size = 10 * 1024 * 1024  # 10MB
            
            if file_size > max_size:
                reply = QMessageBox.question(
                    self,
                    "Large File Warning",
                    f"File is {file_size / 1024 / 1024:.1f}MB. Opening large files may be slow.\nContinue?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply != QMessageBox.Yes:
                    return
            
            # Check for autosave
            autosave_content, autosave_path = self.file_manager.load_autosave(file_path)
            
            if autosave_content:
                reply = QMessageBox.question(
                    self,
                    "Autosave Found",
                    "An autosave file was found. Do you want to recover it?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )
                
                if reply == QMessageBox.Yes:
                    content = autosave_content
                    self.file_manager.delete_autosave(file_path)
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            self.editor.setPlainText(content)
            self.current_file = file_path
            self.is_modified = False
            self.update_title()
            
            # Add to recent files
            self.file_manager.add_recent_file(file_path)
            self.update_recent_files_menu()
            
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
        """Save the file with a new name."""
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
        """Save content to a file."""
        try:
            # SECURITY: Validate file path
            file_path = os.path.abspath(file_path)
            
            # Ensure parent directory exists
            parent_dir = os.path.dirname(file_path)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            
            self.current_file = file_path
            self.is_modified = False
            self.update_title()
            
            # Delete autosave
            self.file_manager.delete_autosave(file_path)
            
            # Add to recent files
            self.file_manager.add_recent_file(file_path)
            self.update_recent_files_menu()
            
            return True
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not save file:\n{str(e)}"
            )
            return False
    
    def check_save_changes(self):
        """Check for unsaved changes."""
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
    
    # Export functions
    
    def export_html(self):
        """Export as HTML file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export HTML",
            "",
            "HTML Files (*.html);;All Files (*)"
        )
        
        if file_path:
            try:
                text = self.editor.toPlainText()
                html = self.markdown_processor.convert(text, force=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                
                QMessageBox.information(self, "Success", "HTML exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed:\n{str(e)}")
    
    def export_pdf(self):
        """Export as PDF file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export PDF",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if file_path:
            # Use QWebEngineView's printToPdf
            self.preview.page().printToPdf(file_path)
            QMessageBox.information(self, "Success", f"PDF exported to:\n{file_path}")
    
    # Recent files
    
    def update_recent_files_menu(self):
        """Update the recent files menu."""
        self.recent_menu.clear()
        
        recent_files = self.file_manager.get_recent_files()
        
        if recent_files:
            for i, filepath in enumerate(recent_files):
                if i < 9:  # Limit to 9 files with shortcuts
                    filename = os.path.basename(filepath)
                    action = QAction(f"&{i+1}. {filename}", self)
                    action.setData(filepath)
                    action.triggered.connect(lambda checked, f=filepath: self.load_file(f))
                    self.recent_menu.addAction(action)
            
            self.recent_menu.addSeparator()
            
            clear_action = QAction("Clear Recent Files", self)
            clear_action.triggered.connect(self.clear_recent_files)
            self.recent_menu.addAction(clear_action)
        else:
            no_files_action = QAction("No recent files", self)
            no_files_action.setEnabled(False)
            self.recent_menu.addAction(no_files_action)
    
    def clear_recent_files(self):
        """Clear recent files list."""
        self.file_manager.clear_recent_files()
        self.update_recent_files_menu()
    
    # Auto-save
    
    def autosave(self):
        """Auto-save the current document."""
        if not self.is_modified or not self.file_manager.is_autosave_enabled():
            return
        
        content = self.editor.toPlainText()
        self.file_manager.save_autosave(content, self.current_file)
    
    # Preview updates
    
    def on_text_changed(self):
        """Handle text changes."""
        self.is_modified = True
        self.update_title()
        self.update_statistics()
        
        # Restart debounce timer
        self.preview_timer.start()
    
    def update_preview(self):
        """Update the preview pane."""
        text = self.editor.toPlainText()
        html = self.markdown_processor.convert(text)
        
        # Set base URL for relative paths
        if self.current_file:
            base_url = QUrl.fromLocalFile(str(Path(self.current_file).parent) + os.sep)
        else:
            base_url = QUrl()
        
        self.preview.setHtml(html, base_url)
    
    def update_preview_theme(self):
        """Update preview theme based on UI theme."""
        theme_name = self.theme_manager.get_preview_theme_name()
        self.markdown_processor.set_theme(theme_name)
        self.update_preview()
    
    # Theme management
    
    def change_ui_theme(self, theme_name):
        """Change the UI theme."""
        self.theme_manager.apply_theme(theme_name)
        self.update_preview_theme()
    
    def change_preview_theme(self, theme_name):
        """Change the preview theme."""
        self.markdown_processor.set_theme(theme_name)
        self.update_preview()
    
    # Statistics
    
    def update_statistics(self):
        """Update statistics in status bar."""
        text = self.editor.toPlainText()
        self.statistics.update_text(text)
        stats_text = self.statistics.format_stats(compact=True)
        self.stats_label.setText(stats_text)
    
    def show_statistics_dialog(self):
        """Show detailed statistics dialog."""
        text = self.editor.toPlainText()
        self.statistics.update_text(text)
        stats_text = self.statistics.format_stats(compact=False)
        
        QMessageBox.information(self, "Document Statistics", stats_text)
    
    # Find and replace
    
    def show_find_dialog(self):
        """Show the find and replace dialog."""
        if self._find_dialog is None:
            self._find_dialog = FindReplaceDialog(self.editor, self)
        
        self._find_dialog.show()
        self._find_dialog.raise_()
        self._find_dialog.activateWindow()
    
    # Spell checking
    
    def toggle_spell_check(self):
        """Toggle spell checking."""
        self.spell_check_enabled = not self.spell_check_enabled
        
        if self.spell_check_enabled:
            if self.spell_checker is None:
                self.spell_checker = SpellCheckHighlighter(self.editor.document())
            self.spell_checker.set_enabled(True)
        else:
            if self.spell_checker:
                self.spell_checker.set_enabled(False)
    
    def contextMenuEvent(self, event):
        """Handle context menu for spell checking suggestions."""
        if self.spell_check_enabled and self.spell_checker:
            cursor = self.editor.cursorForPosition(event.pos())
            cursor.select(QTextCursor.WordUnderCursor)
            word = cursor.selectedText()
            
            menu = self.editor.createStandardContextMenu()
            
            if word and not self.spell_checker.spell_checker.check(word):
                suggestions = self.spell_checker.get_suggestions(word)
                
                if suggestions:
                    menu.insertSeparator(menu.actions()[0])
                    for suggestion in suggestions:
                        action = menu.insertAction(
                            menu.actions()[0],
                            QAction(suggestion, self)
                        )
                        action.triggered.connect(
                            lambda checked, s=suggestion, c=cursor: self.replace_word(c, s)
                        )
                    menu.insertSeparator(menu.actions()[0])
            
            menu.exec(event.globalPos())
        else:
            super().contextMenuEvent(event)
    
    def replace_word(self, cursor, word):
        """Replace a word at the cursor position."""
        self.editor.setTextCursor(cursor)
        cursor.insertText(word)
    
    # View modes
    
    def set_horizontal_split(self):
        """Set horizontal split mode."""
        self.splitter.setOrientation(Qt.Horizontal)
    
    def set_vertical_split(self):
        """Set vertical split mode."""
        self.splitter.setOrientation(Qt.Vertical)
    
    def set_view_mode(self, mode):
        """Set view mode."""
        if mode == 'editor':
            self.editor.show()
            self.preview.hide()
        elif mode == 'preview':
            self.editor.hide()
            self.preview.show()
        else:  # both
            self.editor.show()
            self.preview.show()
    
    # Synchronized scrolling
    
    def toggle_sync_scroll(self):
        """Toggle synchronized scrolling."""
        self.sync_scroll_enabled = not self.sync_scroll_enabled
        
        if self.sync_scroll_enabled:
            self.editor.verticalScrollBar().valueChanged.connect(self.sync_scroll)
        else:
            try:
                self.editor.verticalScrollBar().valueChanged.disconnect(self.sync_scroll)
            except:
                pass
    
    def sync_scroll(self):
        """Synchronize preview scroll with editor scroll."""
        if not self.sync_scroll_enabled:
            return
        
        scrollbar = self.editor.verticalScrollBar()
        if scrollbar.maximum() > 0:
            percent = scrollbar.value() / scrollbar.maximum()
            script = f"window.scrollTo(0, document.body.scrollHeight * {percent});"
            self.preview.page().runJavaScript(script)
    
    # Window management
    
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
            # Stop timers
            self.preview_timer.stop()
            self.autosave_timer.stop()
            
            # Clear preview
            self.preview.setHtml("")
            
            event.accept()
        else:
            event.ignore()
