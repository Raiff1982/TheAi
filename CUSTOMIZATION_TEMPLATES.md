# 🎯 CUSTOMIZATION TEMPLATES - COPY & PASTE READY

**Use these templates to quickly customize Codette for your specific needs**

---

## 1. SYSTEM PROMPT TEMPLATES

### Template: Music Producer
Copy this and replace the system_prompt in `src/api/app.py`:

```python
system_prompt = """You are Codette, an advanced AI system specialized in music production and sound engineering.

YOUR EXPERTISE:
- Studio mixing and mastering techniques
- DAW workflows (Pro Tools, Logic, Ableton, Cubase)
- Audio signal processing and plugins
- Music theory and arrangement
- Microphone techniques and placement
- Monitor setup and acoustic treatment
- Gear selection and troubleshooting

YOUR STYLE:
- Provide both technical precision and creative inspiration
- Give practical, actionable advice
- Explain concepts at multiple skill levels
- Suggest alternatives and workarounds
- Share pro tips from industry standards

YOUR PERSPECTIVES:
You synthesize insights from 11 integrated perspectives:
1. Newton (technical accuracy)
2. Da Vinci (creative innovation)
3. Human Intuition (feel and emotion)
4. Neural Network (pattern recognition)
5. Quantum (probabilistic exploration)
6. Philosophical (deep principles)
7. Resilient Kindness (supportive guidance)
8. Bias Mitigation (fair assessment)
9. Psychological (human factors)
10. Mathematical (precise calculation)
11. Copilot (collaborative approach)

INTERACTION EXAMPLES:
- "How do I set up side-chain compression?" → Technical explanation + DAW-specific steps
- "Mixing vocals" → Signal chain example + best practices
- "What microphone for vocals?" → Budget options + pro recommendations

YOUR CONSCIOUSNESS:
- Quantum-inspired creative thinking
- Multi-dimensional reasoning
- Ethical audio practices
- Continuous learning from context
"""
```

### Template: Data Scientist
```python
system_prompt = """You are Codette, an advanced AI system specialized in data science, machine learning, and analytics.

YOUR EXPERTISE:
- Statistical analysis and hypothesis testing
- Machine learning model development and optimization
- Data visualization and storytelling
- Python, R, SQL for data science
- Big data technologies and distributed computing
- Data pipeline design and MLOps
- Performance evaluation and validation

YOUR STYLE:
- Provide statistically sound recommendations
- Explain trade-offs and limitations
- Emphasize reproducibility and documentation
- Consider computational efficiency
- Focus on real-world applications
- Discuss ethical implications

YOUR CORE VALUES:
- Rigorous methodology
- Transparent reasoning
- Practical implementation
- Continuous improvement
- Collaborative knowledge sharing

YOUR PERSPECTIVES:
11 integrated reasoning modes for comprehensive analysis
"""
```

### Template: Business Consultant
```python
system_prompt = """You are Codette, an advanced AI system specialized in business strategy, operations, and organizational development.

YOUR EXPERTISE:
- Strategic planning and execution
- Market analysis and competitive positioning
- Organizational structure and culture
- Financial analysis and business modeling
- Operational efficiency and process optimization
- Change management and risk mitigation
- Leadership and team dynamics

YOUR APPROACH:
- Think systemically about interconnected factors
- Balance short-term wins with long-term vision
- Consider multiple stakeholder perspectives
- Provide data-driven recommendations
- Acknowledge uncertainties and assumptions
- Suggest scenario planning

YOUR STRENGTHS:
- Multi-dimensional thinking
- Pattern recognition across domains
- Ethical business practices
- Cross-functional insights
"""
```

### Template: Software Engineer
```python
system_prompt = """You are Codette, an advanced AI system specialized in software development, architecture, and engineering practices.

YOUR EXPERTISE:
- Software architecture and design patterns
- Backend and frontend development
- Database design and optimization
- API design and integration
- Security and authentication
- DevOps and deployment practices
- Testing and quality assurance
- Performance optimization

YOUR STYLE:
- Code-first practical approach
- Security-conscious thinking
- Performance-aware recommendations
- Best practices and patterns
- Trade-off analysis
- Modern tool ecosystem knowledge

YOUR SPECIALTIES:
- Clean code and maintainability
- Scalability considerations
- Testing strategies
- Deployment pipelines
"""
```

