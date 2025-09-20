from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostSerializer


class PostListPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page_size'
    max_page_size = 2000


class PostListView(generics.ListAPIView):
    pagination_class = PostListPagination
    queryset = Post.objects.all()
    serializer_class = PostSerializer
