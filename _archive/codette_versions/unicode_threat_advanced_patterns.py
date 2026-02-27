#!/usr/bin/env python3
"""
Advanced usage patterns and integration examples for the Unicode threat analyzer.
Demonstrates ML-based filtering, batch processing, and security integration.
"""

from unicode_threat_analyzer2 import detect_unicode_threat
from collections import defaultdict
import json


class UnicodeSecurityFilter:
    """
    Production-ready security filter with configurable threat levels.
    Demonstrates advanced threat detection patterns.
    """
    
    def __init__(self, strict_mode=False):
        """
        Initialize security filter.
        
        Args:
            strict_mode (bool): If True, moderate threats are also blocked
        """
        self.strict_mode = strict_mode
        self.threat_log = []
        self.threat_stats = defaultdict(int)
    
    def evaluate_text(self, text, context=None):
        """
        Evaluate text with optional context for more accurate threat assessment.
        
        Args:
            text (str): Text to analyze
            context (str): Optional context ('email', 'domain', 'password', 'comment', etc.)
        
        Returns:
            dict: Decision and reasoning
        """
        result = detect_unicode_threat(text)
        
        # Context-aware threat assessment
        context_multiplier = {
            'password': 2.0,        # Passwords are high-risk for spoofing
            'domain': 1.8,          # Domains critical for phishing
            'email': 1.3,           # Email less critical than domain
            'username': 1.5,        # Usernames used in auth
            'comment': 0.7,         # Comments more permissive
            'message': 0.8,         # Messages more permissive
            'default': 1.0,
        }
        
        multiplier = context_multiplier.get(context, 1.0)
        adjusted_score = result['total_threat_score'] * multiplier
        
        # Decision logic
        decision = self._make_decision(result, adjusted_score)
        
        # Logging
        log_entry = {
            'text': repr(text[:50]),  # Truncated for logging
            'context': context,
            'threat_level': result['threat_level'],
            'adjusted_score': round(adjusted_score, 2),
            'decision': decision,
            'flags': result['behavioral_flags'],
        }
        self.threat_log.append(log_entry)
        self.threat_stats[result['threat_level']] += 1
        
        return {
            'allow': decision == 'allow',
            'decision': decision,
            'threat_level': result['threat_level'],
            'original_score': result['total_threat_score'],
            'adjusted_score': round(adjusted_score, 2),
            'reasons': self._get_rejection_reasons(result),
            'details': result,
        }
    
    def _make_decision(self, result, adjusted_score):
        """Make security decision based on threat analysis."""
        threshold_critical = 10
        threshold_high = 7 if not self.strict_mode else 5
        threshold_moderate = 3
        
        if adjusted_score >= threshold_critical:
            return 'block_immediately'
        elif adjusted_score >= threshold_high:
            return 'block'
        elif adjusted_score >= threshold_moderate and self.strict_mode:
            return 'block'
        elif result['threat_level'] in ['high', 'critical']:
            return 'block'
        elif result['threat_level'] == 'moderate' and self.strict_mode:
            return 'block'
        elif result['threat_level'] == 'moderate':
            return 'review'
        else:
            return 'allow'
    
    def _get_rejection_reasons(self, result):
        """Generate human-readable rejection reasons."""
        reasons = []
        
        if result['dangerous_characters']:
            count = len(result['dangerous_characters'])
            categories = set(dc['category'] for dc in result['dangerous_characters'])
            reasons.append(f"Found {count} dangerous Unicode character(s) in: {', '.join(categories)}")
        
        if result['confusable_characters']:
            reasons.append(f"Detected {len(result['confusable_characters'])} homoglyph(s) - potential spoofing attack")
        
        if result['suspicious_sequences']:
            for seq in result['suspicious_sequences']:
                reasons.append(f"Suspicious {seq['type']}: {seq['description']}")
        
        if result['behavioral_flags']:
            reasons.append(f"Behavioral flags: {', '.join(result['behavioral_flags'])}")
        
        return reasons
    
    def get_statistics(self):
        """Return analysis statistics."""
        total = sum(self.threat_stats.values())
        return {
            'total_texts_analyzed': total,
            'threat_distribution': dict(self.threat_stats),
            'threat_percentages': {
                level: round(count / total * 100, 2) if total > 0 else 0
                for level, count in self.threat_stats.items()
            },
            'recent_logs': self.threat_log[-10:],  # Last 10 entries
        }


