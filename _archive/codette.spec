# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

# Initialize key variables
block_cipher = None

# Get the directory containing the spec file
import os
SPECPATH = os.getcwd()  # Use current directory
excludes = []  # Initialize excludes list

print(f"Using SPECPATH: {SPECPATH}")

# Add patch_pytensor to the entry point
patch_pytensor = os.path.join(SPECPATH, 'patch_pytensor.py')
if not os.path.exists(patch_pytensor):
    raise FileNotFoundError(f"patch_pytensor.py not found at {patch_pytensor}")

# Collect all data files with specific includes
arviz_data = collect_data_files('arviz', includes=['**/static/**', '**/*.html', '**/*.css', '**/example_data/**', '**/*.json'])
pymc_data = collect_data_files('pymc', includes=['**/*.dat', '**/*.json', '**/*.txt'])
pytensor_data = collect_data_files('pytensor')
numpy_data = collect_data_files('numpy')
scipy_data = collect_data_files('scipy')
xarray_data = collect_data_files('xarray')

# Add package metadata (needed for some dependencies)
metadata = []
packages_with_data = ['pymc', 'arviz', 'pytensor', 'numpy', 'xarray']
print("\nCollecting metadata and data files:")
for pkg in packages_with_data:
    try:
        meta = copy_metadata(pkg)
        print(f"Found metadata for {pkg}")
        metadata.extend(meta)
    except Exception as e:
        print(f"Warning: Could not collect metadata for {pkg}: {e}")

# Collect all necessary submodules
hidden = []

# Explicitly collect all arviz submodules
arviz_submodules = collect_submodules('arviz')
print(f"\nCollected {len(arviz_submodules)} arviz submodules")
hidden.extend(arviz_submodules)

# Collect other package submodules
for pkg in [
    'pymc',
    'pytensor',
    'numpy',
    'scipy',
    'pandas',
    'xarray',
    'netCDF4',
    'cftime'
]:
    hidden.extend(collect_submodules(pkg))

# Add Codette-specific imports
codette_modules = []

# Check which modules actually exist
potential_modules = [
    'cognitive_processor',
    'codette_quantum_core',
    'agireasoning',
    'ai_core_system',
    'ai_core_identityscan',
    'analyze_cocoons'
]

for module in potential_modules:
    if os.path.exists(os.path.join(SPECPATH, f"{module}.py")):
        codette_modules.append(module)

hidden.extend(codette_modules)

# Handle PyTensor/Numba warnings by making them optional
try:
    import numba
    hidden.extend(['numba', 'pytensor.link.numba.dispatch'])
except ImportError:
    print("Numba not found - skipping numba-related imports")

# Skip test modules to avoid pytest dependencies
excludes.extend([
    'numpy.f2py.tests',
    'scipy.tests',
    'pandas.tests',
    'xarray.tests'
])

# Combine all data files with error handling
datas = []
data_collections = [
    ('arviz', arviz_data),
    ('pymc', pymc_data),
    ('pytensor', pytensor_data),
    ('numpy', numpy_data),
    ('scipy', scipy_data),
    ('xarray', xarray_data)
]

print("\nAdding data files:")
for pkg_name, data_files in data_collections:
    try:
        print(f"Adding {len(data_files)} files from {pkg_name}")
        datas.extend(data_files)
    except Exception as e:
        print(f"Warning: Error adding data files from {pkg_name}: {e}")

# Add metadata files
try:
    print(f"Adding {len(metadata)} metadata files")
    datas.extend(metadata)
except Exception as e:
    print(f"Warning: Error adding metadata files: {e}")

# Add Codette's own data files and check their existence
codette_core_files = [
    ('cognitive_processor.py', '.'),
    ('codette_quantum_core.py', '.'),
    ('agireasoning.py', '.'),
    ('ai_core_system.py', '.'),
    ('ai_core_identityscan.py', '.'),
    ('analyze_cocoons.py', '.'),
    ('analyze_cocoons1.py', '.'),
    ('analyze_cocoons2.py', '.'),
    ('analyze_cocoons3.py', '.')
]

# Only add files that exist
datas.extend([
    (src, dst) for src, dst in codette_core_files 
    if os.path.exists(os.path.join(SPECPATH, src))
])

# Add models directory if it exists
models_dir = os.path.join(SPECPATH, 'models')
if os.path.exists(models_dir):
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, SPECPATH)
                datas.append((full_path, rel_path))

# Print summary of what we're including
print("\nBuild Summary:")
print(f"Total data files: {len(datas)}")
print(f"Hidden imports: {len(hidden)}")
print(f"Excluded modules: {len(excludes)}")

a = Analysis(
    ['launcher.py'],
    pathex=[SPECPATH],  # Add the current directory to path
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['hook-runtime-arviz.py'] if os.path.exists('hook-runtime-arviz.py') else [],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='Codette',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,  # Keep console for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Collect everything into a directory
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Codette'
)
