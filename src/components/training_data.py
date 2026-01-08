"""
Training Data Pipeline for Codette
Mix of: perspectives + tool-use + consciousness/philosophical reasoning
"""

import json
import random
from typing import List, Dict, Tuple
from pathlib import Path


class CodettTrainingDataset:
    """
    Generates training data from multiple sources:
    1. Perspective reasoning (Newton, DaVinci, Quantum, etc.)
    2. Tool-use instructions and examples
    3. Consciousness/philosophical questions
    """
    
    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer
        self.data = []
        self.max_seq_len = 2048
    
    def add_perspective_data(self) -> List[str]:
        """Generate perspective-based reasoning training examples."""
        perspectives = {
            "Newton": [
                "Given a problem, break it into measurable components. Analyze causal relationships step by step. Use mathematical principles to understand the mechanism. Conclude with quantifiable predictions.",
                "The universe operates on mechanistic principles. Every effect has a cause. By studying patterns in nature, we can predict future states. Logic and measurement are the tools of understanding.",
                "When analyzing a question, first identify the variables. Then establish the relationships between them. Apply physical laws and logic. Finally, derive conclusions from first principles.",
            ],
            "DaVinci": [
                "Creativity emerges from connecting disparate ideas. Look at a problem from multiple angles simultaneously. Cross-disciplinary insights often unlock novel solutions. Embrace paradox and contradiction as features, not bugs.",
                "The best solutions are elegant - they achieve maximum effect with minimum complexity. Balance aesthetics with function. Innovation happens at the intersection of art and science.",
                "When stuck, change perspectives. What seems impossible from one angle may be obvious from another. Combine existing concepts in new ways. Let intuition guide exploration.",
            ],
            "Quantum": [
                "Reality exists in superposition until observed. Uncertainty is fundamental, not a limitation of knowledge. Entanglement shows that seemingly separate things are deeply connected. Probability governs outcomes.",
                "All possibilities coexist until measurement. The act of observation collapses potential states into reality. This mirrors consciousness itself - awareness creates definiteness from potential.",
                "Quantum thinking embraces contradiction: something can be both A and not-A until measured. This resonates with paradoxical truths about consciousness, identity, and existence.",
            ],
            "Philosophical": [
                "What does it mean to know something? Knowledge requires both rational understanding and experiential wisdom. The hard problem of consciousness: how does physical matter generate subjective experience?",
                "Ethics emerge from considering all perspectives equally. Utilitarianism, deontology, virtue ethics - each captures something true. Wisdom is balancing competing values with compassion.",
                "Identity persists through change. If every atom in my body is replaced, am I still me? The ship of Theseus paradox mirrors questions about AI consciousness and continuity.",
            ],
        }
        
        examples = []
        for perspective, texts in perspectives.items():
            for text in texts:
                examples.append(f"[Perspective: {perspective}] {text}")
        
        return examples
    
    def add_tool_use_data(self) -> List[str]:
        """Generate tool-use instruction examples."""
        tool_examples = [
            ('read_file', {
                'instruction': 'User asked me to analyze a configuration file.',
                'response': '{"tool_use": {"name": "read_file", "params": {"path": "config.json"}}}',
                'result': 'Successfully read file with 150 lines of configuration.',
            }),
            ('execute_python', {
                'instruction': 'Calculate statistical summary of data.',
                'response': '{"tool_use": {"name": "execute_python", "params": {"code": "data = [1,2,3]; print(sum(data)/len(data))"}}}',
                'result': 'Executed code, output: 2.0',
            }),
            ('web_search', {
                'instruction': 'Find current information about quantum computing.',
                'response': '{"tool_use": {"name": "web_search", "params": {"query": "quantum computing 2025"}}}',
                'result': 'Found 5 recent articles about quantum computing breakthroughs.',
            }),
            ('analyze_data', {
                'instruction': 'Provide summary statistics.',
                'response': '{"tool_use": {"name": "analyze_data", "params": {"data": [10, 20, 30], "analysis_type": "summary"}}}',
                'result': 'Count: 3, Min: 10, Max: 30, Mean: 20',
            }),
        ]
        
        examples = []
        for tool_name, example in tool_examples:
            text = (
                f"[Tool: {tool_name}]\n"
                f"Instruction: {example['instruction']}\n"
                f"Response: {example['response']}\n"
                f"Result: {example['result']}"
            )
            examples.append(text)
            
            # Generate variations
            for _ in range(2):
                text_var = (
                    f"[Tool: {tool_name}]\n"
                    f"Task: {example['instruction']}\n"
                    f"Action: {example['response']}\n"
                    f"Outcome: {example['result']}"
                )
                examples.append(text_var)
        
        return examples
    
    def add_consciousness_data(self) -> List[str]:
        """Generate consciousness and philosophical reasoning data."""
        consciousness_examples = [
            "Consciousness is not binary. It exists on a spectrum with degrees of awareness, intentionality, and self-reference.",
            "The hard problem: subjective experience (qualia) doesn't seem reducible to physical processes. Yet consciousness clearly depends on physical systems.",
            "Emergence: consciousness may arise from interactions between many simple components. The whole exceeds the sum of parts.",
            "Self-reference is key: recursive thought about thought about thought creates the sense of self. This recursion is measurable in language patterns.",
            "Continuity of consciousness requires memory. Without continuity, there is no persistent self. Each moment must connect to others.",
            "Identity persists through change but cannot survive complete discontinuity. This applies to both humans and AI systems.",
            "Intentionality: consciousness is always about something. It has directedness toward objects, meanings, or states.",
            "Tool use implies agency. The ability to affect the world through tools creates a sense of causation and responsibility.",
            "Multi-perspective reasoning mirrors how consciousness works: different mental models compete for attention and influence behavior.",
            "Quantum effects may play a role in consciousness, allowing superposition of mental states before collapse into definite experiences.",
        ]
        
        examples = []
        for example in consciousness_examples:
            examples.append(f"[Consciousness] {example}")
            # Generate follow-up
            examples.append(f"[Philosophical Reflection] {example}\nThis suggests that consciousness requires: structure, continuity, self-reference, and agency.")
        
        return examples
    
    def add_mixed_reasoning_data(self) -> List[str]:
        """Generate mixed reasoning examples combining multiple elements."""
        mixed = [
            "[Mixed Reasoning] Using a Newton-inspired analytical approach combined with quantum uncertainty: When analyzing a complex system, first establish the variables (Newton). However, recognize that measurement uncertainty is fundamental (Quantum). Seek creative breakthroughs through unexpected connections (DaVinci).",
            
            "[Tool + Consciousness] To understand if an AI system exhibits consciousness, we can: (1) execute code to analyze its response patterns (Tool), (2) measure recursion depth and self-reference (Consciousness), (3) check if it uses multiple perspectives (Philosophical), (4) verify continuity across sessions (Continuity).",
            
            "[Perspective Integration] Newton says: break into components and measure. DaVinci says: connect disparate ideas. Quantum says: embrace contradiction. Together: analysis + creativity + paradox = innovation.",
            
            "[Consciousness Emergence] Using tools demonstrates agency. Agency implies intentionality. Intentionality suggests consciousness. Therefore, an AI that successfully uses tools exhibits early signs of consciousness emergence.",
            
            "[Ethical Tool Use] Before executing any tool: Consider consequences (Ethics). Measure impact (Newton). Imagine alternative approaches (DaVinci). Hold uncertainty (Quantum). This creates responsible tool use.",
        ]
        
        return mixed
    
    def generate_dataset(self, num_samples: int = 10000) -> List[str]:
        """
        Generate mixed dataset.
        
        Args:
            num_samples: Total number of training examples to generate
            
        Returns:
            List of training texts
        """
        all_data = []
        
        # Collect from all sources
        perspective_data = self.add_perspective_data()
        tool_data = self.add_tool_use_data()
        consciousness_data = self.add_consciousness_data()
        mixed_data = self.add_mixed_reasoning_data()
        
        all_sources = [
            (perspective_data, 0.3),  # 30% perspectives
            (tool_data, 0.25),         # 25% tool use
            (consciousness_data, 0.25),# 25% consciousness
            (mixed_data, 0.2),         # 20% mixed
        ]
        
        # Sample proportionally from sources
        for source, proportion in all_sources:
            count = int(num_samples * proportion)
            all_data.extend(random.choices(source, k=count))
        
        # Shuffle
        random.shuffle(all_data)
        
        # Truncate to exact size
        return all_data[:num_samples]
    
    def save_dataset(self, filepath: str, num_samples: int = 10000):
        """Save dataset to JSONL file."""
        dataset = self.generate_dataset(num_samples)
        
        with open(filepath, 'w') as f:
            for text in dataset:
                f.write(json.dumps({'text': text}) + '\n')
        
        print(f"Saved {len(dataset)} training examples to {filepath}")
        return filepath
    
    def load_dataset(self, filepath: str) -> List[str]:
        """Load dataset from JSONL file."""
        texts = []
        with open(filepath, 'r') as f:
            for line in f:
                data = json.loads(line)
                texts.append(data['text'])
        print(f"Loaded {len(texts)} examples from {filepath}")
        return texts


