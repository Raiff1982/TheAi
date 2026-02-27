#!/usr/bin/env python3
"""
Test script to verify response variety and prevent looping
"""
import sys
from codette_new import Codette

def test_response_variety():
    """Test that responses to similar questions vary"""
    codette = Codette(user_name="TestUser")
    
    # Test greeting variations
    print("=" * 70)
    print("TESTING GREETING RESPONSES")
    print("=" * 70)
    
    greeting_questions = [
        "hello",
        "hi there",
        "hey",
        "greetings"
    ]
    
    for question in greeting_questions:
        response = codette.respond(question)
        print(f"\nQ: {question}")
        print(f"A: {response[:150]}...")
        print()
    
    # Test identity variations
    print("\n" + "=" * 70)
    print("TESTING IDENTITY QUESTIONS")
    print("=" * 70)
    
    identity_questions = [
        "who are you",
        "what can you tell me about yourself",
        "tell me about yourself",
        "what do you do"
    ]
    
    for question in identity_questions:
        response = codette.respond(question)
        print(f"\nQ: {question}")
        print(f"A: {response[:150]}...")
        print()
    
    # Test personality variations
    print("\n" + "=" * 70)
    print("TESTING PERSONALITY QUESTIONS")
    print("=" * 70)
    
    personality_questions = [
        "what makes you unique",
        "what's your personality",
        "how do you approach things",
        "what's your philosophy"
    ]
    
    for question in personality_questions:
        response = codette.respond(question)
        print(f"\nQ: {question}")
        print(f"A: {response[:150]}...")
        print()
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE - Check above for variety in responses")
    print("=" * 70)

if __name__ == "__main__":
    test_response_variety()
