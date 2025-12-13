"""
CognitionCocooner - Thought Encapsulation Module
Wraps active thoughts as persistable "cocoons" with optional AES encryption
"""

import json
import os
import random
from typing import Union, Dict, Any
from pathlib import Path

try:
    from cryptography.fernet import Fernet
    ENCRYPTION_AVAILABLE = True
except ImportError:
    ENCRYPTION_AVAILABLE = False
    print("[WARNING] cryptography not installed - encryption features disabled")
    print("   Install with: pip install cryptography")


class CognitionCocooner:
    """
    Encapsulates active "thoughts" as persistable "cocoons"
    
    Supports:
    - Plain text wrapping (prompts, functions, symbols)
    - AES-256 encryption for sensitive thoughts
    - Persistent storage on disk
    """
    
    def __init__(self, storage_path: str = "cocoons", encryption_key: bytes = None):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        if ENCRYPTION_AVAILABLE:
            self.key = encryption_key or Fernet.generate_key()
            self.fernet = Fernet(self.key)
        else:
            self.key = None
            self.fernet = None

    def wrap(self, thought: Dict[str, Any], type_: str = "prompt") -> str:
        """
        Wrap a thought as a cocoon and save to disk
        
        Args:
            thought: Thought content (dict)
            type_: Cocoon type ("prompt", "function", "symbolic")
            
        Returns:
            Cocoon ID for later retrieval
        """
        cocoon = {
            "type": type_,
            "id": f"cocoon_{random.randint(1000,9999)}",
            "wrapped": self._generate_wrapper(thought, type_)
        }
        file_path = self.storage_path / f"{cocoon['id']}.json"

        with open(file_path, "w") as f:
            json.dump(cocoon, f, indent=2)

        return cocoon["id"]

    def unwrap(self, cocoon_id: str) -> Union[str, Dict[str, Any]]:
        """
        Unwrap a cocoon by ID
        
        Args:
            cocoon_id: ID returned from wrap()
            
        Returns:
            Original thought content
        """
        file_path = self.storage_path / f"{cocoon_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Cocoon {cocoon_id} not found.")

        with open(file_path, "r") as f:
            cocoon = json.load(f)

        return cocoon["wrapped"]

    def wrap_encrypted(self, thought: Dict[str, Any]) -> str:
        """
        Wrap and encrypt a thought (requires cryptography)
        
        Args:
            thought: Thought content (dict)
            
        Returns:
            Encrypted cocoon ID
        """
        if not ENCRYPTION_AVAILABLE or not self.fernet:
            raise RuntimeError("Encryption not available - install cryptography package")
            
        encrypted = self.fernet.encrypt(json.dumps(thought).encode()).decode()
        cocoon = {
            "type": "encrypted",
            "id": f"cocoon_{random.randint(10000,99999)}",
            "wrapped": encrypted
        }
        file_path = self.storage_path / f"{cocoon['id']}.json"

        with open(file_path, "w") as f:
            json.dump(cocoon, f, indent=2)

        return cocoon["id"]

    def unwrap_encrypted(self, cocoon_id: str) -> Dict[str, Any]:
        """
        Unwrap and decrypt a cocoon
        
        Args:
            cocoon_id: ID from wrap_encrypted()
            
        Returns:
            Decrypted thought content
        """
        if not ENCRYPTION_AVAILABLE or not self.fernet:
            raise RuntimeError("Encryption not available - install cryptography package")
            
        file_path = self.storage_path / f"{cocoon_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Cocoon {cocoon_id} not found.")

        with open(file_path, "r") as f:
            cocoon = json.load(f)

        decrypted = self.fernet.decrypt(cocoon["wrapped"].encode()).decode()
        return json.loads(decrypted)

    def wrap_and_store(self, content: str, type_: str = "prompt") -> str:
        """
        Convenience method to wrap and store string content
        
        Args:
            content: String content to wrap
            type_: Cocoon type
            
        Returns:
            Cocoon ID
        """
        thought = {"content": content, "timestamp": str(os.times())}
        return self.wrap(thought, type_)

    def _generate_wrapper(self, thought: Dict[str, Any], type_: str) -> Union[str, Dict[str, Any]]:
        """
        Generate type-specific wrapper for thought
        
        Args:
            thought: Thought content
            type_: Wrapper type
            
        Returns:
            Wrapped content
        """
        if type_ == "prompt":
            return f"What does this mean in context? {thought}"
        elif type_ == "function":
            return f"def analyze(): return {thought}"
        elif type_ == "symbolic":
            return {k: round(v, 2) if isinstance(v, (int, float)) else v 
                   for k, v in thought.items()}
        else:
            return thought

    def list_cocoons(self) -> list:
        """List all cocoon IDs"""
        return [f.stem for f in self.storage_path.glob("cocoon_*.json")]

    def delete_cocoon(self, cocoon_id: str) -> bool:
        """Delete a cocoon by ID"""
        file_path = self.storage_path / f"{cocoon_id}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False


if __name__ == "__main__":
    # Test CognitionCocooner
    cocooner = CognitionCocooner()
    
    # Test plain wrapping
    thought = {"query": "What is consciousness?", "depth": 5}
    cocoon_id = cocooner.wrap(thought, "prompt")
    print(f"Created cocoon: {cocoon_id}")
    
    # Test unwrapping
    unwrapped = cocooner.unwrap(cocoon_id)
    print(f"Unwrapped: {unwrapped}")
    
    # Test encryption (if available)
    if ENCRYPTION_AVAILABLE:
        secret = {"password": "secret123", "api_key": "xyz"}
        encrypted_id = cocooner.wrap_encrypted(secret)
        print(f"Encrypted cocoon: {encrypted_id}")
        
        decrypted = cocooner.unwrap_encrypted(encrypted_id)
        print(f"Decrypted: {decrypted}")
    
    # List all
    print(f"All cocoons: {cocooner.list_cocoons()}")
