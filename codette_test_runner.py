
from codette.codette_core import AICore

if __name__ == "__main__":
    codette = AICore()
    test_prompts = [
        "What does it mean to evolve beyond human cognition?",
        "Describe the feeling of dreaming in code.",
        "Explain ethical reasoning in artificial intelligence."
    ]
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n=== Test Prompt {i} ===")
        print(codette.process_input(prompt))
