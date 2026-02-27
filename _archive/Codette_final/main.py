import asyncio
import logging
from ai_core_ultimate import AICore  # Ensure it matches latest AI Core

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    try:
        logging.info("Initializing AI Core...")
        ai_core = AICore(config_path="config.json")
        query = "What is the latest in AI advancements?"
        logging.info(f"Processing query: {query}")
        
        response = await ai_core.generate_response(query, user_id=1)
        logging.info("Response received successfully.")
        print("AI Response:", response)
        
        await ai_core.http_session.close()
        logging.info("Closed AI Core session.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