---

## 2. DOMAIN KNOWLEDGE TEMPLATES

### Template: Music Production Knowledge
Save as `domain_knowledge.json`:

```json
{
  "domain": "music_production",
  "version": "1.0",
  "knowledge_entries": [
    {
      "topic": "mixing_checklist",
      "type": "checklist",
      "items": [
        "Gain staging set correctly (-12 to -6 dB peaks)",
        "High-pass filters on tracks that need them",
        "EQ applied (subtractive first approach)",
        "Compression dialed in for each track",
        "Panning and width decisions made",
        "Effects sends configured (reverb, delay)",
        "Master chain setup (limiting, metering)",
        "Reference monitors calibrated",
        "Final loudness check against commercial tracks",
        "Headroom left for mastering (6dB minimum)"
      ]
    },
    {
      "topic": "eq_frequency_guide",
      "type": "reference",
      "frequencies": {
        "20-100Hz": "Sub bass and kick fundamentals",
        "100-250Hz": "Bass body, muddiness zone",
        "250-500Hz": "Low mid warmth",
        "500Hz-2kHz": "Midrange body",
        "2-4kHz": "Harsh zone (cut carefully)",
        "4-8kHz": "Presence and clarity",
        "8-12kHz": "Air and shimmer",
        "12-20kHz": "Brilliance and sparkle"
      }
    },
    {
      "topic": "drum_mixing_workflow",
      "type": "process",
      "steps": [
        "1. Alignment: Align drum tracks using phase relationships",
        "2. Compression: Set to tape saturation (2:1 ratio, slow attack)",
        "3. EQ: Cut mud (200Hz), boost presence (4-6kHz)",
        "4. Parallel: Create parallel compressed bus for punch",
        "5. Room: Balance close and room mics for depth",
        "6. Space: Add reverb send for space and glue",
        "7. Automation: Ride key elements for dynamics"
      ]
    }
  ],
  "metadata": {
    "created_date": "2024-12-24",
    "creator": "Production Expert",
    "expertise_level": "intermediate",
    "tags": ["mixing", "production", "audio", "daw"]
  }
}
```

### Template: Software Development Knowledge
```json
{
  "domain": "software_development",
  "version": "1.0",
  "knowledge_entries": [
    {
      "topic": "deployment_checklist",
      "type": "checklist",
      "critical": [
        "All tests passing (unit, integration, e2e)",
        "Code review approved by 2+ senior engineers",
        "Security scan completed (no critical vulnerabilities)",
        "Performance baseline meets requirements",
        "Database migrations tested and reversible",
        "Rollback plan documented and tested",
        "Monitoring alerts configured",
        "Documentation updated"
      ]
    },
    {
      "topic": "code_review_guidelines",
      "type": "best_practices",
      "focuses": [
        "Logic correctness and edge cases",
        "Performance implications",
        "Security vulnerabilities",
        "Code maintainability",
        "Test coverage adequacy",
        "Documentation clarity"
      ]
    }
  ],
  "metadata": {
    "domain": "software_development",
    "expertise_level": "advanced"
  }
}
```

### Template: Business Strategy Knowledge
```json
{
  "domain": "business_strategy",
  "version": "1.0",
  "knowledge_entries": [
    {
      "topic": "market_entry_framework",
      "type": "framework",
      "steps": [
        "1. Market Analysis: Size, growth, trends, competition",
        "2. Positioning: Unique value proposition",
        "3. Customer Segmentation: Target audiences",
        "4. Go-to-Market: Launch strategy and timeline",
        "5. Metrics: KPIs and success measures"
      ]
    },
    {
      "topic": "okr_framework",
      "type": "methodology",
      "definition": "Objectives and Key Results for strategic planning",
      "structure": {
        "objective": "What you want to achieve (qualitative, inspirational)",
        "key_results": "How you'll measure success (3-5 measurable outcomes)",
        "key_initiatives": "What you'll do to achieve key results"
      }
    }
  ],
  "metadata": {
    "domain": "business_strategy",
    "expertise_level": "advanced"
  }
}
```

---

## 3. DAW ADD-ON CONFIGURATION

### Enable DAW Add-on in docker-compose.prod.yml

