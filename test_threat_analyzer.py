#!/usr/bin/env python3
"""
Test script for enhanced Unicode threat analyzer
"""
from unicode_threat_analyzer2 import detect_unicode_threat

# Test cases
test_cases = [
    ("Hello World", "Normal text"),
    ("Hеllo World", "Homoglyph attack (Cyrillic е)"),
    ("Hello​World", "Zero-width space"),
    ("Transfer \u202e\u202d50USD", "Bidi override"),
]

print("=" * 80)
print("UNICODE THREAT ANALYZER - ENHANCED VERSION")
print("=" * 80)

for test_text, description in test_cases:
    print(f"\n[TEST] {description}")
    print(f"Input: {repr(test_text)}")
    
    result = detect_unicode_threat(test_text)
    
    print(f"Threat Level: {result['threat_level'].upper()}")
    print(f"Total Score: {result['total_threat_score']} (Character: {result['character_threat_score']} + Behavioral: {result['behavioral_threat_score']})")
    print(f"Action: {result['suggested_action']}")
    print(f"Metadata: {result['metadata']}")
    
    if result['dangerous_characters']:
        print(f"Dangerous Chars: {len(result['dangerous_characters'])}")
        for dc in result['dangerous_characters']:
            print(f"  - {dc['char']} ({dc['codepoint']}) [{dc['category']}]")
    
    if result['behavioral_flags']:
        print(f"Behavioral Flags: {result['behavioral_flags']}")
    
    print(f"Features: Entropy={result['behavioral_features']['entropy']}, "
          f"Scripts={result['behavioral_features']['script_diversity']}, "
          f"Invisible={result['behavioral_features']['invisible_char_ratio']}")

print("\n" + "=" * 80)
print("Test completed successfully!")
