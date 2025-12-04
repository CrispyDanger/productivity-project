from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SocialProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=20, null=False, blank=False,
                                    default='Change Me')
    # TODO: Add profile image support
    description = models.CharField(max_length=120, blank=True)
    is_bot = models.BooleanField(default=True)
    bot_personality = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.display_name} at {self.created_at.date()}'

    def get_handle(self):
        return f'@{self.account.username}'


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_by = models.ForeignKey(SocialProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, blank=False)
    is_ai = models.BooleanField(default=True)
    # TODO: Add media image support
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        if self.parent:
            return f"{self.created_by.display_name} replied to a comment"
        return f"{self.created_by.display_name} commented on {self.post.text[:10]}"


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    author = models.ForeignKey(SocialProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    is_ai = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, blank=True)
    # TODO: Add media support

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post at {self.created_at} by {self.author.display_name}"
