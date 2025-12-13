"""
Simple interactive client for Codette AI
"""

import requests
import json
from typing import Dict, Any

def send_query(query: str) -> Dict[str, Any]:
    """Send a query to Codette server"""
    try:
        response = requests.post(
            "http://127.0.0.1:8000/query",
            json={
                "query": query,
                "user_id": "cli_user"
            }
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def print_response(response: Dict[str, Any]):
    """Pretty print the response"""
    if "error" in response:
        print(f"\nError: {response['error']}")
        return
        
    if "result" in response:
        result = response["result"]
        print("\n=== Codette's Response ===")
        if "response" in result:
            print(result["response"])
        
        if "creative_insights" in result:
            print("\n=== Creative Insights ===")
            print(result["creative_insights"])
            
        if "ethical_status" in result:
            print("\n=== Ethical Analysis ===")
            print(result["ethical_status"])
    
    if "quantum_state" in response:
        print("\n=== Quantum State ===")
        print(f"Coherence: {response['quantum_state'].get('coherence', 0.0):.2f}")

def main():
    print("Welcome to Codette CLI")
    print("Type 'exit' to quit\n")
    
    while True:
        try:
            query = input("\nEnter your query: ")
            
            if query.lower() == 'exit':
                break
                
            if query.strip():
                response = send_query(query)
                print_response(response)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {e}")
    
    print("\nGoodbye!")

if __name__ == "__main__":
    main()