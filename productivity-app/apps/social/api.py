from django.db import transaction
from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from social.models import Post, Comment, PostLike, SocialProfile
from social.serializers import (
    CreateCommentSerializer,
    CommentListSerializer,
    CreatePostSerializer,
    PostListSerializer,
)
from social.permissions import isPostAuthor


class PostListPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page_size"
    max_page_size = 2000


class PostListView(generics.ListAPIView):
    pagination_class = PostListPagination
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostListSerializer

    def get_queryset(self):
        user = self.request.user.socialprofile

        return Post.objects.select_related('author').with_interactions(user).order_by('-created_at')


class CreatePostView(generics.CreateAPIView):
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user.socialprofile
        serializer.save(author=user)

    def create(self, request, *args, **kwargs):
        data = self.request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeletePostView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, isPostAuthor]
    queryset = Post.objects.all()


class CommentListView(generics.ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = PostListPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id)\
                              .select_related('created_by')\
                              .order_by('-created_at')


class CreateCommentView(generics.CreateAPIView):
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.socialprofile)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['post'] = self.kwargs.get("post_id")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        response_data = serializer.data

        return Response(response_data, status=status.HTTP_201_CREATED)


class DeleteCommentView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user.socialprofile
        post_id = self.kwargs.get('post_id')

        with transaction.atomic():
            like = PostLike.objects.filter(user=user, post=post_id).first()

            if like:
                like.delete()
                return Response({'is_liked': False}, status=status.HTTP_200_OK)

            PostLike.objects.create(post_id=post_id, user=user)

            return Response({'is_liked': True}, status=status.HTTP_201_CREATED)


class RepostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = self.request.data
        user = request.user.socialprofile
        post_id = self.kwargs.get('post_id')

        data['original_post'] = post_id

        with transaction.atomic():
            repost = Post.objects.filter(author=user, original_post_id=post_id).first()

            if repost:
                repost.delete()
                return Response(status=status.HTTP_200_OK)

            serializer = CreatePostSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            post = serializer.save(author=user)

            data = PostListSerializer(post).data

            return Response(data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    def get_queryset(self, user):
        return Post.objects.filter(author=user).with_interactions(self.request.user.socialprofile)

    def get(self, requests, *args, **kwargs):
        user = self.kwargs.get('profile_username')

        social_profile = get_object_or_404(SocialProfile, account__username=user)

        queryset = self.get_queryset(social_profile)

        serializer = PostListSerializer(instance=queryset, many=True)

        data = {
            'profile': {
                'username': user,
                'display_name': social_profile.display_name
            },
            'feed': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
