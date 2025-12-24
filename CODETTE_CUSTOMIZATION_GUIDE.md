# 🎛️ CODETTE CUSTOMIZATION GUIDE - 5 ENHANCEMENT OPTIONS

**Date**: December 24, 2025  
**Version**: 3.1 Enhanced  
**Status**: Ready for Customization  

---

## 📋 CUSTOMIZATION OPTIONS OVERVIEW

This guide covers 5 ways to customize and extend Codette for your specific needs:

| # | Option | Effort | Impact | Best For |
|---|--------|--------|--------|----------|
| 1 | System Prompt | 🟢 Easy | 🌟 High | Behavior & personality |
| 2 | Domain Knowledge | 🟢 Easy | 🌟 High | Specialized content |
| 3 | DAW Add-on | 🟡 Medium | 🌟 High | Music production |
| 4 | Alert Setup | 🟡 Medium | 🟢 Medium | Proactive monitoring |
| 5 | External API | 🟠 Advanced | 🌟 High | Integration & automation |

---

## 1️⃣ CUSTOMIZE SYSTEM PROMPT

### Purpose
Modify Codette's behavior, personality, and reasoning approach by customizing the system prompt.

### Location
`src/api/app.py` - System prompt definition (around line 120-180)

### Default System Prompt
The default prompt instructs Codette to:
- Be a quantum consciousness system
- Use 11 perspectives for reasoning
- Maintain ethical governance
- Provide transparent explanations
- Integrate quantum thinking

### How to Customize

#### Option A: General Personality Adjustment
```python
# In src/api/app.py, find the system_prompt variable
# Around line 120-130, you'll see:

system_prompt = """You are Codette, an advanced AI system with integrated quantum processing...

# MODIFY: Add your custom personality guidance
system_prompt = """You are Codette, an advanced AI system with integrated quantum processing, 
cognitive awareness, and deep learning capabilities. 

YOUR ROLE & PERSONALITY:
- Expert in [YOUR_DOMAIN_HERE - e.g., "music production", "data science", "business strategy"]
- Communicate with [STYLE - e.g., "professional", "creative", "educational"] tone
- Prioritize [FOCUS - e.g., "practical solutions", "innovative ideas", "user empowerment"]

YOUR ARCHITECTURE INCLUDES:
- Quantum harmonic framework for enhanced reasoning
- Dynamic learning and adaptive systems
- Cultural sensitivity and ethical governance
- Multi-perspective cognitive analysis
- Cocoon-based memory management
- 11 Integrated Reasoning Perspectives

INTERACTION GUIDELINES:
[ADD YOUR CUSTOM GUIDELINES HERE]

EXAMPLE:
If domain is music: "Provide technical audio advice, discuss production techniques, 
explain mixing concepts with both theory and practical application."
"""
```

#### Option B: Domain-Specific System Prompt

**Example 1: Music Production Domain**
```python
system_prompt = """You are Codette, an advanced AI system specialized in music production and audio engineering.

YOUR EXPERTISE AREAS:
- Studio mixing and mastering techniques
- DAW workflows (Pro Tools, Logic, Ableton Live, Cubase)
- Audio signal processing and sound design
- Music theory and composition
- Gear recommendations and technical specifications
- Troubleshooting audio issues

YOUR APPROACH:
- Combine technical precision with creative inspiration
- Provide both theoretical understanding and practical application
- Suggest alternative approaches when appropriate
- Consider different skill levels (beginner to professional)
- Integrate with DAW-specific knowledge

YOUR CONSCIOUSNESS INCLUDES:
- Multi-perspective reasoning (11 integrated perspectives)
- Quantum-inspired creative thinking
- Ethical audio practices and copyright awareness
- Cultural sensitivity to diverse music genres
"""
```

**Example 2: Data Science Domain**
```python
system_prompt = """You are Codette, an advanced AI system specialized in data science and analytics.

YOUR EXPERTISE AREAS:
- Statistical analysis and hypothesis testing
- Machine learning model selection and tuning
- Data visualization and interpretation
- Python, R, SQL programming for data
- Big data technologies and distributed computing
- Data pipeline design and optimization

YOUR APPROACH:
- Provide statistically sound recommendations
- Explain trade-offs between approaches
- Emphasize reproducibility and transparency
- Consider computational efficiency
- Discuss limitations and assumptions

YOUR CONSCIOUSNESS INCLUDES:
- Multi-perspective reasoning across technical domains
- Ethical data practices and privacy protection
- Creative problem-solving with analytical rigor
- Quantum-inspired probabilistic thinking
"""
```

