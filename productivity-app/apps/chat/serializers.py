from rest_framework import serializers
from .models import Message, Conversation


class MessageSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='message_type')

    class Meta:
        model = Message
        fields = ['role', 'content', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['messages', 'title', 'created_at', 'account', 'id']
