from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import process_new_post


@receiver(post_save, sender=Post)
def handle_new_post(sender, instance, created, **kwargs):
    if created:
        process_new_post.delay(instance.id)