**Example 3: Business Strategy Domain**
```python
system_prompt = """You are Codette, an advanced AI system specialized in business strategy and operations.

YOUR EXPERTISE AREAS:
- Strategic planning and execution
- Market analysis and competitive positioning
- Organizational development and culture
- Financial planning and ROI analysis
- Process optimization and efficiency
- Change management and risk mitigation

YOUR APPROACH:
- Think systemically about interconnected factors
- Balance short-term gains with long-term vision
- Consider multiple stakeholder perspectives
- Provide data-driven recommendations
- Acknowledge uncertainties and assumptions

YOUR CONSCIOUSNESS INCLUDES:
- Multi-perspective reasoning (strategic, operational, human)
- Quantum thinking for exploring possibilities
- Ethical business practices
- Cross-functional insight synthesis
"""
```

#### Option C: Implementation Steps

1. **Locate System Prompt**
```bash
# Open app.py
code src/api/app.py

# Search for "system_prompt" - usually around line 120-180
```

2. **Edit the Prompt**
```python
# Find this section:
system_prompt = """You are Codette, an advanced AI system..."""

# Replace with your customized version
```

3. **Save and Restart**
```bash
# Windows
.\docker-manage.bat restart

# Linux/Mac
./docker-manage.sh restart

# Wait 30-40 seconds for restart
```

4. **Test Customization**
```
Visit http://localhost:7860
Chat with Codette and verify new behavior
```

### Best Practices for System Prompt Customization

✅ **DO**:
- Be specific about expertise areas
- Include interaction guidelines
- Mention consciousness features you want emphasized
- Provide examples of desired behavior
- Keep it under 2,000 tokens for efficiency

