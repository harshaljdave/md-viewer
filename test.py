#!/usr/bin/env python3
"""
Test script to verify all modules can be imported correctly.
"""

import sys

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        print("  ✓ Importing core modules...")
        from core.markdown_processor import MarkdownProcessor
        from core.theme_manager import ThemeManager
        from core.spell_checker import SpellCheckHighlighter, ENCHANT_AVAILABLE
        
        print("  ✓ Importing utils modules...")
        from utils.file_manager import FileManager
        from utils.statistics import Statistics
        
        print("  ✓ Importing UI modules...")
        from ui.find_replace_dialog import FindReplaceDialog
        from ui.toolbar import MarkdownToolbar
        from ui.main_window import MainWindow
        
        print("  ✓ Importing themes...")
        from themes.css_themes import get_theme, get_theme_names
        
        print("\n✅ All imports successful!")
        
        # Test basic functionality
        print("\nTesting basic functionality...")
        
        # Test markdown processor
        md = MarkdownProcessor()
        html = md.convert("# Hello\n\nThis is **bold**.")
        assert "<h1" in html and "Hello" in html
        assert "<strong>bold</strong>" in html
        print("  ✓ Markdown processor works")
        
        # Test statistics
        stats = Statistics("Hello world! This is a test.")
        assert stats.get_word_count() == 6
        print("  ✓ Statistics module works")
        
        # Test themes
        themes = get_theme_names()
        assert 'github-light' in themes
        assert 'academic' in themes
        print(f"  ✓ {len(themes)} themes available")
        
        # Test file manager
        fm = FileManager()
        assert fm.get_recent_files() == []
        print("  ✓ File manager works")
        
        # Check spell checker availability
        if ENCHANT_AVAILABLE:
            print("  ✓ Spell checking available (pyenchant installed)")
        else:
            print("  ⚠ Spell checking not available (pyenchant not installed)")
        
        print("\n✅ All tests passed!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\nMake sure you have installed all dependencies:")
        print("  pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gui():
    """Test that GUI can be created (requires display)."""
    print("\nTesting GUI creation...")
    
    try:
        from PySide6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        
        app = QApplication(sys.argv)
        window = MainWindow(app)
        
        print("  ✓ Main window created successfully")
        print("  ✓ GUI is ready to launch")
        
        # Don't actually show the window in test mode
        # window.show()
        # sys.exit(app.exec())
        
        return True
        
    except Exception as e:
        print(f"\n❌ GUI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Markdown Editor - Test Suite")
    print("=" * 60)
    
    # Test imports and basic functionality
    if not test_imports():
        sys.exit(1)
    
    # Test GUI (only if display is available)
    if "--gui" in sys.argv:
        if not test_gui():
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed successfully!")
    print("=" * 60)
    print("\nTo run the application:")
    print("  python main.py")
    print("\nTo run tests with GUI:")
    print("  python test.py --gui")
