from rest_framework import generics
from .serializers import UserDetailSerializer


class UserDetailView(generics.RetrieveAPIView):
    class Meta:
        serializer_class = UserDetailSerializer

    def get(self, request):
        serializer = self.get_serializer_context(request.user)
        return serializer.data
