# -*- mode: python ; coding: utf-8 -*-
"""
Codette AI Hybrid System - PyInstaller Specification
====================================================
Builds standalone executable with all quantum consciousness,
advanced features, and Supabase integration.

Version: 3.0.0-hybrid
Date: December 2025
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata
import os

block_cipher = None

# ==============================================================================
# DATA FILES COLLECTION
# ==============================================================================

datas = []

# Core AI/ML package data files
print("Collecting AI/ML package data...")
core_packages = [
    'nltk',
    'vaderSentiment',
    'transformers',
    'torch',
    'sklearn',
]

for pkg in core_packages:
    try:
        datas.extend(collect_data_files(pkg, include_py_files=True))
        print(f"  ? Collected {pkg}")
    except Exception as e:
        print(f"  ? Could not collect {pkg}: {e}")

# Optional quantum packages (if available)
quantum_packages = ['arviz', 'pymc', 'qiskit', 'pytensor']
for pkg in quantum_packages:
    try:
        datas.extend(collect_data_files(pkg, include_py_files=True))
        print(f"  ? Collected {pkg} (quantum)")
    except Exception as e:
        print(f"  ? {pkg} not available (optional)")

# ==============================================================================
# CODETTE-SPECIFIC FILES
# ==============================================================================

print("\nCollecting Codette-specific files...")

# Configuration files (if they exist)
config_files = [
    ('.env', '.'),
    ('.env.example', '.'),
]

for src, dst in config_files:
    if os.path.exists(src):
        datas.append((src, dst))
        print(f"  ? Added {src}")

# Codette modules
codette_dirs = [
    ('Codette/*', 'Codette'),
    ('Codette/src/*', 'Codette/src'),
]

for src, dst in codette_dirs:
    datas.append((src, dst))
    print(f"  ? Added {src}")

# DAW Core DSP effects
if os.path.exists('daw_core'):
    datas.append(('daw_core/*', 'daw_core'))
    print("  ? Added daw_core (DSP effects)")

# Supabase Edge Functions (documentation only - deployed separately)
if os.path.exists('supabase'):
    datas.append(('supabase/*.md', 'supabase'))
    print("  ? Added supabase docs")

# Memory cocoons directory
if os.path.exists('cocoons'):
    datas.append(('cocoons/*', 'cocoons'))
    print("  ? Added cocoons directory")
else:
    # Create empty cocoons directory
    os.makedirs('cocoons', exist_ok=True)
    print("  ? Created cocoons directory")

# Documentation
doc_files = [
    'README.md',
    'CODETTE_IMPLEMENTATION_COMPLETE.md',
    'CODETTE_ADVANCED_INTEGRATION.md',
    'SUPABASE_CODETTE_INTEGRATION.md',
    'DEVELOPMENT.md',
]

for doc in doc_files:
    if os.path.exists(doc):
        datas.append((doc, '.'))
        print(f"  ? Added {doc}")

# ==============================================================================
# PACKAGE METADATA
# ==============================================================================

print("\nCollecting package metadata...")

metadata_pkgs = [
    # Core ML
    'torch', 'transformers', 'numpy', 'scipy',
    # NLP
    'nltk', 'vaderSentiment', 'tokenizers',
    # Utilities
    'tqdm', 'regex', 'requests', 'packaging', 'filelock',
    # Web
    'fastapi', 'uvicorn', 'pydantic', 'starlette',
    # Database
    'supabase', 'httpx',
]

for pkg in metadata_pkgs:
    try:
        datas.extend(copy_metadata(pkg))
        print(f"  ? {pkg}")
    except Exception as e:
        print(f"  ? {pkg} metadata not found (may be optional)")

# ==============================================================================
# HIDDEN IMPORTS
# ==============================================================================

print("\nConfiguring hidden imports...")

hiddenimports = [
    # Core Python
    'json', 'logging', 'asyncio', 'typing', 'datetime', 'pathlib',
    
    # Core Processing
    'numpy', 'scipy', 'pandas',
    
    # AI and ML Core
    'torch', 'transformers', 'sklearn', 'nltk', 'vaderSentiment',
    
    # Codette Modules
    'codette_new',
    'codette_advanced',
    'codette_hybrid',
    'codette_capabilities',
    'codette_stable_responder',
    
    # Web Framework
    'fastapi', 'uvicorn', 'pydantic', 'starlette',
    'uvicorn.logging', 'uvicorn.loops', 'uvicorn.protocols',
    'uvicorn.lifespan.on',
    
    # HTTP/WebSocket
    'httpx', 'websockets', 'httpcore',
    
    # Database
    'supabase', 'postgrest', 'realtime', 'gotrue', 'storage3',
    
    # Utilities
    'tqdm', 'colorama', 'tokenizers', 'filelock', 'regex',
    'dotenv', 'python-dotenv',
    
    # Network
    'requests', 'urllib3', 'certifi', 'charset_normalizer', 'idna',
    
    # Optional Quantum (if available)
    'networkx', 'matplotlib',
]

# Add all sklearn submodules
hiddenimports.extend(collect_submodules('sklearn'))

print(f"  Total hidden imports: {len(hiddenimports)}")

# ==============================================================================
# ANALYSIS CONFIGURATION
# ==============================================================================

a = Analysis(
    ['codette_server_unified.py'],  # Main entry point
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unused packages to reduce size
        'matplotlib.tests',
        'numpy.tests',
        'pandas.tests',
        'pytest',
        'IPython',
        'jupyter',
        'notebook',
        # Exclude GUI if not needed
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'tkinter',
        # Exclude dev tools
        'setuptools', 'pip', 'wheel',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ==============================================================================
# PYZ (Python ZIP Archive)
# ==============================================================================

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# ==============================================================================
# EXECUTABLE CONFIGURATION
# ==============================================================================

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CodetteAI-Hybrid',  # Output executable name
    debug=False,  # Set to True for debugging build issues
    bootloader_ignore_signals=False,
    strip=False,  # Keep symbols for debugging
    upx=True,  # Compress with UPX
    upx_exclude=[
        # Don't compress these (may cause issues)
        'vcruntime140.dll',
        'python*.dll',
    ],
    runtime_tmpdir=None,
    console=True,  # Show console for server logs
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,  # Optional icon
)

print("\n" + "="*70)
print("PyInstaller spec configured successfully!")
print("="*70)
print("\nTo build:")
print("  pyinstaller codette_hybrid.spec")
print("\nOutput will be in: dist/CodetteAI-Hybrid.exe")
print("\nFeatures included:")
print("  ? Quantum Consciousness (11 perspectives)")
print("  ? Defense Modifiers")
print("  ? Vector Search")
print("  ? Prompt Engineering")
print("  ? Creative Sentences")
print("  ? DAW DSP Effects")
print("  ? Supabase Integration")
print("  ? FastAPI Server")
print("  ? WebSocket Support")
print("="*70 + "\n")
