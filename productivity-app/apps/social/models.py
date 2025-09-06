from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Topic(models.Model):
    name = models.CharField(max_length=120,
                            blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class SocialProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=20, null=False, blank=False,
                                    default='Change Me')
    # TODO: Add profile image support
    description = models.CharField(max_length=120, blank=True)
    is_bot = models.BooleanField(default=True)
    bot_personality = models.CharField(max_length=150, blank=True)
    interests = models.ManyToManyField(Topic,
                                       related_name='interest_topics',
                                       blank=True)
    dislikes = models.ManyToManyField(Topic,
                                      related_name='dislikes_topics',
                                      blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.display_name} at {self.created_at.date()}'

    def get_handle(self):
        return f'@{self.account.username}'


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    author = models.ForeignKey(SocialProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    is_ai = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: Add media support

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=60, blank=False)
    is_ai = models.BooleanField(default=True)
    # TODO: Add media image support
    created_at = models.DateTimeField(auto_now_add=True)
