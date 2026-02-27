# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, copy_metadata

# Collect all data files from required packages
datas = []

# Core package data files
datas.extend(collect_data_files('arviz', include_py_files=True))
datas.extend(collect_data_files('pymc', include_py_files=True))
datas.extend(collect_data_files('nltk', include_py_files=True))
datas.extend(collect_data_files('vaderSentiment', include_py_files=True))
datas.extend(collect_data_files('transformers', include_py_files=True))
datas.extend(collect_data_files('torch', include_py_files=True))

# Required JSON configuration files
json_files = [
    ('config.json', '.'),
    ('Codette_Quantum_Harmonic_Baseline_FFT.json', '.'),
    ('Codette_Integrity_Certificate.json', '.'),
    ('agischema.json', '.'),
    ('dataset-metadata.json', '.'),
    ('fractle_schema.json', '.'),
]
datas.extend(json_files)

# Core model and data directories
core_dirs = [
    ('models/*', 'models'),
    ('static/*', 'static'),
    ('data/*', 'data'),
    ('gotchu/*', 'gotchu'),  # Contains quantum and harmonic data
    ('cocoons/*', 'cocoons'),  # Memory cocoons directory
]
datas.extend(core_dirs)

# Neural network and quantum state files
quantum_files = [
    ('quantum_states/*.npy', 'quantum_states'),
    ('neural_weights/*.pt', 'neural_weights'),
    ('dream_sequences/*.json', 'dream_sequences'),
]
datas.extend(quantum_files)

# Package metadata for core dependencies
metadata_pkgs = [
    'torch', 'tqdm', 'regex', 'requests', 'packaging', 'filelock',
    'numpy', 'tokenizers', 'transformers', 'scipy'
]
for pkg in metadata_pkgs:
    datas.extend(copy_metadata(pkg))

a = Analysis(
    ['codette.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        # Core Processing
        'numpy', 'scipy', 'pandas', 'xarray',
        
        # AI and ML
        'torch', 'transformers', 'sklearn', 'nltk', 'vaderSentiment',
        
        # Quantum Processing
        'qiskit', 'pymc', 'arviz', 'pytensor',
        
        # Visualization
        'matplotlib', 'networkx',
        
        # UI and Interface
        'PyQt5',
        
        # Utilities
        'tqdm', 'yaml', 'colorama', 'tokenizers', 'filelock',
        
        # Additional Dependencies
        'regex', 'requests', 'packaging', 'json', 'logging'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Codette',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
