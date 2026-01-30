# Markdown Editor + Viewer

A feature-rich desktop markdown editor with live preview, built with PySide6.

## Features

### High-Impact Features
✅ **Export Functionality** - Export to HTML and PDF formats with multiple themes
✅ **Synchronized Scrolling** - Link editor and preview scroll positions  
✅ **Dark Mode** - Light/dark theme switcher for UI
✅ **Formatting Toolbar** - Quick buttons for bold, italic, headers, lists, links, etc.
✅ **Find & Replace** - Full-featured search with regex support
✅ **Recent Files** - Quick access to recently opened documents
✅ **Auto-save** - Automatic saving with crash recovery
✅ **Statistics** - Real-time word count, character count, reading time in status bar

### Advanced Features
✅ **Live Spell Checking** - Underline misspelled words with suggestions (powered by pyenchant)
✅ **Mermaid Diagram Support** - Render diagrams directly in preview
✅ **Split Modes** - Horizontal/vertical/editor-only/preview-only layouts

### Performance Optimizations
✅ **Debounced Preview** - 300ms delay prevents lag during typing
✅ **MD5 Caching** - Skip redundant re-renders of unchanged content
✅ **Optimized WebEngine** - Disabled unnecessary features for better memory usage

### Security Features
✅ **XSS Prevention** - HTML sanitization in Mermaid code blocks
✅ **Content Security Policy** - CSP headers restrict script sources
✅ **Local Resource Bundling** - No external CDN dependencies
✅ **File Validation** - Path validation and size limits (10MB files, 50MB autosave)

## Installation

```
md viewer/
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
├── core/                   # Core functionality
│   ├── markdown_processor.py  # Markdown conversion with Mermaid
│   ├── theme_manager.py       # Light/dark mode management
│   └── spell_checker.py       # Spell checking with pyenchant
├── ui/                     # User interface modules
│   ├── main_window.py         # Main application window
│   ├── toolbar.py             # Formatting toolbar
│   └── find_replace_dialog.py # Find & replace dialog
├── themes/                 # CSS themes for export
│   └── css_themes.py          # GitHub, Academic, Minimal themes
└── utils/                  # Utility modules
    ├── file_manager.py        # Recent files & auto-save
    └── statistics.py          # Text statistics calculation
```

## Installation

**Note:** For full Mermaid diagram support, download the actual mermaid.min.js:
```bash
curl -o mermaid.min.js https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js
```

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Dependencies

- **PySide6** >= 6.6.0 - Qt6 bindings for Python
- **PySide6-WebEngine** >= 6.6.0 - Web engine for HTML preview
- **markdown** >= 3.5.0 - Markdown parser with extensions
- **Pygments** >= 2.17.0 - Syntax highlighting
- **pyenchant** >= 3.2.0 - Spell checking (requires libenchant)

## Usage

### Keyboard Shortcuts

- `Ctrl+N` - New file
- `Ctrl+O` - Open file
- `Ctrl+S` - Save file
- `Ctrl+Shift+S` - Save as
- `Ctrl+Q` - Quit
- `Ctrl+F` - Find and replace
- `Ctrl+B` - Bold
- `Ctrl+I` - Italic
- `Ctrl+K` - Insert link
- `F11` - Editor only mode
- `F12` - Preview only mode

### Markdown Extensions Supported

- **Extra** - Tables, fenced code blocks, footnotes, definitions
- **CodeHilite** - Syntax highlighting for code blocks
- **TOC** - Table of contents generation
- **Sane Lists** - Better list handling
- **Smarty** - Smart quotes and typography

### Mermaid Diagrams

Use fenced code blocks with `mermaid` language:

\`\`\`mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
\`\`\`

### Export Themes

Choose from multiple CSS themes when exporting:

- **GitHub Light/Dark** - GitHub-style rendering
- **Academic** - Paper-style formatting for academic documents
- **Minimal** - Clean, distraction-free design

## Features in Detail

### Auto-save
- Automatically saves every 60 seconds (configurable)
- Creates `.autosave` backup files
- Recovery dialog on restart
- Cleanup of old autosave files

### Spell Checking
- Real-time spell checking with red underlines
- Right-click for suggestions
- Add to personal dictionary
- Can be toggled on/off

### Statistics
- Word count, character count, line count
- Reading time estimation (200 wpm)
- Markdown-specific stats (headings, links, images, code blocks)
- Compact view in status bar, detailed view in dialog

### View Modes
- **Horizontal Split** - Editor and preview side-by-side
- **Vertical Split** - Editor and preview top-bottom
- **Editor Only** - Focus mode for writing
- **Preview Only** - Reading mode

## Performance Tips

- For large documents (>500KB), preview updates may be slower
- Disable synchronized scrolling for better performance with large files
- Use auto-save to prevent data loss without manual saving

## Known Issues

- Spell checking requires libenchant to be installed on your system
- Mermaid diagrams require internet connection (uses CDN)
- PDF export quality depends on QWebEngine rendering

## Future Enhancements

- [ ] Offline Mermaid support (bundle library locally)
- [ ] Custom CSS for preview
- [ ] Multiple tabs for editing multiple files
- [ ] Git integration
- [ ] Table of contents panel
- [ ] Image paste from clipboard

## License

This project is provided as-is for educational and personal use.

## Credits

Built with:
- PySide6 (Qt for Python)
- Python-Markdown
- Pygments
- pyenchant
- Mermaid.js
