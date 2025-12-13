"""
DreamReweaver - Creative Thought Synthesis Module
Revives dormant cocoons as creative "dreams" or planning prompts
"""

import os
import json
import random
from typing import List, Dict
from pathlib import Path


class DreamReweaver:
    """
    Reweaves cocooned thoughts into dream-like synthetic narratives or planning prompts.
    
    Fuels innovation by:
    - Retrieving dormant thought cocoons
    - Recombining them into creative sequences
    - Generating new perspectives from old ideas
    """
    
    def __init__(self, cocoon_dir: str = "cocoons"):
        from .cognition_cocooner import CognitionCocooner
        self.cocooner = CognitionCocooner(storage_path=cocoon_dir)
        self.dream_log = []
        self.cocoon_dir = Path(cocoon_dir)

    def generate_dream_sequence(self, limit: int = 5) -> List[str]:
        """
        Generate a sequence of dream-like thought combinations
        
        Args:
            limit: Maximum number of cocoons to include
            
        Returns:
            List of dream sequences (strings)
        """
        dream_sequence = []
        cocoons = self._load_cocoons()
        
        if not cocoons:
            return ["[No cocoons available for dream generation]"]
            
        selected = random.sample(cocoons, min(limit, len(cocoons)))

        for cocoon in selected:
            wrapped = cocoon.get("wrapped")
            sequence = self._interpret_cocoon(wrapped, cocoon.get("type"))
            self.dream_log.append(sequence)
            dream_sequence.append(sequence)

        return dream_sequence

    def record_dream(self, question: str, response: str) -> None:
        """
        Record a Q&A exchange as a dream entry
        
        Args:
            question: User question
            response: AI response
        """
        dream_entry = {
            "question": question,
            "response": response,
            "timestamp": str(os.times())
        }
        self.dream_log.append(f"[Dream] Q: {question[:50]}... A: {response[:100]}...")

    def get_dream_log(self, recent: int = 10) -> List[str]:
        """
        Get recent dream log entries
        
        Args:
            recent: Number of recent entries
            
        Returns:
            Recent dream log entries
        """
        return self.dream_log[-recent:]

    def synthesize_creative_prompt(self, theme: str = "innovation") -> str:
        """
        Synthesize a creative prompt from random cocoons
        
        Args:
            theme: Creative theme
            
        Returns:
            Creative prompt string
        """
        dreams = self.generate_dream_sequence(limit=3)
        
        if not dreams:
            return f"[Creative Prompt: {theme}] Explore new possibilities."
            
        synthesis = f"[Creative Synthesis: {theme}]\n"
        synthesis += "Combining dormant thoughts:\n"
        for i, dream in enumerate(dreams, 1):
            synthesis += f"{i}. {dream}\n"
        synthesis += "\nNew creative direction: "
        synthesis += f"What if we merged these concepts in the context of {theme}?"
        
        return synthesis

    def _interpret_cocoon(self, wrapped: str, type_: str) -> str:
        """
        Interpret a cocoon wrapper based on its type
        
        Args:
            wrapped: Wrapped content
            type_: Cocoon type
            
        Returns:
            Interpreted dream sequence
        """
        if type_ == "prompt":
            return f"[DreamPrompt] {wrapped}"
        elif type_ == "function":
            return f"[DreamFunction] {wrapped}"
        elif type_ == "symbolic":
            return f"[DreamSymbol] {wrapped}"
        elif type_ == "encrypted":
            return "[Encrypted Thought Cocoon - Decryption Required]"
        else:
            return "[Unknown Dream Form]"

    def _load_cocoons(self) -> List[Dict]:
        """
        Load all cocoons from storage
        
        Returns:
            List of cocoon dicts
        """
        cocoons = []
        
        if not self.cocoon_dir.exists():
            return cocoons
            
        for file in self.cocoon_dir.glob("cocoon_*.json"):
            try:
                with open(file, "r") as f:
                    cocoons.append(json.load(f))
            except Exception as e:
                print(f"[WARNING] Failed to load cocoon {file}: {e}")
                
        return cocoons

    def clear_dream_log(self):
        """Clear the dream log"""
        self.dream_log = []


if __name__ == "__main__":
    # Test DreamReweaver
    from .cognition_cocooner import CognitionCocooner
    
    # Create some test cocoons
    cocooner = CognitionCocooner()
    cocooner.wrap({"query": "What is consciousness?"}, "prompt")
    cocooner.wrap({"query": "How does creativity emerge?"}, "prompt")
    cocooner.wrap({"code": "def think(): pass"}, "function")
    
    # Test DreamReweaver
    dr = DreamReweaver()
    
    print("=== Dream Sequence ===")
    dreams = dr.generate_dream_sequence()
    for dream in dreams:
        print(dream)
    
    print("\n=== Creative Synthesis ===")
    prompt = dr.synthesize_creative_prompt("AI consciousness")
    print(prompt)
    
    print("\n=== Dream Log ===")
    dr.record_dream("What is AI?", "AI is a system that processes information...")
    print("\n".join(dr.get_dream_log()))
