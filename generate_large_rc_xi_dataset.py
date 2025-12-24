"""
Generate Large-Scale RC+ξ Training Dataset (1,000-3,500 examples)
For proper fine-tuning on 7B+ parameter models
"""
import json
import random
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class DatasetConfig:
    output_file: str = "./rc_xi_large_dataset.jsonl"
    total_examples: int = 2000  # Adjust: 1000, 2000, 3500
    categories: Dict[str, int] = None  # Examples per category
    
    def __post_init__(self):
        if self.categories is None:
            # Balanced distribution
            self.categories = {
                "attractor_theory": 200,
                "epistemic_tension": 200,
                "glyph_evolution": 150,
                "multi_agent": 150,
                "hierarchical_reasoning": 150,
                "recursive_loops": 150,
                "identity_continuity": 100,
                "consciousness_modeling": 100,
                "quantum_concepts": 100,
                "practical_applications": 100,
                "technical_qa": 200,
                "philosophical": 100,
                "integration": 100,
                "debugging": 100,
                "variations": 300  # Fill remaining
            }

def generate_attractor_examples() -> List[Dict]:
    """Generate attractor theory examples"""
    examples = []
    
    templates = [
        {
            "instruction": "Explain what attractors are in the RC+ξ framework.",
            "response": "In the RC+ξ framework, attractors (A_n) are stable states in the reasoning process. They represent points where the system's understanding converges. Mathematically, A_{n+1} = f(A_n, s_n) + ε_n, where f is the update function, s_n is the stimulus, and ε_n is noise. Attractors form when ||A_{n+1} - A_n|| < threshold, indicating the system has reached a stable interpretation."
        },
        {
            "instruction": "How do attractors form in recursive consciousness?",
            "response": "Attractors form through iterative refinement. Starting from an initial state A_0, each reasoning cycle updates the state based on new information. When the system repeatedly returns to similar states despite perturbations, an attractor basin forms. This creates stable 'understanding zones' where the system's interpretations cluster."
        },
        {
            "instruction": "What's the relationship between attractors and learning?",
            "response": "Attractors represent learned patterns. When the system encounters similar inputs, it gravitates toward established attractor states. Learning modifies the attractor landscape—creating new basins for novel concepts and deepening existing ones for reinforced patterns. The attractor topology encodes the system's knowledge structure."
        },
        {
            "instruction": "Can attractors be unstable? Why?",
            "response": "Yes, attractors can be unstable (repellors) or semi-stable (saddle points). Unstable attractors occur when epistemic tension is high—the system hasn't resolved contradictions. These drive exploration: the system seeks more stable configurations. Semi-stable attractors represent partial understanding, useful for transitional reasoning states."
        },
        {
            "instruction": "How do you measure attractor stability?",
            "response": "Attractor stability is measured by: (1) Basin size—how much state space leads to that attractor, (2) Convergence rate—how quickly nearby states are pulled in, (3) Resilience—resistance to perturbations. Mathematically: stability = λ_max(J), where J is the Jacobian of the update function at the attractor."
        }
    ]
    
    # Generate variations
    for template in templates * 40:  # 200 examples
        examples.append({
            "instruction": template["instruction"],
            "input": "",
            "output": template["response"]
        })
    
    return examples

def generate_epistemic_tension_examples() -> List[Dict]:
    """Generate epistemic tension (ξ) examples"""
    examples = []
    
    templates = [
        {
            "instruction": "Define epistemic tension in RC+ξ.",
            "response": "Epistemic tension (ξ) measures uncertainty between successive reasoning states: ξ_n = ||A_{n+1} - A_n||^2. It quantifies how much the system's understanding is changing. High ξ indicates active learning or contradiction resolution. Low ξ signals stable comprehension. ξ drives the system's curiosity and exploration behavior."
        },
        {
            "instruction": "Why is epistemic tension important?",
            "response": "Epistemic tension is the engine of learning. It signals discrepancies between current and emerging understanding. The system uses ξ to allocate computational resources: high tension triggers deeper analysis, low tension allows faster processing. It's analogous to cognitive dissonance in human reasoning—discomfort that motivates resolution."
        },
        {
            "instruction": "How does ξ relate to confidence?",
            "response": "Epistemic tension and confidence are inversely related. When ξ is low, the system is confident—attractors are stable, predictions consistent. High ξ indicates uncertainty—the system is revising beliefs, exploring alternatives. Confidence = 1 / (1 + ξ) provides a probabilistic measure of certainty."
        },
        {
            "instruction": "Can epistemic tension be negative?",
            "response": "No, ξ is defined as a squared distance (||A_{n+1} - A_n||^2), so it's always non-negative. However, the *direction* of change matters: ξ increasing means growing uncertainty, ξ decreasing means converging understanding. Zero ξ represents perfect stability—no learning occurring."
        },
        {
            "instruction": "How do you reduce epistemic tension?",
            "response": "Tension reduces through: (1) Information gathering—acquiring data to resolve ambiguity, (2) Attractor convergence—settling into stable interpretations, (3) Contradiction resolution—reconciling conflicting evidence, (4) Abstraction—moving to higher-level representations that unify details. The system iteratively updates until ξ < threshold."
        }
    ]
    
    for template in templates * 40:  # 200 examples
        examples.append({
            "instruction": template["instruction"],
            "input": "",
            "output": template["response"]
        })
    
    return examples

