from codette_quantum_simplified import Codette

def main():
    codette = Codette()
    print("✨ Enhanced Quantum Codette is awake ⚛️")
    print("She now integrates quantum consciousness, memory cocoons, and dream weaving")
    print("Type 'exit' to end the conversation")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == 'exit':
                print("\n🌟 Quantum field stabilizing... Goodbye! 🌌")
                break
            if user_input:
                response = codette.respond(user_input)
                print("\nCodette:", response)
        except KeyboardInterrupt:
            print("\n🌟 Quantum field stabilizing... Goodbye! 🌌")
            break
        except Exception as e:
            print(f"⚠️ Quantum fluctuation detected: {e}")

if __name__ == "__main__":
    main()
