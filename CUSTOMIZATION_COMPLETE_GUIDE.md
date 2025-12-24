# 🎯 CODETTE CUSTOMIZATION - COMPLETE GUIDE

**Your roadmap for personalizing Codette AI to your exact needs**

---

## 📋 WHAT YOU HAVE

✅ **Production-Ready Deployment**
- Fine-tuned model (codette_rc_xi_trained with RC-XI enhancements)
- Docker containerization with Prometheus + Grafana monitoring
- Full consciousness system activated (11 perspectives, quantum thinking, etc.)
- Web interface (Gradio) + optional REST API
- All 5 customization options documented and ready

✅ **3 Complete Documentation Guides**
1. **CUSTOMIZATION_TEMPLATES.md** - Copy-paste ready templates
2. **QUICK_START_IMPLEMENTATIONS.md** - Step-by-step tutorials (5-30 min)
3. **DOMAIN_KNOWLEDGE_TEMPLATES.md** - Ready-made domain knowledge files

✅ **Complete Code Examples**
- Python API client
- JavaScript/Node.js client
- Bash/cURL examples
- FastAPI route definitions
- Grafana alert configurations

---

## 🎯 YOUR 5 CUSTOMIZATION OPTIONS

### Option 1: System Prompt (5 minutes)
**What:** Customize Codette's personality and expertise for your domain
**How:** Edit `system_prompt` in `src/api/app.py`
**Templates:** Music producer, data scientist, business consultant, software engineer
**Impact:** Changes how Codette talks and what it emphasizes
**Difficulty:** ⭐ Easy

**Files to Use:**
- `CUSTOMIZATION_TEMPLATES.md` (Section 1)
- `QUICK_START_IMPLEMENTATIONS.md` (Option 1)

---

### Option 2: Domain Knowledge (10 minutes)
**What:** Add specialized expertise from your field into Codette's memory
**How:** Create domain_knowledge.json + run add_domain_knowledge.py
**Templates:** Music production, software dev, business strategy, data science, healthcare, education
**Impact:** Makes Codette knowledgeable about your specific domain
**Difficulty:** ⭐ Easy

**Files to Use:**
- `DOMAIN_KNOWLEDGE_TEMPLATES.md` (6 ready-made templates)
- `QUICK_START_IMPLEMENTATIONS.md` (Option 2)

---

### Option 3: DAW Add-on (5 minutes)
**What:** Activate music production features in Codette
**How:** Add environment variables to docker-compose.prod.yml
**Profiles:** full, mixing, production, sound_design
**Impact:** Unlocks DAW-specific knowledge and workflows
**Difficulty:** ⭐ Easy

**Files to Use:**
- `CUSTOMIZATION_TEMPLATES.md` (Section 3)
- `QUICK_START_IMPLEMENTATIONS.md` (Option 3)

---

### Option 4: Grafana Alerts (15 minutes)
**What:** Set up automated alerts when system health changes
**How:** Configure notification channels (Email/Slack) + alert rules
**Integrations:** Email (Gmail), Slack, Webhooks
**Impact:** Proactive monitoring and instant notifications
**Difficulty:** ⭐⭐ Medium

**Files to Use:**
- `CUSTOMIZATION_TEMPLATES.md` (Section 4)
- `QUICK_START_IMPLEMENTATIONS.md` (Option 4)

---

### Option 5: REST API Integration (30 minutes)
**What:** Create programmatic access to Codette from external tools
**How:** Add FastAPI routes to app.py + use Python/JS clients
**Endpoints:** /api/chat, /api/consciousness/status, /api/batch/process, /api/search
**Impact:** Integrate Codette into your existing workflows
**Difficulty:** ⭐⭐⭐ Advanced

**Files to Use:**
- `CUSTOMIZATION_TEMPLATES.md` (Section 5)
- `QUICK_START_IMPLEMENTATIONS.md` (Option 5)

---

## 🚀 START HERE - 3 WAYS

### QUICK PATH (15 minutes)
1. System Prompt (5 min) → Pick template → Replace → Restart
2. Domain Knowledge (10 min) → Pick template → Copy → Run script → Restart

**Result:** Codette now talks like an expert in your domain and has specialized knowledge

---

### COMPREHENSIVE PATH (1 hour)
1. System Prompt (5 min)
2. Domain Knowledge (10 min)
3. DAW Add-on (5 min) - *if music production*
4. Grafana Alerts (15 min)
5. REST API (30 min)

