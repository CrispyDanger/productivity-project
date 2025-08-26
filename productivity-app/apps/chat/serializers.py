from rest_framework import serializers
from .models import Message, Conversation


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['message_type', 'content', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer()

    class Meta:
        model = Conversation
        fields = ['messages', 'title', 'created_at', 'account']
