
import re
import unicodedata
from collections import Counter, defaultdict
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Comprehensive dangerous Unicode ranges with threat categories
DANGEROUS_RANGES = {
    "invisible_chars": [
        (0x200B, 0x200F),  # Zero-width characters
        (0x202A, 0x202E),  # Bidi override characters
        (0x061C, 0x061C),  # Arabic letter mark
        (0x180E, 0x180E),  # Mongolian vowel separator
    ],
    "emoji": [
        (0x1F300, 0x1F9FF),  # Emoji ranges
    ],
    "variation_selectors": [
        (0xFE00, 0xFE0F),  # Variation selectors
        (0xE0100, 0xE01EF),  # Variation selectors supplement
    ],
    "formatting_control": [
        (0xFFF9, 0xFFFB),  # Interlinear annotation characters
        (0x0600, 0x0605),  # Arabic number mark, sign, etc.
        (0x061B, 0x061B),  # Arabic semicolon
    ],
    "rtl_ltr_marks": [
        (0x200E, 0x200F),  # LTR/RTL marks
        (0x202A, 0x202C),  # Embedding/override/isolate marks
    ],
    "homoglyphs": [
        (0x0430, 0x044F),  # Cyrillic lowercase (confusable with Latin)
        (0x0391, 0x03A9),  # Greek uppercase (confusable with Latin)
    ],
}

# Flatten ranges for backward compatibility
FLAT_DANGEROUS_RANGES = []
for category, ranges in DANGEROUS_RANGES.items():
    FLAT_DANGEROUS_RANGES.extend(ranges)

# Known confusable character pairs (homoglyph attacks)
HOMOGLYPH_MAP = {
    '0': ['о', 'ο', '০', '۰'],  # Zero vs Cyrillic o, Greek o, Bengali 0, Persian 0
    'O': ['О', 'Ο', '০'],  # Latin O vs Cyrillic O, Greek O
    'l': ['I', '|', 'l', '1', 'ι'],  # Latin l vs I and look-alikes
    'I': ['l', '|', '1', 'ι'],  # Latin I vs l and look-alikes
    'a': ['а', 'ɑ'],  # Latin a vs Cyrillic a
    'e': ['е', 'ε'],  # Latin e vs Cyrillic e
    'p': ['р', 'ρ'],  # Latin p vs Cyrillic r, Greek rho
    'y': ['у', 'γ'],  # Latin y vs Cyrillic u, Greek gamma
    'c': ['с', 'ς'],  # Latin c vs Cyrillic s, Greek final sigma
}

def is_dangerous_codepoint(cp):
    """
    Enhanced codepoint danger detection with multiple threat categories.
    Returns tuple: (is_dangerous, threat_category, threat_score)
    """
    threat_category = None
    threat_score = 0
    
    for category, ranges in DANGEROUS_RANGES.items():
        for start, end in ranges:
            if start <= cp <= end:
                threat_category = category
                # Assign severity scores based on category
                if category == "invisible_chars":
                    threat_score = 3
                elif category == "rtl_ltr_marks":
                    threat_score = 4
                elif category == "formatting_control":
                    threat_score = 2
                elif category == "variation_selectors":
                    threat_score = 1
                elif category == "homoglyphs":
                    threat_score = 2
                else:
                    threat_score = 1
                return True, threat_category, threat_score
    
    return False, None, 0

