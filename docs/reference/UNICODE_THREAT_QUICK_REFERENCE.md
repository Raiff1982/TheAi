# Unicode Threat Analyzer - Quick Reference

## Installation & Setup

```bash
# No additional dependencies required beyond standard library
# Optional: numpy, sklearn (but not required for core functionality)

python unicode_threat_analyzer2.py          # Run with built-in examples
python test_threat_analyzer.py              # Run test suite
python unicode_threat_advanced_patterns.py  # Run advanced demonstrations
```

## Basic Usage

### Simple Threat Detection
```python
from unicode_threat_analyzer2 import detect_unicode_threat

result = detect_unicode_threat("your text here")
print(f"Threat Level: {result['threat_level']}")
print(f"Action: {result['suggested_action']}")
```

### Check for Specific Threat Types
```python
result = detect_unicode_threat(text)

# Check for homoglyphs (spoofing)
if result['confusable_characters']:
    print(f"Found {len(result['confusable_characters'])} homoglyphs")

# Check for invisible characters
if result['dangerous_characters']:
    for dc in result['dangerous_characters']:
        if dc['category'] == 'invisible_chars':
            print(f"Found hidden character: {dc['unicode_name']}")

# Check for suspicious patterns
if result['suspicious_sequences']:
    for seq in result['suspicious_sequences']:
        print(f"Pattern: {seq['type']} at position {seq['position']}")
```

## Advanced Usage

### Context-Aware Security Filter
```python
from unicode_threat_advanced_patterns import UnicodeSecurityFilter

filter = UnicodeSecurityFilter(strict_mode=False)

# Different contexts have different risk levels
email_check = filter.evaluate_text("user@domain.com", context="email")
domain_check = filter.evaluate_text("domain.com", context="domain")
password_check = filter.evaluate_text("password123", context="password")

if email_check['allow']:
    process_email(email)
else:
    alert(f"Blocked: {email_check['reasons']}")
```

### Batch Analysis
```python
from unicode_threat_advanced_patterns import BatchThreatAnalyzer

analyzer = BatchThreatAnalyzer()
texts = ["Hello World", "Hеllo World", "мир world"]
descriptions = ["Normal", "Homoglyph", "Mixed Script"]

report = analyzer.analyze_batch(texts, descriptions)
print(f"Threats Found: {report['summary']['threats_found']}")
print(f"High-Risk Percentage: {report['statistics']['high_risk_percentage']}%")
```

### Homoglyph Detection
```python
from unicode_threat_advanced_patterns import HomoglyphDetector

analysis = HomoglyphDetector.find_all_homoglyphs("амазон.com")
if analysis['has_homoglyphs']:
    print(f"Risk: {analysis['risk_assessment']}")
    for base, homoglyphs in analysis['by_base_character'].items():
        print(f"  '{base}' → {len(homoglyphs)} lookalikes")
```

### Behavioral Analysis
```python
from unicode_threat_advanced_patterns import BehavioralAnalyzer

analysis = BehavioralAnalyzer.analyze_features("Hello мир 世界")
print(f"Risk Level: {analysis['risk_level']}")
for anomaly in analysis['anomalies']:
    print(f"  - {anomaly}")
```

## Threat Levels & Actions

| Level | Score | Action | Use Case |
|-------|-------|--------|----------|
| Critical | ≥10 | QUARANTINE | Definite malicious intent |
| High | ≥7 | BLOCK | Likely attack pattern |
| Moderate | ≥3 | MONITOR | Suspicious but maybe legitimate |
| Low | ≥1 | ALLOW_WITH_CAUTION | Probably safe |
| None | 0 | ALLOW | Safe |

## Common Attack Patterns

### 1. Homoglyph Attack (Domain Spoofing)
```
Legitimate:  amazon.com  (Latin 'a')
Malicious:   амазон.com  (Cyrillic 'а')

Detection:
- result['confusable_characters'] contains items
- character 'а' confuses_with 'a'
```

### 2. Bidi Override (Scareware)
```
Display:    Transfer 50USD
Actual:     Transfer \u202e\u202d50USD (reverses text)

Detection:
- result['threat_level'] = 'high'
- result['behavioral_flags'] = ['excessive_invisible_chars']
- result['dangerous_characters'] shows U+202E, U+202D
```

### 3. Zero-Width Character Injection
```
Display:    HelloWorld
Actual:     Hello​World (zero-width space between)

Detection:
- result['invisible_char_ratio'] > 0.05
- result['suspicious_sequences'] shows zero_width pattern
```

