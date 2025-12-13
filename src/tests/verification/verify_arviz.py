"""
Heldef verify_arviz_files():
    """Verify that all required arviz static files are present."""
    try:
        # Check in dist directory first
        possible_paths = [
            Path('dist/test_codette_exe'),
            Path('dist/_internal/arviz/static'),
            Path('dist/arviz/static'),
            Path('.venv/Lib/site-packages/arviz/static')
        ]
        
        static_dir = None
        for path in possible_paths:
            if path.exists():
                static_dir = path
                print(f"Found static directory at: {static_dir}")
                break
                
        if not static_dir:
            print("Could not find arviz static directory")
            print("Checked paths:")
            for path in possible_paths:
                print(f"  - {path}")
            return False
            
        required_files = [
            'html/icons-svg-inline.html',
            'html/require.min.js',
            'html/style.css'
        ]
            
        missing_files = []
        for file in required_files:
            file_path = static_dir / filefy arviz static files are properly bundled
"""
import os
import sys
import logging
from pathlib import Path

def verify_arviz_files():
    """Verify that all required arviz static files are present."""
    try:
        # Check in dist directory
        dist_dir = Path('dist/test_codette_exe')
        if not dist_dir.exists():
            dist_dir = Path('dist/_internal/arviz/static')
            
        if not dist_dir.exists():
            print(f"Could not find bundled files directory at {dist_dir}")
            return False
            
        required_files = [
            'html/icons-svg-inline.html',
            'html/require.min.js',
            'html/style.css'
        ]
        
        missing_files = []
        for file in required_files:
            file_path = static_dir / file
            if not file_path.exists():
                missing_files.append(str(file_path))
                
        if missing_files:
            print("Missing arviz static files:")
            for file in missing_files:
                print(f"  - {file}")
            return False
            
        print("All arviz static files found!")
        return True
        
    except ImportError as e:
        print(f"Error importing arviz: {e}")
        return False
    except Exception as e:
        print(f"Error checking arviz files: {e}")
        return False

def main():
    success = verify_arviz_files()
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
