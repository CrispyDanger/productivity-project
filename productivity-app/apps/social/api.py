from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from .tasks import make_post


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        make_post.delay()
        return super().get(request, *args, **kwargs)
