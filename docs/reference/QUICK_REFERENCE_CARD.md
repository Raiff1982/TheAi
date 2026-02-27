# ⚡ CODETTE CUSTOMIZATION QUICK REFERENCE

**Print this or keep it open while customizing** 

---

## 5 OPTIONS AT A GLANCE

| # | Option | Time | Difficulty | What It Does | Files |
|---|--------|------|-----------|---|---|
| 1️⃣ | **System Prompt** | 5 min | ⭐ Easy | Change personality/expertise | QUICK_START_1 |
| 2️⃣ | **Domain Knowledge** | 10 min | ⭐ Easy | Add specialized knowledge | QUICK_START_2 + TEMPLATES |
| 3️⃣ | **DAW Add-on** | 5 min | ⭐ Easy | Unlock music features | QUICK_START_3 |
| 4️⃣ | **Grafana Alerts** | 15 min | ⭐⭐ Medium | Setup monitoring notifications | QUICK_START_4 |
| 5️⃣ | **REST API** | 30 min | ⭐⭐⭐ Advanced | Integrate with external tools | QUICK_START_5 |

---

## QUICK COMMANDS

### Check Deployment Status
```bash
# All services running?
docker ps | findstr codette

# Can reach Codette?
curl http://localhost:7860

# Can reach API?
curl http://localhost:8000/health
```

### Restart Services
```bash
# Full restart
.\docker-manage.bat restart

# Or manual
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

### View Logs
```bash
# Codette logs
docker-compose logs -f codette-ai

# All services
docker-compose logs -f
```

---

## OPTION 1: SYSTEM PROMPT (5 min)

**File to edit:** `src/api/app.py`  
**Find:** `system_prompt =` (around line 120)  
**Replace with:** Template from CUSTOMIZATION_TEMPLATES.md (Section 1)  
**Restart:** `.\docker-manage.bat restart`  
**Test:** http://localhost:7860 → Chat greeting  

```
Template Options:
✓ Music producer
✓ Data scientist  
✓ Business consultant
✓ Software engineer
```

---

## OPTION 2: DOMAIN KNOWLEDGE (10 min)

**Step 1:** Get template from DOMAIN_KNOWLEDGE_TEMPLATES.md  
**Step 2:** Save as `domain_knowledge.json`  
**Step 3:** Create `add_domain_knowledge.py` (from QUICK_START_2)  
**Step 4:** Run: `python add_domain_knowledge.py`  
**Step 5:** Restart: `.\docker-manage.bat restart`  
**Test:** http://localhost:7860 → Ask domain question  

```
Ready-made templates:
✓ Music production
✓ Software development
✓ Business strategy
✓ Data science
✓ Healthcare
✓ Education
```

---

## OPTION 3: DAW ADD-ON (5 min)

**File to edit:** `docker-compose.prod.yml`  
**Find:** `codette-ai:` service  
**Add to environment:**
```yaml
- CODETTE_ENABLE_DAW=1
- CODETTE_DAW_PROFILE=full
```

**Restart:** `.\docker-manage.bat restart`  
**Test:** http://localhost:7860 → Ask "What DAW features do you support?"  

```
DAW Profiles:
- full (all features)
- mixing (mixing focus)
- production (general)
- sound_design (synthesis)
```

---

## OPTION 4: GRAFANA ALERTS (15 min)

**Open:** http://localhost:3000  
**Login:** admin/admin  
**Go to:** Settings ⚙️ → Alerting → Notification channels  
**Create channel:** Email or Slack  
**Test:** Send test notification  
**Create rule:** Alert rules → New rule → Link to channel  
**Trigger:** Verify alert fires when threshold exceeded  

```
Email (Gmail):
- Host: smtp.gmail.com:587
- Username: your-email@gmail.com
- Password: [app-specific password]

Slack:
- Webhook URL: [from Slack API]
- Channel: #codette-alerts
```

---

## OPTION 5: REST API (30 min)

**Step 1:** Add routes to `src/api/app.py` (from TEMPLATES Section 5)  
**Step 2:** Update `docker-compose.prod.yml` - add port 8000  
**Step 3:** Create client (Python or JavaScript)  
**Step 4:** Restart: `.\docker-manage.bat restart`  
**Test:** 
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/consciousness/status
```

```
Endpoints available:
POST /api/chat
GET /api/consciousness/status
POST /api/batch/process
GET /api/search?query=...
GET /api/perspectives
```

---

## 🎯 BY YOUR USE CASE

### 🎵 MUSIC PRODUCER
1. System Prompt: Music template (5 min)
2. Domain Knowledge: Music template (10 min)
3. DAW Add-on (5 min)
→ **Total: 20 minutes**

### 💼 BUSINESS CONSULTANT
1. System Prompt: Business template (5 min)
2. Domain Knowledge: Business template (10 min)
3. REST API (30 min) - for integrations
→ **Total: 45 minutes**

