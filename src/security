
import re
import unicodedata

DANGEROUS_RANGES = [
    (0x200B, 0x200F),
    (0x202A, 0x202E),
    (0x1F300, 0x1F9FF),
    (0xFE00, 0xFE0F),
    (0xFFF9, 0xFFFB)
]

def is_dangerous_codepoint(cp):
    return any(start <= cp <= end for start, end in DANGEROUS_RANGES)

def detect_unicode_threat(text):
    threat_score = 0
    confusables = []
    normalized = unicodedata.normalize('NFKD', text)
    for c in text:
        cp = ord(c)
        if is_dangerous_codepoint(cp):
            threat_score += 1
        try:
            name = unicodedata.name(c)
            if "ZERO WIDTH" in name or "BIDI" in name or "VARIATION SELECTOR" in name:
                threat_score += 1
        except ValueError:
            continue
    threat_level = "low"
    if threat_score >= 5:
        threat_level = "high"
    elif threat_score >= 2:
        threat_level = "moderate"
    return {
        "input": text,
        "threat_level": threat_level,
        "unicode_score": round(threat_score / max(len(text), 1), 2),
        "suggested_action": "quarantine" if threat_level == "high" else "monitor",
        "normalized": normalized
    }
