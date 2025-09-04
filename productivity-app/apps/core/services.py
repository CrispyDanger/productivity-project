from .llm import llm, prompt
from asgiref.sync import sync_to_async


class LLMService:
    def generate(self, prompt_template=prompt, **kwargs):
        formatted = prompt_template.format_messages(**kwargs)
        return llm.invoke(formatted)

    async def async_generate(self, **kwargs):
        return await sync_to_async(self.generate)(**kwargs)