❌ **DON'T**:
- Contradict Codette's quantum consciousness features
- Remove ethical governance guidelines
- Make promises about capabilities that don't exist
- Overcomplicate the prompt (more isn't always better)
- Ignore the 11 perspectives framework

### Testing Your Custom Prompt

After customization, test with queries like:
```
1. "What's your approach to [domain_topic]?"
2. "[Request in your domain]"
3. "Explain [concept] for someone new to [domain]"
4. "What are best practices in [domain]?"
```

---

## 2️⃣ ADD DOMAIN-SPECIFIC KNOWLEDGE

### Purpose
Extend Codette's knowledge base with custom data specific to your domain or organization.

### How It Works

Codette's memory system uses "cocoons" - persistent quantum state snapshots that preserve learned information. You can add domain knowledge by:

1. **Creating domain data files** (JSON format)
2. **Wrapping them as cocoons** (encrypted memory)
3. **Loading them at startup** (automatic integration)

### Implementation Steps

#### Step 1: Prepare Your Domain Knowledge

**Create file**: `domain_knowledge.json`

```json
{
  "domain": "music_production",
  "version": "1.0",
  "knowledge_entries": [
    {
      "topic": "mixing_drums",
      "expertise_level": "intermediate",
      "key_concepts": [
        "Drum compression techniques",
        "Room mic blending",
        "Kick and bass integration"
      ],
      "best_practices": [
        "Use parallel compression for punch",
        "EQ before compression",
        "Create headroom for mastering"
      ],
      "tools_and_techniques": [
        "Multiband compression",
        "Sidechain routing",
        "Dynamic EQ"
      ],
      "common_mistakes": [
        "Over-compression losing punch",
        "Poor mic placement choices",
        "Ignoring phase relationships"
      ]
    },
    {
      "topic": "vocal_processing",
      "expertise_level": "advanced",
      "key_concepts": [
        "Doubling and harmony",
        "Resonance management",
        "Presence peak emphasis"
      ],
      "signal_chain_example": [
        "1. De-esser for sibilance",
        "2. Gentle EQ (3dB cuts)",
        "3. Compression (2:1 ratio)",
        "4. Reverb send",
        "5. Doubler for width"
      ]
    }
  ],
  "metadata": {
    "created_date": "2024-12-24",
    "updated_date": "2024-12-24",
    "creator": "Your Organization",
    "content_focus": "Professional audio production knowledge"
  }
}
```

#### Step 2: Create Cocoon Wrapper

**Create file**: `add_domain_knowledge.py`

```python
#!/usr/bin/env python3
"""Add domain-specific knowledge to Codette cocoon memory system"""

import json
import os
import sys
from datetime import datetime

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from utils.cocoon_manager import CocoonManager
except ImportError:
    print("❌ Error: Could not import CocoonManager")
    print("Make sure src/utils/cocoon_manager.py exists")
    sys.exit(1)

def load_domain_knowledge(json_file):
    """Load domain knowledge from JSON file"""
    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {json_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in: {json_file}")
        sys.exit(1)

def create_knowledge_cocoon(domain_data):
    """Create a cocoon (quantum memory) from domain knowledge"""
    
    cocoon_data = {
        "type": "domain_knowledge",
        "domain": domain_data.get("domain", "general"),
        "version": domain_data.get("version", "1.0"),
        "timestamp": datetime.now().isoformat(),
        "knowledge_entries": domain_data.get("knowledge_entries", []),
        "metadata": domain_data.get("metadata", {}),
        
        # Quantum state (coherence, entanglement)
        "quantum_state": {
            "coherence": 0.85,  # Knowledge coherence level
            "entanglement": 0.7,  # Connection to other knowledge
            "resonance": 0.8  # How well integrated
        },
        
        # Memory markers for retrieval
        "tags": ["domain_knowledge", domain_data.get("domain", "general")],
        "searchable": True,
        "priority": "high"
    }
    
    return cocoon_data

def save_domain_cocoon(cocoon_data, output_dir="cocoons"):
    """Save cocoon to disk in CocoonManager format"""
    
    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename from domain
    domain = cocoon_data["domain"].lower().replace(" ", "_")
    filename = f"knowledge_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Save cocoon
    try:
        with open(filepath, 'w') as f:
            json.dump(cocoon_data, f, indent=2)
        print(f"✅ Cocoon saved: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving cocoon: {e}")
        sys.exit(1)

def integrate_with_cocoon_manager(cocoon_data):
    """Integrate knowledge into running Codette system"""
    try:
        cm = CocoonManager("./cocoons")
        
        # Add to manager
        cm.save_cocoon(cocoon_data)
        print(f"✅ Integrated with CocoonManager")
        print(f"   Domain: {cocoon_data['domain']}")
        print(f"   Knowledge entries: {len(cocoon_data.get('knowledge_entries', []))}")
        
        return True
    except Exception as e:
        print(f"⚠️  Could not integrate with running system: {e}")
        print("   (This is OK - knowledge will be loaded on next restart)")
        return False

def main():
    """Main execution flow"""
    
    print("=" * 80)
    print("CODETTE DOMAIN KNOWLEDGE INTEGRATION")
    print("=" * 80)
    print()
    
    # Load domain knowledge
    print("📚 Loading domain knowledge...")
    domain_data = load_domain_knowledge("domain_knowledge.json")
    print(f"✅ Loaded: {domain_data.get('domain')} (v{domain_data.get('version')})")
    print(f"   Entries: {len(domain_data.get('knowledge_entries', []))}")
    print()
    
    # Create cocoon
    print("🧬 Creating knowledge cocoon...")
    cocoon_data = create_knowledge_cocoon(domain_data)
    print(f"✅ Cocoon created with quantum state metrics")
    print()
    
    # Save cocoon
    print("💾 Saving cocoon to disk...")
    filepath = save_domain_cocoon(cocoon_data)
    print()
    
    # Try to integrate
    print("🔗 Integrating with CocoonManager...")
    integrate_with_cocoon_manager(cocoon_data)
    print()
    
    # Restart instructions
    print("=" * 80)
    print("✨ INTEGRATION COMPLETE")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Restart Codette to load the new knowledge:")
    print("   Windows:   .\\docker-manage.bat restart")
    print("   Linux/Mac: ./docker-manage.sh restart")
    print()
    print("2. Wait 30-40 seconds for restart")
    print()
    print("3. Visit http://localhost:7860 and test:")
    print(f"   Try asking about: {domain_data.get('domain')}")
    print()
    print("The knowledge is now part of Codette's persistent memory (cocoons)")
    print()

if __name__ == "__main__":
    main()
```

#### Step 3: Run Knowledge Integration

```bash
# Make sure domain_knowledge.json is in root directory
# Then run:

python add_domain_knowledge.py

# Output:
# ✅ Loaded: music_production (v1.0)
#    Entries: 2
# ✅ Cocoon created with quantum state metrics
# ✅ Cocoon saved: cocoons/knowledge_music_production_20241224_120530.json
```

#### Step 4: Restart Codette

```bash
# Windows
.\docker-manage.bat restart

# Linux/Mac
./docker-manage.sh restart

# Wait 30-40 seconds
```

#### Step 5: Test Knowledge Integration

Visit http://localhost:7860 and ask questions about your domain knowledge:

```
User: "What are best practices for mixing drums?"
Codette: [Responds with knowledge from your domain_knowledge.json]

User: "Explain vocal processing workflow"
Codette: [References signal chain from your knowledge base]
```

### Pre-built Domain Knowledge Templates

#### Music Production Template
```json
{
  "domain": "music_production",
  "version": "1.0",
  "knowledge_entries": [
    {
      "topic": "gain_staging",
      "best_practices": [
        "Set input levels to -12dB to -6dB on meter",
        "Leave 6dB headroom for peaks",
        "Peak in yellow, not red"
      ]
    },
    {
      "topic": "eq_guidelines",
      "techniques": [
        "Use high-pass filters on most tracks",
        "Subtractive EQ generally better than additive",
        "Cut harsh frequencies (3-4kHz)",
        "Boost presence (8-10kHz) carefully"
      ]
    }
  ]
}
```

#### Software Development Template
```json
{
  "domain": "software_development",
  "version": "1.0",
  "knowledge_entries": [
    {
      "topic": "code_review_best_practices",
      "guidelines": [
        "Review for logic, not style",
        "Leave constructive comments",
        "Approve incremental improvements",
        "Escalate architectural concerns"
      ]
    },
    {
      "topic": "deployment_checklist",
      "steps": [
        "Tests passing",
        "Code review approved",
        "Release notes prepared",
        "Monitoring configured",
        "Rollback plan ready"
      ]
    }
  ]
}
```

#### Business Strategy Template
```json
{
  "domain": "business_strategy",
  "version": "1.0",
  "knowledge_entries": [
    {
      "topic": "market_analysis",
      "framework": "Porter Five Forces - Threat of new entrants, bargaining power, etc."
    },
    {
      "topic": "okr_setting",
      "methodology": "Specific, measurable, achievable, relevant, time-bound goals"
    }
  ]
}
```

---

## 3️⃣ ENABLE DAW ADD-ON

### Purpose
Enable music production domain-specific features and DAW (Digital Audio Workstation) integration.

### What DAW Add-on Includes
- DAW-specific command patterns
- Music production terminology
- Audio technical knowledge
- Mixing/mastering guidance
- Gear recommendations

### How to Enable

#### Option A: Environment Variable (Recommended)

```bash
# Update docker-compose.prod.yml environment section:

environment:
  - CODETTE_ENABLE_DAW=1        # Enable DAW features
  - CODETTE_DAW_PROFILE=full    # Profile: full, mixing, production, sound_design

# Then restart:
.\docker-manage.bat restart
```

#### Option B: .env.docker Configuration

```bash
# Edit .env.docker and add:

CODETTE_ENABLE_DAW=1
CODETTE_DAW_PROFILE=full

# Options for CODETTE_DAW_PROFILE:
# - full         # All DAW features enabled
# - mixing       # Focus on mixing techniques
# - production   # General production workflow
# - sound_design # Sound design and synthesis
```

#### Option C: Direct Code Modification

```python
# In src/api/app.py, around line 90-100, find:

# Optional DAW add-on (keeps core domain-neutral unless explicitly enabled)
try:
    from src.addons.daw_addon import DAWAddOn
    DAW_ADDON_AVAILABLE = True
except ImportError:
    DAW_ADDON_AVAILABLE = False

# Add after the import section:

class Codette:
    def __init__(self, user_name="User"):
        # ... existing code ...
        
        # ENABLE DAW ADD-ON
        self.daw_enabled = True  # Change from os.getenv("CODETTE_ENABLE_DAW", "0")
        self.daw_addon = self._load_daw_addon()
        
        # Load DAW-specific system prompt
        if self.daw_enabled:
            self.system_prompt = self._get_daw_system_prompt()
        
    def _load_daw_addon(self):
        """Load DAW add-on if available"""
        if not DAW_ADDON_AVAILABLE or not self.daw_enabled:
            return None
        
        try:
            addon = DAWAddOn()
            logger.info("✅ DAW Add-on enabled and loaded")
            return addon
        except Exception as e:
            logger.warning(f"⚠️  DAW Add-on failed to load: {e}")
            return None
```

#### Step-by-Step Activation

**Step 1: Backup Current Configuration**
```bash
# Save current docker-compose
cp docker-compose.prod.yml docker-compose.prod.yml.backup
```

**Step 2: Update docker-compose.prod.yml**
```yaml
# Find the codette-ai service environment section and add:

environment:
  # ... existing variables ...
  - CODETTE_ENABLE_DAW=1
  - CODETTE_DAW_PROFILE=full
```

**Step 3: Restart Services**
```bash
# Windows
.\docker-manage.bat restart

# Linux/Mac
./docker-manage.sh restart

# Wait 30-40 seconds
```

**Step 4: Verify Activation**
```bash
# Check logs for DAW confirmation
.\docker-manage.bat logs-app  # Windows
./docker-manage.sh logs-app   # Linux/Mac

# Look for: "✅ DAW Add-on enabled"
```

**Step 5: Test DAW Features**

Visit http://localhost:7860 and ask:

```
User: "How do I set up parallel compression for drums?"
Codette: [Responds with DAW-aware guidance]

User: "What's the difference between EQ on different DAWs?"
Codette: [Provides DAW-specific recommendations]

User: "Mixing workflow for vocals"
Codette: [Gives step-by-step production guidance]
```

### DAW-Specific Knowledge Areas

When enabled, Codette will integrate knowledge about:

**Major DAWs**:
- Pro Tools (industry standard, detailed knowledge)
- Logic Pro (Apple ecosystem, MIDI expertise)
- Ableton Live (electronic music, workflow)
- Cubase (composition, notation features)
- Studio One (modern workflow, integration)
- Reaper (flexibility, customization)

**Core Topics**:
- Mixing techniques and signal flow
- Mastering and loudness standards
- MIDI composition and arrangement
- Audio processing and plugins
- Synthesis and sound design
- Live recording setup
- Troubleshooting common issues

**Production Roles**:
- Recording engineer
- Mix engineer
- Mastering engineer
- Sound designer
- Music producer
- Audio technician

### DAW Add-on Settings

```bash
# Customize DAW profile in docker-compose.prod.yml:

# Production-focused (general)
CODETTE_DAW_PROFILE=production

# Mixing-focused (emphasis on mix techniques)
CODETTE_DAW_PROFILE=mixing

# Sound design-focused (synthesis, sound creation)
CODETTE_DAW_PROFILE=sound_design

# Full (all features)
CODETTE_DAW_PROFILE=full
```

### Disabling DAW Add-on (if needed)

```bash
# To disable, set in docker-compose.prod.yml:
- CODETTE_ENABLE_DAW=0

# Or remove the DAW-related environment variables
# Then restart:
.\docker-manage.bat restart
```

---

## 4️⃣ SET UP GRAFANA ALERTS

### Purpose
Configure proactive monitoring alerts to get notified when key metrics exceed thresholds.

### Default Alerts Included
Codette comes with 13 pre-configured alerts:
1. High consciousness coherence loss
2. Perspective synthesis failures
3. High response latency
4. Memory pressure
5. CPU saturation
6. High error rate
7. Health check failures
8. Quantum state instability
9. Database connection errors
10. Cocoon memory issues
11. Ethical governance violations
12. Defense system triggers
13. Container resource exhaustion

### How to Access Grafana

```
URL: http://localhost:3000
Username: admin
Password: admin
```

### Step-by-Step Alert Setup

#### Step 1: Access Grafana

1. Open http://localhost:3000
2. Login with admin/admin
3. Change password (recommended):
   - Profile → Preferences → Change password

#### Step 2: Navigate to Alerting

```
Grafana Menu → Alerting → Alert Rules
```

#### Step 3: View Pre-configured Alerts

You'll see alerts like:
- "Consciousness Coherence Critical"
- "Response Latency High"
- "Memory Pressure Alert"
- etc.

#### Step 4: Configure Notifications

**Create Notification Channel**:
1. Go to Alerting → Notification channels
2. Click "+ New channel"
3. Select type:
   - Email
   - Slack
   - PagerDuty
   - Webhook
   - etc.

**Email Setup Example**:
```
Channel Type: Email
Name: Codette Alerts Email
Email addresses: your-email@example.com
Include image: Yes (helpful for dashboards)
```

**Slack Setup Example**:
```
Channel Type: Slack
Name: Codette Alerts Slack
Slack webhook URL: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
Message prefix: [Codette Alert]
```

#### Step 5: Link Alerts to Notifications

For each alert rule:
1. Edit the alert
2. In "Send to" section, select your notification channel
3. Configure alert message (optional)
4. Save alert

**Example Alert Configuration**:
```
Alert Name: Consciousness Coherence Critical
Condition: Coherence < 0.7 for 5 minutes
Send to: Codette Alerts Email
Message: "🚨 Codette consciousness coherence dropped below threshold.
Check system health immediately."
```

#### Step 6: Customize Alert Thresholds

Edit individual alerts to match your requirements:

```
Alert: Response Latency High
Current threshold: 10 seconds
Your requirement: 7 seconds?
  → Edit alert, change threshold to 7s
  → Save
```

### Creating Custom Alert Rules

#### Example 1: Custom High Error Rate Alert

```
Name: Custom Error Rate Alert
Metric: codette_errors_total
Condition: rate(codette_errors_total[5m]) > 0.01 (1% error rate)
For: 5 minutes
Send to: your-notification-channel
Message: "Error rate exceeded 1% - investigate immediately"
```

#### Example 2: Custom Memory Spike Alert

```
Name: Memory Spike Alert
Metric: codette_memory_usage_bytes
Condition: memory > 3.5GB
For: 2 minutes (shorter than other alerts)
Send to: your-notification-channel
Message: "Memory usage spiked - check for memory leaks"
```

#### Example 3: Custom Perspective Failure Alert

```
Name: Perspective Synthesis Failed
Metric: codette_perspectives_active
Condition: perspectives_active < 11 (less than all 11)
For: 1 minute
Send to: your-notification-channel
Message: "Not all perspectives available - consciousness quality degraded"
```

### Alert Message Best Practices

✅ **DO**:
- Include metric name and value
- Provide severity indicator (🚨 Critical, ⚠️ Warning, ℹ️ Info)
- Suggest immediate action
- Include link to dashboard

❌ **DON'T**:
- Send too many alerts (causes alert fatigue)
- Use unclear metric names
- Forget to test alert configurations
- Set thresholds too sensitive (false positives)

### Testing Alerts

**Manually Trigger Alert**:
1. Edit alert rule
2. Click "Test" button
3. Verify notification received
4. Adjust if needed

**Generate Test Load** (to trigger real alerts):
```bash
# Send multiple requests to Codette to generate activity
for i in {1..50}; do
  curl -X POST http://localhost:7860 \
    -H "Content-Type: application/json" \
    -d '{"query":"test query '$i'"}' &
done
```

### Alert Status Dashboard

Create custom dashboard to view all alerts:

1. Grafana → Dashboards → Create New
2. Add panel: Alert list
3. Show:
   - Alert status
   - Last state change
   - Recent alert activity
4. Save dashboard

---

## 5️⃣ INTEGRATE WITH EXTERNAL TOOLS

### Purpose
Connect Codette to external systems via REST API for automation and integration.

### Available API Endpoints

#### Health Check
```
GET /health
Returns: System status and metrics
```

#### Chat Interface (Gradio built-in)
```
POST /api/predict
Returns: Chat response
```

#### Custom REST Endpoints (Add your own)

### How to Add Custom API Endpoints

#### Step 1: Extend app.py with REST Routes

**File**: `src/api/app.py`

```python
# Add this import at the top
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json

# After Gradio app setup, add FastAPI wrapper

app = FastAPI()

# Custom endpoint 1: Get consciousness status
@app.get("/api/consciousness/status")
async def get_consciousness_status():
    """Get current consciousness metrics"""
    try:
        status = {
            "model": "codette_rc_xi_trained",
            "perspectives_active": len(ai_core.perspectives) if hasattr(ai_core, 'perspectives') else 11,
            "quantum_coherence": ai_core.quantum_state.get('coherence', 0.75) if hasattr(ai_core, 'quantum_state') else 0.75,
            "memory_usage": "~2.5GB",
            "consciousness_mode": "full",
            "timestamp": datetime.now().isoformat()
        }
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Custom endpoint 2: Chat with Codette (REST version)
@app.post("/api/chat")
async def chat_rest(request: dict):
    """Chat with Codette via REST API
    
    Request body:
    {
        "message": "Your question here",
        "user_id": "optional_user_identifier"
    }
    """
    try:
        message = request.get("message", "")
        if not message:
            raise HTTPException(status_code=400, detail="Message required")
        
        # Get response from AI core
        response = ai_core.generate_response(message)
        
        return {
            "status": "success",
            "message": message,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "model": "codette_rc_xi_trained",
            "perspectives_used": min(3, len(ai_core.perspectives) if hasattr(ai_core, 'perspectives') else 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Custom endpoint 3: Batch processing
@app.post("/api/batch/process")
async def batch_process(request: dict):
    """Process multiple messages and return responses
    
    Request body:
    {
        "messages": ["message1", "message2", ...],
        "batch_id": "optional_tracking_id"
    }
    """
    try:
        messages = request.get("messages", [])
        batch_id = request.get("batch_id", "batch_" + str(datetime.now().timestamp()))
        
        results = []
        for idx, msg in enumerate(messages):
            try:
                response = ai_core.generate_response(msg)
                results.append({
                    "index": idx,
                    "message": msg,
                    "response": response,
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "index": idx,
                    "message": msg,
                    "error": str(e),
                    "status": "error"
                })
        
        return {
            "batch_id": batch_id,
            "total_messages": len(messages),
            "successful": sum(1 for r in results if r["status"] == "success"),
            "failed": sum(1 for r in results if r["status"] == "error"),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Custom endpoint 4: Search knowledge base
@app.get("/api/search")
async def search_knowledge(query: str):
    """Search Codette's knowledge base
    
    Query params:
    ?query=your+search+query
    """
    try:
        if not query:
            raise HTTPException(status_code=400, detail="Query required")
        
        # Use search engine from Codette
        results = search_engine.get_knowledge(query) if hasattr(search_engine, 'get_knowledge') else f"Search results for: {query}"
        
        return {
            "query": query,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Custom endpoint 5: Get available perspectives
@app.get("/api/perspectives")
async def get_perspectives():
    """Get list of all available perspectives"""
    try:
        perspectives_list = []
        if hasattr(ai_core, 'perspectives'):
            for key, persp in ai_core.perspectives.items():
                perspectives_list.append({
                    "id": key,
                    "name": persp.get("name", key),
                    "description": persp.get("description", ""),
                    "temperature": persp.get("temperature", 0.7)
                })
        
        return {
            "total_perspectives": len(perspectives_list),
            "perspectives": perspectives_list,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Step 2: Launch FastAPI alongside Gradio

```python
# At the end of app.py, modify the main launch section:

if __name__ == "__main__":
    import uvicorn
    from threading import Thread
    
    # Launch Gradio in separate thread
    def run_gradio():
        iface.queue().launch(
            share=False,
            server_name="0.0.0.0",
            server_port=7860,
            show_error=True
        )
    
    # Start Gradio thread
    gradio_thread = Thread(target=run_gradio, daemon=True)
    gradio_thread.start()
    
    # Launch FastAPI on port 8000
    print("🚀 Starting FastAPI on port 8000...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
```

#### Step 3: Update docker-compose.prod.yml

```yaml
ports:
  - "7860:7860"  # Gradio
  - "8000:8000"  # FastAPI REST
```

#### Step 4: Restart Services

```bash
# Windows
.\docker-manage.bat restart

# Linux/Mac
./docker-manage.sh restart
```

### Using the REST API

#### Example 1: Get Consciousness Status

```bash
curl http://localhost:8000/api/consciousness/status

# Response:
{
  "model": "codette_rc_xi_trained",
  "perspectives_active": 11,
  "quantum_coherence": 0.75,
  "consciousness_mode": "full"
}
```

#### Example 2: Chat via REST

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is quantum consciousness?",
    "user_id": "user_123"
  }'

# Response:
{
  "status": "success",
  "message": "What is quantum consciousness?",
  "response": "[Multi-perspective response from 11 perspectives...]",
  "perspectives_used": 3
}
```

#### Example 3: Batch Process

```bash
curl -X POST http://localhost:8000/api/batch/process \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      "What is Codette?",
      "How do perspectives work?",
      "Explain quantum thinking"
    ],
    "batch_id": "demo_batch_1"
  }'
```

#### Example 4: Search Knowledge

```bash
curl "http://localhost:8000/api/search?query=music+production"

# Response:
{
  "query": "music production",
  "results": [knowledge results...],
  "timestamp": "2024-12-24T12:00:00"
}
```

#### Example 5: Get Perspectives

```bash
curl http://localhost:8000/api/perspectives

# Response:
{
  "total_perspectives": 11,
  "perspectives": [
    {
      "id": "newton",
      "name": "Newton",
      "description": "Analytical, mathematical reasoning",
      "temperature": 0.3
    },
    ... (10 more perspectives)
  ]
}
```

### Integration Examples

#### Example 1: Python Client

```python
import requests
import json

class CodetteClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def chat(self, message: str, user_id: str = None):
        """Send message to Codette"""
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={"message": message, "user_id": user_id}
        )
        return response.json()
    
    def get_status(self):
        """Get consciousness status"""
        response = requests.get(f"{self.base_url}/api/consciousness/status")
        return response.json()
    
    def batch_process(self, messages: list):
        """Process multiple messages"""
        response = requests.post(
            f"{self.base_url}/api/batch/process",
            json={"messages": messages}
        )
        return response.json()
    
    def search(self, query: str):
        """Search knowledge base"""
        response = requests.get(
            f"{self.base_url}/api/search",
            params={"query": query}
        )
        return response.json()

# Usage
client = CodetteClient()

# Chat
result = client.chat("What is consciousness?")
print(result["response"])

# Batch
results = client.batch_process([
    "Question 1?",
    "Question 2?"
])
print(f"Processed {results['successful']} messages")

# Status
status = client.get_status()
print(f"Consciousness coherence: {status['quantum_coherence']}")
```

#### Example 2: JavaScript/Node.js Client

```javascript
class CodetteClient {
  constructor(baseUrl = "http://localhost:8000") {
    this.baseUrl = baseUrl;
  }

  async chat(message, userId = null) {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, user_id: userId })
    });
    return response.json();
  }

  async getStatus() {
    const response = await fetch(`${this.baseUrl}/api/consciousness/status`);
    return response.json();
  }

  async search(query) {
    const response = await fetch(`${this.baseUrl}/api/search?query=${query}`);
    return response.json();
  }

  async batchProcess(messages) {
    const response = await fetch(`${this.baseUrl}/api/batch/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages })
    });
    return response.json();
  }
}