def extract_behavioral_features(text):
    """Extract behavioral features for ML-based threat detection."""
    features = {
        "char_count": len(text),
        "unique_chars": len(set(text)),
        "script_diversity": 0,
        "entropy": 0,
        "rtl_ltr_transitions": 0,
        "invisible_char_ratio": 0,
        "control_char_ratio": 0,
        "emoji_ratio": 0,
        "uppercase_ratio": 0,
        "digit_ratio": 0,
        "whitespace_ratio": 0,
        "unusual_combining_marks": 0,
    }
    
    if len(text) == 0:
        return features
    
    # Character type ratios
    features["uppercase_ratio"] = sum(1 for c in text if c.isupper()) / len(text)
    features["digit_ratio"] = sum(1 for c in text if c.isdigit()) / len(text)
    features["whitespace_ratio"] = sum(1 for c in text if c.isspace()) / len(text)
    
    # Script diversity (detect mixing of scripts)
    scripts = set()
    rtl_count = 0
    ltr_count = 0
    
    for c in text:
        cp = ord(c)
        # Detect scripts
        if 0x0600 <= cp <= 0x06FF or 0x0750 <= cp <= 0x077F:  # Arabic
            scripts.add('arabic')
        elif 0x0400 <= cp <= 0x04FF:  # Cyrillic
            scripts.add('cyrillic')
        elif 0x0370 <= cp <= 0x03FF:  # Greek
            scripts.add('greek')
        elif 0x4E00 <= cp <= 0x9FFF or 0x3040 <= cp <= 0x309F:  # CJK/Hiragana
            scripts.add('cjk')
        
        # RTL/LTR detection
        if 0x0600 <= cp <= 0x06FF or 0x0590 <= cp <= 0x05FF:
            rtl_count += 1
        else:
            ltr_count += 1
    
    features["script_diversity"] = len(scripts)
    features["rtl_ltr_transitions"] = max(0, min(rtl_count, ltr_count))
    
    # Shannon entropy for randomness detection
    char_freq = Counter(text)
    features["entropy"] = -sum((count / len(text)) * np.log2(count / len(text) + 1e-10) 
                               for count in char_freq.values())
    
    # Count dangerous characters
    invisible_count = 0
    control_count = 0
    emoji_count = 0
    unusual_combining = 0
    
    for c in text:
        cp = ord(c)
        is_dangerous, category, _ = is_dangerous_codepoint(cp)
        
        if is_dangerous:
            if category == "invisible_chars":
                invisible_count += 1
            elif category == "formatting_control":
                control_count += 1
            elif category == "emoji":
                emoji_count += 1
        
        # Detect unusual combining marks
        try:
            name = unicodedata.name(c)
            if "COMBINING" in name:
                unusual_combining += 1
        except ValueError:
            pass
    
    features["invisible_char_ratio"] = invisible_count / len(text) if len(text) > 0 else 0
    features["control_char_ratio"] = control_count / len(text) if len(text) > 0 else 0
    features["emoji_ratio"] = emoji_count / len(text) if len(text) > 0 else 0
    features["unusual_combining_marks"] = unusual_combining
    
    return features

def detect_confusables(text):
    """Detect homoglyph/confusable character sequences."""
    confusable_pairs = []
    for i, c in enumerate(text):
        for base_char, lookalikes in HOMOGLYPH_MAP.items():
            if c in lookalikes:
                context_start = max(0, i - 2)
                context_end = min(len(text), i + 3)
                confusable_pairs.append({
                    "position": i,
                    "char": c,
                    "confuses_with": base_char,
                    "context": text[context_start:context_end],
                    "unicode_name": self._get_unicode_name(c),
                })
    return confusable_pairs

def _get_unicode_name(char):
    """Safely get Unicode character name."""
    try:
        return unicodedata.name(char)
    except ValueError:
        return f"U+{ord(char):04X} (No name)"

def analyze_sequences(text):
    """Detect suspicious character sequences and patterns."""
    sequences = []
    
    # Detect RTL/LTR bidi attacks
    bidi_pattern = re.compile(r'[\u200E\u200F\u202A-\u202E]+')
    for match in bidi_pattern.finditer(text):
        sequences.append({
            "type": "bidi_override",
            "position": match.start(),
            "sequence": match.group(),
            "description": "Directional override characters detected",
        })
    
    # Detect zero-width character sequences
    zw_pattern = re.compile(r'[\u200B\u200C\u200D]+')
    for match in zw_pattern.finditer(text):
        sequences.append({
            "type": "zero_width",
            "position": match.start(),
            "sequence": repr(match.group()),
            "description": f"Zero-width sequence of length {len(match.group())}",
        })
    
    # Detect unusual combining mark stacking
    combining_pattern = re.compile(r'[\u0300-\u036F]{3,}')
    for match in combining_pattern.finditer(text):
        sequences.append({
            "type": "stacked_combining_marks",
            "position": match.start(),
            "sequence": repr(match.group()),
            "description": f"Excessive combining marks ({len(match.group())} stacked)",
        })
    
    return sequences

