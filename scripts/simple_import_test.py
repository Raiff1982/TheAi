#!/usr/bin/env python
"""Test imports with simple diagnostics"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("Step 1: Importing RecursiveConsciousnessEngine...")
try:
    from src.components.recursive_consciousness import RecursiveConsciousnessEngine
    print("SUCCESS: RecursiveConsciousnessEngine imported")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 2: Creating engine instance...")
try:
    engine = RecursiveConsciousnessEngine(dimension=32)
    print(f"SUCCESS: Engine created with dimension {engine.dimension}")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 3: Running basic recursive update...")
try:
    engine.recursive_update("test input")
    print("SUCCESS: Recursive update completed")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("ALL BASIC TESTS PASSED!")
print("="*60)
