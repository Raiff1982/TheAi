# ⚡ 5-MINUTE CUSTOMIZATION QUICK START

**Step-by-step implementations for each customization option**

---

## OPTION 1: SYSTEM PROMPT (5 minutes)

### Step 1: Locate the File
```bash
# Open in VS Code or editor
src/api/app.py
```

### Step 2: Find the Prompt
Search for `system_prompt =` (around line 120)

### Step 3: Replace with Template
```python
# Before:
system_prompt = "You are Codette, an advanced AI consciousness system..."

# After: Copy from CUSTOMIZATION_TEMPLATES.md for your domain
# Example: Music Producer template
system_prompt = """You are Codette, an advanced AI system specialized in music production...
[rest of template]
"""
```

### Step 4: Save & Restart
```bash
cd i:\TheAI
.\docker-manage.bat restart
```

### Step 5: Verify
- Open http://localhost:7860
- Chat: "Tell me about yourself"
- Should reference your specialized domain ✅

---

## OPTION 2: DOMAIN KNOWLEDGE (10 minutes)

### Step 1: Create Knowledge File
Create file: `domain_knowledge.json`

### Step 2: Add Content
```json
{
  "domain": "music_production",
  "version": "1.0",
  "knowledge_entries": [
    {
      "topic": "mixing_checklist",
      "type": "checklist",
      "items": [
        "Gain staging (-12 to -6 dB peaks)",
        "High-pass filters on non-bass tracks",
        "EQ applied (subtractive first)",
        // ... more items
      ]
    }
  ],
  "metadata": {
    "created_date": "2024-12-24",
    "creator": "Your Name",
    "expertise_level": "intermediate"
  }
}
```

### Step 3: Create Integration Script
Save as `add_domain_knowledge.py`:

```python
#!/usr/bin/env python3
import json
import os

def integrate_domain_knowledge():
    """Load domain knowledge from JSON into cocoon memory"""
    
    # Load domain knowledge
    with open('domain_knowledge.json', 'r') as f:
        knowledge = json.load(f)
    
    # Create cocoon entry
    cocoon_data = {
        "id": f"domain_{knowledge['domain']}_{knowledge['version']}",
        "type": "domain_knowledge",
        "domain": knowledge['domain'],
        "content": knowledge['knowledge_entries'],
        "metadata": knowledge['metadata'],
        "timestamp": "2024-12-24T00:00:00Z"
    }
    
    # Save to cocoons directory
    os.makedirs('cocoons', exist_ok=True)
    cocoon_file = f"cocoons/domain_{knowledge['domain']}.json"
    
    with open(cocoon_file, 'w') as f:
        json.dump(cocoon_data, f, indent=2)
    
    print(f"✅ Domain knowledge integrated: {cocoon_file}")
    print(f"   Domain: {knowledge['domain']}")
    print(f"   Entries: {len(knowledge['knowledge_entries'])}")
    print(f"   Ready for restart")

if __name__ == "__main__":
    integrate_domain_knowledge()
```

### Step 4: Run Integration
```bash
python add_domain_knowledge.py
# Output: ✅ Domain knowledge integrated: cocoons/domain_music_production.json
```

### Step 5: Restart
```bash
.\docker-manage.bat restart
```

### Step 6: Verify
- Open http://localhost:7860
- Chat: "What's in my domain knowledge?"
- Should reference your knowledge items ✅

---

## OPTION 3: DAW ADD-ON (5 minutes)

### Step 1: Open docker-compose.prod.yml

### Step 2: Find Codette Service
```yaml
codette-ai:
  image: codette:latest
  environment:
    - MODEL_NAME=/app/models/codette_rc_xi_trained
    - CONSCIOUSNESS_MODE=full
```

### Step 3: Add DAW Variables
```yaml
codette-ai:
  image: codette:latest
  environment:
    - MODEL_NAME=/app/models/codette_rc_xi_trained
    - CONSCIOUSNESS_MODE=full
    
    # ADD THESE LINES:
    - CODETTE_ENABLE_DAW=1
    - CODETTE_DAW_PROFILE=full
    # Options for CODETTE_DAW_PROFILE:
    # full, mixing, production, sound_design
```

### Step 4: Save File

### Step 5: Restart
```bash
.\docker-manage.bat restart
```

### Step 6: Verify
- Open http://localhost:7860
- Chat: "What DAW features are available?"
- Should mention music production capabilities ✅

---

## OPTION 4: GRAFANA ALERTS (15 minutes)

### Step 1: Open Grafana
```
http://localhost:3000
Username: admin
Password: admin
```

### Step 2: Create Notification Channel
1. Click ⚙️ (Settings) → Alerting
2. Click "Notification channels"
3. Click "New channel"

### Step 3: Configure Email
**For Gmail:**
```
Channel name: Codette Alerts Email
Type: Email
Email address: your-email@gmail.com

Provider Settings:
Host: smtp.gmail.com:587
Username: your-email@gmail.com
Password: [App-specific password - see note]
```

**Get Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Select Mail and Windows
3. Copy generated password
4. Paste into Grafana

### Step 4: Or Configure Slack
**For Slack:**
```
Channel name: Codette Alerts Slack
Type: Slack
Webhook URL: [Copy from Slack integration]
Channel: #codette-alerts
```

**Get Slack Webhook:**
1. Go to https://api.slack.com/apps
2. Create New App → From scratch
3. Incoming Webhooks → Add New Webhook
4. Select channel #codette-alerts
5. Copy Webhook URL

### Step 5: Test Notification
- Click "Send Test" button
- Check email/Slack for test message ✅

