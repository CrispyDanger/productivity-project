from typing import List
from django.conf import settings
from langchain.chat_models import init_chat_model
from core.langchain.graph import LLMFLow


class LLMService:
    def __init__(self):
        self.llm = init_chat_model(model_provider='openai',
                                   api_key='none',
                                   model='unsloth_Qwen3-VL-30B-A3B-Instruct-GGUF_Qwen3-VL-30B-A3B-Instruct-Q4_K_M.gguf',
                                   base_url=settings.LLM_BASE_URL)
        self.flow = LLMFLow(self.llm)

    def invoke(self, personality: str, action: str, previous_messages: List) -> dict:
        return self.flow.run(personality=personality, action=action,
                             previous_messages=previous_messages)
