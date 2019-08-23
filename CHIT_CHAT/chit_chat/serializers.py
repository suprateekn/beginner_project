from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Message, UserProfile


class UserSerializer(serializers.ModelSerializer):
    # profile_pic = serializers.ImageField(source='user_profile.profile_pic', read_only=True)

    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_pic']

    def get_profile_pic(self, obj):
        try:
            if obj.user_profile.profile_pic:
                return 'media/' + str(obj.user_profile.profile_pic)
            return '../static/images/default-user-icon-4.jpg'
        except:
            return '../static/images/default-user-icon-4.jpg'


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