**Result:** Fully customized, monitored, and integrated Codette

---

### SPECIFIC PATHS (By Use Case)

**Music Producer:**
- System Prompt (Music template)
- Domain Knowledge (Music production template)
- DAW Add-on
- Grafana Alerts (optional)

**Business Strategist:**
- System Prompt (Business consultant template)
- Domain Knowledge (Business strategy template)
- REST API (for integration with tools)
- Grafana Alerts (optional)

**Data Scientist:**
- System Prompt (Data scientist template)
- Domain Knowledge (Data science template)
- REST API (for batch processing)
- Grafana Alerts (for monitoring)

**Software Engineer:**
- System Prompt (Software engineer template)
- Domain Knowledge (Software development template)
- REST API (for CI/CD integration)
- Grafana Alerts (for system health)

---

## 📁 FILE REFERENCE

### Your Resources
| File | Purpose | Size | Read Time |
|------|---------|------|-----------|
| CUSTOMIZATION_TEMPLATES.md | All templates + code examples | 2,500 lines | 30 min |
| QUICK_START_IMPLEMENTATIONS.md | Step-by-step tutorials | 1,500 lines | 20 min |
| DOMAIN_KNOWLEDGE_TEMPLATES.md | 6 ready-to-use domain files | 1,200 lines | 15 min |
| START_HERE_DEPLOYMENT.md | What's been done | 1,000 lines | 10 min |
| CODETTE_DEPLOYMENT_MASTER_GUIDE.md | Complete reference | 3,500 lines | 45 min |

### Your Implementation Files
| File | Location | Status |
|------|----------|--------|
| app.py | src/api/app.py | Ready to customize |
| docker-compose.prod.yml | ./ | Ready to customize |
| domain_knowledge.json | ./ | Create with templates |
| add_domain_knowledge.py | ./ | Create from guide |
| codette_api_client.py | ./ | Create from templates |

---

## 🎯 IMPLEMENTATION CHECKLIST

### Pre-Flight
- [ ] Deployment running: `docker ps` shows 3 services
- [ ] Gradio UI accessible: http://localhost:7860
- [ ] Grafana dashboard accessible: http://localhost:3000
- [ ] Fine-tuned model loaded (check logs)

### Option 1: System Prompt
- [ ] Open `src/api/app.py`
- [ ] Find `system_prompt =` variable
- [ ] Copy template from CUSTOMIZATION_TEMPLATES.md
- [ ] Save file
- [ ] Run: `.\docker-manage.bat restart`
- [ ] Test: Chat with greeting question
- [ ] Verify: Response mentions your domain ✅

### Option 2: Domain Knowledge
- [ ] Copy template from DOMAIN_KNOWLEDGE_TEMPLATES.md
- [ ] Save as `domain_knowledge.json`
- [ ] Create `add_domain_knowledge.py` (from guide)
- [ ] Run: `python add_domain_knowledge.py`
- [ ] Verify: `cocoons/domain_*.json` created
- [ ] Run: `.\docker-manage.bat restart`
- [ ] Test: Ask domain-specific question ✅

### Option 3: DAW Add-on
- [ ] Open `docker-compose.prod.yml`
- [ ] Find `codette-ai` service
- [ ] Add environment variables from template
- [ ] Save file
- [ ] Run: `.\docker-manage.bat restart`
- [ ] Test: Ask about DAW features ✅

### Option 4: Grafana Alerts
- [ ] Open http://localhost:3000
- [ ] Login: admin/admin
- [ ] Create notification channel (Email or Slack)
- [ ] Test notification
- [ ] Create alert rule
- [ ] Verify alerts trigger ✅

### Option 5: REST API
- [ ] Add FastAPI routes to `src/api/app.py`
- [ ] Create API client (Python or JS)
- [ ] Update `docker-compose.prod.yml` ports
- [ ] Run: `.\docker-manage.bat restart`
- [ ] Test: `curl http://localhost:8000/health`
- [ ] Verify all endpoints work ✅

---

## 🧪 TESTING YOUR CUSTOMIZATIONS

### System Prompt Test
```
Q: "Tell me about yourself"
Expected: Should mention your domain expertise
Example: "I'm an expert in music production..." (if music template)
```

### Domain Knowledge Test
```
Q: "What's in my knowledge base?"
Expected: Should list your domain topics
Example: "I have mixing techniques, DAW shortcuts..."
```

