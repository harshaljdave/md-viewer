"""
File management: recent files and auto-save
"""

import os
import time
from pathlib import Path
from PySide6.QtCore import QSettings, QStandardPaths


class FileManager:
    """Manages recent files and auto-save functionality."""
    
    MAX_RECENT_FILES = 10
    
    def __init__(self):
        self.settings = QSettings("MarkdownEditor", "Files")
        self.recent_files = self.settings.value("recent_files", [], list)
        self.autosave_enabled = self.settings.value("autosave_enabled", True, bool)
        self.autosave_interval = self.settings.value("autosave_interval", 60, int)
    
    # Recent Files Management
    
    def add_recent_file(self, filepath):
        """Add a file to the recent files list."""
        filepath = os.path.abspath(filepath)
        
        # Remove if already exists
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        
        # Add to beginning
        self.recent_files.insert(0, filepath)
        
        # Trim to max size
        self.recent_files = self.recent_files[:self.MAX_RECENT_FILES]
        
        # Save to settings
        self.settings.setValue("recent_files", self.recent_files)
    
    def get_recent_files(self):
        """Get list of recent files (only existing ones)."""
        # Filter out non-existent files
        valid_files = [f for f in self.recent_files if os.path.exists(f)]
        
        # Update list if any were invalid
        if len(valid_files) != len(self.recent_files):
            self.recent_files = valid_files
            self.settings.setValue("recent_files", self.recent_files)
        
        return self.recent_files
    
    def clear_recent_files(self):
        """Clear the recent files list."""
        self.recent_files = []
        self.settings.setValue("recent_files", [])
    
    # Auto-save Management
    
    def get_autosave_path(self, filepath=None):
        """
        Get the autosave path for a file.
        
        Args:
            filepath: Original file path, or None for new files
            
        Returns:
            Path to autosave file
        """
        if filepath:
            # Save next to original file
            return filepath + ".autosave"
        else:
            # Save to temp directory for unsaved files
            temp_dir = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
            return os.path.join(temp_dir, f"markdown_autosave_{int(time.time())}.md")
    
    def save_autosave(self, content, filepath=None):
        """
        Save autosave file.
        
        Args:
            content: Content to save
            filepath: Original file path (optional)
            
        Returns:
            Path to autosave file, or None on error
        """
        if not self.autosave_enabled:
            return None
        
        try:
            # SECURITY: Validate file size before saving
            content_size = len(content.encode('utf-8'))
            max_size = 50 * 1024 * 1024  # 50MB limit for autosave
            
            if content_size > max_size:
                print(f"Autosave skipped: content too large ({content_size / 1024 / 1024:.1f}MB)")
                return None
            
            autosave_path = self.get_autosave_path(filepath)
            
            # SECURITY: Validate autosave path
            autosave_path = os.path.abspath(autosave_path)
            
            with open(autosave_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return autosave_path
        except Exception as e:
            print(f"Autosave failed: {e}")
            return None
    
    def load_autosave(self, filepath):
        """
        Load autosave file if it exists.
        
        Args:
            filepath: Original file path
            
        Returns:
            (content, autosave_path) tuple, or (None, None) if no autosave
        """
        autosave_path = self.get_autosave_path(filepath)
        
        if os.path.exists(autosave_path):
            try:
                with open(autosave_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return (content, autosave_path)
            except Exception as e:
                print(f"Failed to load autosave: {e}")
        
        return (None, None)
    
    def delete_autosave(self, filepath):
        """Delete autosave file for a given filepath."""
        autosave_path = self.get_autosave_path(filepath)
        
        if os.path.exists(autosave_path):
            try:
                os.remove(autosave_path)
            except Exception as e:
                print(f"Failed to delete autosave: {e}")
    
    def cleanup_old_autosaves(self, max_age_days=7):
        """Clean up old autosave files from temp directory."""
        temp_dir = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
        
        try:
            for filename in os.listdir(temp_dir):
                if filename.startswith("markdown_autosave_"):
                    filepath = os.path.join(temp_dir, filename)
                    
                    # Check file age
                    file_age = time.time() - os.path.getmtime(filepath)
                    if file_age > (max_age_days * 24 * 60 * 60):
                        os.remove(filepath)
        except Exception as e:
            print(f"Failed to cleanup autosaves: {e}")
    
    # Settings
    
    def set_autosave_enabled(self, enabled):
        """Enable or disable autosave."""
        self.autosave_enabled = enabled
        self.settings.setValue("autosave_enabled", enabled)
    
    def is_autosave_enabled(self):
        """Check if autosave is enabled."""
        return self.autosave_enabled
    
    def set_autosave_interval(self, seconds):
        """Set autosave interval in seconds."""
        self.autosave_interval = seconds
        self.settings.setValue("autosave_interval", seconds)
    
    def get_autosave_interval(self):
        """Get autosave interval in seconds."""
        return self.autosave_interval
