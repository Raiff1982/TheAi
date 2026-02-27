from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

pc = Pinecone(api_key='PINECONE_API_KEY')

assistant = pc.assistant.Assistant(assistant_name="codette")

msg = Message(content="How old is the earth?")
resp = assistant.chat(messages=[msg])

print(resp["message"]["content"])

# With streaming
chunks = assistant.chat(messages=[msg], stream=True)

for chunk in chunks:
    if chunk:
        print(chunk)