### 4. Script Mixing (Homoglyph)
```
Text:       "Hello мир"  (Latin + Cyrillic)

Detection:
- result['behavioral_features']['script_diversity'] > 1
- result['behavioral_flags'] may include 'multiple_script_mixing'
```

## Threat Score Breakdown

```python
result = detect_unicode_threat(text)

# Total score components:
total = result['character_threat_score'] + result['behavioral_threat_score']

# Character threats (from dangerous codepoints):
# - invisible_chars: +3 each
# - rtl_ltr_marks: +4 each
# - formatting_control: +2 each
# - variation_selectors: +1 each
# - homoglyphs: +2 each

# Behavioral threats (from patterns):
# - high_entropy: +2
# - multiple_script_mixing: +2
# - excessive_invisible_chars: +3
# - suspicious_rtl_ltr_mixing: +2
# - stacked_combining_marks: +2
# - emoji_script_mixing: +1
```

## Response Structure

```python
{
    # Decision
    'threat_level': 'low'|'moderate'|'high'|'critical',
    'total_threat_score': int,
    'suggested_action': 'allow_with_caution'|'monitor'|'block'|'quarantine',
    
    # Threats Found
    'dangerous_characters': [{...}],      # Codepoint threats
    'confusable_characters': [{...}],     # Homoglyph threats
    'suspicious_sequences': [{...}],      # Pattern threats
    
    # Analysis Data
    'behavioral_features': {...},         # 7 ML features
    'metadata': {...},                    # Text properties
    'character_frequency': {...},         # char → count
    
    # Details
    'behavioral_flags': [str],            # Warning indicators
    'unicode_score': float,               # Score per character
    'normalized': str,                    # NFKD form
}
```

## Integration Examples

### Web Request Input Validation
```python
def validate_username(username):
    result = detect_unicode_threat(username)
    
    # Block critical or high threats
    if result['threat_level'] in ['critical', 'high']:
        raise ValueError(f"Invalid username: {result['suggested_action']}")
    
    # Allow with caution for moderate
    if result['threat_level'] == 'moderate':
        log_security_event("suspicious_username", username)
    
    return True
```

### Email Security Gateway
```python
def check_email(sender, subject, body):
    sender_result = detect_unicode_threat(sender)
    subject_result = detect_unicode_threat(subject)
    
    # High threats get quarantined
    if any(r['threat_level'] == 'high' for r in [sender_result, subject_result]):
        quarantine_email()
    
    # Moderate threats get flagged
    elif any(r['threat_level'] == 'moderate' for r in [sender_result, subject_result]):
        add_warning_banner()
    
    deliver_email()
```

### URL/Domain Validation
```python
def validate_domain(domain):
    result = detect_unicode_threat(domain)
    
    # Homoglyph attacks are critical for domains
    if result['confusable_characters']:
        return False  # Block domain
    
    # Multiple scripts suggest spoofing
    if result['behavioral_features']['script_diversity'] > 1:
        return False
    
    return True
```

## Performance Tips

1. **Batch Processing**: Use `BatchThreatAnalyzer` for 10+ texts
2. **Context Selection**: Use appropriate context for threshold tuning
3. **Caching**: Cache results for identical inputs
4. **Monitoring**: Track threat statistics for trending

## Troubleshooting

### Q: False Positives for Multi-Language Text
A: Use `context` parameter or moderate-only blocking. Script mixing is legitimate in some contexts.

### Q: Need Stricter Detection
A: Use `UnicodeSecurityFilter(strict_mode=True)` for authentication contexts

### Q: Need More Lenient Detection
A: Only block if `threat_level == 'high'` or higher

### Q: Want Custom Thresholds
A: Modify behavioral rules in `detect_unicode_threat()` or use `evaluate_text()` with custom multipliers

## References

- Unicode Security: https://unicode.org/reports/tr36/
- Bidi Algorithm: https://unicode.org/reports/tr9/
- Homoglyph Attacks: https://en.wikipedia.org/wiki/Homoglyph_attack

---

**Version**: 2.0 (Enhanced)  
**Files**: 
- `unicode_threat_analyzer2.py` - Core library
- `UNICODE_THREAT_ANALYZER_GUIDE.md` - Full documentation
- `unicode_threat_advanced_patterns.py` - Production patterns
- `test_threat_analyzer.py` - Test suite

**Ready for**: Authentication, email security, content moderation, domain validation, input sanitization