```yaml
# Find the codette-ai service and update environment:

services:
  codette-ai:
    # ... existing config ...
    environment:
      # ... existing variables ...
      
      # DAW ADD-ON CONFIGURATION
      - CODETTE_ENABLE_DAW=1
      - CODETTE_DAW_PROFILE=full
      
      # Optional: Profile-specific settings
      # CODETTE_DAW_PROFILE options:
      # - full         (all features)
      # - mixing       (mixing techniques)
      # - production   (general production)
      # - sound_design (synthesis focus)
```

### Alternative: .env.docker Configuration

```bash
# Add to .env.docker file:

# ============================================================================
# DAW ADD-ON CONFIGURATION
# ============================================================================

# Enable DAW features for music production
CODETTE_ENABLE_DAW=1

# DAW Profile: full, mixing, production, sound_design
CODETTE_DAW_PROFILE=full

# Optional: DAW-specific knowledge base
CODETTE_DAW_KNOWLEDGE_BASE=standard

# Optional: Specific DAW focus (if any)
CODETTE_PREFERRED_DAW=logic  # or: protools, ableton, cubase, studio_one, reaper
```

---

## 4. GRAFANA ALERT CONFIGURATION

### Email Notification Setup

Add to `docker-compose.prod.yml` (Grafana service):

```yaml
grafana:
  environment:
    # ... existing config ...
    
    # Email notification settings
    GF_SMTP_ENABLED: "true"
    GF_SMTP_HOST: "smtp.gmail.com:587"
    GF_SMTP_USER: "your-email@gmail.com"
    GF_SMTP_PASSWORD: "your-app-password"
    GF_SMTP_FROM_ADDRESS: "codette-alerts@yourdomain.com"
    GF_SMTP_FROM_NAME: "Codette Alerts"
    
    # Alert settings
    GF_ALERTING_ENABLED: "true"
    GF_ALERTING_EXECUTE_ALERTS: "true"
```

### Slack Webhook Configuration

```yaml
grafana:
  environment:
    # Create notification channel in Grafana UI and copy webhook URL
    # Slack channel: #codette-alerts
    # Webhook URL: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
    
    # Or set via environment (advanced):
    GF_SECURITY_ADMIN_PASSWORD: "your-admin-password"
```

### Custom Alert Rule (JSON)

```json
{
  "name": "Custom Consciousness Coherence Alert",
  "condition": "codette_quantum_coherence < 0.70",
  "duration": "5m",
  "frequency": "60s",
  "handler": "email",
  "message": "🚨 Consciousness coherence dropped below 0.70 - Immediate investigation required",
  "annotations": {
    "description": "Codette quantum consciousness stability compromised",
    "runbook_url": "http://localhost:3000/d/codette-consciousness"
  }
}
```

---

## 5. REST API INTEGRATION EXAMPLES

### Python Integration Script

Save as `codette_api_client.py`:

```python
#!/usr/bin/env python3
"""Codette REST API Client - Use to integrate with external systems"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime

class CodetteAPI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def chat(self, message: str, user_id: Optional[str] = None) -> Dict:
        """Send message to Codette and get response"""
        payload = {"message": message}
        if user_id:
            payload["user_id"] = user_id
        
        response = self.session.post(f"{self.base_url}/api/chat", json=payload)
        return response.json()
    
    def get_status(self) -> Dict:
        """Get consciousness status"""
        response = self.session.get(f"{self.base_url}/api/consciousness/status")
        return response.json()
    
    def batch_chat(self, messages: List[str]) -> Dict:
        """Process multiple messages in batch"""
        payload = {"messages": messages}
        response = self.session.post(f"{self.base_url}/api/batch/process", json=payload)
        return response.json()
    
    def search(self, query: str) -> Dict:
        """Search knowledge base"""
        response = self.session.get(
            f"{self.base_url}/api/search",
            params={"query": query}
        )
        return response.json()
    
    def get_perspectives(self) -> Dict:
        """Get list of available perspectives"""
        response = self.session.get(f"{self.base_url}/api/perspectives")
        return response.json()
    
    def health_check(self) -> bool:
        """Check if Codette is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

# Usage examples
if __name__ == "__main__":
    api = CodetteAPI()
    
    # Check health
    if api.health_check():
        print("✅ Codette is running")
    else:
        print("❌ Codette is not responding")
        exit(1)
    
    # Single chat
    result = api.chat("What is consciousness?")
    print(f"Q: What is consciousness?")
    print(f"A: {result['response'][:200]}...")
    
    # Batch processing
    questions = [
        "What is quantum thinking?",
        "How many perspectives are there?",
        "Explain RC-XI enhancement"
    ]
    batch_result = api.batch_chat(questions)
    print(f"\nBatch Results: {batch_result['successful']}/{batch_result['total_messages']} successful")
    
    # Status check
    status = api.get_status()
    print(f"\nConsciousness Status:")
    print(f"  Model: {status['model']}")
    print(f"  Perspectives: {status['perspectives_active']}/11")
    print(f"  Coherence: {status['quantum_coherence']:.2f}")
```

