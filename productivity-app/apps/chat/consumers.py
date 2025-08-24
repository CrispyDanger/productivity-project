import os
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


llm = OllamaLLM(model="mistral",
                base_url=os.environ.get('LLM_BASE_URL', default=''))

prompt = ChatPromptTemplate([
    ("system", "You are a helpful django coding assistant."),
    ("user", "{input}"),
])


class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            "role": "system", "content": "Connected to AI"
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data["content"]

        await self.send(text_data=json.dumps({
            "role": "user", "content": user_message
        }))

        # Build prompt for LLM via LangChain
        formatted = prompt.format_messages(input=user_message)
        response = llm.invoke(formatted)

        await self.send(text_data=json.dumps({
            "role": "assistant", "content": response
        }))