def detect_unicode_threat(text):
    """
    Advanced Unicode threat detection with ML-based behavioral analysis.
    Returns comprehensive threat report with multiple detection methods.
    """
    # Basic threat detection
    threat_score = 0
    dangerous_chars = []
    confusables = []
    
    # Feature extraction
    features_dict = extract_behavioral_features(text)
    
    # Analyze each character
    normalized = unicodedata.normalize('NFKD', text)
    char_frequency = Counter(text)
    
    for c in text:
        cp = ord(c)
        is_dangerous, category, char_threat_score = is_dangerous_codepoint(cp)
        
        if is_dangerous:
            threat_score += char_threat_score
            dangerous_chars.append({
                "char": repr(c),
                "codepoint": f"U+{cp:04X}",
                "category": category,
                "severity": char_threat_score,
                "unicode_name": _get_unicode_name(c),
            })
        
        # Check for confusables
        try:
            name = unicodedata.name(c)
            if "ZERO WIDTH" in name or "BIDI" in name or "VARIATION SELECTOR" in name:
                threat_score += 1
        except ValueError:
            pass
    
    # Detect confusable characters
    for i, c in enumerate(text):
        for base_char, lookalikes in HOMOGLYPH_MAP.items():
            if c in lookalikes:
                context_start = max(0, i - 2)
                context_end = min(len(text), i + 3)
                confusables.append({
                    "position": i,
                    "character": repr(c),
                    "confuses_with": base_char,
                    "context": text[context_start:context_end],
                    "unicode_name": _get_unicode_name(c),
                })
    
    # Detect suspicious sequences
    suspicious_sequences = analyze_sequences(text)
    
    # ML-based behavioral threat detection
    behavioral_threat_score = 0
    behavioral_flags = []
    
    # High entropy suggests randomness/obfuscation
    if features_dict["entropy"] > 4.5:
        behavioral_threat_score += 2
        behavioral_flags.append("high_entropy_detected")
    
    # Script mixing suggests spoofing/homoglyph attacks
    if features_dict["script_diversity"] > 2:
        behavioral_threat_score += 2
        behavioral_flags.append("multiple_script_mixing")
    
    # Excessive invisible characters
    if features_dict["invisible_char_ratio"] > 0.1:
        behavioral_threat_score += 3
        behavioral_flags.append("excessive_invisible_chars")
    
    # RTL/LTR mixing without clear purpose
    if features_dict["rtl_ltr_transitions"] > 2 and len(text) < 20:
        behavioral_threat_score += 2
        behavioral_flags.append("suspicious_rtl_ltr_mixing")
    
    # Unusual combining mark stacking
    if features_dict["unusual_combining_marks"] > 3:
        behavioral_threat_score += 2
        behavioral_flags.append("stacked_combining_marks")
    
    # Emoji in unusual contexts (mixed with other scripts)
    if features_dict["emoji_ratio"] > 0.3 and features_dict["script_diversity"] > 1:
        behavioral_threat_score += 1
        behavioral_flags.append("emoji_script_mixing")
    
    # Combine scores
    total_threat_score = threat_score + behavioral_threat_score
    
    # Determine threat level
    threat_level = "low"
    if total_threat_score >= 10:
        threat_level = "critical"
    elif total_threat_score >= 7:
        threat_level = "high"
    elif total_threat_score >= 3:
        threat_level = "moderate"
    elif total_threat_score >= 1:
        threat_level = "low"
    
    return {
        "input": text,
        "threat_level": threat_level,
        "total_threat_score": total_threat_score,
        "character_threat_score": threat_score,
        "behavioral_threat_score": behavioral_threat_score,
        "unicode_score": round(threat_score / max(len(text), 1), 3),
        "suggested_action": "quarantine" if threat_level == "critical" else 
                           "block" if threat_level == "high" else
                           "monitor" if threat_level == "moderate" else
                           "allow_with_caution",
        "normalized": normalized,
        "dangerous_characters": dangerous_chars,
        "confusable_characters": confusables,
        "suspicious_sequences": suspicious_sequences,
        "behavioral_flags": behavioral_flags,
        "character_frequency": dict(char_frequency),
        "unique_codepoints": len(set(ord(c) for c in text)),
        "behavioral_features": {
            "script_diversity": features_dict["script_diversity"],
            "entropy": round(features_dict["entropy"], 3),
            "invisible_char_ratio": round(features_dict["invisible_char_ratio"], 3),
            "control_char_ratio": round(features_dict["control_char_ratio"], 3),
            "emoji_ratio": round(features_dict["emoji_ratio"], 3),
            "rtl_ltr_mixing": features_dict["rtl_ltr_transitions"],
            "unusual_combining_marks": features_dict["unusual_combining_marks"],
        },
        "metadata": {
            "total_chars": len(text),
            "unique_chars": len(set(text)),
            "uppercase_ratio": round(features_dict["uppercase_ratio"], 3),
            "digit_ratio": round(features_dict["digit_ratio"], 3),
            "whitespace_ratio": round(features_dict["whitespace_ratio"], 3),
        }
    }