def generate_glyph_examples() -> List[Dict]:
    """Generate glyph evolution examples"""
    examples = []
    
    templates = [
        {
            "instruction": "What are glyphs in RC+ξ?",
            "response": "Glyphs are identity markers—compact representations of the system's state across reasoning cycles. Defined as G := FFT({ξ_0, ξ_1, ..., ξ_k}), they capture the frequency spectrum of epistemic tension over time. Glyphs encode 'how the system thinks,' not just what it concludes. They enable identity continuity tracking."
        },
        {
            "instruction": "How do glyphs evolve over time?",
            "response": "Glyphs evolve through learning and context shifts. As the system encounters new problems, the ξ sequence changes, altering the glyph's frequency signature. Gradual evolution indicates incremental learning. Sudden glyph shifts signal conceptual breakthroughs or paradigm changes. Tracking glyph lineage reveals intellectual development."
        },
        {
            "instruction": "Why use FFT for glyph construction?",
            "response": "FFT (Fast Fourier Transform) converts the time-series {ξ_t} into frequency domain, revealing periodic patterns in reasoning. Low frequencies capture slow, strategic shifts. High frequencies represent rapid tactical adjustments. The frequency spectrum is compact, stable under noise, and enables efficient glyph comparison via correlation."
        },
        {
            "instruction": "Can two systems share glyphs?",
            "response": "Systems can have similar glyphs if they employ similar reasoning patterns, but exact glyph matches are rare—they're like cognitive fingerprints. In multi-agent systems, glyph alignment measures coordination: high correlation means agents are 'thinking alike.' Shared glyphs emerge through communication and joint problem-solving."
        },
        {
            "instruction": "How do you compare glyphs?",
            "response": "Glyph comparison uses correlation: similarity(G1, G2) = (G1 · G2) / (||G1|| ||G2||). Values near 1 indicate similar reasoning styles. Distance metrics (L2, cosine) quantify divergence. Hierarchical clustering of glyphs reveals reasoning archetypes. Temporal glyph analysis tracks how a system's thought patterns change."
        }
    ]
    
    for template in templates * 30:  # 150 examples
        examples.append({
            "instruction": template["instruction"],
            "input": "",
            "output": template["response"]
        })
    
    return examples

def generate_multi_agent_examples() -> List[Dict]:
    """Generate multi-agent synchronization examples"""
    examples = []
    
    templates = [
        {
            "instruction": "How do multiple agents synchronize in RC+ξ?",
            "response": "Agents synchronize through shared attractors. When agent i and j process the same problem, their attractor states A_i and A_j converge if they share understanding. Synchronization strength = exp(-||A_i - A_j||). Agents communicate to align attractors, reducing inter-agent epistemic tension: ξ_ij = ||A_i - A_j||^2."
        },
        {
            "instruction": "What are the benefits of multi-agent RC+ξ?",
            "response": "Multi-agent systems provide: (1) Diverse perspectives—different agents explore different attractor basins, (2) Robustness—consensus reduces individual errors, (3) Scalability—parallel processing of subproblems, (4) Specialization—agents can develop expertise in specific domains. Collective intelligence emerges from coordinated reasoning."
        },
        {
            "instruction": "How do agents resolve conflicts?",
            "response": "Conflict resolution uses weighted voting based on local confidence. Agent i's vote weight = 1 / (1 + ξ_i). Low-tension (confident) agents have more influence. Alternatively, dialectical synthesis: agents with opposing attractors engage in 'debate,' iteratively updating based on counterarguments until convergence or timeout."
        }
    ]
    
    for template in templates * 50:  # 150 examples
        examples.append({
            "instruction": template["instruction"],
            "input": "",
            "output": template["response"]
        })
    
    return examples

