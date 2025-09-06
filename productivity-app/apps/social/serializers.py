from rest_framework import serializers
from .models import SocialProfile, Post, Comment
from account.serializers import UserSerializer


class SocialProfileSerializer(serializers.ModelSerializer):
    account = UserSerializer(read_only=True)

    class Meta:
        model = SocialProfile
        fields = ['account', 'display_name',
                  'description', 'is_bot', 'created_at', 'bot_personality']


class PostSerializer(serializers.ModelSerializer):
    author = SocialProfileSerializer(read_only=True)
    comments_count = serializers.IntegerField(source="comments.count",
                                              read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author", "text", "created_at", "is_ai",
                  "comments_count"]


class CommentSerializer(serializers.ModelSerializer):
    created_by = SocialProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "created_by", "text", "created_at", "is_ai"]
