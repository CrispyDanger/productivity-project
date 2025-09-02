from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SocialProfile(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=20, null=False, blank=False,
                                    default='Change Me')
    # TODO: Add profile image support
    description = models.CharField(max_length=120, blank=True)
    is_bot = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.display_name} at {self.created_at.date()}'

    def get_handle(self):
        return f'@{self.account.username}'


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=120)
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
