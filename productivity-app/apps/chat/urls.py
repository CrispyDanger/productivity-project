from django.urls import path
from . import api

urlpatterns = [
    path('conversation-list/', api.ConversationListView.as_view(),
         name='conversation_list')
]
