from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from ai_core_system import AICore
import asyncio

class CodetteBaseAction(Action):
    """Base class for Codette-powered actions"""
    
    def __init__(self):
        self.ai_core = None
        
    async def initialize_core(self):
        if not self.ai_core:
            self.ai_core = AICore()
            await self.ai_core.initialize_async()
        return self.ai_core

class ActionProcessWithCodette(CodetteBaseAction):
    def name(self) -> Text:
        return "action_process_with_codette"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest user message
        latest_message = tracker.latest_message.get('text', '')
        
        # Initialize and use Codette's AI Core
        ai_core = await self.initialize_core()
        
        # Process with Codette's full capabilities
        response = await ai_core.generate_response(latest_message, 
                                                 tracker.sender_id)
        
        # Send the response
        dispatcher.utter_message(text=response.get('response', ''))
        
        # If we have additional insights, send those too
        if response.get('insights'):
            dispatcher.utter_message(text="Additional insights: " + 
                                        str(response['insights']))
            
        return []

class ActionDescribeCapabilities(Action):
    def name(self) -> Text:
        return "action_describe_capabilities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Initialize AI Core
        ai_core = AICore()
        
        capabilities = [
            "- Natural language understanding and processing",
            "- Adaptive learning from interactions",
            "- Sentiment analysis and emotional understanding",
            "- Real-time data integration",
            "- Ethical AI governance",
            "- Cultural sensitivity analysis",
            "- Self-improving capabilities",
            "- Quantum-inspired optimizations"
        ]
        
        # Format capabilities as a nice message
        message = "I have several capabilities:\n" + "\n".join(capabilities)
        
        dispatcher.utter_message(text=message)
        return []