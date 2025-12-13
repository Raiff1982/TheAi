"""
Script to verify arviz static files are properly bundled
"""
import os
import sys
from pathlib import Path

def find_static_dir():
    """Find the arviz static directory."""
    possible_paths = [
        Path('dist/test_codette_exe'),
        Path('dist/_internal/arviz/static'),
        Path('dist/arviz/static'),
        Path('.venv/Lib/site-packages/arviz/static')
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"Found directory: {path}")
            return path
            
    print("Could not find arviz static directory")
    print("Checked paths:")
    for path in possible_paths:
        print(f"  - {path}")
    return None

def verify_static_files(static_dir):
    """Verify required static files exist."""
    required_files = [
        'html/icons-svg-inline.html'  # This is the main required file for arviz
    ]
    
    missing = []
    for file in required_files:
        file_path = static_dir / file
        if not file_path.exists():
            missing.append(file)
            
    if missing:
        print("\nMissing files:")
        for file in missing:
            print(f"  - {file}")
        return False
        
    print("\nAll required files found!")
    return True

def main():
    print("=== Verifying arviz static files ===")
    
    static_dir = find_static_dir()
    if not static_dir:
        return 1
        
    if verify_static_files(static_dir):
        return 0
    return 1

if __name__ == '__main__':
    sys.exit(main())
