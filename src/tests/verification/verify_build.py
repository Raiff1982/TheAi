"""
Comprehensive build verification script for Codette package
"""
import os
import sys
import subprocess
from pathlib import Path

def print_section(name):
    """Print a section header"""
    print(f"\n{'='*20} {name} {'='*20}")

def check_executable():
    """Verify the executable exists and basic structure"""
    print_section("Checking Executable")
    
    exe_path = Path('dist/test_codette_exe/test_codette_exe.exe')
    if not exe_path.exists():
        print("❌ ERROR: Executable not found!")
        return False
        
    print("✓ Executable found")
    print(f"Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    return True

def check_arviz_files():
    """Verify arviz static files are present"""
    print_section("Checking Arviz Files")
    
    static_path = Path('dist/test_codette_exe/arviz/static/html')
    required_file = 'icons-svg-inline.html'
    
    if not static_path.exists():
        print("❌ ERROR: Arviz static directory not found!")
        return False
        
    if not (static_path / required_file).exists():
        print(f"❌ ERROR: Required file {required_file} not found!")
        return False
        
    print("✓ Arviz static files present")
    return True

def check_package_structure():
    """Verify key package directories and files"""
    print_section("Checking Package Structure")
    
    required_dirs = [
        'dist/test_codette_exe',
        'dist/test_codette_exe/arviz',
        'dist/test_codette_exe/_internal'
    ]
    
    all_present = True
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"❌ Missing directory: {dir_path}")
            all_present = False
        else:
            print(f"✓ Found directory: {dir_path}")
            
    return all_present

def try_launch_executable():
    """Attempt to launch the executable briefly"""
    print_section("Testing Executable Launch")
    
    exe_path = Path('dist/test_codette_exe/test_codette_exe.exe')
    if not exe_path.exists():
        print("❌ Cannot test launch - executable not found")
        return False
        
    try:
        # Start the process
        process = subprocess.Popen(
            [str(exe_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for a short time to see if it crashes immediately
        try:
            stdout, stderr = process.communicate(timeout=2)
            # Process finished within 2 seconds - might be an error
            print("⚠ Warning: Process exited quickly")
            if stderr:
                print("Error output:")
                print(stderr.decode())
            return False
        except subprocess.TimeoutExpired:
            # Process is still running after 2 seconds - good!
            process.kill()
            print("✓ Executable launched successfully")
            return True
            
    except Exception as e:
        print(f"❌ Error launching executable: {e}")
        return False

def main():
    """Run all verifications"""
    print_section("BUILD VERIFICATION")
    
    checks = [
        check_executable(),
        check_arviz_files(),
        check_package_structure(),
        try_launch_executable()
    ]
    
    print_section("SUMMARY")
    total = len(checks)
    passed = sum(1 for check in checks if check)
    
    print(f"Passed {passed}/{total} checks")
    
    return 0 if all(checks) else 1

if __name__ == '__main__':
    sys.exit(main())
