"""
CSS themes for markdown preview and export
"""

from pygments.formatters import HtmlFormatter


def get_syntax_css(style='monokai'):
    """Generate Pygments CSS for syntax highlighting."""
    return HtmlFormatter(style=style).get_style_defs('.highlight')


class CSSTheme:
    """Base class for CSS themes."""
    
    def __init__(self, name, syntax_style='monokai'):
        self.name = name
        self.syntax_style = syntax_style
    
    def get_css(self):
        """Return the complete CSS for this theme."""
        raise NotImplementedError
    
    def get_html_template(self, content):
        """Return complete HTML with this theme applied."""
        import os
        from pathlib import Path
        
        # Try to use local bundled Mermaid.js, fallback to CDN
        module_dir = Path(__file__).parent.parent
        mermaid_path = module_dir / 'mermaid.min.js'
        
        # Check if local mermaid exists and is valid (>1KB)
        use_local = False
        if mermaid_path.exists():
            try:
                if os.path.getsize(mermaid_path) > 1024:  # More than 1KB (not just stub)
                    use_local = True
                    mermaid_url = f'file://{mermaid_path.absolute()}'
            except:
                pass
        
        # Fallback to CDN if local file not available
        if not use_local:
            mermaid_url = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'
        
        # Adjust CSP to allow CDN if needed
        if use_local:
            csp = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;"
        else:
            csp = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;"
        
        return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<style>
{self.get_css()}
</style>
<script src="{mermaid_url}"></script>
<script>
if (typeof mermaid !== 'undefined') {{
    mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
}}
</script>
</head>
<body>
{content}
</body>
</html>'''


class GitHubTheme(CSSTheme):
    """GitHub-style theme."""
    
    def __init__(self, dark_mode=False):
        style = 'monokai' if dark_mode else 'github-dark'
        super().__init__('GitHub', style)
        self.dark_mode = dark_mode
    
    def get_css(self):
        syntax_css = get_syntax_css(self.syntax_style)
        
        if self.dark_mode:
            bg_color = "#0d1117"
            text_color = "#c9d1d9"
            border_color = "#30363d"
            code_bg = "#161b22"
            table_bg = "#161b22"
            blockquote_border = "#3b434b"
        else:
            bg_color = "#ffffff"
            text_color = "#24292f"
            border_color = "#d0d7de"
            code_bg = "#f6f8fa"
            table_bg = "#f6f8fa"
            blockquote_border = "#d0d7de"
        
        return f'''{syntax_css}

body {{
    margin: 20px auto;
    max-width: 900px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: {text_color};
    background-color: {bg_color};
    padding: 0 20px;
}}

h1, h2, h3, h4, h5, h6 {{
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
    color: {text_color};
}}

h1 {{
    font-size: 2em;
    border-bottom: 1px solid {border_color};
    padding-bottom: 0.3em;
}}

h2 {{
    font-size: 1.5em;
    border-bottom: 1px solid {border_color};
    padding-bottom: 0.3em;
}}