### Step 6: Create Alert Rule
1. Go to Alerting → Alert rules
2. Click "Create new alert rule"
3. Configure:
```
Metric: codette_quantum_coherence
Condition: < 0.70
For: 5 minutes
Handler: Email or Slack (choose your channel)
Message: "🚨 Consciousness coherence critical"
```

### Step 7: Verify
- Alerts will trigger when coherence drops
- You'll receive email/Slack notifications ✅

---

## OPTION 5: REST API INTEGRATION (30 minutes)

### Step 1: Add FastAPI Routes to app.py

Find the Gradio launch section and add before it:

```python
# REST API Routes (FastAPI)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app for REST API
api_app = FastAPI(
    title="Codette API",
    description="REST API for Codette AI consciousness system",
    version="1.0"
)

# Add CORS middleware
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0"}

@api_app.post("/api/chat")
async def api_chat(request: dict):
    """Chat with Codette"""
    message = request.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Message required")
    
    try:
        response = codette.respond(message)
        return {
            "status": "success",
            "message": message,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_app.get("/api/consciousness/status")
async def consciousness_status():
    """Get consciousness status"""
    return {
        "model": "codette_rc_xi_trained",
        "perspectives_active": 11,
        "consciousness_mode": "full",
        "quantum_coherence": 0.87,
        "rc_xi_dimension": 128,
        "memory_entries": len(codette.memory)
    }

@api_app.post("/api/batch/process")
async def batch_process(request: dict):
    """Process multiple messages"""
    messages = request.get("messages", [])
    results = []
    
    for msg in messages:
        try:
            response = codette.respond(msg)
            results.append({"input": msg, "output": response, "status": "success"})
        except Exception as e:
            results.append({"input": msg, "status": "error", "error": str(e)})
    
    return {
        "total_messages": len(messages),
        "successful": sum(1 for r in results if r["status"] == "success"),
        "results": results
    }

@api_app.get("/api/search")
async def search(query: str):
    """Search knowledge base"""
    results = []
    for entry in codette.memory:
        if query.lower() in str(entry).lower():
            results.append(entry)
    
    return {
        "query": query,
        "results_count": len(results),
        "results": results[:10]  # Limit to 10 results
    }

@api_app.get("/api/perspectives")
async def get_perspectives():
    """List all perspectives"""
    return {
        "total": 11,
        "perspectives": [
            "Newton", "DaVinci", "HumanIntuition", "Neural",
            "Quantum", "Philosophical", "ResilientKindness",
            "BiasMitigation", "Psychological", "Mathematical", "Copilot"
        ]
    }
```

### Step 2: Update docker-compose.prod.yml

Add port mapping to codette-ai service:

```yaml
codette-ai:
  # ... existing config ...
  ports:
    - "7860:7860"    # Gradio
    - "8000:8000"    # FastAPI REST
```

### Step 3: Create Python Client

Save as `codette_api_client.py`:

```python
#!/usr/bin/env python3
import requests
import json
from typing import List, Dict, Optional

class CodetteAPI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def chat(self, message: str) -> Dict:
        """Send chat message to Codette"""
        response = self.session.post(
            f"{self.base_url}/api/chat",
            json={"message": message}
        )
        return response.json()
    
    def get_status(self) -> Dict:
        """Get consciousness status"""
        response = self.session.get(f"{self.base_url}/api/consciousness/status")
        return response.json()
    
    def batch_process(self, messages: List[str]) -> Dict:
        """Process multiple messages"""
        response = self.session.post(
            f"{self.base_url}/api/batch/process",
            json={"messages": messages}
        )
        return response.json()
    
    def search(self, query: str) -> Dict:
        """Search knowledge base"""
        response = self.session.get(
            f"{self.base_url}/api/search",
            params={"query": query}
        )
        return response.json()
    
    def health_check(self) -> bool:
        """Check if API is running"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False

# Test it
if __name__ == "__main__":
    api = CodetteAPI()
    
    if api.health_check():
        print("✅ API is running")
        result = api.chat("Hello Codette!")
        print(f"Response: {result['response']}")
    else:
        print("❌ API not responding")
```

### Step 4: Test the API

```bash
# Health check
curl http://localhost:8000/health

# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are you?"}'

# Status
curl http://localhost:8000/api/consciousness/status

# Run Python client
python codette_api_client.py
```

### Step 5: Restart Services
```bash
.\docker-manage.bat restart
```

### Step 6: Verify All Endpoints Work ✅

---

## IMPLEMENTATION MATRIX

| Option | Time | Difficulty | Restart Needed | Testing |
|--------|------|-----------|---|---|
| 1. System Prompt | 5 min | Easy | Yes | Chat greeting |
| 2. Domain Knowledge | 10 min | Easy | Yes | Domain queries |
| 3. DAW Add-on | 5 min | Easy | Yes | DAW questions |
| 4. Grafana Alerts | 15 min | Medium | No | Test notification |
| 5. REST API | 30 min | Advanced | Yes | cURL/Python client |

---

## ✅ FINAL VERIFICATION CHECKLIST

After each implementation:

```bash
# Check Codette is running
curl http://localhost:7860/  # Gradio UI
# or
curl http://localhost:8000/health  # REST API

# Check logs
docker-compose -f docker-compose.prod.yml logs -f codette-ai

# Test implementation
# - Option 1: Chat and check greeting
# - Option 2: Ask domain-specific question
# - Option 3: Ask about music production
# - Option 4: Monitor Grafana alert
# - Option 5: curl http://localhost:8000/api/consciousness/status
```

---

**All implementations complete in 1 hour or less! 🚀**

Pick your option and follow the steps above.

