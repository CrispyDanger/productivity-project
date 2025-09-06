import random
from celery import shared_task
from core.services import LLMService
from .models import SocialProfile, Post
from .prompts import TOPIC_SEEDS, POST_PROMPT
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def make_post():
    profiles = SocialProfile.objects.filter(is_bot=True)
    author_profile = random.choice(profiles)
    topic = random.choice(TOPIC_SEEDS)
    text = LLMService().generate(prompt_template=POST_PROMPT,
                                 persona=author_profile.bot_personality,
                                 topic=topic)
    Post.objects.create(author=author_profile, text=text)
