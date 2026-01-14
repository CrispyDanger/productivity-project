from uuid import uuid4

from django.db import models
from django.db.models import Count, Exists, OuterRef, QuerySet
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


class PostQuerySet(QuerySet):
    def with_interactions(self, user):
        return self.annotate(comments_count=Count('comments', distinct=True),
                             likes_count=Count('likes', distinct=True),
                             reposts_count=Count('reposts', distinct=True),
                             is_liked=Exists(PostLike.objects.filter(user=user, post=OuterRef('pk'))),
                             is_reposted=Exists(Post.objects.filter(author=user, original_post=OuterRef('pk'))))


class Post(models.Model):
    objects = PostQuerySet.as_manager()
    id = models.UUIDField(primary_key=True, default=uuid4)
    author = models.ForeignKey(SocialProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    is_ai = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: Add media support

    original_post = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reposts"
    )

    class Meta:
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(
            fields=["author", "original_post"],
            name="unique_repost_per_user"
        )
    ]

    def __str__(self):
        return f"Post at {self.created_at} by {self.author.display_name}"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_by = models.ForeignKey(SocialProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, blank=False)
    is_ai = models.BooleanField(default=True)
    # TODO: Add media image support
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
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


class PostLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(SocialProfile, on_delete=models.CASCADE,
                             related_name='liked_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
        ]