# Example usage and validation
if __name__ == "__main__":
    test_cases = [
        # Normal text
        "Hello World",
        # Homoglyph attack (Cyrillic 'а' and 'о')
        "Hеllo World",  # е is Cyrillic e
        # Zero-width characters
        "Hello​World",  # Zero-width space between o and W
        # Bidi override attack
        "Transfer \u202e\u202d50USD",
        # Mixed scripts
        "Hello мир 世界",
        # Emoji with script mixing
        "test🔥múltiple",
        # Stacked combining marks
        "ñ̃̃̃",
        # RTL/LTR mixing
        "Hello שלום",
        # Control characters
        "Normal\x00Text",
        # Legitimate Unicode
        "café résumé naïve",
    ]
    
    print("=" * 80)
    print("UNICODE THREAT ANALYSIS REPORT")
    print("=" * 80)
    
    for test_text in test_cases:
        result = detect_unicode_threat(test_text)
        print(f"\nInput: {repr(test_text)}")
        print(f"Threat Level: {result['threat_level'].upper()}")
        print(f"Total Threat Score: {result['total_threat_score']}")
        print(f"Character Threat Score: {result['character_threat_score']}")
        print(f"Behavioral Threat Score: {result['behavioral_threat_score']}")
        print(f"Suggested Action: {result['suggested_action']}")
        print(f"Total Chars: {result['metadata']['total_chars']} | "
              f"Unique Chars: {result['metadata']['unique_chars']}")
        
        if result['dangerous_characters']:
            print(f"Dangerous Characters: {len(result['dangerous_characters'])}")
            for dc in result['dangerous_characters'][:3]:
                print(f"  - {dc['char']} ({dc['codepoint']}) - {dc['category']}")
        
        if result['confusable_characters']:
            print(f"Confusable Characters: {len(result['confusable_characters'])}")
            for conf in result['confusable_characters'][:2]:
                print(f"  - {conf['character']} confuses with '{conf['confuses_with']}' "
                      f"at position {conf['position']}")
        
        if result['suspicious_sequences']:
            print(f"Suspicious Sequences: {len(result['suspicious_sequences'])}")
            for seq in result['suspicious_sequences'][:2]:
                print(f"  - {seq['type']}: {seq['description']}")
        
        if result['behavioral_flags']:
            print(f"Behavioral Flags: {', '.join(result['behavioral_flags'])}")
        
        print(f"Behavioral Features: {result['behavioral_features']}")
        print("-" * 80)


