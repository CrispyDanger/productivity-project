from account.serializers import UserSerializer
from rest_framework import serializers

from .models import Comment, Post, SocialProfile, PostLike


class SocialProfileSerializer(serializers.ModelSerializer):
    account = UserSerializer(read_only=True)

    class Meta:
        model = SocialProfile
        fields = [
            "account",
            "display_name",
            "description",
            "is_bot",
            "created_at",
            "bot_personality",
        ]


class PostSerializer(serializers.ModelSerializer):
    author = SocialProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'created_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'author': {'read_only': True},
            'text': {'read_only': True},
            'created_at': {'read_only': True},
        }


class PostListSerializer(serializers.ModelSerializer):
    author = SocialProfileSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    reposts_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    is_reposted = serializers.BooleanField(read_only=True)
    original_post = PostSerializer(read_only=True, required=False)

    class Meta:
        model = Post
        fields = ["id", "author", "text",
                  "created_at", "is_ai", 'is_liked',
                  "comments_count", "likes_count", "reposts_count",
                  'original_post', "is_reposted"]


class CreatePostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = SocialProfileSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True, default=0)
    likes_count = serializers.IntegerField(read_only=True, default=0)
    reposts_count = serializers.IntegerField(read_only=True, default=0)
    is_liked = serializers.BooleanField(read_only=True, default=False)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', "text", "author", "created_at", 'original_post',
                  'comments_count', 'likes_count', 'reposts_count', 'is_liked']
        extra_kwargs = {
            'original_post': {'required': False}
        }


class CommentListSerializer(serializers.ModelSerializer):
    author = SocialProfileSerializer(source='created_by', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_at']


class CommentDetailSerializer(serializers.ModelSerializer):
    replies = CommentListSerializer(many=True, read_only=True)
    created_by = SocialProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_by', 'created_at', 'replies']


class CreateCommentSerializer(serializers.ModelSerializer):
    author = SocialProfileSerializer(source='created_by', read_only=True)

    class Meta:
        model = Comment
        fields = ["post", "text", "parent", 'author']
        extra_kwargs = {
            "text": {"required": True, "allow_blank": False},
            "parent": {"required": False, "allow_null": True},
        }


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = ['post']
