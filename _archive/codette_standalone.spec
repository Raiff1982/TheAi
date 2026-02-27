# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

# Collect all data files from required packages
arviz_datas = collect_data_files('arviz', include_py_files=True)
pymc_datas = collect_data_files('pymc', include_py_files=True)
nltk_datas = collect_data_files('nltk', include_py_files=True)
vader_datas = collect_data_files('vaderSentiment', include_py_files=True)

# Additional resource files
extra_datas = [
    ('config.json', '.'),
    ('*.json', '.'),
    ('static/*', 'static'),
    ('models/*', 'models'),
    ('data/*', 'data'),
]

a = Analysis(
    ['codette.py'],
    pathex=[],
    binaries=[],
    datas=[*extra_datas, *arviz_datas, *pymc_datas, *nltk_datas, *vader_datas],
    hiddenimports=[
        'numpy', 'arviz', 'pymc', 'pytensor', 'scipy', 'pandas', 'xarray',
        'nltk', 'vaderSentiment', 'PyQt5', 'torch', 'transformers',
        'sklearn', 'matplotlib'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
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
