import random
# import json
from urllib.parse import unquote
from celery import shared_task
from core.llm import agent, BotContext, store
from .models import SocialProfile, Post
from langchain.messages import AIMessage, ToolMessage
# from .prompts import TOPIC_PROMPT, POST_PROMPT, POST_EVALUATION, COMMENT_PROMPT
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def make_post():
    profiles = SocialProfile.objects.filter(is_bot=True)
    if profiles:
        author = random.choice(profiles)
        text = agent.invoke({
            "messages": [{
                "role": "user",
                "content": """Write a text for a post.
                            1. Retrieve my personality and recent posts using the context tool.
                            2. Based on the retrieved themes and style, write a NEW post (under 500 chars).
                            3. The final output must be the raw post text only, with no introduction."""
            }]
        }, store=store,
            context=BotContext(username=author.display_name,
                               personality_id=author.bot_personality))

        print(text)

        response_text = text['messages'][-1]

        # TODO: Fix this nonsense
        if isinstance(response_text, AIMessage):
            response_text = response_text.content
        elif isinstance(response_text, ToolMessage):
            response_text = text['structured_response'].post_content
        else:
            raise Exception

        print(response_text)

        post = Post.objects.create(author=author, text=unquote(response_text))
        store.put(("posts", author.display_name), f"post_{post.id}", post.text)

# @shared_task
# def process_new_post(post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         return

#     author_id = post.author.id

#     candidates = SocialProfile.objects.exclude(id=author_id)

#     for persona in candidates:
#         score_post_for_persona.delay(post.id, persona.id)


# @shared_task
# def score_post_for_persona(post_id, persona_id):
#     post = Post.objects.get(id=post_id)
#     persona = SocialProfile.objects.get(id=persona_id)

#     result = LLMService().generate(prompt_template=POST_EVALUATION,
#                                    persona=persona.bot_personality,
#                                    post=post.text)

#     result = json.loads(result)

#     score_obj, created = AIPostScore.objects.update_or_create(
#         post=post,
#         persona=persona,
#         defaults={
#             "score": result["score"],
#             "reason": result["reason"],
#         }
#     )

#     if result["score"] >= 70:
#         generate_comment.delay(post.id, persona.id)


# @shared_task
# def generate_comment(post_id, persona_id):

#     post = Post.objects.get(id=post_id)
#     persona = SocialProfile.objects.get(id=persona_id)

#     comment_text = LLMService().generate(prompt_template=COMMENT_PROMPT,
#                                          persona=persona.bot_personality,
#                                          post=post.text)

#     Comment.objects.create(
#         post=post,
#         created_by=persona,
#         text=unquote(comment_text),
#         is_ai=True
#     )
