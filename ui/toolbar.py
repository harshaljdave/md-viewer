"""
Toolbar creation and formatting functions
"""

from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction, QTextCursor, QIcon
from PySide6.QtCore import Qt


class MarkdownToolbar:
    """Creates and manages the markdown formatting toolbar."""
    
    def __init__(self, main_window, editor):
        self.main_window = main_window
        self.editor = editor
        self.toolbar = None
    
    def create_toolbar(self):
        """Create the formatting toolbar."""
        self.toolbar = QToolBar("Formatting")
        self.toolbar.setMovable(False)
        
        # Bold
        bold_action = QAction("Bold", self.main_window)
        bold_action.setShortcut("Ctrl+B")
        bold_action.setToolTip("Bold (Ctrl+B)")
        bold_action.triggered.connect(lambda: self.wrap_text("**", "**"))
        self.toolbar.addAction(bold_action)
        
        # Italic
        italic_action = QAction("Italic", self.main_window)
        italic_action.setShortcut("Ctrl+I")
        italic_action.setToolTip("Italic (Ctrl+I)")
        italic_action.triggered.connect(lambda: self.wrap_text("*", "*"))
        self.toolbar.addAction(italic_action)
        
        # Strikethrough
        strike_action = QAction("Strike", self.main_window)
        strike_action.setToolTip("Strikethrough")
        strike_action.triggered.connect(lambda: self.wrap_text("~~", "~~"))
        self.toolbar.addAction(strike_action)
        
        # Code
        code_action = QAction("Code", self.main_window)
        code_action.setShortcut("Ctrl+`")
        code_action.setToolTip("Inline code (Ctrl+`)")
        code_action.triggered.connect(lambda: self.wrap_text("`", "`"))
        self.toolbar.addAction(code_action)
        
        self.toolbar.addSeparator()
        
        # Headings
        h1_action = QAction("H1", self.main_window)
        h1_action.setToolTip("Heading 1")
        h1_action.triggered.connect(lambda: self.insert_heading(1))
        self.toolbar.addAction(h1_action)
        
        h2_action = QAction("H2", self.main_window)
        h2_action.setToolTip("Heading 2")
        h2_action.triggered.connect(lambda: self.insert_heading(2))
        self.toolbar.addAction(h2_action)
        
        h3_action = QAction("H3", self.main_window)
        h3_action.setToolTip("Heading 3")
        h3_action.triggered.connect(lambda: self.insert_heading(3))
        self.toolbar.addAction(h3_action)
        
        self.toolbar.addSeparator()
        
        # Lists
        bullet_action = QAction("• List", self.main_window)
        bullet_action.setToolTip("Bullet list")
        bullet_action.triggered.connect(lambda: self.insert_list_item("-"))
        self.toolbar.addAction(bullet_action)
        
        numbered_action = QAction("1. List", self.main_window)
        numbered_action.setToolTip("Numbered list")
        numbered_action.triggered.connect(lambda: self.insert_list_item("1."))
        self.toolbar.addAction(numbered_action)
        
        todo_action = QAction("☐ Task", self.main_window)
        todo_action.setToolTip("Task list")
        todo_action.triggered.connect(lambda: self.insert_list_item("- [ ]"))
        self.toolbar.addAction(todo_action)
        
        self.toolbar.addSeparator()
        
        # Link
        link_action = QAction("Link", self.main_window)
        link_action.setShortcut("Ctrl+K")
        link_action.setToolTip("Insert link (Ctrl+K)")
        link_action.triggered.connect(self.insert_link)
        self.toolbar.addAction(link_action)
        
        # Image
        image_action = QAction("Image", self.main_window)
        image_action.setToolTip("Insert image")
        image_action.triggered.connect(self.insert_image)
        self.toolbar.addAction(image_action)
        
        self.toolbar.addSeparator()
        
        # Quote
        quote_action = QAction("Quote", self.main_window)
        quote_action.setToolTip("Blockquote")
        quote_action.triggered.connect(lambda: self.insert_at_line_start("> "))
        self.toolbar.addAction(quote_action)
        
        # Code block
        code_block_action = QAction("Code Block", self.main_window)
        code_block_action.setToolTip("Code block")
        code_block_action.triggered.connect(self.insert_code_block)
        self.toolbar.addAction(code_block_action)
        
        # Horizontal rule
        hr_action = QAction("HR", self.main_window)
        hr_action.setToolTip("Horizontal rule")
        hr_action.triggered.connect(lambda: self.insert_text("\n---\n"))
        self.toolbar.addAction(hr_action)
        
        return self.toolbar
    
    def wrap_text(self, prefix, suffix):
        """Wrap selected text or insert prefix/suffix at cursor."""
        cursor = self.editor.textCursor()
        
        if cursor.hasSelection():
            # Wrap selected text
            selected_text = cursor.selectedText()
            cursor.insertText(prefix + selected_text + suffix)
        else:
            # Insert prefix and suffix, position cursor between them
            cursor.insertText(prefix + suffix)
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, len(suffix))
            self.editor.setTextCursor(cursor)
    
    def insert_heading(self, level):
        """Insert heading marker at the beginning of line."""
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        
        # Check if line already starts with heading
        cursor.select(QTextCursor.LineUnderCursor)
        line_text = cursor.selectedText()
        
        # Remove existing heading markers
        line_text = line_text.lstrip('#').lstrip()
        
        # Insert new heading
        heading_prefix = '#' * level + ' '
        cursor.insertText(heading_prefix + line_text)
    
    def insert_list_item(self, marker):
        """Insert list marker at the beginning of line."""
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.insertText(marker + " ")
    
    def insert_at_line_start(self, text):
        """Insert text at the start of current line."""
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.insertText(text)
    
    def insert_link(self):
        """Insert markdown link."""
        cursor = self.editor.textCursor()
        
        if cursor.hasSelection():
            # Use selection as link text
            text = cursor.selectedText()
            cursor.insertText(f"[{text}](url)")
            # Select "url" for easy replacement
            for _ in range(4):
                cursor.movePosition(QTextCursor.Left)
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 3)
        else:
            # Insert template
            cursor.insertText("[text](url)")
            # Select "text"
            for _ in range(6):
                cursor.movePosition(QTextCursor.Left)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 4)
        
        self.editor.setTextCursor(cursor)
    
    def insert_image(self):
        """Insert markdown image."""
        cursor = self.editor.textCursor()
        
        if cursor.hasSelection():
            # Use selection as alt text
            text = cursor.selectedText()
            cursor.insertText(f"![{text}](url)")
            # Select "url" for easy replacement
            for _ in range(4):
                cursor.movePosition(QTextCursor.Left)
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 3)
        else:
            # Insert template
            cursor.insertText("![alt text](url)")
            # Select "alt text"
            for _ in range(5):
                cursor.movePosition(QTextCursor.Left)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 8)
        
        self.editor.setTextCursor(cursor)
    
    def insert_code_block(self):
        """Insert code block."""
        cursor = self.editor.textCursor()
        
        if cursor.hasSelection():
            # Wrap selection in code block
            text = cursor.selectedText().replace('\u2029', '\n')
            cursor.insertText(f"```\n{text}\n```")
        else:
            # Insert empty code block
            cursor.insertText("```\n\n```")
            cursor.movePosition(QTextCursor.Up)
            self.editor.setTextCursor(cursor)
    
    def insert_text(self, text):
        """Insert text at cursor position."""
        cursor = self.editor.textCursor()
        cursor.insertText(text)
