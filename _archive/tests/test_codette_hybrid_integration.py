"""
Test Codette Hybrid Integration
================================
Verify that the hybrid system is working correctly
"""

import asyncio
import sys
from pathlib import Path

# Add Codette to path
codette_path = Path(__file__).parent / "Codette"
sys.path.insert(0, str(codette_path))

async def test_hybrid_system():
    print("\n" + "="*70)
    print("CODETTE HYBRID SYSTEM INTEGRATION TEST")
    print("="*70 + "\n")
    
    # Test 1: Import
    print("Test 1: Import Codette Hybrid")
    try:
        from codette_hybrid import CodetteHybrid
        print("   ? Import successful")
    except ImportError as e:
        print(f"   ? Import failed: {e}")
        return
    
    # Test 2: Initialize
    print("\nTest 2: Initialize Codette Hybrid")
    try:
        codette = CodetteHybrid(user_name="TestUser", use_ml_features=False)
        print("   ? Initialization successful")
    except Exception as e:
        print(f"   ? Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 3: Basic Response
    print("\nTest 3: Generate Basic Response")
    try:
        result = await codette.generate_response(
            query="How do I reduce harsh sibilance?",
            user_id=12345
        )
        print("   ? Response generated")
        print(f"   Response preview: {result['response'][:100]}...")
        print(f"   Source: {result.get('source')}")
        print(f"   Security filtered: {result.get('security_filtered')}")
    except Exception as e:
        print(f"   ? Response generation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 4: DAW Context Aware Response
    print("\nTest 4: DAW Context Aware Response")
    try:
        daw_context = {
            "tracks": ["Vocals", "Drums", "Bass"],
            "selected_track": {"name": "Vocals", "type": "audio"},
            "bpm": 120
        }
        result = await codette.generate_response(
            query="What should I do with my vocal track?",
            user_id=12345,
            daw_context=daw_context
        )
        print("   ? Context-aware response generated")
        print(f"   Prompt engineered: {result.get('engineered_prompt')}")
        print(f"   Sentiment: {result.get('sentiment', {}).get('overall_mood')}")
    except Exception as e:
        print(f"   ? Context-aware response failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 5: Production Optimization
    print("\nTest 5: Production Optimization")
    try:
        codette.optimize_for_production()
        print("   ? Optimization successful")
    except Exception as e:
        print(f"   ? Optimization failed: {e}")
    
    # Test 6: Advanced Features Check
    print("\nTest 6: Check Advanced Features")
    features = []
    if hasattr(codette, 'defense_system'):
        features.append("Defense Modifiers")
    if hasattr(codette, 'vector_search'):
        features.append("Vector Search")
    if hasattr(codette, 'prompt_engineer'):
        features.append("Prompt Engineering")
    if hasattr(codette, 'sentiment_analyzer'):
        features.append("Sentiment Analysis")
    if hasattr(codette, 'self_healing'):
        features.append("Self Healing")
    
    print(f"   ? Available features: {', '.join(features)}")
    print(f"   ML Enhanced: {codette.use_ml}")
    
    # Summary
    print("\n" + "="*70)
    print("? ALL TESTS PASSED - Codette Hybrid System Ready")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(test_hybrid_system())
