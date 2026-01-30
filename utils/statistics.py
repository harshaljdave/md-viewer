"""
Text statistics calculation
"""

import re


class Statistics:
    """Calculate statistics for text documents."""
    
    def __init__(self, text=""):
        self.text = text
        self._cache = {}
    
    def update_text(self, text):
        """Update text and clear cache."""
        if text != self.text:
            self.text = text
            self._cache = {}
    
    def get_character_count(self, include_spaces=True):
        """Get character count."""
        if 'chars' not in self._cache:
            self._cache['chars'] = len(self.text)
            self._cache['chars_no_spaces'] = len(self.text.replace(' ', '').replace('\n', '').replace('\t', ''))
        
        return self._cache['chars'] if include_spaces else self._cache['chars_no_spaces']
    
    def get_word_count(self):
        """Get word count."""
        if 'words' not in self._cache:
            # Find all words (Unicode-aware)
            words = re.findall(r'\b\w+\b', self.text)
            self._cache['words'] = len(words)
        
        return self._cache['words']
    
    def get_line_count(self):
        """Get line count."""
        if 'lines' not in self._cache:
            self._cache['lines'] = self.text.count('\n') + 1 if self.text else 0
        
        return self._cache['lines']
    
    def get_paragraph_count(self):
        """Get paragraph count (non-empty blocks)."""
        if 'paragraphs' not in self._cache:
            paragraphs = [p for p in self.text.split('\n\n') if p.strip()]
            self._cache['paragraphs'] = len(paragraphs)
        
        return self._cache['paragraphs']
    
    def get_sentence_count(self):
        """Get sentence count."""
        if 'sentences' not in self._cache:
            # Simple sentence detection
            sentences = re.findall(r'[.!?]+', self.text)
            self._cache['sentences'] = len(sentences)
        
        return self._cache['sentences']
    
    def get_reading_time(self, words_per_minute=200):
        """
        Calculate estimated reading time.
        
        Args:
            words_per_minute: Average reading speed (default: 200 wpm)
            
        Returns:
            Reading time in minutes
        """
        word_count = self.get_word_count()
        return max(1, word_count // words_per_minute)
    
    def get_markdown_stats(self):
        """Get markdown-specific statistics."""
        if 'markdown' not in self._cache:
            stats = {
                'headings': len(re.findall(r'^#{1,6}\s', self.text, re.MULTILINE)),
                'links': len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', self.text)),
                'images': len(re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', self.text)),
                'code_blocks': len(re.findall(r'```', self.text)) // 2,
                'lists': len(re.findall(r'^[\*\-\+]\s', self.text, re.MULTILINE)),
            }
            self._cache['markdown'] = stats
        
        return self._cache['markdown']
    
    def get_all_stats(self):
        """Get all statistics as a dictionary."""
        return {
            'characters': self.get_character_count(include_spaces=True),
            'characters_no_spaces': self.get_character_count(include_spaces=False),
            'words': self.get_word_count(),
            'lines': self.get_line_count(),
            'paragraphs': self.get_paragraph_count(),
            'sentences': self.get_sentence_count(),
            'reading_time': self.get_reading_time(),
            'markdown': self.get_markdown_stats()
        }
    
    def format_stats(self, compact=True):
        """
        Format statistics as a string.
        
        Args:
            compact: If True, return compact single-line format
            
        Returns:
            Formatted statistics string
        """
        stats = self.get_all_stats()
        
        if compact:
            return (f"Words: {stats['words']} | "
                   f"Chars: {stats['characters']} | "
                   f"Lines: {stats['lines']} | "
                   f"Reading time: {stats['reading_time']} min")
        else:
            md_stats = stats['markdown']
            return f"""Statistics:
Words: {stats['words']}
Characters: {stats['characters']} ({stats['characters_no_spaces']} without spaces)
Lines: {stats['lines']}
Paragraphs: {stats['paragraphs']}
Sentences: {stats['sentences']}
Reading time: {stats['reading_time']} minutes

Markdown Elements:
Headings: {md_stats['headings']}
Links: {md_stats['links']}
Images: {md_stats['images']}
Code blocks: {md_stats['code_blocks']}
List items: {md_stats['lists']}
"""
