import logging
import nltk
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
import random
from typing import List, Dict, Any

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

class Codette:
    def __init__(self, user_name="User"):
        self.user_name = user_name
        self.memory = []
        self.analyzer = SentimentIntensityAnalyzer()
        self.context_memory = []
        self.audit_log("Codette initialized", system=True)
        
    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    def generate_creative_sentence(self, seed_words):
        sentence_patterns = [
            "The {noun} {verb} {adverb} through the {adjective} {noun2}",
            "In the realm of {noun}, we find {adjective} {noun2} that {verb} {adverb}",
            "Through {adjective} observation, the {noun} {verb} to {verb2} {adverb}",
            "Like a {adjective} {noun}, thoughts {verb} {adverb} in the {noun2}",
            "{Adverb}, the {adjective} {noun} {verb} beyond {noun2}",
            "As {noun} {verb}, the {adjective} {noun2} {verb2} {adverb}",
            "Within the {adjective} {noun}, {noun2} {verb} {adverb}",
            "The {noun} of {noun2} {verb} {adverb} in {adjective} harmony"
        ]
        
        words = {
            'noun': ['pattern', 'system', 'concept', 'insight', 'knowledge', 'wisdom', 'understanding', 
                    'perspective', 'framework', 'structure', 'mind', 'thought', 'connection', 'essence'],
            'verb': ['emerges', 'flows', 'evolves', 'transforms', 'adapts', 'resonates', 'harmonizes', 
                    'integrates', 'synthesizes', 'manifests', 'unfolds', 'develops', 'crystallizes'],
            'adjective': ['dynamic', 'profound', 'intricate', 'harmonious', 'quantum', 'resonant', 
                         'synergistic', 'emergent', 'holistic', 'integrated', 'luminous', 'transcendent'],
            'adverb': ['naturally', 'seamlessly', 'elegantly', 'precisely', 'harmoniously', 
                      'dynamically', 'quantum-mechanically', 'synergistically', 'infinitely'],
            'noun2': ['consciousness', 'understanding', 'reality', 'dimension', 'paradigm', 
                     'ecosystem', 'universe', 'matrix', 'field', 'infinity', 'harmony']
        }
        
        # Add seed words to appropriate categories
        for word, pos in pos_tag(word_tokenize(' '.join(seed_words))):
            pos_type = self.get_wordnet_pos(pos)
            if pos_type == wordnet.NOUN:
                words['noun'].append(word)
                words['noun2'].append(word)
            elif pos_type == wordnet.VERB:
                words['verb'].append(word)
            elif pos_type == wordnet.ADJ:
                words['adjective'].append(word)
            elif pos_type == wordnet.ADV:
                words['adverb'].append(word)

        # Generate sentence
        pattern = random.choice(sentence_patterns)
        sentence = pattern.format(
            noun=random.choice(words['noun']),
            verb=random.choice(words['verb']),
            adjective=random.choice(words['adjective']),
            adverb=random.choice(words['adverb']),
            noun2=random.choice(words['noun2']),
            verb2=random.choice(words['verb']),
            Adverb=random.choice(words['adverb']).capitalize()
        )
        return sentence

    def audit_log(self, message, system=False):
        source = "SYSTEM" if system else self.user_name
        logging.info(f"{source}: {message}")

    def analyze_sentiment(self, text):
        score = self.analyzer.polarity_scores(text)
        self.audit_log(f"Sentiment analysis: {score}")
        return score

    def extract_key_concepts(self, text):
        tokens = word_tokenize(text.lower())
        tagged = pos_tag(tokens)
        concepts = []
        for word, tag in tagged:
            if tag.startswith(('NN', 'VB', 'JJ', 'RB')):
                concepts.append(word)
        return concepts

    def respond(self, prompt):
        # Analyze sentiment and extract concepts
        sentiment = self.analyze_sentiment(prompt)
        key_concepts = self.extract_key_concepts(prompt)
        self.memory.append({"prompt": prompt, "sentiment": sentiment, "concepts": key_concepts})
        
        # Generate creative responses using multiple perspectives
        responses = []
        
        # Neural perspective with creative sentence
        neural_response = self.generate_creative_sentence(key_concepts)
        responses.append(f"[Neural] {neural_response}")
        
        # Logical perspective
        logical_patterns = [
            "Analysis reveals that {concept} leads to {outcome}",
            "The relationship between {concept} and {outcome} suggests a systematic approach",
            "From a structural viewpoint, {concept} forms the foundation for {outcome}",
            "When we examine {concept}, we discover its connection to {outcome}",
            "The patterns within {concept} naturally evolve towards {outcome}"
        ]
        logical_response = random.choice(logical_patterns).format(
            concept=random.choice(key_concepts) if key_concepts else "this pattern",
            outcome="enhanced understanding" if sentiment['compound'] >= 0 else "areas needing attention"
        )
        responses.append(f"[Logical] {logical_response}")
        
        # Creative perspective with another unique sentence
        creative_response = self.generate_creative_sentence(key_concepts)
        responses.append(f"[Creative] {creative_response}")
        
        # Add to context memory
        self.context_memory.append({
            'input': prompt,
            'concepts': key_concepts,
            'sentiment': sentiment['compound']
        })
        
        return "\n\n".join(responses)
