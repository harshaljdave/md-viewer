"""
Markdown processing with Mermaid diagram support
"""

import hashlib
import markdown
from themes.css_themes import get_theme


class MarkdownProcessor:
    """Handles markdown to HTML conversion with caching and Mermaid support."""
    
    def __init__(self, theme_name='github-light'):
        self.theme_name = theme_name
        self.last_hash = None
        self.last_html = ""
        
        # Initialize markdown processor
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
    
    def convert(self, text, force=False):
        """
        Convert markdown to HTML with caching.
        
        Args:
            text: Markdown text to convert
            force: Force conversion even if cached
            
        Returns:
            Complete HTML document with theme applied
        """
        # Hash check for caching
        text_hash = hashlib.md5(text.encode()).hexdigest()
        if not force and text_hash == self.last_hash:
            return self.last_html
        
        self.last_hash = text_hash
        
        # Convert markdown to HTML
        html_body = self.md.convert(text)
        self.md.reset()  # Important: reset for next conversion
        
        # Process Mermaid diagrams
        html_body = self._process_mermaid(html_body)
        
        # Wrap in full HTML with theme
        theme = get_theme(self.theme_name)
        self.last_html = theme.get_html_template(html_body)
        
        return self.last_html
    
    def _process_mermaid(self, html):
        """
        Convert Mermaid code blocks to renderable divs.
        
        Markdown with ```mermaid gets converted to:
        <div class="mermaid">...mermaid code...</div>
        
        SECURITY: Keep HTML entities escaped to prevent XSS.
        """
        import re
        
        # Pattern to find code blocks with mermaid language
        pattern = r'<code class="language-mermaid">(.*?)</code>'
        
        def replace_mermaid(match):
            mermaid_code = match.group(1)
            # SECURITY FIX: Do NOT unescape - keep HTML entities escaped
            # This prevents XSS injection through mermaid code blocks
            # Mermaid.js will handle the escaped entities correctly
            return f'<div class="mermaid">{mermaid_code}</div>'
        
        # Replace all mermaid code blocks
        html = re.sub(pattern, replace_mermaid, html, flags=re.DOTALL)
        
        # Also handle when it's wrapped in <pre>
        pattern2 = r'<pre><code class="language-mermaid">(.*?)</code></pre>'
        html = re.sub(pattern2, replace_mermaid, html, flags=re.DOTALL)
        
        return html
    
    def set_theme(self, theme_name):
        """Change the theme and force re-render on next convert."""
        self.theme_name = theme_name
        self.last_hash = None  # Force re-render
    
    def clear_cache(self):
        """Clear the conversion cache."""
        self.last_hash = None
        self.last_html = ""
