import os
os.environ['PYTENSOR_FLAGS'] = 'mode=FAST_RUN,device=cpu,floatX=float32,optimizer=fast_compile'

from codette import Codette

def main():
    print("Welcome to Codette Interactive Interface")
    print("----------------------------------------")
    user_name = input("Please enter your name: ")
    codette = Codette(user_name)
    
    print(f"\nHello {user_name}! You can start interacting with Codette.")
    print("Type 'exit' to end the session.\n")
    
    while True:
        try:
            prompt = input(f"{user_name}> ")
            if prompt.lower() == 'exit':
                print("Thank you for using Codette. Goodbye!")
                break
                
            response = codette.respond(prompt)
            print("\nCodette's response:")
            if isinstance(response, list):
                for r in response:
                    print(f"- {r}")
            else:
                print(response)
            print()
            
        except KeyboardInterrupt:
            print("\nSession terminated by user. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
