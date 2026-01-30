# Quick Start Guide

## Installation

1. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Note: For spell checking to work, you'll need libenchant installed:
   - **Ubuntu/Debian:** `sudo apt-get install libenchant-2-2`
   - **Fedora:** `sudo dnf install enchant2`
   - **macOS:** `brew install enchant`
   - **Windows:** Usually included with pyenchant package

3. **Run tests:**
   ```bash
   python test.py
   ```

4. **Launch the application:**
   ```bash
   python main.py
   ```

## First Steps

1. **Open the sample file:**
   - Click `File` → `Open` and select `sample.md`
   - See live preview with Mermaid diagrams, syntax highlighting, and tables

2. **Try formatting:**
   - Use toolbar buttons to format text
   - Or use keyboard shortcuts: Ctrl+B (bold), Ctrl+I (italic), Ctrl+K (link)

3. **Test find & replace:**
   - Press Ctrl+F to open Find & Replace dialog
   - Try searching with regex enabled

4. **Switch themes:**
   - `View` → `UI Theme` → Choose Light or Dark
   - `View` → `Preview Theme` → Choose GitHub, Academic, or Minimal

5. **Export:**
   - `File` → `Export` → Choose HTML or PDF
   - Select export theme for styled output

## Keyboard Shortcuts

### File Operations
- `Ctrl+N` - New file
- `Ctrl+O` - Open file
- `Ctrl+S` - Save file
- `Ctrl+Shift+S` - Save as
- `Ctrl+Q` - Quit

### Editing
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+F` - Find and replace
- `Ctrl+B` - Bold
- `Ctrl+I` - Italic
- `Ctrl+K` - Insert link

### View
- `F11` - Editor only mode
- `F12` - Preview only mode
- `Ctrl+Shift+S` - Show statistics

## Tips

1. **Auto-save is enabled by default** - Your work is automatically saved every 60 seconds

2. **Enable spell checking** - Go to `Edit` → `Enable Spell Check` (requires pyenchant)

3. **Synchronized scrolling** - Enable in `View` → `Synchronized Scrolling` to link editor and preview scroll

4. **Recent files** - Access recently opened files from `File` → `Recent Files`

5. **Split modes** - Change layout with `View` → `Split Mode`:
   - Horizontal (side-by-side)
   - Vertical (top-bottom)
   - Editor only
   - Preview only
   - Both panes

## Troubleshooting

### Spell checking not working
- Install libenchant: `sudo apt-get install libenchant-2-2` (Ubuntu/Debian)
- Verify pyenchant is installed: `pip list | grep pyenchant`

### Mermaid diagrams not rendering
- Requires internet connection (uses CDN)
- Check browser console in preview pane

### PDF export not working
- Ensure PySide6-WebEngine is installed: `pip install PySide6-WebEngine`

### Application won't start
- Run tests: `python test.py`
- Check for missing dependencies
- Activate virtual environment

## Module Structure

```
core/                    # Core functionality
├── markdown_processor.py   # Markdown → HTML conversion
├── theme_manager.py        # UI theme management
└── spell_checker.py        # Spell checking

ui/                      # User interface
├── main_window.py          # Main application window
├── toolbar.py              # Formatting toolbar
└── find_replace_dialog.py  # Find & replace

themes/                  # Export themes
└── css_themes.py           # CSS templates

utils/                   # Utilities
├── file_manager.py         # File operations
└── statistics.py           # Text statistics
```

## Next Steps

1. Explore all features in the sample document
2. Create your own markdown documents
3. Customize themes and settings
4. Try exporting to different formats

Enjoy your markdown editing experience! 🚀
