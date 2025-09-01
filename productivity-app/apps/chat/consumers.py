import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from core.services import LLMService


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

        try:
            conversation_id = await self.create_message(
                conversation_id=conversation_id,
                message_type="user",
                content=user_message,
                user_id=self.user_id
            )

            response = await LLMService().async_generate(user_message)
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
