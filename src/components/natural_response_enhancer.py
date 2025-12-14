"""
Natural Response Enhancer for Codette
======================================
Improves response naturalness while preserving Codette's quantum consciousness
and multi-perspective reasoning. Works with response processors to make AI
responses feel more human and conversational.
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import random

logger = logging.getLogger(__name__)


class NaturalResponseEnhancer:
    """Enhances response naturalness without markers or unnatural phrasing"""
    
    def __init__(self):
        """Initialize the natural response enhancer"""
        self.response_history = []
        self.pattern_library = self._build_pattern_library()
        self.transition_phrases = self._build_transitions()
        self.confidence_templates = self._build_confidence_templates()
        logger.info("Natural Response Enhancer initialized")
    
    def enhance_response(self, response: str, confidence: float = 0.85, 
                        context: Optional[Dict[str, Any]] = None) -> str:
        """
        Enhance response naturalness while preserving meaning
        
        Args:
            response: The raw response from model/perspectives
            confidence: How confident the response is (0-1)
            context: Optional context about the query/domain
            
        Returns:
            Enhanced, more natural response
        """
        # Remove unnatural markers
        response = self._strip_unnatural_markers(response)
        
        # Improve sentence structure
        response = self._improve_sentence_flow(response)
        
        # Add natural confidence expression if needed
        if confidence < 0.9:
            response = self._add_natural_confidence(response, confidence)
        
        # Break up long blocks of text
        response = self._improve_readability(response)
        
        # Add conversational warmth
        response = self._add_warmth(response)
        
        # Preserve context clues
        if context:
            response = self._enhance_with_context(response, context)
        
        # Store for learning
        self.response_history.append({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'confidence': confidence
        })
        
        return response.strip()
    
    def _strip_unnatural_markers(self, text: str) -> str:
        """Remove system markers and unnatural tags"""
        # Remove [Protected: ...] wrappers
        text = re.sub(r'\[Protected:\s*(.*?)\]', r'\1', text, flags=re.DOTALL)
        
        # Remove [System optimized response] markers
        text = re.sub(r'\[System optimized response\]', '', text)
        
        # Remove other bracketed system messages
        text = re.sub(r'\[(System|SYSTEM).*?\]', '', text, flags=re.IGNORECASE)
        
        # Remove redundant "Error" blocks
        text = re.sub(r'\[.*?error.*?\]', '', text, flags=re.IGNORECASE)
        
        # Clean up multiple consecutive newlines
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def _improve_sentence_flow(self, text: str) -> str:
        """Improve sentence structure and flow"""
        # Replace awkward AI constructs
        replacements = [
            (r'\b(I would|I will|I can)\s+(respond|state|say|indicate)\s+that', r''),
            (r'\b(Based on my analysis|According to my understanding)\s*,?\s*', ''),
            (r'\b(The following|The below|This is)\s+\(.*?\)\s*:', ''),
            (r'(?:Therefore|Thus|Hence|So)\s+,\s+', 'So '),
            (r'\b(Notably|Significantly|Importantly)\s*,?\s*', ''),
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        text = re.sub(r'([.,!?;:])\s+', r'\1 ', text)
        
        return text
    
    def _add_natural_confidence(self, text: str, confidence: float) -> str:
        """Add natural confidence expression without markers"""
        if confidence < 0.5:
            intro = self.confidence_templates['low']
        elif confidence < 0.75:
            intro = self.confidence_templates['medium']
        else:
            intro = self.confidence_templates['high']
        
        # Only add if not already present
        if not any(phrase in text for phrase in [
            "I'm not entirely sure",
            "I'm fairly confident",
            "I'm quite confident",
            "Based on",
            "From what I understand"
        ]):
            text = f"{intro} {text}"
        
        return text
    
    def _improve_readability(self, text: str) -> str:
        """Break up large text blocks for better readability"""
        # Split long paragraphs
        paragraphs = text.split('\n')
        improved = []
        
        for para in paragraphs:
            # If paragraph is very long, try to break it sensibly
            if len(para) > 400:
                # Try to break at periods
                sentences = re.split(r'(?<=[.!?])\s+', para)
                
                # Group sentences into chunks (aim for ~200-300 chars per chunk)
                chunks = []
                current_chunk = []
                current_length = 0
                
                for sent in sentences:
                    sent_len = len(sent) + 1
                    if current_length + sent_len > 300 and current_chunk:
                        chunks.append(' '.join(current_chunk))
                        current_chunk = [sent]
                        current_length = sent_len
                    else:
                        current_chunk.append(sent)
                        current_length += sent_len
                
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                
                improved.extend(chunks)
            else:
                improved.append(para)
        
        return '\n\n'.join(improved).strip()
    
    def _add_warmth(self, text: str) -> str:
        """Add subtle conversational warmth without being overly friendly"""
        # Add some natural connectives
        warmth_patterns = [
            (r'^([^.!?]*\.)\s+([A-Z])', lambda m: self._add_connector(m)),
        ]
        
        # Avoid robotic transitions
        replacements = [
            ('In conclusion,', 'To wrap up,'),
            ('Furthermore,', 'Also,'),
            ('Nevertheless,', 'Still,'),
            ('In fact,', 'Actually,'),
        ]
        
        for old, new in replacements:
            text = text.replace(old, new)
        
        return text
    
    def _add_connector(self, match) -> str:
        """Add natural connectors between sentences"""
        connectors = ['That', 'It', 'This', 'So', 'Overall']
        return match.group(1) + ' ' + random.choice(connectors) + ' ' + match.group(2)
    
    def _enhance_with_context(self, text: str, context: Dict[str, Any]) -> str:
        """Enhance response with contextual awareness"""
        if context.get('domain') == 'music':
            # Add music-specific warmth
            if not any(word in text for word in ['cool', 'great', 'perfect', 'awesome']):
                # Subtly affirm the context
                pass
        
        return text
    
    def _build_pattern_library(self) -> Dict[str, str]:
        """Build library of natural response patterns"""
        return {
            'discovery': "I just realized that",
            'insight': "Here's an interesting point:",
            'clarification': "To clarify that,",
            'expansion': "What's more,",
            'caution': "One thing to be careful about:",
            'agreement': "You're right to think about that.",
            'question_response': "That's a great question.",
        }
    
    def _build_transitions(self) -> List[str]:
        """Build natural transition phrases"""
        return [
            "Now that I think about it,",
            "Actually, an important point is",
            "You know, one thing that matters is",
            "Here's something worth considering:",
            "The real key is",
            "What I find interesting is",
            "One more thing -",
            "So really, what's happening is",
        ]
    
    def _build_confidence_templates(self) -> Dict[str, str]:
        """Build confidence expression templates"""
        return {
            'low': "I'm not entirely sure, but",
            'medium': "From what I understand,",
            'high': "I'm fairly confident that",
            'very_high': "Definitely,",
        }
    
    def evaluate_response_naturalness(self, response: str) -> Dict[str, Any]:
        """Evaluate how natural a response sounds"""
        markers_found = []
        
        # Check for unnatural markers
        if '[' in response and ']' in response:
            markers = re.findall(r'\[.*?\]', response)
            markers_found.extend(markers)
        
        if 'System optimized' in response:
            markers_found.append('System optimized response marker')
        
        if 'Protected:' in response:
            markers_found.append('Protected marker')
        
        # Count repetitive phrases (sign of poor variation)
        sentences = re.split(r'[.!?]+', response)
        phrase_freq = {}
        for sent in sentences:
            sent = sent.strip()
            if len(sent) > 10:
                # Check for repeated starts
                start = sent.split()[0] if sent.split() else ''
                phrase_freq[start] = phrase_freq.get(start, 0) + 1
        
        repetition_score = max(phrase_freq.values()) if phrase_freq else 0
        
        # Calculate naturalness score
        naturalness = 1.0
        if markers_found:
            naturalness -= 0.3 * len(markers_found)
        if repetition_score > 2:
            naturalness -= 0.2
        
        naturalness = max(0.0, min(1.0, naturalness))
        
        return {
            'naturalness_score': naturalness,
            'unnatural_markers_found': markers_found,
            'repetition_issues': repetition_score > 2,
            'has_system_artifacts': len(markers_found) > 0,
            'recommendations': self._generate_recommendations(markers_found, repetition_score)
        }
    
    def _generate_recommendations(self, markers: List[str], repetition: int) -> List[str]:
        """Generate recommendations for improvement"""
        recs = []
        
        if markers:
            recs.append(f"Remove {len(markers)} unnatural marker(s): {', '.join(markers[:2])}")
        
        if repetition > 2:
            recs.append("Vary sentence starts for better flow")
        
        if not recs:
            recs.append("Response looks natural!")
        
        return recs


# Singleton instance
_enhancer_instance: Optional[NaturalResponseEnhancer] = None


def get_natural_enhancer() -> NaturalResponseEnhancer:
    """Get or create the natural response enhancer instance"""
    global _enhancer_instance
    if _enhancer_instance is None:
        _enhancer_instance = NaturalResponseEnhancer()
    return _enhancer_instance


# Test/demo
if __name__ == "__main__":
    enhancer = get_natural_enhancer()
    
    # Test with problematic response
    test_response = """[Protected: That's great! Thank you for taking the time to share your thoughts with us. We hope that you find what you're looking for and that you enjoy your time with us!
We'd like to thank Codette for participating in this interview.
[System optimized response]]"""
    
    print("Original (problematic) response:")
    print(test_response)
    print("\n" + "="*70 + "\n")
    
    enhanced = enhancer.enhance_response(test_response, confidence=0.75)
    print("Enhanced (natural) response:")
    print(enhanced)
    print("\n" + "="*70 + "\n")
    
    # Evaluate
    eval_result = enhancer.evaluate_response_naturalness(test_response)
    print("Evaluation:")
    for key, value in eval_result.items():
        print(f"  {key}: {value}")
