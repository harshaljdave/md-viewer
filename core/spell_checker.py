"""
Spell checking with pyenchant
"""

import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import Qt

try:
    import enchant
    ENCHANT_AVAILABLE = True
except ImportError:
    ENCHANT_AVAILABLE = False


class SpellCheckHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for spell checking."""
    
    def __init__(self, document, language='en_US'):
        super().__init__(document)
        
        self.enabled = False
        self.spell_checker = None
        
        if ENCHANT_AVAILABLE:
            try:
                self.spell_checker = enchant.Dict(language)
                self.enabled = True
            except enchant.errors.DictNotFoundError:
                print(f"Dictionary for '{language}' not found. Spell checking disabled.")
                self.enabled = False
        
        # Format for spelling errors
        self.error_format = QTextCharFormat()
        self.error_format.setUnderlineColor(QColor("red"))
        self.error_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        
        # Patterns to skip (code blocks, URLs, etc.)
        self.skip_patterns = [
            r'`[^`]+`',  # Inline code
            r'```[\s\S]*?```',  # Code blocks
            r'http[s]?://\S+',  # URLs
            r'www\.\S+',  # www URLs
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',  # Emails
        ]
    
    def highlightBlock(self, text):
        """Highlight misspelled words in the block."""
        if not self.enabled or not self.spell_checker:
            return
        
        # Skip if in code block (basic check)
        if text.strip().startswith('```') or text.strip().startswith('    '):
            return
        
        # Word pattern
        word_pattern = re.compile(r'\b[a-zA-Z]+\b')
        
        for match in word_pattern.finditer(text):
            word = match.group()
            start = match.start()
            length = len(word)
            
            # Skip short words
            if length < 2:
                continue
            
            # Skip if in a pattern we should ignore
            skip = False
            for pattern in self.skip_patterns:
                if re.search(pattern, text[max(0, start-50):start+length+50]):
                    skip = True
                    break
            
            if skip:
                continue
            
            # Check spelling
            if not self.spell_checker.check(word):
                self.setFormat(start, length, self.error_format)
    
    def get_suggestions(self, word):
        """Get spelling suggestions for a word."""
        if not self.enabled or not self.spell_checker:
            return []
        
        return self.spell_checker.suggest(word)[:5]  # Return top 5 suggestions
    
    def add_to_dictionary(self, word):
        """Add a word to the personal dictionary."""
        if self.enabled and self.spell_checker:
            self.spell_checker.add(word)
    
    def set_enabled(self, enabled):
        """Enable or disable spell checking."""
        self.enabled = enabled and ENCHANT_AVAILABLE and self.spell_checker is not None
        self.rehighlight()
