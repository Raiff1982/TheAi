from typing import Dict, Any, List, Optional
from knowledge_base.grounding_truth import GroundingTruth

class ResponseProcessor:
    """
    Processes and verifies AI responses using the grounding truth system
    """
    
    def __init__(self):
        self.grounding_truth = GroundingTruth()
        self.context_history = []
        
    def process_response(self, query: str, response: str, context: Optional[str] = None) -> str:
        """
        Process and verify a response using grounding truth
        
        Args:
            query: The original user query
            response: The generated response
            context: Optional context category
            
        Returns:
            Processed and verified response
        """
        # Split response into statements for verification
        statements = self._split_into_statements(response)
        
        verified_statements = []
        uncertain_statements = []
        
        # Verify each statement
        for statement in statements:
            verification = self.grounding_truth.verify_statement(statement, context)
            
            if verification["verified"]:
                verified_statements.append(statement)
            else:
                # Add confidence qualifier
                qualified_statement = self._add_qualifier(statement, verification["confidence"])
                uncertain_statements.append(qualified_statement)
        
        # Reconstruct response with proper qualifiers
        processed_response = self._construct_response(
            query, verified_statements, uncertain_statements
        )
        
        return processed_response
        
    def _split_into_statements(self, response: str) -> List[str]:
        """Split response into verifiable statements"""
        # Basic sentence splitting
        sentences = [s.strip() for s in response.split('.') if s.strip()]
        
        # Further split complex sentences with conjunctions
        statements = []
        for sentence in sentences:
            if any(conj in sentence.lower() for conj in ['and', 'or', 'but']):
                parts = sentence.split(' and ')
                parts.extend(sentence.split(' or '))
                parts.extend(sentence.split(' but '))
                statements.extend([p.strip() for p in parts if p.strip()])
            else:
                statements.append(sentence)
                
        return statements
        
    def _add_qualifier(self, statement: str, confidence: float) -> str:
        """Add appropriate qualifier based on confidence level"""
        if confidence >= 0.8:
            return f"{statement} (highly likely)"
        elif confidence >= 0.6:
            return f"{statement} (probably)"
        elif confidence >= 0.4:
            return f"{statement} (possibly)"
        elif confidence >= 0.2:
            return f"It's uncertain, but {statement.lower()}"
        else:
            return f"I'm not certain about this, but {statement.lower()}"
            
    def _construct_response(
        self, 
        query: str, 
        verified_statements: List[str], 
        uncertain_statements: List[str]
    ) -> str:
        """Construct final response with proper structure and qualifiers"""
        response_parts = []
        
        # Add verified information first
        if verified_statements:
            response_parts.append("Here's what I know for certain:")
            response_parts.extend(verified_statements)
            
        # Add uncertain information with clear separation
        if uncertain_statements:
            if verified_statements:
                response_parts.append("\nAdditionally:")
            else:
                response_parts.append("Based on my current understanding:")
            response_parts.extend(uncertain_statements)
            
        # Add general disclaimer if there are uncertain statements
        if uncertain_statements:
            response_parts.append(
                "\nNote: Some parts of this response are based on my current understanding "
                "and might need verification. Feel free to ask for clarification on specific points."
            )
            
        return "\n".join(response_parts)
        
    def update_context(self, query: str, response: str):
        """Update context history for better response processing"""
        self.context_history.append({
            "query": query,
            "response": response,
            "timestamp": time.time()
        })
        
        # Keep only recent context
        if len(self.context_history) > 10:
            self.context_history.pop(0)