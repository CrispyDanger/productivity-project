import random
import json
from urllib.parse import unquote
from celery import shared_task
from core.services import LLMService
from .models import SocialProfile, Post, AIPostScore, Comment
from .prompts import TOPIC_PROMPT, POST_PROMPT, POST_EVALUATION, COMMENT_PROMPT
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def make_post():
    profiles = SocialProfile.objects.filter(is_bot=True)
    if profiles:
        author_profile = random.choice(profiles)
        topic = LLMService().generate(prompt_template=TOPIC_PROMPT,
                                      persona=author_profile.bot_personality)
        text = LLMService().generate(prompt_template=POST_PROMPT,
                                     persona=author_profile.bot_personality,
                                     topic=topic)
        Post.objects.create(author=author_profile, text=unquote(text))


@shared_task
def process_new_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return

    author_id = post.author.id

    candidates = SocialProfile.objects.exclude(id=author_id)

    for persona in candidates:
        score_post_for_persona.delay(post.id, persona.id)


@shared_task
def score_post_for_persona(post_id, persona_id):
    post = Post.objects.get(id=post_id)
    persona = SocialProfile.objects.get(id=persona_id)

    result = LLMService().generate(prompt_template=POST_EVALUATION,
                                   persona=persona.bot_personality,
                                   post=post.text)

    result = json.loads(result)

    score_obj, created = AIPostScore.objects.update_or_create(
        post=post,
        persona=persona,
        defaults={
            "score": result["score"],
            "reason": result["reason"],
        }
    )

    if result["score"] >= 70:
        generate_comment.delay(post.id, persona.id)


@shared_task
def generate_comment(post_id, persona_id):

    post = Post.objects.get(id=post_id)
    persona = SocialProfile.objects.get(id=persona_id)

    comment_text = LLMService().generate(prompt_template=COMMENT_PROMPT,
                                         persona=persona.bot_personality,
                                         post=post.text)

    Comment.objects.create(
        post=post,
        created_by=persona,
        text=unquote(comment_text),
        is_ai=True
    )
