#!/usr/bin/env python3
"""Test script for enhanced quantum_mathematics module"""

import sys
sys.path.insert(0, 'i:\\TheAI')

try:
    from quantum_mathematics import (
        QuantumMathematics,
        QuantumTensorAnalysis,
        QuantumInspiredML,
        demonstrate_quantum_mathematics
    )
    print("✓ All imports successful")
    print("\nRunning comprehensive test suite...\n")
    demonstrate_quantum_mathematics()
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