h3 {{ font-size: 1.25em; }}
h4 {{ font-size: 1em; }}
h5 {{ font-size: 0.875em; }}
h6 {{ font-size: 0.85em; color: #6a737d; }}

p {{
    margin-top: 0;
    margin-bottom: 16px;
}}

code {{
    background: {code_bg};
    padding: 2px 6px;
    border-radius: 6px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 0.85em;
}}

pre {{
    background: #272822;
    padding: 16px;
    border-radius: 6px;
    overflow-x: auto;
    line-height: 1.45;
    margin-bottom: 16px;
}}

pre code {{
    background: transparent;
    padding: 0;
    border-radius: 0;
}}

blockquote {{
    border-left: 4px solid {blockquote_border};
    padding-left: 16px;
    color: #6a737d;
    margin: 0 0 16px 0;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
}}

table th, table td {{
    border: 1px solid {border_color};
    padding: 8px 13px;
}}

table th {{
    background: {table_bg};
    font-weight: 600;
}}

table tr:nth-child(2n) {{
    background: {table_bg};
}}

a {{
    color: #0969da;
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
    border-top: 2px solid {border_color};
    margin: 24px 0;
}}

ul, ol {{
    padding-left: 2em;
    margin-bottom: 16px;
}}

li {{
    margin-bottom: 0.25em;
}}

.mermaid {{
    text-align: center;
    margin: 20px 0;
}}
'''


class AcademicTheme(CSSTheme):
    """Academic/paper-style theme."""
    
    def __init__(self):
        super().__init__('Academic', 'colorful')
    
    def get_css(self):
        syntax_css = get_syntax_css(self.syntax_style)
        
        return f'''{syntax_css}

body {{
    margin: 40px auto;
    max-width: 800px;
    font-family: "Georgia", "Times New Roman", Times, serif;
    font-size: 18px;
    line-height: 1.8;
    color: #222;
    background-color: #ffffff;
    padding: 0 40px;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif;
    margin-top: 32px;
    margin-bottom: 16px;
    font-weight: 700;
    line-height: 1.3;
    color: #1a1a1a;
}}

h1 {{
    font-size: 2.5em;
    text-align: center;
    margin-top: 0;
    margin-bottom: 8px;
}}

h2 {{
    font-size: 1.8em;
    margin-top: 48px;
}}

h3 {{
    font-size: 1.4em;
}}

h4 {{
    font-size: 1.2em;
}}

p {{
    margin-top: 0;
    margin-bottom: 16px;
    text-align: justify;
}}

code {{
    background: #f5f5f5;
    padding: 2px 4px;
    border: 1px solid #ddd;
    border-radius: 3px;
    font-family: "Courier New", Courier, monospace;
    font-size: 0.9em;
}}

pre {{
    background: #f8f8f8;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 4px;
    overflow-x: auto;
    line-height: 1.5;
    margin: 24px 0;
}}

pre code {{
    background: transparent;
    padding: 0;
    border: none;
}}

blockquote {{
    border-left: 4px solid #999;
    padding-left: 20px;
    margin-left: 0;
    margin-right: 0;
    font-style: italic;
    color: #555;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 24px 0;
    font-size: 0.9em;
}}

table th, table td {{
    border: 1px solid #333;
    padding: 10px 15px;
    text-align: left;
}}

table th {{
    background: #f0f0f0;
    font-weight: 700;
}}

a {{
    color: #0066cc;
    text-decoration: underline;
}}

a:hover {{
    color: #0052a3;
}}

img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 20px auto;
}}

hr {{
    border: 0;
    border-top: 1px solid #333;
    margin: 48px 0;
}}

ul, ol {{
    padding-left: 2em;
    margin-bottom: 16px;
}}

li {{
    margin-bottom: 8px;
}}

.mermaid {{
    text-align: center;
    margin: 30px 0;
}}

/* Footnotes styling */
.footnote {{
    font-size: 0.85em;
    vertical-align: super;
}}
'''


class MinimalTheme(CSSTheme):
    """Clean minimal theme."""
    
    def __init__(self):
        super().__init__('Minimal', 'friendly')
    
    def get_css(self):
        syntax_css = get_syntax_css(self.syntax_style)
        
        return f'''{syntax_css}

body {{
    margin: 30px auto;
    max-width: 750px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 16px;
    line-height: 1.7;
    color: #333;
    background-color: #fff;
    padding: 0 20px;
}}

h1, h2, h3, h4, h5, h6 {{
    margin-top: 32px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.3;
    color: #111;
}}

h1 {{ font-size: 2.2em; }}
h2 {{ font-size: 1.7em; }}
h3 {{ font-size: 1.4em; }}
h4 {{ font-size: 1.1em; }}
h5 {{ font-size: 1em; }}
h6 {{ font-size: 0.9em; }}

p {{
    margin: 0 0 16px 0;
}}

code {{
    background: #f4f4f4;
    padding: 3px 6px;
    border-radius: 3px;
    font-family: "Monaco", "Menlo", "Consolas", monospace;
    font-size: 0.9em;
}}

pre {{
    background: #2d2d2d;
    padding: 16px;
    border-radius: 4px;
    overflow-x: auto;
    margin: 20px 0;
}}

pre code {{
    background: transparent;
    padding: 0;
    color: #f8f8f2;
}}

blockquote {{
    border-left: 3px solid #ccc;
    padding-left: 16px;
    color: #666;
    margin: 16px 0;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}}

table th, table td {{
    border: 1px solid #ddd;
    padding: 8px 12px;
}}

table th {{
    background: #f8f8f8;
    font-weight: 600;
    text-align: left;
}}

a {{
    color: #0066cc;
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
    border-top: 1px solid #eee;
    margin: 30px 0;
}}

ul, ol {{
    padding-left: 2em;
    margin-bottom: 16px;
}}

.mermaid {{
    text-align: center;
    margin: 20px 0;
}}
'''


# Theme registry
THEMES = {
    'github-light': GitHubTheme(dark_mode=False),
    'github-dark': GitHubTheme(dark_mode=True),
    'academic': AcademicTheme(),
    'minimal': MinimalTheme(),
}


def get_theme(theme_name='github-light'):
    """Get a theme by name."""
    return THEMES.get(theme_name, THEMES['github-light'])


def get_theme_names():
    """Get list of available theme names."""
    return list(THEMES.keys())