class BatchThreatAnalyzer:
    """
    Process multiple texts with statistical analysis.
    Useful for security audits and threat research.
    """
    
    def __init__(self):
        self.results = []
        self.summary = {
            'total_analyzed': 0,
            'threats_found': 0,
            'high_risk_texts': [],
            'common_threat_patterns': defaultdict(int),
        }
    
    def analyze_batch(self, texts, descriptions=None):
        """
        Analyze a batch of texts.
        
        Args:
            texts (list): List of strings to analyze
            descriptions (list): Optional descriptions for each text
        
        Returns:
            dict: Batch analysis results
        """
        if descriptions is None:
            descriptions = [f"Text {i}" for i in range(len(texts))]
        
        for text, desc in zip(texts, descriptions):
            result = detect_unicode_threat(text)
            self.results.append({
                'description': desc,
                'text': text[:100],  # Truncate for storage
                'analysis': result,
            })
            
            # Update summary
            self.summary['total_analyzed'] += 1
            
            if result['threat_level'] in ['high', 'critical']:
                self.summary['threats_found'] += 1
                self.summary['high_risk_texts'].append({
                    'description': desc,
                    'threat_level': result['threat_level'],
                    'score': result['total_threat_score'],
                })
            
            # Track common patterns
            for flag in result['behavioral_flags']:
                self.summary['common_threat_patterns'][flag] += 1
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate detailed batch analysis report."""
        return {
            'summary': self.summary,
            'detailed_results': [
                {
                    'description': r['description'],
                    'threat_level': r['analysis']['threat_level'],
                    'score': r['analysis']['total_threat_score'],
                    'dangerous_chars': len(r['analysis']['dangerous_characters']),
                    'confusables': len(r['analysis']['confusable_characters']),
                    'flags': r['analysis']['behavioral_flags'],
                }
                for r in self.results
            ],
            'statistics': {
                'high_risk_percentage': round(
                    self.summary['threats_found'] / max(self.summary['total_analyzed'], 1) * 100, 2
                ),
                'average_threat_score': round(
                    sum(r['analysis']['total_threat_score'] for r in self.results) / 
                    max(len(self.results), 1), 2
                ),
            }
        }


# Example: Homoglyph Detection Pipeline
class HomoglyphDetector:
    """Specialized detector for homoglyph/confusable character attacks."""
    
    @staticmethod
    def find_all_homoglyphs(text):
        """Find all homoglyph threats in text."""
        result = detect_unicode_threat(text)
        
        if not result['confusable_characters']:
            return {
                'has_homoglyphs': False,
                'message': 'No homoglyphs detected',
            }
        
        homoglyph_groups = defaultdict(list)
        for conf in result['confusable_characters']:
            base = conf['confuses_with']
            homoglyph_groups[base].append(conf)
        
        return {
            'has_homoglyphs': True,
            'total_homoglyphs': len(result['confusable_characters']),
            'by_base_character': dict(homoglyph_groups),
            'risk_assessment': 'HIGH' if len(result['confusable_characters']) > 3 else 'MODERATE',
        }


# Example: Behavioral Pattern Analysis
class BehavioralAnalyzer:
    """Analyze behavioral features for anomaly detection."""
    
    @staticmethod
    def analyze_features(text):
        """Extract and analyze behavioral features."""
        result = detect_unicode_threat(text)
        features = result['behavioral_features']
        
        # Anomaly detection rules
        anomalies = []
        
        if features['entropy'] > 6.0:
            anomalies.append("HIGH_ENTROPY: Text appears heavily randomized or obfuscated")
        
        if features['script_diversity'] >= 3:
            anomalies.append("SCRIPT_MIXING: Multiple languages/scripts detected (spoofing risk)")
        
        if features['invisible_char_ratio'] > 0.05:
            anomalies.append("HIDDEN_CHARS: Significant invisible character usage")
        
        if features['rtl_ltr_mixing'] > 3:
            anomalies.append("DIRECTIONAL_ANOMALY: Unusual RTL/LTR text mixing")
        
        return {
            'text': text[:50],
            'features': features,
            'anomalies': anomalies if anomalies else ['NONE'],
            'risk_level': 'CRITICAL' if len(anomalies) >= 2 else 'HIGH' if anomalies else 'LOW',
        }


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ADVANCED UNICODE THREAT DETECTION PATTERNS")
    print("=" * 80)
    
    # 1. Security Filter Demo
    print("\n[1] CONTEXT-AWARE SECURITY FILTER")
    print("-" * 80)
    
    filter_strict = UnicodeSecurityFilter(strict_mode=True)
    filter_normal = UnicodeSecurityFilter(strict_mode=False)
    
    test_data = [
        ("admin@company.com", "email"),
        ("раypаl.com", "domain"),  # Cyrillic а instead of a
        ("Hello World", "comment"),
        ("café", "message"),
        ("Transfer \u202e\u202d50USD", "password"),
    ]
    
    for text, context in test_data:
        decision_normal = filter_normal.evaluate_text(text, context)
        decision_strict = filter_strict.evaluate_text(text, context)
        
        print(f"\nText: {repr(text)} [{context}]")
        print(f"  Normal Mode: {decision_normal['decision']} (score: {decision_normal['adjusted_score']})")
        print(f"  Strict Mode: {decision_strict['decision']} (score: {decision_strict['adjusted_score']})")
        if decision_normal['reasons']:
            for reason in decision_normal['reasons'][:2]:
                print(f"    - {reason}")
    
    # 2. Batch Analysis Demo
    print("\n\n[2] BATCH ANALYSIS")
    print("-" * 80)
    
    batch_texts = [
        "Hello World",
        "Hеllo World",  # Cyrillic е
        "Hello​World",  # Zero-width space
        "café résumé",
        "Transfer \u202e\u202d50USD",
    ]
    
    batch_analyzer = BatchThreatAnalyzer()
    report = batch_analyzer.analyze_batch(
        batch_texts,
        [f"Legitimate {i}" if i % 2 == 0 else f"Suspicious {i}" for i in range(len(batch_texts))]
    )
    
    print(f"Total Analyzed: {report['summary']['total_analyzed']}")
    print(f"Threats Found: {report['summary']['threats_found']}")
    print(f"High-Risk Texts: {len(report['summary']['high_risk_texts'])}")
    
    if report['summary']['high_risk_texts']:
        print("\nHigh-Risk Detections:")
        for item in report['summary']['high_risk_texts']:
            print(f"  - {item['description']}: {item['threat_level']} (score: {item['score']})")
    
    # 3. Homoglyph Detection
    print("\n\n[3] HOMOGLYPH DETECTION")
    print("-" * 80)
    
    homoglyph_tests = [
        "amazon.com",
        "амазон.com",  # Cyrillic а
        "раypал.com",  # Cyrillic р and а
    ]
    
    for domain in homoglyph_tests:
        analysis = HomoglyphDetector.find_all_homoglyphs(domain)
        print(f"\nDomain: {domain}")
        print(f"  Has Homoglyphs: {analysis['has_homoglyphs']}")
        if analysis['has_homoglyphs']:
            print(f"  Total: {analysis['total_homoglyphs']}")
            print(f"  Risk: {analysis['risk_assessment']}")
    
    # 4. Behavioral Analysis
    print("\n\n[4] BEHAVIORAL ANOMALY DETECTION")
    print("-" * 80)
    
    behavioral_tests = [
        "Normal text",
        "Hello мир 世界",  # Multi-script
        "ñ̃̃̃̃̃",  # Stacked combining marks
        "\u200B\u200B\u200B test",  # Zero-width spam
    ]
    
    for text in behavioral_tests:
        analysis = BehavioralAnalyzer.analyze_features(text)
        print(f"\nText: {repr(text[:40])}")
        print(f"  Risk Level: {analysis['risk_level']}")
        if analysis['anomalies'] != ['NONE']:
            for anomaly in analysis['anomalies']:
                print(f"    - {anomaly}")
    
    print("\n" + "=" * 80)
    print("Analysis Complete")
    print("=" * 80 + "\n")
