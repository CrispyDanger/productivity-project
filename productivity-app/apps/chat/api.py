from rest_framework.generics import ListAPIView
from .models import Conversation
from .serializers import ConversationSerializer


class ConversationListView(ListAPIView):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return (
            Conversation.objects
            .filter(account=self.request.user)
            .prefetch_related("messages")
        )
