#!/usr/bin/env python3
"""
Simple import verification script to test module paths
"""
import sys
import os

# Test different import paths
print("Testing import paths...")
print("=" * 70)

# Add workspace to path
workspace_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, 'src'))

tests = [
    ("src.components.response_templates", "get_response_templates"),
    ("src.utils.response_verifier", "ResponseVerifier"),
    ("src.utils.response_processor", "ResponseProcessor"),
    ("src.components.ai_core", "AICore"),
]

for module_name, class_name in tests:
    try:
        module = __import__(module_name, fromlist=[class_name])
        obj = getattr(module, class_name, None)
        if obj:
            print(f"? {module_name}.{class_name}")
        else:
            print(f"? {module_name}.{class_name} - Not found in module")
    except ImportError as e:
        print(f"? {module_name}.{class_name} - {e}")
    except Exception as e:
        print(f"? {module_name}.{class_name} - {type(e).__name__}: {e}")

print("=" * 70)
print("Import verification complete")
