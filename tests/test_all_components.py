#!/usr/bin/env python3
"""
Comprehensive test to verify response variety across all components
"""
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def test_response_templates():
    """Test response templates module for variety"""
    print("=" * 70)
    print("TESTING RESPONSE TEMPLATES")
    print("=" * 70)
    
    from src.components.response_templates import ResponseTemplates
    
    templates = ResponseTemplates()
    
    # Test error responses
    print("\nError Response Variations (should be different):")
    error_responses = []
    for i in range(4):
        response = templates.get_error_response()
        error_responses.append(response)
        print(f"  {i+1}. {response[:60]}...")
    
    # Verify they're different
    if len(set(error_responses)) == len(error_responses):
        print("? Error responses vary")
    else:
        print("? Error responses are repeating!")
    
    # Test empty responses
    print("\nEmpty Response Variations (should be different):")
    empty_responses = []
    for i in range(4):
        response = templates.get_empty_response_fallback()
        empty_responses.append(response)
        print(f"  {i+1}. {response[:60]}...")
    
    if len(set(empty_responses)) == len(empty_responses):
        print("? Empty responses vary")
    else:
        print("? Empty responses are repeating!")
    
    # Test understanding prefixes
    print("\nUnderstanding Prefix Variations:")
    understanding = []
    for i in range(5):
        response = templates.get_understanding_prefix()
        understanding.append(response)
        print(f"  {i+1}. {response}")
    
    if len(set(understanding)) >= 4:
        print(f"? Understanding prefixes vary ({len(set(understanding))} unique)")
    else:
        print("? Understanding prefixes are repeating!")
    
    print("\n" + "=" * 70)

def test_codette_new():
    """Test codette_new.py response variety"""
    print("=" * 70)
    print("TESTING CODETTE_NEW RESPONSE VARIETY")
    print("=" * 70)
    
    try:
        from codette_new import Codette
        
        codette = Codette(user_name="TestUser")
        
        # Test greeting variations
        print("\nGreeting Response Variations:")
        greeting_responses = []
        for i in range(3):
            response = codette.respond("hello")
            greeting_responses.append(response)
            print(f"  {i+1}. {response[:70]}...")
        
        if len(set(greeting_responses)) == len(greeting_responses):
            print("? Greeting responses vary")
        else:
            print("? Greeting responses are repeating!")
        
        # Test identity variations
        print("\nIdentity Response Variations:")
        identity_responses = []
        for i in range(3):
            response = codette.respond("who are you")
            identity_responses.append(response)
            print(f"  {i+1}. {response[:70]}...")
        
        if len(set(identity_responses)) == len(identity_responses):
            print("? Identity responses vary")
        else:
            print("? Identity responses are repeating!")
        
        # Test personality variations
        print("\nPersonality Response Variations:")
        personality_responses = []
        for i in range(3):
            response = codette.respond("what makes you unique")
            personality_responses.append(response)
            print(f"  {i+1}. {response[:70]}...")
        
        if len(set(personality_responses)) == len(personality_responses):
            print("? Personality responses vary")
        else:
            print("? Personality responses are repeating!")
            
    except ImportError as e:
        print(f"? Could not import codette_new: {e}")
    
    print("\n" + "=" * 70)

def test_ai_core_components():
    """Test AICore components import correctly"""
    print("=" * 70)
    print("TESTING AI CORE COMPONENTS")
    print("=" * 70)
    
    try:
        from src.components.ai_core import AICore
        print("? AICore imports successfully")
        
        from src.components.ai_core_async_methods import generate_text_async
        print("? ai_core_async_methods imports successfully")
        
        from src.utils.response_processor import ResponseProcessor
        print("? ResponseProcessor imports successfully")
        
        from src.utils.response_verifier import ResponseVerifier
        print("? ResponseVerifier imports successfully")
        
        # Test instantiation
        try:
            ai_core = AICore(test_mode=True)
            print("? AICore instantiates successfully (test mode)")
        except Exception as e:
            print(f"? AICore instantiation failed: {e}")
        
        try:
            processor = ResponseProcessor()
            print("? ResponseProcessor instantiates successfully")
        except Exception as e:
            print(f"? ResponseProcessor instantiation failed: {e}")
        
        try:
            verifier = ResponseVerifier()
            print("? ResponseVerifier instantiates successfully")
        except Exception as e:
            print(f"? ResponseVerifier instantiation failed: {e}")
            
    except ImportError as e:
        print(f"? Import failed: {e}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    print("\n")
    print("?" + "=" * 68 + "?")
    print("?" + " RESPONSE LOOPING FIX - COMPREHENSIVE TEST ".center(68) + "?")
    print("?" + "=" * 68 + "?")
    print()
    
    # Run all tests
    test_response_templates()
    test_codette_new()
    test_ai_core_components()
    
    print("\n" + "?" + "=" * 68 + "?")
    print("?" + " TEST COMPLETE ".center(68) + "?")
    print("?" + " Check above for ? marks indicating successful variety ".center(68) + "?")
    print("?" + "=" * 68 + "?")
    print()
