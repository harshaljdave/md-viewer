"""
Find and Replace dialog
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QCheckBox, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument, QTextCursor


class FindReplaceDialog(QDialog):
    """Modeless dialog for find and replace operations."""
    
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.last_position = 0
        
        self.setWindowTitle("Find and Replace")
        self.setModal(False)  # Modeless dialog
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Find input
        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        self.find_input.returnPressed.connect(self.find_next)
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)
        
        # Replace input
        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        self.replace_input.returnPressed.connect(self.replace_current)
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)
        
        # Options
        options_layout = QHBoxLayout()
        self.case_sensitive = QCheckBox("Case sensitive")
        self.whole_word = QCheckBox("Whole words")
        self.use_regex = QCheckBox("Regular expression")
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_word)
        options_layout.addWidget(self.use_regex)
        layout.addLayout(options_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        find_next_btn = QPushButton("Find Next")
        find_next_btn.clicked.connect(self.find_next)
        buttons_layout.addWidget(find_next_btn)
        
        find_prev_btn = QPushButton("Find Previous")
        find_prev_btn.clicked.connect(self.find_previous)
        buttons_layout.addWidget(find_prev_btn)
        
        replace_btn = QPushButton("Replace")
        replace_btn.clicked.connect(self.replace_current)
        buttons_layout.addWidget(replace_btn)
        
        replace_all_btn = QPushButton("Replace All")
        replace_all_btn.clicked.connect(self.replace_all)
        buttons_layout.addWidget(replace_all_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
    
    def get_find_flags(self):
        """Get search flags based on options."""
        flags = QTextDocument.FindFlags()
        
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        
        if self.whole_word.isChecked():
            flags |= QTextDocument.FindWholeWords
        
        return flags
    
    def find_next(self):
        """Find next occurrence."""
        search_text = self.find_input.text()
        
        if not search_text:
            self.status_label.setText("Please enter text to find")
            return
        
        flags = self.get_find_flags()
        
        if self.use_regex.isChecked():
            # Use regex search
            from PySide6.QtCore import QRegularExpression
            regex = QRegularExpression(search_text)
            if not self.case_sensitive.isChecked():
                regex.setPatternOptions(QRegularExpression.CaseInsensitiveOption)
            
            found = self.editor.find(regex, flags)
        else:
            found = self.editor.find(search_text, flags)
        
        if not found:
            # Wrap around to beginning
            cursor = self.editor.textCursor()
            cursor.movePosition(QTextCursor.Start)
            self.editor.setTextCursor(cursor)
            
            if self.use_regex.isChecked():
                from PySide6.QtCore import QRegularExpression
                regex = QRegularExpression(search_text)
                if not self.case_sensitive.isChecked():
                    regex.setPatternOptions(QRegularExpression.CaseInsensitiveOption)
                found = self.editor.find(regex, flags)
            else:
                found = self.editor.find(search_text, flags)
            
            if found:
                self.status_label.setText("Wrapped to beginning")
            else:
                self.status_label.setText("Not found")
        else:
            self.status_label.setText("")
    
    def find_previous(self):
        """Find previous occurrence."""
        search_text = self.find_input.text()
        
        if not search_text:
            self.status_label.setText("Please enter text to find")
            return
        
        flags = self.get_find_flags()
        flags |= QTextDocument.FindBackward
        
        if self.use_regex.isChecked():
            from PySide6.QtCore import QRegularExpression
            regex = QRegularExpression(search_text)
            if not self.case_sensitive.isChecked():
                regex.setPatternOptions(QRegularExpression.CaseInsensitiveOption)
            found = self.editor.find(regex, flags)
        else:
            found = self.editor.find(search_text, flags)
        
        if not found:
            # Wrap around to end
            cursor = self.editor.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.editor.setTextCursor(cursor)
            
            if self.use_regex.isChecked():
                from PySide6.QtCore import QRegularExpression
                regex = QRegularExpression(search_text)
                if not self.case_sensitive.isChecked():
                    regex.setPatternOptions(QRegularExpression.CaseInsensitiveOption)
                found = self.editor.find(regex, flags)
            else:
                found = self.editor.find(search_text, flags)
            
            if found:
                self.status_label.setText("Wrapped to end")
            else:
                self.status_label.setText("Not found")
        else:
            self.status_label.setText("")
    
    def replace_current(self):
        """Replace current selection."""
        cursor = self.editor.textCursor()
        
        if cursor.hasSelection():
            cursor.insertText(self.replace_input.text())
            self.status_label.setText("Replaced")
            # Find next occurrence
            self.find_next()
        else:
            self.status_label.setText("No selection. Use Find Next first.")
    
    def replace_all(self):
        """Replace all occurrences."""
        search_text = self.find_input.text()
        replace_text = self.replace_input.text()
        
        if not search_text:
            self.status_label.setText("Please enter text to find")
            return
        
        # Confirm with user
        reply = QMessageBox.question(
            self,
            "Replace All",
            f"Replace all occurrences of '{search_text}' with '{replace_text}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Move to beginning
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()  # Single undo operation
        cursor.movePosition(QTextCursor.Start)
        self.editor.setTextCursor(cursor)
        
        count = 0
        flags = self.get_find_flags()
        
        # Replace all
        while True:
            if self.use_regex.isChecked():
                from PySide6.QtCore import QRegularExpression
                regex = QRegularExpression(search_text)
                if not self.case_sensitive.isChecked():
                    regex.setPatternOptions(QRegularExpression.CaseInsensitiveOption)
                found = self.editor.find(regex, flags)
            else:
                found = self.editor.find(search_text, flags)
            
            if not found:
                break
            
            self.editor.textCursor().insertText(replace_text)
            count += 1
        
        cursor.endEditBlock()
        
        self.status_label.setText(f"Replaced {count} occurrence(s)")
    
    def showEvent(self, event):
        """When dialog is shown, focus the find input."""
        super().showEvent(event)
        self.find_input.setFocus()
        self.find_input.selectAll()
