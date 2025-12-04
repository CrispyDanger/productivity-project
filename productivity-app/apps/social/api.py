from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Post
from .serializers import PostListSerializer, CreatePostSerializer


class PostListPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 2000


class PostListView(generics.ListAPIView):
    pagination_class = PostListPagination
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class CreatePostView(generics.CreateAPIView):
    serializer_class = CreatePostSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data
        data['author'] = request.user.socialprofile.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
