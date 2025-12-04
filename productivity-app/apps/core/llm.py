from dataclasses import dataclass
from pydantic import BaseModel, Field
from django.conf import settings
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool, ToolRuntime
from langchain_ollama import ChatOllama
from langgraph.store.memory import InMemoryStore


@dataclass
class BotContext:
    username: str
    personality_id: str


class OutputFormat(BaseModel):
    """Post content"""
    post_content: str = Field(..., description="Post content")


@tool
def get_personality_context(runtime: ToolRuntime[BotContext]) -> str:
    """Retrieve personality and recent posts for context."""
    store = runtime.store
    username = runtime.context.username.strip()
    personality = runtime.context.personality_id.strip()

    # personality = store.get(("personalities",), username)

    recent_posts = store.search(
        ("posts", username),
        query="recent posts",
        limit=5
    )

    print("RECENT_POSTS:\n", recent_posts)

    if len(recent_posts) > 0:
        posts_summary = "\n".join([
            f"- {item.value.get('content', '')}"
            for item in recent_posts
        ])
    else:
        posts_summary = "No recent posts"

    return f""" Personality Profile: {personality}

                Recent Posts:
                {posts_summary}
                """


store = InMemoryStore()

ollama = ChatOllama(model=settings.LLM_MODEL,
                    base_url=settings.LLM_BASE_URL)

agent = create_agent(ollama,
                     tools=[get_personality_context],
                     store=store,
                     context_schema=BotContext,
                     response_format=ToolStrategy(OutputFormat))
