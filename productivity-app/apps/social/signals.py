from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import create_tags


@receiver(post_save, sender=Post)
def handle_new_post(sender, instance, created, **kwargs):
    if created:
        create_tags.delay(instance)
