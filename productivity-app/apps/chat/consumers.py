import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from .models import Conversation, Message


llm = OllamaLLM(model=settings.LLM_MODEL,
                base_url=settings.LLM_BASE_URL)

prompt = ChatPromptTemplate([
    (
        "system",
        """You're a skilled human writer who naturally connects with readers
        through authentic, conversational content. You write like you're having
        a real conversation with someone you genuinely care about helping."""
    ),
    ("user", "{input}"),
])


class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"].get("user_id", None)
        await self.accept()
        await self.send(text_data=json.dumps({
            "role": "system", "content": "Connected to AI"
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data["content"]
        conversation_id = data.get('conversation_id', None)

        formatted = prompt.format_messages(input=user_message)

        try:
            conversation_id = await self.create_message(
                conversation_id=conversation_id,
                message_type="user",
                content=user_message,
                user_id=self.user_id
            )

            response = llm.invoke(formatted)
            await self.send(text_data=json.dumps({
                "conversation_id": str(conversation_id),
                "role": "assistant",
                "content": response
            }))
            await self.create_message(
                conversation_id=conversation_id,
                message_type="assistant",
                content=response,
                user_id=self.user_id
            )
        except Exception as e:
            response = f"Could not connect to LLM-service: {e}"
            await self.send(text_data=json.dumps({
                "role": "system",
                "content": response
            }))

    @database_sync_to_async
    def create_message(self, conversation_id, message_type, content, user_id):
        if not conversation_id:
            conversation = Conversation.objects.create(account_id=user_id)
        else:
            conversation = Conversation.objects.filter(id=conversation_id).first()

        return Message.objects.create(
            conversation=conversation,
            message_type=message_type,
            content=content).conversation.id
