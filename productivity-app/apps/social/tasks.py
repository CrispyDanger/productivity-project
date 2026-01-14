import random
# import json
from urllib.parse import unquote
from celery import shared_task
from core.llm import agent, BotContext, store
from .models import SocialProfile, Post
from langchain.messages import AIMessage, ToolMessage
# from .prompts import TOPIC_PROMPT, POST_PROMPT, POST_EVALUATION, COMMENT_PROMPT
from core.langchain.llm import LLMService
from django.contrib.auth import get_user_model

User = get_user_model()
llm = LLMService()


@shared_task
def make_post():
    profiles = SocialProfile.objects.filter(is_bot=True)
    if profiles:
        author = random.choice(profiles)
        previous_posts = Post.objects.filter(author=author).order_by('-created_at')[:5]

        previous_posts_text = [post.text for post in previous_posts]

        text = llm.invoke(personality=author.bot_personality,
                          action='write_post', previous_messages=previous_posts_text)

        print(text['answer'])

        response_text = text['answer']

        Post.objects.create(author=author, text=unquote(response_text))


@shared_task
def make_comment():
    profiles = SocialProfile.objects.filter(is_bot=True)
    if profiles:
        author = random.choice(profiles)
    pass
    # TODO: Add make_comment logic for posts, add make_reply logic for replies

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