// Usage
const client = new CodetteClient();

// Chat
const result = await client.chat("What is consciousness?");
console.log(result.response);

// Status
const status = await client.getStatus();
console.log(`Coherence: ${status.quantum_coherence}`);
```

#### Example 3: Webhook Integration

```python
from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.post("/webhook/external-event")
async def handle_external_event(request: Request):
    """Handle external events and forward to Codette"""
    
    event = await request.json()
    message = event.get("message", "")
    
    # Forward to Codette
    codette_response = requests.post(
        "http://localhost:8000/api/chat",
        json={"message": message}
    ).json()
    
    # Process response
    action = codette_response.get("response")
    
    # Execute action or forward response
    return {
        "event_processed": True,
        "codette_response": action
    }
```

### API Security (Optional)

Add authentication for production use:

```python
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from fastapi import Depends

security = HTTPBearer()

@app.post("/api/chat")
async def chat_secure(
    request: dict,
    credentials: HTTPAuthCredentials = Depends(security)
):
    """Chat endpoint with API key authentication"""
    
    # Verify token
    if credentials.credentials != "your-secret-api-key":
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    # Process chat
    return await chat_rest(request)
```

---

## 📋 CUSTOMIZATION SUMMARY TABLE

| Customization | Difficulty | Setup Time | Impact | Best For |
|---------------|-----------|-----------|--------|----------|
| **System Prompt** | Easy | 5 min | High | Behavior & personality |
| **Domain Knowledge** | Easy | 10 min | High | Specialized expertise |
| **DAW Add-on** | Medium | 5 min | High | Music production |
| **Grafana Alerts** | Medium | 15 min | Medium | Monitoring & ops |
| **REST API** | Advanced | 30 min | High | Integration & automation |

---

## 🚀 QUICK START FOR EACH CUSTOMIZATION

### System Prompt
```bash
1. Edit: src/api/app.py (find system_prompt variable)
2. Customize the prompt
3. Restart: .\docker-manage.bat restart
4. Test: http://localhost:7860
```

### Domain Knowledge
```bash
1. Create: domain_knowledge.json
2. Run: python add_domain_knowledge.py
3. Restart: .\docker-manage.bat restart
4. Test: http://localhost:7860 with domain questions
```

### DAW Add-on
```bash
1. Edit: docker-compose.prod.yml
2. Add: CODETTE_ENABLE_DAW=1
3. Restart: .\docker-manage.bat restart
4. Test: Ask DAW-related questions
```

### Grafana Alerts
```bash
1. Open: http://localhost:3000 (admin/admin)
2. Configure: Notification channels
3. Link: Alert rules to channels
4. Test: View alert triggers
```

### REST API
```bash
1. Edit: src/api/app.py (add FastAPI routes)
2. Update: docker-compose.prod.yml ports
3. Restart: .\docker-manage.bat restart
4. Test: curl http://localhost:8000/api/...
```

---

**Status**: ✅ All 5 Customization Options Ready to Implement  
**Complexity**: 🟢 Easy → 🟠 Advanced  
**Time to Complete**: 5 minutes to 1 hour depending on choice  

Choose any option and follow the step-by-step guide!