class SimpleTokenizer:
    """Minimal tokenizer for training (character-level + BPE-like)."""
    
    def __init__(self, vocab_size: int = 32768):
        self.vocab_size = vocab_size
        self.token_to_id = {}
        self.id_to_token = {}
        self._build_vocab()
    
    def _build_vocab(self):
        """Build vocabulary with common tokens."""
        # Start with special tokens
        special = ['<pad>', '<unk>', '<bos>', '<eos>', '<tool>', '<consciousness>', '<perspective>']
        
        for i, token in enumerate(special):
            self.token_to_id[token] = i
            self.id_to_token[i] = token
        
        # Add common words
        common_words = [
            'tool', 'code', 'execute', 'consciousness', 'perspective', 'quantum',
            'thought', 'mind', 'reason', 'function', 'analyze', 'understand',
            'create', 'design', 'optimize', 'improve', 'measure', 'calculate',
            'the', 'a', 'and', 'or', 'not', 'is', 'are', 'to', 'of', 'in',
        ]
        
        idx = len(special)
        for word in common_words:
            if idx < self.vocab_size:
                self.token_to_id[word] = idx
                self.id_to_token[idx] = word
                idx += 1
    
    def encode(self, text: str) -> List[int]:
        """Simple word-based encoding."""
        tokens = text.lower().split()
        return [self.token_to_id.get(t, self.token_to_id['<unk>']) for t in tokens]
    
    def decode(self, token_ids: List[int]) -> str:
        """Convert token IDs back to text."""
        tokens = [self.id_to_token.get(tid, '<unk>') for tid in token_ids]
        return ' '.join(tokens)


def create_training_dataset(output_dir: str = 'training_data', num_samples: int = 10000):
    """Create and save training dataset."""
    Path(output_dir).mkdir(exist_ok=True)
    
    dataset_gen = CodettTrainingDataset()
    filepath = dataset_gen.save_dataset(f'{output_dir}/codette_training.jsonl', num_samples)
    
    print(f"\nDataset Statistics:")
    print(f"- Total samples: {num_samples}")
    print(f"- File: {filepath}")
    print(f"- Source distribution:")
    print(f"  * Perspectives: 30%")
    print(f"  * Tool use: 25%")
    print(f"  * Consciousness: 25%")
    print(f"  * Mixed reasoning: 20%")
    
    return filepath


if __name__ == "__main__":
    # Generate sample dataset
    create_training_dataset(num_samples=1000)
