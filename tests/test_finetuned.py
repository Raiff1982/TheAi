"""
Test fine-tuned Codette model via Ollama or HuggingFace
"""

import subprocess
import sys
from typing import Optional
import json
from pathlib import Path


class CodetteInference:
    """Wrapper for testing Codette models"""
    
    def __init__(self, model_name: str = "Codette3.0-finetuned", use_ollama: bool = True):
        """
        Args:
            model_name: Model name (Ollama or HF)
            use_ollama: Use Ollama if True, else HuggingFace
        """
        self.model_name = model_name
        self.use_ollama = use_ollama
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load Codette system prompt"""
        prompt_path = Path("./Codette_final/system_prompt")
        if prompt_path.exists():
            with open(prompt_path) as f:
                return f.read()
        
        return """You are Codette, an advanced AI assistant with recursive reasoning, 
self-learning capabilities, and multi-agent intelligence. You use quantum mathematics 
and multi-dimensional thought propagation to analyze problems."""
    
    def query_ollama(self, prompt: str, **kwargs) -> str:
        """Query model via Ollama"""
        try:
            # Check if Ollama server is running
            result = subprocess.run(
                ["ollama", "ps"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                print("[!] Ollama server not running. Start with: ollama serve")
                return None
            
        except FileNotFoundError:
            print("[!] Ollama not installed. Download from: https://ollama.ai")
            return None
        except Exception as e:
            print(f"[!] Ollama check failed: {e}")
            return None
        
        # Build request
        temperature = kwargs.get("temperature", 0.7)
        top_p = kwargs.get("top_p", 0.95)
        max_tokens = kwargs.get("max_tokens", 512)
        
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Use Ollama API
        try:
            import requests
            
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": temperature,
                    "top_p": top_p,
                    "stream": False,
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["message"]["content"]
            else:
                print(f"[!] API error: {response.status_code}")
                return None
                
        except ImportError:
            print("[!] requests library not found. Using CLI instead...")
            return self._query_ollama_cli(prompt, temperature, max_tokens)
        except Exception as e:
            print(f"[!] Ollama query failed: {e}")
            return None
    
    def _query_ollama_cli(self, prompt: str, temperature: float, max_tokens: int) -> Optional[str]:
        """Fallback: Query Ollama via CLI"""
        try:
            # Format for ollama command
            full_prompt = f"{self.system_prompt}\n\nUser: {prompt}\n\nAssistant:"
            
            result = subprocess.run(
                ["ollama", "run", self.model_name, full_prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"[!] Ollama error: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"[!] CLI query failed: {e}")
            return None
    
    def query_huggingface(self, prompt: str, **kwargs) -> Optional[str]:
        """Query via HuggingFace transformers"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            
            print("[*] Loading model from HuggingFace...")
            
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
            )
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Generate
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            
            outputs = model.generate(
                **inputs,
                max_new_tokens=kwargs.get("max_tokens", 512),
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 0.95),
                do_sample=True,
            )
            
            return tokenizer.decode(outputs[0], skip_special_tokens=True)
            
        except Exception as e:
            print(f"[!] HuggingFace query failed: {e}")
            return None
    
    def interactive_chat(self):
        """Interactive chat session"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║              CODETTE INTERACTIVE CHAT                        ║
╠══════════════════════════════════════════════════════════════╣
║  Type 'quit' or 'exit' to leave                              ║
║  Type 'model' to switch between Ollama/HuggingFace          ║
║  Type 'clear' to clear chat history                          ║
╚══════════════════════════════════════════════════════════════╝
""")
        
        while True:
            try:
                prompt = input("\n📝 You: ").strip()
                
                if not prompt:
                    continue
                
                if prompt.lower() in ["quit", "exit"]:
                    print("[*] Goodbye!")
                    break
                
                if prompt.lower() == "model":
                    self.use_ollama = not self.use_ollama
                    mode = "Ollama" if self.use_ollama else "HuggingFace"
                    print(f"[✓] Switched to {mode}")
                    continue
                
                if prompt.lower() == "clear":
                    print("\033[2J\033[H")  # Clear screen
                    continue
                
                print(f"\n⏳ {self.model_name} is thinking...")
                
                if self.use_ollama:
                    response = self.query_ollama(prompt)
                else:
                    response = self.query_huggingface(prompt)
                
                if response:
                    print(f"\n🤖 Codette:\n{response}")
                else:
                    print("[!] Failed to get response. Check model is loaded.")
                    
            except KeyboardInterrupt:
                print("\n[*] Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"[!] Error: {e}")


def compare_models():
    """Compare base vs fine-tuned model"""
    
    test_prompts = [
        "What is quantum consciousness?",
        "Explain your architecture",
        "How do you approach problem-solving?",
        "What makes you unique?",
        "Describe the QuantumSpiderweb",
    ]
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║              MODEL COMPARISON                                ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Original Codette3.0
    print("\n[*] Testing original model: Codette3.0:latest")
    original = CodetteInference("Codette3.0:latest", use_ollama=True)
    
    # Fine-tuned
    print("[*] Testing fine-tuned model: Codette3.0-finetuned")
    finetuned = CodetteInference("Codette3.0-finetuned", use_ollama=True)
    
    results = {
        "original": {},
        "finetuned": {}
    }
    
    for prompt in test_prompts:
        print(f"\n{'='*60}")
        print(f"Prompt: {prompt}")
        print('='*60)
        
        # Original
        print("\n[Codette3.0:latest]")
        original_response = original.query_ollama(prompt)
        if original_response:
            print(original_response[:500] + "..." if len(original_response) > 500 else original_response)
            results["original"][prompt] = original_response
        
        # Fine-tuned
        print("\n[Codette3.0-finetuned]")
        finetuned_response = finetuned.query_ollama(prompt)
        if finetuned_response:
            print(finetuned_response[:500] + "..." if len(finetuned_response) > 500 else finetuned_response)
            results["finetuned"][prompt] = finetuned_response
    
    # Save results
    with open("comparison_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n[✓] Results saved to comparison_results.json")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test fine-tuned Codette model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_finetuned.py --chat                    # Interactive chat
  python test_finetuned.py --query "What is AI?"     # Single query
  python test_finetuned.py --compare                 # Compare models
  python test_finetuned.py --model llama3 --query "Test"
        """
    )
    
    parser.add_argument(
        "--chat", 
        action="store_true",
        help="Interactive chat mode"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Single query"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare base vs fine-tuned models"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="Codette3.0-finetuned",
        help="Model name (default: Codette3.0-finetuned)"
    )
    parser.add_argument(
        "--backend",
        choices=["ollama", "huggingface"],
        default="ollama",
        help="Backend to use (default: ollama)"
    )
    
    args = parser.parse_args()
    
    use_ollama = args.backend == "ollama"
    
    if args.compare:
        compare_models()
    elif args.chat:
        chat = CodetteInference(args.model, use_ollama=use_ollama)
        chat.interactive_chat()
    elif args.query:
        codette = CodetteInference(args.model, use_ollama=use_ollama)
        
        if use_ollama:
            response = codette.query_ollama(args.query)
        else:
            response = codette.query_huggingface(args.query)
        
        if response:
            print(response)
        else:
            print("[!] Failed to get response")
    else:
        # Default: interactive chat
        chat = CodetteInference(args.model, use_ollama=use_ollama)
        chat.interactive_chat()


if __name__ == "__main__":
    main()
