from .llm import llm, prompt
from asgiref.sync import sync_to_async


class LLMService:
    def generate(self, user_message):
        formatted = prompt.format_messages(input=user_message)
        return llm.invoke(formatted)

    async def async_generate(self, user_message):
        return await sync_to_async(self.generate)(user_message)
