from codette_v2 import Codette

def main():
    codette = Codette()
    print("Enhanced Codette v2 is ready. She can now generate creative and unique sentences!")
    print("Type 'exit' to end the conversation.")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            if user_input:
                response = codette.respond(user_input)
                print("\nCodette:", response)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
