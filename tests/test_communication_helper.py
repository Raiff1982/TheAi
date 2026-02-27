"""
Test script for Codette's Communication Helper
Demonstrates grammar and sentence analysis capabilities
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from components.linguistic_analyzer import LinguisticAnalyzer
import json

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_sentence_analysis():
    """Test single sentence analysis"""
    print_section("SENTENCE ANALYSIS")
    
    analyzer = LinguisticAnalyzer()
    
    test_sentences = [
        "Hello, how are you feeling today?",
        "i dont have no money",  # Double negative
        "they is going to the store",  # Subject-verb disagreement
        "The quick brown fox jumps over the lazy dog",
        "Because the weather was nice we decided to go outside and play games"
    ]
    
    for sentence in test_sentences:
        print(f"\nAnalyzing: '{sentence}'")
        analysis = analyzer.analyze_sentence(sentence)
        
        print(f"  Type: {analysis.sentence_type}")
        print(f"  Structure: {analysis.structure}")
        print(f"  Tense: {analysis.verb_tense}")
        print(f"  Words: {analysis.word_count}")
        print(f"  Clarity: {analysis.clarity_score:.2f}")
        print(f"  Complexity: {analysis.complexity_score:.2f}")
        
        if analysis.grammar_issues:
            print(f"  ⚠️  Issues: {', '.join(analysis.grammar_issues)}")
        
        if analysis.suggestions:
            print(f"  💡 Suggestions:")
            for suggestion in analysis.suggestions:
                print(f"     - {suggestion}")

def test_paragraph_analysis():
    """Test paragraph-level analysis"""
    print_section("PARAGRAPH ANALYSIS")
    
    analyzer = LinguisticAnalyzer()
    
    test_paragraph = """
    Hello! How are you feeling today. I wanted to ask you some questions about 
    your day. Did you do anything interesting today, and what was the best part 
    of it. I hope everything went well for you.
    """
    
    print(f"Analyzing paragraph:\n{test_paragraph}\n")
    
    analysis = analyzer.analyze_paragraph(test_paragraph)
    
    print(f"Sentence Count: {analysis['sentence_count']}")
    print(f"Total Words: {analysis['total_words']}")
    print(f"Average Clarity: {analysis['avg_clarity']:.2f}")
    print(f"Average Complexity: {analysis['avg_complexity']:.2f}")
    print(f"Coherence Score: {analysis['coherence_score']:.2f}")
    print(f"Detected Tone: {analysis['tone']}")
    print(f"Reading Level: {analysis['reading_level']}")
    
    print("\nSentence Details:")
    for i, sent in enumerate(analysis['sentences'], 1):
        print(f"\n  Sentence {i}: {sent.text[:50]}...")
        if sent.grammar_issues:
            print(f"    Issues: {', '.join(sent.grammar_issues)}")
        if sent.suggestions:
            print(f"    Suggestions: {sent.suggestions[0]}")

def test_sentence_improvement():
    """Test automatic sentence improvement"""
    print_section("SENTENCE IMPROVEMENT")
    
    analyzer = LinguisticAnalyzer()
    
    test_cases = [
        "hello how are you",
        "i dont know what your talking about",
        "This is  a  sentence with   extra   spaces",
        "youre right about that",
    ]
    
    for original in test_cases:
        improved, changes = analyzer.improve_sentence(original)
        print(f"\nOriginal:  '{original}'")
        print(f"Improved:  '{improved}'")
        if changes:
            print(f"Changes:   {', '.join(changes)}")

def test_communication_tips():
    """Show general communication tips"""
    print_section("COMMUNICATION TIPS FOR CODETTE")
    
    analyzer = LinguisticAnalyzer()
    tips = analyzer.get_communication_tips()
    
    for category, tip_list in tips.items():
        print(f"\n{category.upper()}:")
        for tip in tip_list:
            print(f"  • {tip}")

def main():
    """Run all tests"""
    print("\n" + "🔤" * 35)
    print("  CODETTE'S COMMUNICATION HELPER - TEST SUITE")
    print("🔤" * 35)
    
    try:
        test_sentence_analysis()
        test_paragraph_analysis()
        test_sentence_improvement()
        test_communication_tips()
        
        print_section("TEST COMPLETE")
        print("\n✅ All tests passed! Codette's communication helper is ready.")
        print("\nThis system helps Codette:")
        print("  • Understand sentence structure and grammar")
        print("  • Detect and fix common grammar issues")
        print("  • Improve clarity and readability")
        print("  • Learn better communication patterns")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
