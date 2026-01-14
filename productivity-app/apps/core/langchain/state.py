from typing import List, Literal
from pydantic import BaseModel, Field


class LLMState(BaseModel):
    action: Literal['write_post', 'write_comment']
    personality: str
    answer: str = ''
    post: str = ''
    comment_context: str = ''
    previous_messages: List[str] = []


class MessageStructure(BaseModel):
    body: str = Field(description='Text of the post')
