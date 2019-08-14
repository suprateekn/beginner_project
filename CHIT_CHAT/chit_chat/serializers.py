from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class MessagingSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'text_msg', 'sent_time', 'sender_name', 'receiver_name']
        read_only_fields = ['sender']

    def get_sender_name(self, obj):
        return obj.sender.username

    def get_receiver_name(self, obj):
        return obj.receiver.username