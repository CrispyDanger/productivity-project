from django.conf import settings

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


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