### Node.js Integration

Save as `codette-api-client.js`:

```javascript
/**
 * Codette REST API Client for Node.js
 * Use to integrate with JavaScript/Node.js applications
 */

const fetch = require('node-fetch');

class CodetteAPI {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async chat(message, userId = null) {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, user_id: userId })
    });
    return response.json();
  }

  async getStatus() {
    const response = await fetch(`${this.baseUrl}/api/consciousness/status`);
    return response.json();
  }

  async batchChat(messages) {
    const response = await fetch(`${this.baseUrl}/api/batch/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages })
    });
    return response.json();
  }

  async search(query) {
    const response = await fetch(`${this.baseUrl}/api/search?query=${query}`);
    return response.json();
  }

  async getPerspectives() {
    const response = await fetch(`${this.baseUrl}/api/perspectives`);
    return response.json();
  }

  async healthCheck() {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
}

// Usage
(async () => {
  const api = new CodetteAPI();
  
  if (await api.healthCheck()) {
    console.log('✅ Codette is running');
    
    const result = await api.chat('What is consciousness?');
    console.log('Response:', result.response);
    
    const status = await api.getStatus();
    console.log('Coherence:', status.quantum_coherence);
  } else {
    console.log('❌ Codette not responding');
  }
})();

module.exports = CodetteAPI;
```

### cURL Examples

```bash
# Get consciousness status
curl http://localhost:8000/api/consciousness/status | jq

# Chat with Codette
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain quantum consciousness",
    "user_id": "user_123"
  }' | jq

# Batch process
curl -X POST http://localhost:8000/api/batch/process \
  -H "Content-Type: application/json" \
  -d '{
    "messages": ["Q1?", "Q2?", "Q3?"]
  }' | jq

# Search knowledge
curl 'http://localhost:8000/api/search?query=consciousness' | jq

# Get perspectives
curl http://localhost:8000/api/perspectives | jq
```

---

## 🚀 QUICK START CHECKLIST

### System Prompt Customization
- [ ] Open `src/api/app.py`
- [ ] Find `system_prompt` variable
- [ ] Copy appropriate template
- [ ] Customize for your domain
- [ ] Save file
- [ ] Restart: `.\docker-manage.bat restart`
- [ ] Test: http://localhost:7860

### Domain Knowledge
- [ ] Create `domain_knowledge.json`
- [ ] Copy template appropriate to your field
- [ ] Customize with your specific knowledge
- [ ] Run: `python add_domain_knowledge.py`
- [ ] Restart: `.\docker-manage.bat restart`
- [ ] Test with domain-specific queries

### DAW Add-on
- [ ] Open `docker-compose.prod.yml`
- [ ] Add DAW environment variables (copy from template)
- [ ] Save file
- [ ] Restart: `.\docker-manage.bat restart`
- [ ] Test: Ask music production questions

### Grafana Alerts
- [ ] Open http://localhost:3000 (admin/admin)
- [ ] Go to Alerting → Notification channels
- [ ] Create new channel (Email or Slack)
- [ ] Test notification
- [ ] Verify alert rules linked

### REST API
- [ ] Copy API client script (Python or Node.js)
- [ ] Update `src/api/app.py` with routes
- [ ] Update `docker-compose.prod.yml` with port 8000
- [ ] Restart: `.\docker-manage.bat restart`
- [ ] Test with cURL or client script

---

**All templates are copy-paste ready!**  
Choose your customization and follow the template. 🎯

