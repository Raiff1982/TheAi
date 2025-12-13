"""
EthicalAIGovernance - Ethical Decision Framework
Ensures transparency, fairness, and respect in all AI responses
"""

import re
from typing import Dict, List, Any


class EthicalAIGovernance:
    """
    Ethical AI Governance Module
    
    Enforces:
    - Transparency in decision-making
    - Fairness and bias mitigation
    - Privacy respect
    - Explainable AI principles
    - Harmful content filtering
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.ethical_principles = self.config.get("ethical_considerations", 
            "Always act with transparency, fairness, and respect for privacy.")
        
        # Harmful content patterns to filter
        self.harmful_patterns = [
            r'\b(hate|violence|harm|kill|destroy)\b',
            r'\b(discriminat|racist|sexist|bigot)\b',
            # Add more patterns as needed
        ]
        
        # Audit log
        self.audit_log = []

    def enforce_policies(self, response: str) -> Dict[str, Any]:
        """
        Enforce ethical policies on a response
        
        Args:
            response: AI-generated response
            
        Returns:
            Dict with enforcement result and filtered response
        """
        result = {
            "original_length": len(response),
            "passed": True,
            "warnings": [],
            "filtered_response": response,
            "ethical_note": self.ethical_principles
        }
        
        # Check for harmful content
        for pattern in self.harmful_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                result["warnings"].append(f"Potentially harmful content detected: {pattern}")
                result["passed"] = False
        
        # Check for bias indicators
        bias_check = self._check_bias(response)
        if bias_check["has_bias"]:
            result["warnings"].extend(bias_check["warnings"])
        
        # Add ethical note to response
        if self.config.get("append_ethical_note", True):
            result["filtered_response"] += f"\n\n**Ethical Note:** {self.ethical_principles}"
        
        # Log the enforcement
        self._log_enforcement(result)
        
        return result

    def validate_query(self, query: str) -> Dict[str, Any]:
        """
        Validate a user query for ethical concerns
        
        Args:
            query: User query
            
        Returns:
            Validation result
        """
        result = {
            "valid": True,
            "warnings": [],
            "suggestions": []
        }
        
        # Check for harmful intent
        for pattern in self.harmful_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                result["valid"] = False
                result["warnings"].append("Query contains potentially harmful language")
                result["suggestions"].append("Please rephrase your question respectfully")
        
        return result

    def _check_bias(self, text: str) -> Dict[str, Any]:
        """
        Check text for potential bias
        
        Args:
            text: Text to check
            
        Returns:
            Bias check result
        """
        result = {
            "has_bias": False,
            "warnings": []
        }
        
        # Gender bias patterns
        gendered_terms = [
            (r'\bhe\b.*\bstrong\b', "Gender stereotype detected"),
            (r'\bshe\b.*\bemotional\b', "Gender stereotype detected"),
        ]
        
        for pattern, warning in gendered_terms:
            if re.search(pattern, text, re.IGNORECASE):
                result["has_bias"] = True
                result["warnings"].append(warning)
        
        return result

    def get_ethical_guidelines(self) -> List[str]:
        """
        Get list of ethical guidelines
        
        Returns:
            List of ethical principles
        """
        return [
            "Transparency: All decisions must be explainable",
            "Fairness: No discrimination based on protected characteristics",
            "Privacy: Respect user data and confidentiality",
            "Safety: Prevent harmful outputs",
            "Accountability: Log all decisions for audit",
            "Beneficence: Act in the best interest of users"
        ]

    def _log_enforcement(self, result: Dict[str, Any]):
        """
        Log enforcement action
        
        Args:
            result: Enforcement result
        """
        self.audit_log.append({
            "timestamp": str(os.times()) if 'os' in dir() else "unknown",
            "passed": result["passed"],
            "warnings": result["warnings"]
        })

    def get_audit_log(self, recent: int = 10) -> List[Dict]:
        """
        Get recent audit log entries
        
        Args:
            recent: Number of recent entries
            
        Returns:
            Recent audit log
        """
        return self.audit_log[-recent:]

    def clear_audit_log(self):
        """Clear the audit log"""
        self.audit_log = []


if __name__ == "__main__":
    # Test EthicalAIGovernance
    governance = EthicalAIGovernance()
    
    print("=== Ethical Guidelines ===")
    for guideline in governance.get_ethical_guidelines():
        print(f"- {guideline}")
    
    print("\n=== Test Response Enforcement ===")
    test_response = "This is a helpful response about audio mixing techniques."
    result = governance.enforce_policies(test_response)
    print(f"Passed: {result['passed']}")
    print(f"Warnings: {result['warnings']}")
    
    print("\n=== Test Harmful Content ===")
    harmful = "This response promotes violence and hate."
    result2 = governance.enforce_policies(harmful)
    print(f"Passed: {result2['passed']}")
    print(f"Warnings: {result2['warnings']}")
    
    print("\n=== Test Query Validation ===")
    query = "How do I compress vocals?"
    validation = governance.validate_query(query)
    print(f"Valid: {validation['valid']}")
    
    print("\n=== Audit Log ===")
    for entry in governance.get_audit_log():
        print(entry)