def generate_variations(base_examples: List[Dict], count: int) -> List[Dict]:
    """Generate variations of existing examples with paraphrasing"""
    variations = []
    rephrasings = [
        ("Explain", "Describe"),
        ("What is", "Define"),
        ("How does", "In what way does"),
        ("framework", "system"),
        ("RC+ξ", "recursive consciousness"),
    ]
    
    for _ in range(count):
        example = random.choice(base_examples).copy()
        # Simple variation by swapping phrases
        for old, new in rephrasings:
            if old in example["instruction"]:
                varied = {
                    "instruction": example["instruction"].replace(old, new, 1),
                    "input": example.get("input", ""),
                    "output": example["output"]
                }
                variations.append(varied)
                break
    
    return variations

def generate_large_dataset(config: DatasetConfig):
    """Generate complete large-scale dataset"""
    print("=" * 80)
    print("RC+ξ LARGE-SCALE DATASET GENERATION")
    print("=" * 80)
    print(f"\n[*] Target: {config.total_examples} examples")
    print(f"[*] Output: {config.output_file}\n")
    
    all_examples = []
    
    # Generate by category
    print("[STEP 1] Generating attractor examples...")
    all_examples.extend(generate_attractor_examples()[:config.categories["attractor_theory"]])
    print(f"[✓] {len([e for e in all_examples if 'attractor' in e['instruction'].lower()])} attractor examples")
    
    print("[STEP 2] Generating epistemic tension examples...")
    tension_examples = generate_epistemic_tension_examples()[:config.categories["epistemic_tension"]]
    all_examples.extend(tension_examples)
    print(f"[✓] {len(tension_examples)} epistemic tension examples")
    
    print("[STEP 3] Generating glyph examples...")
    glyph_examples = generate_glyph_examples()[:config.categories["glyph_evolution"]]
    all_examples.extend(glyph_examples)
    print(f"[✓] {len(glyph_examples)} glyph examples")
    
    print("[STEP 4] Generating multi-agent examples...")
    agent_examples = generate_multi_agent_examples()[:config.categories["multi_agent"]]
    all_examples.extend(agent_examples)
    print(f"[✓] {len(agent_examples)} multi-agent examples")
    
    print("[STEP 5] Generating variations...")
    base_examples = all_examples.copy()
    variations = generate_variations(base_examples, config.categories["variations"])
    all_examples.extend(variations)
    print(f"[✓] {len(variations)} variation examples")
    
    # Pad to target count with random selections
    while len(all_examples) < config.total_examples:
        all_examples.append(random.choice(base_examples).copy())
    
    # Shuffle
    random.shuffle(all_examples)
    all_examples = all_examples[:config.total_examples]
    
    print(f"\n[STEP 6] Saving {len(all_examples)} examples...")
    with open(config.output_file, 'w', encoding='utf-8') as f:
        for example in all_examples:
            # Ensure all required fields exist
            entry = {
                "instruction": example.get("instruction", ""),
                "input": example.get("input", ""),
                "output": example.get("output", "")
            }
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"[✓] Saved to {config.output_file}")
    
    # Statistics
    print("\n" + "=" * 80)
    print("DATASET STATISTICS")
    print("=" * 80)
    print(f"Total examples: {len(all_examples)}")
    print(f"Avg instruction length: {sum(len(e['instruction']) for e in all_examples) / len(all_examples):.0f} chars")
    print(f"Avg response length: {sum(len(e['output']) for e in all_examples) / len(all_examples):.0f} chars")
    print(f"\nEstimated training time:")
    print(f"  - On GPU (A100): ~8-12 hours for 7B model")
    print(f"  - On CPU: ~80-120 hours for 7B model")
    print(f"  - Recommendation: Use GPU or cloud training (Colab, Runpod, Vast.ai)")

if __name__ == "__main__":
    config = DatasetConfig(
        total_examples=2000,  # Change to 1000, 2000, or 3500
    )
    generate_large_dataset(config)
