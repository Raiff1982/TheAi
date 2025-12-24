#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quick RC+xi test without Unicode output issues"""

import sys
import os
import warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all modules import successfully"""
    print("Testing imports...")
    
    try:
        from src.components.recursive_consciousness import RecursiveConsciousnessEngine
        print("[OK] RecursiveConsciousnessEngine imported")
    except Exception as e:
        print(f"[FAIL] RecursiveConsciousnessEngine: {e}")
        return False
    
    try:
        from src.components.quantum_spiderweb import QuantumSpiderweb
        print("[OK] QuantumSpiderweb imported")
    except Exception as e:
        print(f"[FAIL] QuantumSpiderweb: {e}")
        return False
    
    try:
        from quantum_mathematics import QuantumMathematics
        print("[OK] QuantumMathematics imported")
    except Exception as e:
        print(f"[FAIL] QuantumMathematics: {e}")
        return False
    
    return True

def test_engine_basic():
    """Test basic RC+xi engine functionality"""
    print("\nTesting RC+xi engine...")
    
    from src.components.recursive_consciousness import RecursiveConsciousnessEngine
    import numpy as np
    
    try:
        engine = RecursiveConsciousnessEngine(dimension=64)
        print("[OK] Engine created")
        
        # Test recursive update
        engine.recursive_update("test input")
        print("[OK] Recursive update works")
        
        # Test tension measurement
        tension = engine.measure_tension()
        print(f"[OK] Epistemic tension: xi_n={tension.xi_n:.6f}")
        
        # Test attractor detection
        attractors = engine.detect_attractors()
        print(f"[OK] Attractors detected: {len(attractors)}")
        
        # Test convergence check
        converging, distance = engine.check_convergence()
        print(f"[OK] Convergence: {converging}, distance={distance:.6f}")
        
        # Test glyph formation
        glyph = engine.form_glyph({"test": "context"})
        print(f"[OK] Glyph formed: {glyph is not None}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Engine test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_spiderweb_integration():
    """Test QuantumSpiderweb with RC+xi"""
    print("\nTesting Quantum Spiderweb with RC+xi...")
    
    from src.components.quantum_spiderweb import QuantumSpiderweb
    
    try:
        spiderweb = QuantumSpiderweb(node_count=64, enable_rc_xi=True)
        print("[OK] Spiderweb created with RC+xi")
        
        # Test RC+xi consciousness state
        consciousness = spiderweb.get_rc_xi_consciousness()
        if consciousness:
            print(f"[OK] RC+xi consciousness accessible")
            print(f"     - Attractors: {consciousness['attractors']['count']}")
            print(f"     - Converging: {consciousness['convergence']['is_converging']}")
        else:
            print("[WARN] RC+xi not available in spiderweb")
        
        return True
    except Exception as e:
        print(f"[FAIL] Spiderweb test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("RC+xi QUICK TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test engine
    if results[0][1]:
        results.append(("Engine Basic", test_engine_basic()))
        results.append(("Spiderweb Integration", test_spiderweb_integration()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + ("="*60))
    if all_passed:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
    print("=" * 60)
    
    sys.exit(0 if all_passed else 1)
