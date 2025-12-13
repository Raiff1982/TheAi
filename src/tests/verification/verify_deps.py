"""
Verify dependencies before building
"""
import sys
import importlib

def check_import(module_name):
    """Try to import a module and report status."""
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name} successfully imported")
        return True
    except ImportError as e:
        print(f"✗ Error importing {module_name}: {e}")
        return False

# Core dependencies
REQUIRED = [
    'arviz',
    'pymc',
    'pytensor',
    'numpy',
    'scipy',
    'pandas',
    'xarray'
]

# Optional dependencies
OPTIONAL = [
    'numba',
    'dask'
]

def main():
    """Check all dependencies."""
    print("Checking required dependencies...")
    required_ok = all(check_import(mod) for mod in REQUIRED)
    
    print("\nChecking optional dependencies...")
    for mod in OPTIONAL:
        check_import(mod)
    
    if not required_ok:
        print("\n❌ Some required dependencies are missing!")
        sys.exit(1)
    
    print("\n✓ All required dependencies are available")
    return 0

if __name__ == '__main__':
    sys.exit(main())
