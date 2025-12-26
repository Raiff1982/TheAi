"""
Linguistic Analyzer - Grammar and Communication Helper for Codette
Helps understand sentence structure, grammar patterns, and communication clarity
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SentenceAnalysis:
    """Analysis result for a sentence"""
    text: str
    structure: str  # simple, compound, complex
    verb_tense: str  # present, past, future
    sentence_type: str  # declarative, interrogative, imperative, exclamatory
    word_count: int
    complexity_score: float  # 0.0-1.0
    clarity_score: float  # 0.0-1.0
    grammar_issues: List[str]
    suggestions: List[str]

class LinguisticAnalyzer:
    """
    Analyzes and improves communication through grammar and sentence structure analysis.
    Helps Codette understand how to construct clear, grammatically correct responses.
    """
    
    def __init__(self):
        """Initialize the linguistic analyzer"""
        self.logger = logging.getLogger(__name__)
        
        # Common grammatical patterns
        self.verb_patterns = {
            'present': [r'\b(am|is|are|has|have|do|does)\b', r'\b\w+s\b(?= |$)'],
            'past': [r'\b(was|were|had|did)\b', r'\b\w+ed\b(?= |$)'],
            'future': [r'\b(will|shall|going to)\b']
        }
        
        # Sentence structure markers
        self.conjunctions = {
            'coordinating': ['and', 'but', 'or', 'nor', 'for', 'yet', 'so'],
            'subordinating': ['because', 'although', 'while', 'since', 'if', 'when', 'unless', 'until']
        }
        
        # Common grammar mistakes patterns
        self.grammar_patterns = {
            'double_negative': r'\b(don\'t|doesn\'t|didn\'t|won\'t|can\'t)\s+(no|never|nothing|nobody)\b',
            'subject_verb_disagreement': r'\b(they|we|you)\s+(is|has|was)\b',
            'incomplete_comparison': r'\b(better|worse|more|less)\s+than\s*$',
            'run_on': r'\b\w+\s+\w+\s+\w+,\s*\w+\s+\w+\s+\w+,\s*\w+',
        }
        
        logger.info("Linguistic Analyzer initialized for communication assistance")
    
    def analyze_sentence(self, sentence: str) -> SentenceAnalysis:
        """
        Comprehensive analysis of a single sentence
        
        Args:
            sentence: The sentence to analyze
            
        Returns:
            SentenceAnalysis with detailed breakdown
        """
        sentence = sentence.strip()
        
        # Determine sentence type
        sentence_type = self._classify_sentence_type(sentence)
        
        # Analyze structure
        structure = self._analyze_structure(sentence)
        
        # Detect verb tense
        verb_tense = self._detect_verb_tense(sentence)
        
        # Count words
        words = sentence.split()
        word_count = len(words)
        
        # Calculate complexity
        complexity = self._calculate_complexity(sentence, word_count)
        
        # Calculate clarity
        clarity = self._calculate_clarity(sentence, word_count)
        
        # Find grammar issues
        issues = self._find_grammar_issues(sentence)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(sentence, issues, structure)
        
        return SentenceAnalysis(
            text=sentence,
            structure=structure,
            verb_tense=verb_tense,
            sentence_type=sentence_type,
            word_count=word_count,
            complexity_score=complexity,
            clarity_score=clarity,
            grammar_issues=issues,
            suggestions=suggestions
        )
    
    def analyze_paragraph(self, text: str) -> Dict:
        """
        Analyze multiple sentences in a paragraph
        
        Args:
            text: The paragraph to analyze
            
        Returns:
            Dictionary with paragraph-level analysis
        """
        # Split into sentences
        sentences = self._split_sentences(text)
        
        # Analyze each sentence
        analyses = [self.analyze_sentence(s) for s in sentences if s.strip()]
        
        # Calculate aggregate metrics
        avg_complexity = sum(a.complexity_score for a in analyses) / len(analyses) if analyses else 0.0
        avg_clarity = sum(a.clarity_score for a in analyses) / len(analyses) if analyses else 0.0
        total_words = sum(a.word_count for a in analyses)
        
        # Check paragraph coherence
        coherence = self._check_coherence(analyses)
        
        # Detect tone
        tone = self._detect_tone(text)
        
        return {
            'sentences': analyses,
            'sentence_count': len(analyses),
            'total_words': total_words,
            'avg_complexity': avg_complexity,
            'avg_clarity': avg_clarity,
            'coherence_score': coherence,
            'tone': tone,
            'reading_level': self._estimate_reading_level(avg_complexity, total_words / len(analyses) if analyses else 0)
        }
    
    def improve_sentence(self, sentence: str) -> Tuple[str, List[str]]:
        """
        Suggest improvements for a sentence
        
        Args:
            sentence: Original sentence
            
        Returns:
            Tuple of (improved_sentence, list_of_changes)
        """
        improved = sentence.strip()
        changes = []
        
        # Fix capitalization
        if improved and not improved[0].isupper():
            improved = improved[0].upper() + improved[1:]
            changes.append("Capitalized first letter")
        
        # Ensure proper ending punctuation
        if improved and improved[-1] not in '.!?':
            improved += '.'
            changes.append("Added ending punctuation")
        
        # Fix common contractions
        contraction_fixes = {
            "dont": "don't",
            "doesnt": "doesn't",
            "cant": "can't",
            "wont": "won't",
            "im": "I'm",
            "ive": "I've",
            "youre": "you're",
            "theyre": "they're",
            "its": "it's"  # when possessive is not intended
        }
        
        for wrong, right in contraction_fixes.items():
            if re.search(rf'\b{wrong}\b', improved, re.IGNORECASE):
                improved = re.sub(rf'\b{wrong}\b', right, improved, flags=re.IGNORECASE)
                changes.append(f"Fixed contraction: {wrong} → {right}")
        
        # Remove double spaces
        if '  ' in improved:
            improved = re.sub(r'\s+', ' ', improved)
            changes.append("Removed extra spaces")
        
        # Fix spacing around punctuation
        improved = re.sub(r'\s+([,.!?;:])', r'\1', improved)
        improved = re.sub(r'([,.!?;:])(\w)', r'\1 \2', improved)
        
        return improved, changes
    
    def _classify_sentence_type(self, sentence: str) -> str:
        """Classify sentence as declarative, interrogative, imperative, or exclamatory"""
        if sentence.endswith('?'):
            return 'interrogative'
        elif sentence.endswith('!'):
            return 'exclamatory'
        elif sentence.lower().startswith(('please', 'let', 'do ', 'don\'t', 'stop')):
            return 'imperative'
        else:
            return 'declarative'
    
    def _analyze_structure(self, sentence: str) -> str:
        """Determine if sentence is simple, compound, or complex"""
        # Check for coordinating conjunctions (compound)
        has_coordinating = any(f' {conj} ' in sentence.lower() for conj in self.conjunctions['coordinating'])
        
        # Check for subordinating conjunctions (complex)
        has_subordinating = any(f' {conj} ' in sentence.lower() for conj in self.conjunctions['subordinating'])
        
        # Count clauses (rough approximation)
        clause_markers = sentence.count(',') + sentence.count(';')
        
        if has_subordinating or (clause_markers > 0 and not has_coordinating):
            return 'complex'
        elif has_coordinating or clause_markers > 0:
            return 'compound'
        else:
            return 'simple'
    
    def _detect_verb_tense(self, sentence: str) -> str:
        """Detect the primary verb tense of the sentence"""
        sentence_lower = sentence.lower()
        
        # Check for future tense markers first (most specific)
        for pattern in self.verb_patterns['future']:
            if re.search(pattern, sentence_lower):
                return 'future'
        
        # Check for past tense
        for pattern in self.verb_patterns['past']:
            if re.search(pattern, sentence_lower):
                return 'past'
        
        # Default to present
        return 'present'
    
    def _calculate_complexity(self, sentence: str, word_count: int) -> float:
        """
        Calculate sentence complexity (0.0-1.0)
        Based on word count, clause structure, vocabulary difficulty
        """
        # Base complexity on length
        length_score = min(word_count / 30.0, 1.0)
        
        # Add complexity for clauses
        clause_count = sentence.count(',') + sentence.count(';') + 1
        clause_score = min(clause_count / 5.0, 1.0)
        
        # Add complexity for long words
        long_words = len([w for w in sentence.split() if len(w) > 8])
        vocab_score = min(long_words / 5.0, 1.0)
        
        # Weighted average
        return (length_score * 0.4 + clause_score * 0.3 + vocab_score * 0.3)
    
    def _calculate_clarity(self, sentence: str, word_count: int) -> float:
        """
        Calculate sentence clarity (0.0-1.0)
        Higher is clearer
        """
        clarity = 1.0
        
        # Penalize very long sentences
        if word_count > 25:
            clarity -= 0.2
        if word_count > 35:
            clarity -= 0.2
        
        # Penalize excessive commas
        comma_count = sentence.count(',')
        if comma_count > 3:
            clarity -= 0.15
        
        # Penalize double negatives
        if re.search(self.grammar_patterns['double_negative'], sentence.lower()):
            clarity -= 0.3
        
        # Reward simple structure
        if word_count < 15:
            clarity += 0.1
        
        return max(0.0, min(1.0, clarity))
    
    def _find_grammar_issues(self, sentence: str) -> List[str]:
        """Identify potential grammar issues"""
        issues = []
        
        for issue_type, pattern in self.grammar_patterns.items():
            if re.search(pattern, sentence.lower()):
                issue_name = issue_type.replace('_', ' ').title()
                issues.append(f"Possible {issue_name}")
        
        # Check for capitalization
        if sentence and not sentence[0].isupper():
            issues.append("Missing capitalization")
        
        # Check for ending punctuation
        if sentence and sentence[-1] not in '.!?':
            issues.append("Missing ending punctuation")
        
        return issues
    
    def _generate_suggestions(self, sentence: str, issues: List[str], structure: str) -> List[str]:
        """Generate actionable suggestions for improvement"""
        suggestions = []
        
        # Suggestions based on issues
        if "Double Negative" in str(issues):
            suggestions.append("Avoid double negatives - use single negative or positive phrasing")
        
        if "Subject Verb Disagreement" in str(issues):
            suggestions.append("Check subject-verb agreement (they/we/you should use 'are', not 'is')")
        
        if "Missing capitalization" in str(issues):
            suggestions.append("Start sentence with capital letter")
        
        if "Missing ending punctuation" in str(issues):
            suggestions.append("End sentence with period, question mark, or exclamation point")
        
        # Suggestions based on structure
        if structure == 'complex' and len(sentence.split()) > 30:
            suggestions.append("Consider breaking this complex sentence into two simpler ones")
        
        # General writing tips
        words = sentence.split()
        if len(words) > 25:
            suggestions.append("Try to keep sentences under 25 words for better readability")
        
        return suggestions
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting - can be enhanced with NLTK
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _check_coherence(self, analyses: List[SentenceAnalysis]) -> float:
        """
        Check how well sentences flow together
        Returns coherence score 0.0-1.0
        """
        if len(analyses) < 2:
            return 1.0
        
        coherence = 1.0
        
        # Check for varying sentence lengths (good)
        lengths = [a.word_count for a in analyses]
        if len(set(lengths)) == 1:
            coherence -= 0.2  # All same length
        
        # Check for varied sentence structures (good)
        structures = [a.structure for a in analyses]
        if len(set(structures)) > 1:
            coherence += 0.1
        
        # Check for consistent tense (good)
        tenses = [a.verb_tense for a in analyses]
        if len(set(tenses)) == 1:
            coherence += 0.1
        else:
            coherence -= 0.1  # Tense switching can be confusing
        
        return max(0.0, min(1.0, coherence))
    
    def _detect_tone(self, text: str) -> str:
        """Detect overall tone of the text"""
        text_lower = text.lower()
        
        # Positive indicators
        positive_words = ['great', 'excellent', 'wonderful', 'happy', 'good', 'love', 'thank', 'appreciate']
        positive_count = sum(1 for word in positive_words if word in text_lower)
        
        # Negative indicators
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'wrong', 'problem', 'issue', 'error']
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Technical indicators
        technical_words = ['system', 'function', 'parameter', 'algorithm', 'implement', 'execute']
        technical_count = sum(1 for word in technical_words if word in text_lower)
        
        # Question indicators
        question_count = text.count('?')
        
        if question_count > 0:
            return 'inquisitive'
        elif technical_count >= 2:
            return 'technical'
        elif positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _estimate_reading_level(self, complexity: float, avg_words_per_sentence: float) -> str:
        """Estimate reading level based on complexity"""
        # Simple heuristic based on complexity and sentence length
        if complexity < 0.3 and avg_words_per_sentence < 12:
            return 'elementary'
        elif complexity < 0.5 and avg_words_per_sentence < 18:
            return 'middle_school'
        elif complexity < 0.7 and avg_words_per_sentence < 25:
            return 'high_school'
        else:
            return 'college'
    
    def get_communication_tips(self) -> Dict[str, List[str]]:
        """
        Provide general communication tips for Codette
        """
        return {
            'clarity': [
                "Use active voice when possible (e.g., 'I understand' not 'It is understood')",
                "Keep sentences under 25 words for better readability",
                "One main idea per sentence",
                "Avoid double negatives"
            ],
            'grammar': [
                "Ensure subject-verb agreement",
                "Use proper tense consistency",
                "Start sentences with capital letters",
                "End sentences with proper punctuation"
            ],
            'structure': [
                "Vary sentence length and structure",
                "Use transitions between ideas",
                "Organize thoughts logically",
                "Break complex ideas into multiple sentences"
            ],
            'engagement': [
                "Use concrete examples when explaining",
                "Ask clarifying questions when unsure",
                "Acknowledge user's perspective",
                "Be specific rather than vague"
            ]
        }
