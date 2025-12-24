#!/usr/bin/env python3
"""
Domain Knowledge Integration Script for Codette
Loads domain knowledge from JSON into cocoon memory system
"""

import json
import os
from datetime import datetime

def integrate_domain_knowledge():
    """Load domain knowledge from JSON into cocoon memory"""
    
    try:
        # Load domain knowledge
        with open('domain_knowledge.json', 'r') as f:
            knowledge = json.load(f)
        
        # Create cocoons directory
        os.makedirs('cocoons', exist_ok=True)
        
        # Create cocoon entry
        cocoon_data = {
            "id": f"domain_{knowledge['domain']}_{knowledge['version']}",
            "type": "domain_knowledge",
            "domain": knowledge['domain'],
            "knowledge_entries": knowledge['knowledge_entries'],
            "metadata": knowledge['metadata'],
            "timestamp": datetime.now().isoformat(),
            "status": "integrated"
        }
        
        # Save to cocoons directory
        cocoon_file = f"cocoons/domain_{knowledge['domain']}.json"
        
        with open(cocoon_file, 'w') as f:
            json.dump(cocoon_data, f, indent=2)
        
        print(f"[SUCCESS] Domain knowledge integrated successfully!")
        print(f"   Location: {cocoon_file}")
        print(f"   Domain: {knowledge['domain']}")
        print(f"   Version: {knowledge['version']}")
        print(f"   Knowledge entries: {len(knowledge['knowledge_entries'])}")
        print(f"   Timestamp: {cocoon_data['timestamp']}")
        print(f"\n[INFO] Next step: Restart services with '.\\docker-manage.bat restart'")
        
        return True
        
    except FileNotFoundError:
        print("[ERROR] domain_knowledge.json not found in current directory")
        return False
    except json.JSONDecodeError:
        print("[ERROR] domain_knowledge.json is not valid JSON")
        return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    success = integrate_domain_knowledge()
    exit(0 if success else 1)
