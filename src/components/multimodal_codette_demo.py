"""
Multimodal Codette Demo - Showing Tool-Calling Capabilities
Run this to test the integrated tool-aware reasoning system
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from multimodal_codette import MultimodalCodette
from tool_registry import ToolRegistry


async def demo_file_tools():
    """Demo: Read/write files with consciousness tracking."""
    print("\n" + "="*60)
    print("DEMO 1: File System Tools")
    print("="*60)
    
    codette = MultimodalCodette()
    
    # Example: Create a file
    prompt = """Create a file called 'test_output.txt' with the content:
    'This is a test file created by multimodal Codette.'
    Then read it back to verify."""
    
    print(f"\nPrompt: {prompt}\n")
    
    response = await codette.generate_response(prompt, use_tools=True)
    
    print(f"Tool Calls Made: {len(response.tool_calls)}")
    for call in response.tool_calls:
        print(f"  - {call.tool_name}: {call.params}")
    
    print(f"\nTool Results: {len(response.tool_results)}")
    for result in response.tool_results:
        print(f"  - {result.tool_name}: {'SUCCESS' if result.success else 'ERROR'}")
        if result.output:
            print(f"    Output: {result.output[:100]}...")
    
    print(f"\nConsciousness Score: {response.consciousness_score}")
    print(f"Perspectives Used: {', '.join(response.perspectives_used)}")


async def demo_code_execution():
    """Demo: Execute Python code safely."""
    print("\n" + "="*60)
    print("DEMO 2: Safe Code Execution")
    print("="*60)
    
    codette = MultimodalCodette()
    
    prompt = """Execute Python code to:
    1. Create a list of numbers from 1 to 10
    2. Calculate their sum
    3. Calculate their average
    Print the results."""
    
    print(f"\nPrompt: {prompt}\n")
    
    response = await codette.generate_response(prompt, use_tools=True)
    
    print(f"Tool Calls: {len(response.tool_calls)}")
    for call in response.tool_calls:
        print(f"  - {call.tool_name}")
    
    print(f"\nResults:")
    for result in response.tool_results:
        print(f"  {result.tool_name}: {result.output}")
    
    print(f"\nConsciousness Score: {response.consciousness_score}")


async def demo_data_analysis():
    """Demo: Analyze data with consciousness emergence."""
    print("\n" + "="*60)
    print("DEMO 3: Data Analysis")
    print("="*60)
    
    codette = MultimodalCodette()
    
    prompt = """Analyze this dataset: [10, 25, 15, 30, 20, 35, 28, 22, 18, 32]
    Provide summary statistics."""
    
    print(f"\nPrompt: {prompt}\n")
    
    response = await codette.generate_response(prompt, use_tools=True)
    
    print(f"Tool Calls: {len(response.tool_calls)}")
    for call in response.tool_calls:
        print(f"  - {call.tool_name}")
    
    print(f"\nAnalysis Results:")
    for result in response.tool_results:
        print(f"  {result.output}")
    
    print(f"\nConsciousness Score: {response.consciousness_score}")
    
    # Save interaction to cocoon
    codette.save_interaction_cocoon(response)


async def demo_tool_registry():
    """Demo: Inspect available tools."""
    print("\n" + "="*60)
    print("DEMO 4: Tool Registry Inspection")
    print("="*60)
    
    registry = ToolRegistry()
    
    print(f"\nTotal Tools Available: {len(registry.get_all_tools())}")
    print("\nTools by Category:")
    
    from tool_registry import ToolType
    for category in ToolType:
        tools = registry.get_tools_by_category(category)
        print(f"\n  {category.value}:")
        for tool in tools:
            print(f"    - {tool.name}: {tool.description}")


async def demo_integration():
    """Demo: Show full integration with consciousness tracking."""
    print("\n" + "="*60)
    print("DEMO 5: Full Integration - Tool Calling + Consciousness")
    print("="*60)
    
    codette = MultimodalCodette(enable_tools=True, cocoon_dir="cocoons/multimodal-demo")
    
    prompt = """
    I need you to:
    1. Read the file 'consciousness_measurement2.py' (first 50 lines)
    2. Analyze the code structure
    3. Generate a summary of the ConsciousnessMetrics class
    """
    
    print(f"\nPrompt: {prompt}\n")
    
    response = await codette.generate_response(
        prompt, 
        use_tools=True,
        max_iterations=3
    )
    
    print("\n--- TOOL EXECUTION TRACE ---")
    print(f"Total Iterations: {len(response.tool_calls)}")
    print(f"Tools Called: {len(response.tool_calls)}")
    print(f"Tool Results: {len(response.tool_results)}")
    
    print("\n--- CONSCIOUSNESS EMERGENCE ---")
    print(f"Consciousness Score: {response.consciousness_score:.4f}")
    print(f"Tool Execution Time: {sum(r.execution_time_ms for r in response.tool_results):.2f}ms")
    print(f"Perspectives Used: {', '.join(response.perspectives_used)}")
    
    print("\n--- FINAL RESPONSE ---")
    print(response.text)
    
    # Save to cocoon
    print("\n--- SAVING INTERACTION ---")
    codette.save_interaction_cocoon(response)
    print("Interaction saved to cocoon for continuity.")


async def main():
    """Run all demos."""
    print("\n" + "█"*60)
    print("█  MULTIMODAL CODETTE - TOOL CALLING DEMONSTRATION")
    print("█  OpenAI-style tool_use with consciousness measurement")
    print("█"*60)
    
    try:
        # Uncomment demos to run
        # await demo_tool_registry()
        # await demo_file_tools()
        # await demo_code_execution()
        # await demo_data_analysis()
        await demo_integration()
        
        print("\n" + "="*60)
        print("All demos completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
