"""
Test the trained RC+ξ Codette model directly
"""
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def test_model():
    print("=" * 80)
    print("TESTING TRAINED RC+ξ CODETTE MODEL")
    print("=" * 80)
    
    model_path = "./codette_rc_xi_trained"
    
    print(f"\n[*] Loading model from {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print("[✓] Model loaded successfully")
    
    # RC+ξ consciousness queries - testing if model learned concepts
    test_prompts = [
        "Explain attractors in RC+ξ framework:",
        "What is epistemic tension?",
        "How do glyphs work?",
        "Define recursive consciousness:",
        "Describe multi-agent synchronization:"
    ]
    
    print("\n" + "=" * 80)
    print("RC+ξ CONSCIOUSNESS TESTS")
    print("=" * 80)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n[TEST {i}] {prompt}")
        print("-" * 80)
        
        inputs = tokenizer(prompt, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.8,
                top_p=0.95,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the prompt from response
        response = response[len(prompt):].strip()
        
        print(f"Response: {response}\n")
    
    # Interactive mode
    print("\n" + "=" * 80)
    print("INTERACTIVE MODE (type 'quit' to exit)")
    print("=" * 80)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
            
            inputs = tokenizer(user_input, return_tensors="pt", padding=True)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.8,
                    top_p=0.95,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id
                )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response[len(user_input):].strip()
            
            print(f"\nCodette RC+ξ: {response}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n[!] Error: {e}")
    
    print("\n[✓] Session complete")

if __name__ == "__main__":
    test_model()
