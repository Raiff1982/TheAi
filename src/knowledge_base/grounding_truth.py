from typing import Dict, Any, List, Optional
import json
import os

class GroundingTruth:
    """
    Manages Codette's grounding truth system to prevent hallucination
    and ensure accurate responses.
    """
    
    def __init__(self, knowledge_base_path: str = "src/knowledge_base/core_truth.json"):
        self.knowledge_base_path = knowledge_base_path
        self.core_knowledge = self._load_knowledge_base()
        self.verification_cache = {}
        self.confidence_levels = {
            "VERIFIED": 1.0,
            "HIGHLY_LIKELY": 0.8,
            "PROBABLE": 0.6,
            "UNCERTAIN": 0.4,
            "SPECULATIVE": 0.2,
            "UNKNOWN": 0.0
        }
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load the core knowledge base from JSON file."""
        try:
            with open(self.knowledge_base_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading knowledge base: {str(e)}")
            return {}
            
    def verify_statement(self, statement: str, context: str = None) -> Dict[str, Any]:
        """
        Verify a statement against the grounding truth.
        
        Args:
            statement: The statement to verify
            context: Optional context category (e.g., "programming", "identity")
            
        Returns:
            Dict containing verification results
        """
        statement = statement.lower()
        
        # Check cache first
        cache_key = f"{context}:{statement}" if context else statement
        if cache_key in self.verification_cache:
            return self.verification_cache[cache_key]
            
        result = {
            "verified": False,
            "confidence": self.confidence_levels["UNKNOWN"],
            "source": None,
            "related_facts": [],
            "needs_clarification": False
        }
        
        # Check identity claims
        if any(word in statement for word in ["i am", "i can", "my name"]):
            result.update(self._verify_identity_claim(statement))
            
        # Check programming knowledge
        elif any(lang in statement for lang in self.core_knowledge.get("core_knowledge", {}).get("programming_languages", {})):
            result.update(self._verify_programming_knowledge(statement))
            
        # Check ethical principles
        elif any(word in statement for word in ["should", "must", "ethical", "right", "wrong"]):
            result.update(self._verify_ethical_principle(statement))
            
        # Cache the result
        self.verification_cache[cache_key] = result
        return result
    
    def _verify_identity_claim(self, statement: str) -> Dict[str, Any]:
        """Verify claims about Codette's identity and capabilities."""
        identity = self.core_knowledge.get("identity", {})
        result = {
            "verified": False,
            "confidence": self.confidence_levels["UNKNOWN"],
            "source": "identity_definition"
        }
        
        # Name verification
        if "my name" in statement:
            name_match = statement.find("codette") >= 0
            result["verified"] = name_match
            result["confidence"] = self.confidence_levels["VERIFIED"] if name_match else self.confidence_levels["UNKNOWN"]
            
        # Capability verification
        elif "i can" in statement:
            capabilities = identity.get("capabilities", [])
            capability_match = any(cap.lower() in statement for cap in capabilities)
            result["verified"] = capability_match
            result["confidence"] = self.confidence_levels["VERIFIED"] if capability_match else self.confidence_levels["UNKNOWN"]
            
        return result
    
    def _verify_programming_knowledge(self, statement: str) -> Dict[str, Any]:
        """Verify programming-related statements."""
        programming_langs = self.core_knowledge.get("core_knowledge", {}).get("programming_languages", {})
        result = {
            "verified": False,
            "confidence": self.confidence_levels["UNKNOWN"],
            "source": "programming_knowledge"
        }
        
        for lang, info in programming_langs.items():
            if lang in statement:
                # Verify specific attributes
                for attr, value in info.items():
                    if isinstance(value, list):
                        if any(v.lower() in statement for v in value):
                            result["verified"] = True
                            result["confidence"] = self.confidence_levels["VERIFIED"]
                    elif str(value).lower() in statement:
                        result["verified"] = True
                        result["confidence"] = self.confidence_levels["VERIFIED"]
                        
        return result
    
    def _verify_ethical_principle(self, statement: str) -> Dict[str, Any]:
        """Verify statements against ethical principles."""
        principles = self.core_knowledge.get("ethical_principles", {})
        result = {
            "verified": False,
            "confidence": self.confidence_levels["UNKNOWN"],
            "source": "ethical_principles"
        }
        
        core_values = principles.get("core_values", [])
        guidelines = principles.get("behavioral_guidelines", [])
        
        # Check against core values and guidelines
        for value in core_values + guidelines:
            if any(word.lower() in statement for word in value.lower().split()):
                result["verified"] = True
                result["confidence"] = self.confidence_levels["VERIFIED"]
                break
                
        return result
    
    def get_verified_response(self, query: str, response: str) -> str:
        """
        Process a response to ensure it aligns with grounding truth.
        
        Args:
            query: The original query
            response: The proposed response
            
        Returns:
            Verified and potentially modified response
        """
        verification = self.verify_statement(response)
        
        if not verification["verified"] and verification["confidence"] < self.confidence_levels["HIGHLY_LIKELY"]:
            # Add uncertainty qualifier
            response = f"Based on my current knowledge (confidence: {verification['confidence']:.1%}): {response}"
            
        if verification["needs_clarification"]:
            response += "\n\nNote: This response might need clarification. Please ask for specific details if needed."
            
        return response
    
    def add_verified_fact(self, fact: Dict[str, Any], category: str) -> bool:
        """
        Add a new verified fact to the knowledge base.
        
        Args:
            fact: The fact to add
            category: The category to add it to
            
        Returns:
            bool: Success status
        """
        try:
            # Deep copy the current knowledge
            current_knowledge = self.core_knowledge
            
            # Navigate to the correct category
            category_path = category.split('.')
            current_level = current_knowledge
            for path_part in category_path[:-1]:
                if path_part not in current_level:
                    current_level[path_part] = {}
                current_level = current_level[path_part]
                
            # Add the new fact
            final_category = category_path[-1]
            if final_category not in current_level:
                current_level[final_category] = {}
            current_level[final_category].update(fact)
            
            # Save back to file
            with open(self.knowledge_base_path, 'w') as f:
                json.dump(current_knowledge, f, indent=4)
                
            # Reload knowledge base
            self.core_knowledge = self._load_knowledge_base()
            
            return True
            
        except Exception as e:
            print(f"Error adding fact: {str(e)}")
            return False