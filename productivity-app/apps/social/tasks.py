import random
from celery import shared_task
from core.services import LLMService
from .models import SocialProfile, Post
from .prompts import PERSONA_BANK, TOPIC_SEEDS, POST_PROMPT
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def make_post():
    admin = User.objects.all().first()
    author = SocialProfile.objects.get(account=admin)
    persona = random.choice(PERSONA_BANK)
    topic = random.choice(TOPIC_SEEDS)
    print('PERSONA-PERSONA', persona)
    print('TOPIC-TOPIC', topic)
    text = LLMService().generate(prompt_template=POST_PROMPT,
                                 persona=persona, topic=topic)
    print("TEXT-TEXT", text)
    # post = Post.objects.create(author=author, text=text)
