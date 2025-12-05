#!/usr/bin/env python3
"""
Build script for RBLX Files directory listing.
Scans all folders and generates files.json with file information.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

# Folders/files to ignore
IGNORE = {
    '.git',
    '.github',
    '__pycache__',
    'node_modules',
    '.vscode',
    '.idea',
    'index.html',
    'styles.css',
    'script.js',
    'files.json',
    'build.py',
    'README.md',
    '.gitignore',
    '.DS_Store',
    'Thumbs.db',
}

# File extensions to include (empty = all)
ALLOWED_EXTENSIONS = set()  # Add extensions like {'.mid', '.mp3'} to filter


def scan_directory(root_path: Path) -> dict:
    """Scan directory and return file structure."""
    folders = []
    
    # Get all subdirectories
    for item in sorted(root_path.iterdir()):
        if item.name in IGNORE:
            continue
            
        if item.is_dir():
            files = scan_folder(item)
            if files:  # Only include folders with files
                folders.append({
                    'name': item.name,
                    'files': files
                })
    
    return {
        'generated': datetime.now(timezone.utc).isoformat(),
        'folders': folders
    }


def scan_folder(folder_path: Path) -> list:
    """Scan a folder and return list of files."""
    files = []
    
    for item in sorted(folder_path.iterdir()):
        if item.name in IGNORE:
            continue
            
        if item.is_file():
            # Check extension filter
            if ALLOWED_EXTENSIONS:
                if item.suffix.lower() not in ALLOWED_EXTENSIONS:
                    continue
            
            files.append({
                'name': item.name
            })
    
    return files


def main():
    # Get script directory (project root)
    root = Path(__file__).parent.resolve()
    
    print(f"Scanning: {root}")
    
    # Scan and generate data
    data = scan_directory(root)
    
    # Count files
    total_files = sum(len(f['files']) for f in data['folders'])
    total_folders = len(data['folders'])
    
    # Write JSON (completely overwrites)
    output_path = root / 'files.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Generated: {output_path}")
    print(f"Found: {total_folders} folders, {total_files} files")
    
    # Print summary
    for folder in data['folders']:
        print(f"  /{folder['name']}/")
        for file in folder['files']:
            print(f"    - {file['name']}")


if __name__ == '__main__':
    main()

