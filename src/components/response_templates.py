"""
Shared response templates and utilities to prevent looping and ensure variety
across all response generation components
"""
import hashlib
from typing import List, Dict, Optional

class ResponseTemplates:
    """Central repository for response templates with deduplication"""
    
    def __init__(self):
        self.recent_responses = []
        self.recent_response_hashes = set()
        self.max_recent = 20
        
        # Error/Fallback responses with variations
        self.error_responses = [
            "I apologize, but I encountered an error. Could you please rephrase your question?",
            "Something went wrong processing that. Let me try again if you ask differently.",
            "I ran into a technical issue. Could you try rephrasing your question?",
            "That caused an error on my end. Could you ask that in another way?"
        ]
        
        self.empty_response_fallbacks = [
            "I need to collect my thoughts. Could you provide more context?",
            "Let me think about that differently. Could you rephrase?",
            "I'm not quite sure how to respond to that. Could you add more details?",
            "That's an interesting question. Could you elaborate a bit more?"
        ]
        
        self.understanding_responses = [
            "I understand. Let me help with that.",
            "Got it. Here's what I can tell you:",
            "I see what you mean. Let me address that:",
            "I hear you. Here's my perspective:",
            "Understood. Let me explain:"
        ]
        
        self.uncertain_responses = [
            "I'm not entirely certain about this, but",
            "Based on what I understand,",
            "From my perspective,",
            "Here's my best assessment:",
            "To the best of my knowledge,"
        ]
        
        self.reflection_responses = [
            "That's worth considering. ",
            "Good question. ",
            "Interesting point. ",
            "Let me think about that. ",
            "That's a thoughtful inquiry. "
        ]
        
    def get_next_variation(self, template_list: List[str]) -> str:
        """Get next unused variation from template list"""
        if not template_list:
            return ""
        
        for template in template_list:
            template_hash = hashlib.md5(template[:80].encode()).hexdigest()
            if template_hash not in self.recent_response_hashes:
                return template
        
        # If all used, return first one (start cycling)
        return template_list[0]
    
    def track_response(self, response: str) -> None:
        """Track response to prevent immediate repetition"""
        response_hash = hashlib.md5(response[:100].encode()).hexdigest()
        self.recent_response_hashes.add(response_hash)
        self.recent_responses.append(response[:100])
        
        # Keep only recent ones
        if len(self.recent_responses) > self.max_recent:
            old_response = self.recent_responses.pop(0)
            # Remove old hash after half the window passes
            if len(self.recent_responses) > self.max_recent // 2:
                old_hash = hashlib.md5(old_response.encode()).hexdigest()
                self.recent_response_hashes.discard(old_hash)
    
    def get_error_response(self, context: Optional[str] = None) -> str:
        """Get varied error response"""
        response = self.get_next_variation(self.error_responses)
        self.track_response(response)
        return response
    
    def get_empty_response_fallback(self) -> str:
        """Get varied fallback for empty responses"""
        response = self.get_next_variation(self.empty_response_fallbacks)
        self.track_response(response)
        return response
    
    def get_understanding_prefix(self) -> str:
        """Get varied understanding prefix"""
        return self.get_next_variation(self.understanding_responses)
    
    def get_uncertain_prefix(self) -> str:
        """Get varied uncertain prefix"""
        return self.get_next_variation(self.uncertain_responses)
    
    def get_reflection_prefix(self) -> str:
        """Get varied reflection prefix"""
        return self.get_next_variation(self.reflection_responses)
    
    def wrap_response_with_prefix(
        self, 
        response: str, 
        prefix_type: str = "understanding"
    ) -> str:
        """Wrap response with varied prefix"""
        if not response:
            return self.get_empty_response_fallback()
        
        if prefix_type == "understanding":
            prefix = self.get_understanding_prefix()
        elif prefix_type == "uncertain":
            prefix = self.get_uncertain_prefix()
        elif prefix_type == "reflection":
            prefix = self.get_reflection_prefix()
        else:
            prefix = self.get_understanding_prefix()
        
        wrapped = f"{prefix} {response}".strip()
        self.track_response(wrapped)
        return wrapped

# Global instance for shared use
_response_templates_instance = None

def get_response_templates() -> ResponseTemplates:
    """Get singleton instance of ResponseTemplates"""
    global _response_templates_instance
    if _response_templates_instance is None:
        _response_templates_instance = ResponseTemplates()
    return _response_templates_instance