### 📊 DATA SCIENTIST
1. System Prompt: Data scientist template (5 min)
2. Domain Knowledge: Data science template (10 min)
3. REST API (30 min) - for batch processing
4. Grafana Alerts (15 min) - for monitoring
→ **Total: 60 minutes**

### 💻 SOFTWARE ENGINEER
1. System Prompt: Software template (5 min)
2. Domain Knowledge: Software template (10 min)
3. REST API (30 min) - for CI/CD
4. Grafana Alerts (15 min) - for health checks
→ **Total: 60 minutes**

---

## 📁 FILE LOCATIONS

```
i:\TheAI\
├── src\api\app.py ...................... Edit for system prompt + API routes
├── docker-compose.prod.yml ............. Edit for DAW + ports
├── domain_knowledge.json ............... Create from templates
├── add_domain_knowledge.py ............. Create from guide
├── codette_api_client.py ............... Create from templates
│
└── CUSTOMIZATION_TEMPLATES.md .......... 🔑 All code examples
└── QUICK_START_IMPLEMENTATIONS.md ...... 🔑 Step-by-step tutorials
└── DOMAIN_KNOWLEDGE_TEMPLATES.md ....... 🔑 6 ready-made domains
└── CUSTOMIZATION_COMPLETE_GUIDE.md .... 🔑 Overview + checklists
```

---

## ✅ IMPLEMENTATION CHECKLIST

### Before You Start
- [ ] Docker running: `docker ps`
- [ ] Codette UI accessible: http://localhost:7860
- [ ] Grafana accessible: http://localhost:3000

### After Each Option
- [ ] File edited/created
- [ ] Services restarted (if needed)
- [ ] Test query sent
- [ ] Expected result received

### Final Verification
- [ ] All active options working
- [ ] No error logs: `docker-compose logs`
- [ ] Metrics in Prometheus: http://localhost:9090
- [ ] Dashboards updated in Grafana: http://localhost:3000

---

## 🚨 TROUBLESHOOTING

### Services won't start
```bash
# Check logs
docker-compose logs

# Force restart
docker-compose down
docker-compose up -d
```

### Changes not showing
```bash
# Full rebuild
docker-compose down
docker-compose up --build -d
```

### Port conflicts
```bash
# Find what's using port
netstat -ano | findstr :7860

# Kill if needed
taskkill /PID <number> /F
```

### API not responding
```bash
# Wait 30-60 seconds for startup
docker-compose logs codette-ai | grep -i "running"
```

### Domain knowledge not loading
```bash
# Check file created
dir cocoons\
ls -la cocoons/

# Check script output
python add_domain_knowledge.py
```

---

## 🎯 YOUR NEXT STEP

1. **Choose 1-5 options** from the table above
2. **Open QUICK_START_IMPLEMENTATIONS.md** for your chosen option(s)
3. **Follow the step-by-step** instructions
4. **Test your customization** with the provided test queries
5. **Verify in logs** that everything loaded correctly

---

## 💡 PRO TIPS

**Tip 1:** Start with Option 1 (System Prompt)  
→ Fastest to implement, immediate feedback

**Tip 2:** Combine 1 + 2 (Prompt + Domain)  
→ 15 minutes, huge impact on expertise

**Tip 3:** Test each option before moving to next  
→ Easier to debug issues

**Tip 4:** Keep browser tabs open to test  
- http://localhost:7860 (Gradio UI)
- http://localhost:3000 (Grafana)
- http://localhost:9090 (Prometheus metrics)
- http://localhost:8000/health (API health)

**Tip 5:** Use copy-paste templates  
→ No need to rewrite, just customize

---

## 📞 HELP RESOURCES

| Need | File |
|------|------|
| Copy-paste templates | CUSTOMIZATION_TEMPLATES.md |
| Step-by-step instructions | QUICK_START_IMPLEMENTATIONS.md |
| Ready-made domain knowledge | DOMAIN_KNOWLEDGE_TEMPLATES.md |
| Complete overview | CUSTOMIZATION_COMPLETE_GUIDE.md |
| Detailed reference | CODETTE_DEPLOYMENT_MASTER_GUIDE.md |

---

## ⏱️ TIME INVESTMENT

```
Option 1 (System Prompt) ........ 5 min  ⭐ START HERE
Option 2 (Domain Knowledge) .... 10 min ⭐ QUICK IMPACT
Option 3 (DAW Add-on) .......... 5 min  🎵 IF MUSIC
Option 4 (Alerts) .............. 15 min 📊 MONITORING
Option 5 (REST API) ............ 30 min 🔌 INTEGRATION

Total for all 5 ................ ~65 min
Essential path (1+2) ........... 15 min
Your choice combo .............. YOUR TIME
```

---

## 🚀 YOU'RE READY!

All templates are prepared.  
All guides are written.  
All code examples are ready.  

**Pick your option and start customizing.** 🎯

---

*Keep this page open while implementing*

