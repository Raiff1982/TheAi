from typing import Dict, Any, List, Optional
import time
from ..knowledge_base.grounding_truth import GroundingTruth
from ..components.response_templates import get_response_templates

# Try to import generic responder for multi-perspective optimization
GENERIC_RESPONDER_AVAILABLE = False
try:
    from codette_responder_generic import get_generic_responder
    GENERIC_RESPONDER_AVAILABLE = True
except ImportError:
    try:
        # Fallback: Try importing from parent directory
        import sys
        import os
        parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from codette_responder_generic import get_generic_responder
        GENERIC_RESPONDER_AVAILABLE = True
    except ImportError:
        get_generic_responder = None

# Import natural response enhancer
try:
    from ..components.natural_response_enhancer import get_natural_enhancer
    NATURAL_ENHANCER_AVAILABLE = True
except ImportError:
    NATURAL_ENHANCER_AVAILABLE = False


class ResponseProcessor:
    """
    Processes and verifies AI responses using the grounding truth system
    and optimizes perspective selection with the generic responder.
    
    Now includes natural response enhancement to preserve Codette's identity
    while improving conversational naturalness.
    """
    
    def __init__(self):
        self.grounding_truth = GroundingTruth()
        self.context_history = []
        self.generic_responder = get_generic_responder() if GENERIC_RESPONDER_AVAILABLE else None
        self.natural_enhancer = get_natural_enhancer() if NATURAL_ENHANCER_AVAILABLE else None
        self.response_templates = get_response_templates()
        self.user_id = "anonymous"  # Can be set per session
        
    def process_response(self, query: str, response: str, context: Optional[str] = None,
                        confidence: float = 0.85) -> str:
        """
        Process and verify a response using grounding truth and multi-perspective optimization
        
        Args:
            query: The original user query
            response: The generated response
            context: Optional context category
            confidence: How confident the system is in this response (0-1)
            
        Returns:
            Processed and verified response with natural enhancement
        """
        # Step 1: Natural enhancement (removes unnatural markers)
        if self.natural_enhancer:
            try:
                response = self.natural_enhancer.enhance_response(
                    response, confidence=confidence, context={'domain': self._detect_domain(query)}
                )
            except Exception as e:
                # Natural enhancer is optional; if it fails, continue processing
                pass
        
        # Step 2: Analyze query with generic responder to understand domain and select perspectives
        perspective_analysis = None
        if self.generic_responder:
            try:
                perspective_analysis = self.generic_responder.generate_response(
                    query, user_id=self.user_id
                )
                # Attach perspective information to response for later use
                if perspective_analysis.get("perspectives"):
                    response = self._enhance_with_perspectives(response, perspective_analysis["perspectives"])
            except Exception as e:
                # Generic responder is optional; if it fails, continue processing
                pass
        
        # Step 3: Split response into statements for verification
        statements = self._split_into_statements(response)
        
        verified_statements = []
        uncertain_statements = []
        
        # Step 4: Verify each statement
        for statement in statements:
            verification = self.grounding_truth.verify_statement(statement, context)
            
            if verification["verified"]:
                verified_statements.append(statement)
            else:
                # Add confidence qualifier naturally
                qualified_statement = self._add_qualifier(statement, verification["confidence"])
                uncertain_statements.append(qualified_statement)
        
        # Step 5: Reconstruct response with proper qualifiers
        processed_response = self._construct_response(
            query, verified_statements, uncertain_statements
        )
        
        return processed_response
        
    def _detect_domain(self, query: str) -> str:
        """Detect the domain of the query for better context"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['mix', 'eq', 'compress', 'audio', 'track', 'bpm', 'daw']):
            return 'music'
        elif any(word in query_lower for word in ['code', 'program', 'software', 'function', 'class']):
            return 'programming'
        elif any(word in query_lower for word in ['data', 'analysis', 'statistics', 'metric']):
            return 'data'
        else:
            return 'general'
        
    def _enhance_with_perspectives(self, response: str, perspectives: List[Dict]) -> str:
        """
        Enhance response with multi-perspective context subtly
        
        Args:
            response: The original response
            perspectives: List of perspective dicts from generic responder
            
        Returns:
            Response with perspective context (optional enhancement)
        """
        # Optional: Add subtle perspective diversity hints without markers
        # For now, just return original response; perspectives are used for learning
        return response
        
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
        """Add appropriate qualifier based on confidence level - naturally"""
        if confidence >= 0.8:
            return f"{statement}"  # No qualifier needed for high confidence
        elif confidence >= 0.6:
            return f"{statement} (likely)"
        elif confidence >= 0.4:
            return f"{statement} (possibly)"
        elif confidence >= 0.2:
            uncertain = self.response_templates.get_uncertain_prefix()
            return f"{uncertain}{statement.lower()}"
        else:
            return f"I'm not sure about this, but {statement.lower()}"
            
    def _construct_response(
        self, 
        query: str, 
        verified_statements: List[str], 
        uncertain_statements: List[str]
    ) -> str:
        """Construct final response with proper structure and qualifiers - naturally"""
        response_parts = []
        
        # Add verified information first
        if verified_statements:
            response_parts.extend(verified_statements)
            
        # Add uncertain information with clear separation
        if uncertain_statements:
            if verified_statements:
                response_parts.append("")  # Add spacing
            response_parts.extend(uncertain_statements)
            
        # Add general note if there are uncertain statements (less obtrusive)
        if uncertain_statements and not verified_statements:
            reflection = self.response_templates.get_reflection_prefix()
            response_parts.insert(0, reflection)
            
        return "\n".join(response_parts).strip()
        
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
    
    def record_response_feedback(self, query: str, category: str, perspective: str, rating_value: int = 3) -> Dict[str, Any]:
        """
        Record user feedback on response for learning system
        
        Args:
            query: The original query
            category: The detected response category
            perspective: The perspective used
            rating_value: User rating (0-4, where 4 is best)
            
        Returns:
            Feedback confirmation and learning status
        """
        if not self.generic_responder:
            return {"status": "learning_disabled", "message": "Generic responder not available"}
        
        try:
            from codette_responder_generic import UserRating
            
            # Map rating value to UserRating enum
            rating_map = {0: UserRating.UNHELPFUL, 1: UserRating.SLIGHTLY_HELPFUL, 
                         2: UserRating.HELPFUL, 3: UserRating.VERY_HELPFUL, 
                         4: UserRating.EXACTLY_WHAT_NEEDED}
            rating = rating_map.get(rating_value, UserRating.HELPFUL)
            
            # Record feedback
            feedback_result = self.generic_responder.record_user_feedback(
                user_id=self.user_id,
                response_id=f"{query[:20]}_{int(time.time())}",
                category=category,
                perspective=perspective,
                rating=rating
            )
            
            return feedback_result
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def evaluate_response_quality(self, response: str) -> Dict[str, Any]:
        """Evaluate response quality and naturalness"""
        if self.natural_enhancer:
            try:
                return self.natural_enhancer.evaluate_response_naturalness(response)
            except Exception as e:
                return {"error": str(e)}
        return {}