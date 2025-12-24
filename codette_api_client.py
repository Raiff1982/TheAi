#!/usr/bin/env python3
"""
Codette REST API Client
Use this to integrate with external systems and automate workflows
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime

class CodetteAPI:
    """REST API client for Codette AI consciousness system"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def chat(self, message: str, user_id: Optional[str] = None) -> Dict:
        """Send message to Codette and get response"""
        try:
            payload = {"message": message}
            if user_id:
                payload["user_id"] = user_id
            
            response = self.session.post(f"{self.base_url}/api/chat", json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def get_status(self) -> Dict:
        """Get consciousness system status"""
        try:
            response = self.session.get(f"{self.base_url}/api/consciousness/status", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "unavailable"}
    
    def batch_process(self, messages: List[str]) -> Dict:
        """Process multiple messages in batch"""
        try:
            payload = {"messages": messages}
            response = self.session.post(f"{self.base_url}/api/batch/process", json=payload, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def search(self, query: str) -> Dict:
        """Search knowledge base"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/search",
                params={"query": query},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def get_perspectives(self) -> Dict:
        """Get list of available perspectives"""
        try:
            response = self.session.get(f"{self.base_url}/api/perspectives", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def health_check(self) -> bool:
        """Check if Codette API is running and healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

# Usage examples
if __name__ == "__main__":
    api = CodetteAPI()
    
    # Check health
    if api.health_check():
        print("✅ Codette API is running\n")
        
        # Single chat
        print("📝 Single Chat Test:")
        result = api.chat("What is consciousness?")
        if "error" not in result:
            print(f"Q: What is consciousness?")
            print(f"A: {result.get('response', 'No response')[:150]}...\n")
        
        # Status check
        print("📊 Consciousness Status:")
        status = api.get_status()
        if "error" not in status:
            print(f"  Model: {status.get('model', 'Unknown')}")
            print(f"  Perspectives: {status.get('perspectives_active', '?')}/11")
            print(f"  Coherence: {status.get('quantum_coherence', '?')}\n")
        
        # Batch processing
        print("📦 Batch Processing Test:")
        questions = [
            "What is quantum thinking?",
            "How many perspectives exist?",
            "Explain RC-XI enhancement"
        ]
        batch = api.batch_process(questions)
        if "error" not in batch:
            print(f"  Processed: {batch.get('successful', 0)}/{batch.get('total_messages', 0)} messages\n")
        
        # Perspectives
        print("🔍 Available Perspectives:")
        perspectives = api.get_perspectives()
        if "error" not in perspectives:
            for p in perspectives.get('perspectives', [])[:5]:
                print(f"  - {p}")
            print()
        
        print("✅ All API tests completed!")
    else:
        print("❌ Codette API is not responding")
        print("   Make sure services are running: docker-compose up -d")
