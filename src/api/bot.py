
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from ai_core import AICore

class MyBot(ActivityHandler):
    def __init__(self, ai_core: AICore):
        super().__init__()
        self.ai_core = ai_core

    async def on_message_activity(self, turn_context: TurnContext):
        try:
            # Get the message text
            user_message = turn_context.activity.text

            # Generate response using AI Core
            response = self.ai_core.generate_text(user_message)
            
            # Analyze sentiment
            sentiment = self.ai_core.analyze_sentiment(user_message)
            sentiment_info = f"\n[Sentiment: {sentiment['label']} (confidence: {sentiment['score']:.2f})]"
            
            # Send the combined response
            await turn_context.send_activity(response + sentiment_info)
            
        except Exception as e:
            await turn_context.send_activity(f"I encountered an error: {str(e)}")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                welcome_message = (
                    "👋 Welcome to Codette! I'm an AI assistant that can help you with:\n\n"
                    "🤖 Natural language understanding\n"
                    "📊 Sentiment analysis\n"
                    "🎨 Creative text generation\n"
                    "🧠 Semantic analysis\n\n"
                    "Feel free to ask me anything!"
                )
                await turn_context.send_activity(welcome_message)