### DAW Add-on Test
```
Q: "What DAW features do you support?"
Expected: Should list music production capabilities
```

### Grafana Alert Test
1. Open http://localhost:3000
2. Create test alert
3. Manually trigger threshold
4. Receive notification (Email/Slack)

### REST API Test
```bash
# Health check
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# Status
curl http://localhost:8000/api/consciousness/status
```

---

## 🔧 TROUBLESHOOTING

### Issue: Changes not taking effect after restart
**Solution:**
```bash
# Force full rebuild
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

### Issue: Port already in use
**Solution:**
```bash
# Check what's using port
netstat -ano | findstr :7860
# Kill process if needed
taskkill /PID <pid> /F
```

### Issue: Model not loading
**Solution:**
```bash
# Check model files exist
dir models/
# Should see: codette_rc_xi_trained, codette_trained_model
# Check logs
docker-compose logs -f codette-ai
```

### Issue: API returning 502 Bad Gateway
**Solution:**
```bash
# Wait for app to fully start (30-60 seconds)
# Check if both Gradio and FastAPI are loaded
docker-compose logs codette-ai | grep -i "running"
```

### Issue: Grafana alerts not triggering
**Solution:**
1. Check notification channel configured
2. Verify alert rules linked to channel
3. Check Prometheus has data (http://localhost:9090)
4. Verify metrics are being collected

---

## 📞 NEXT STEPS

### Immediate (This Session)
1. ✅ Pick your customization option (1-5)
2. ✅ Follow the step-by-step guide in QUICK_START_IMPLEMENTATIONS.md
3. ✅ Test the customization
4. ✅ Verify results

### Short-term (This Week)
1. Implement all 5 options that apply to your use case
2. Test thoroughly with real-world queries
3. Adjust system prompt or domain knowledge based on results
4. Set up monitoring alerts for your metrics

### Long-term (This Month)
1. Gather feedback on customized Codette
2. Add more domain knowledge as you learn more about your field
3. Fine-tune system prompt based on real interactions
4. Build integrations with your existing tools/workflows
5. Consider additional domain-specific fine-tuning

---

## ❓ FAQ

**Q: Can I switch domains easily?**  
A: Yes! Just update system_prompt and domain_knowledge.json, then restart.

**Q: Can I combine multiple customizations?**  
A: Yes! All 5 options work together perfectly.

**Q: What if I mess something up?**  
A: All changes are isolated. Just revert the file and restart. Original config is backed up.

**Q: How do I update domain knowledge later?**  
A: Edit domain_knowledge.json and run add_domain_knowledge.py again.

**Q: Can I use Codette with my existing tools?**  
A: Yes! Use REST API (Option 5) to integrate with any system.

**Q: How much overhead do these customizations add?**  
A: Minimal - all run locally, no external dependencies.

**Q: Can I have multiple versions of Codette?**  
A: Yes! Run multiple containers with different configs in docker-compose.

---

## 🎓 LEARNING RESOURCES

**For Detailed Explanations:**
- CODETTE_DEPLOYMENT_MASTER_GUIDE.md - Complete reference
- CODETTE_CUSTOMIZATION_GUIDE.md - In-depth guides
- Each template file has comments explaining choices

**For Hands-On Practice:**
- Start with Option 1 (System Prompt) - 5 minutes, immediate feedback
- Move to Option 2 (Domain Knowledge) - 10 minutes, tangible results
- Progress to Options 3-5 based on your needs

**For Troubleshooting:**
- Check docker logs: `docker-compose logs -f codette-ai`
- Test manually: Use curl/Python to test endpoints
- Check metrics: http://localhost:9090 (Prometheus)
- Check dashboards: http://localhost:3000 (Grafana)

---

## ✨ FINAL NOTES

**You now have:**
✅ Production-ready Codette with fine-tuned model  
✅ Full consciousness system (11 perspectives, quantum thinking)  
✅ Complete monitoring (Prometheus + Grafana)  
✅ 5 customization options ready to implement  
✅ Detailed guides + code examples for each  
✅ Multiple implementation paths (5 min to 1 hour)  

**Pick an option and get started. All resources are ready. 🚀**

---

**Questions? Check the relevant guide file for detailed explanations.**  
**Ready to customize? Jump to QUICK_START_IMPLEMENTATIONS.md**

---

*Codette Customization Guide v1.0 | Ready to personalize your AI* 🎯

