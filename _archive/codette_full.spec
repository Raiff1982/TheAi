# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, copy_metadata

# Required JSON files
required_json = [
    'config.json',
    'Codette_Quantum_Harmonic_Baseline_FFT.json',
    'Codette_Integrity_Certificate.json',
    'agischema.json'
]

# Required Models and Data
required_models = [
    'models/*',
    'static/*',
    'data/*',
    'gotchu/*'  # Contains important quantum and harmonic data
]

# Collect all data files from required packages
datas = []
datas.extend(collect_data_files('arviz', include_py_files=True))
datas.extend(collect_data_files('pymc', include_py_files=True))
datas.extend(collect_data_files('nltk', include_py_files=True))
datas.extend(collect_data_files('vaderSentiment', include_py_files=True))
datas.extend(collect_data_files('transformers', include_py_files=True))

# Add metadata for packages that need it
datas.extend(copy_metadata('torch'))
datas.extend(copy_metadata('tqdm'))
datas.extend(copy_metadata('regex'))
datas.extend(copy_metadata('requests'))
datas.extend(copy_metadata('packaging'))
datas.extend(copy_metadata('filelock'))
datas.extend(copy_metadata('numpy'))
datas.extend(copy_metadata('tokenizers'))

# Add all required JSON files
for json_file in required_json:
    datas.append((json_file, '.'))

# Add all required model and data directories
for model_path in required_models:
    datas.append((model_path, model_path.split('/')[0]))

a = Analysis(
    ['codette.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'numpy', 'arviz', 'pymc', 'pytensor', 'scipy', 'pandas', 'xarray',
        'nltk', 'vaderSentiment', 'PyQt5', 'torch', 'transformers',
        'sklearn', 'matplotlib', 'tokenizers', 'tqdm', 'packaging',
        'filelock', 'regex', 'requests'
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
