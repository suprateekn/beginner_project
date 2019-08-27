import operator

from django.contrib.auth.models import User
from django.db.models import Max
from rest_framework import serializers

from chit_chat.models import Message


class MessagingSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()
    max_time = serializers.DateTimeField(required=False)

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'text_msg', 'sent_time', 'sender_name', 'receiver_name', 'max_time']
        read_only_fields = ['sender']

    def get_sender_name(self, obj):
        return obj.sender.username

    def get_receiver_name(self, obj):
        return obj.receiver.username


class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()
    last_msg = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_pic', 'last_msg']

    def get_profile_pic(self, obj):
        try:
            if obj.user_profile.profile_pic:
                return 'media/' + str(obj.user_profile.profile_pic)
            return '../static/images/default-user-icon-4.jpg'
        except:
            return '../static/images/default-user-icon-4.jpg'

    def get_last_msg(self, obj):
        sent_msg_details = obj.msg_receiver.values('sender').annotate(max_time=Max('sent_time')).values('max_time',
                                                                                                        'sender')
        received_msg_details = obj.msg_sender.values('receiver').annotate(max_time=Max('sent_time')).values('max_time',
                                                                                                            'receiver')

        last_text_dict = {}
        if sent_msg_details and received_msg_details:
            for element in sent_msg_details:
                last_text_dict[element['sender']] = element['max_time']

            for element in received_msg_details:
                if element['receiver'] in last_text_dict:
                    last_text_dict[element['receiver']] = max(last_text_dict[element['receiver']], element['max_time'])
                else:
                    last_text_dict[element['receiver']] = element['max_time']

        elif sent_msg_details:
            for element in sent_msg_details:
                last_text_dict[element['sender']] = element['max_time']

        else:
            for element in received_msg_details:
                last_text_dict[element['receiver']] = element['max_time']

        sorted_dict = sorted(last_text_dict.items(), key=operator.itemgetter(1), reverse=True)
        sorted_dict = dict(sorted_dict)

        final_sorted_list = []

        for k, v in sorted_dict.items():
            new_dict = {}
            new_dict['key'] = k
            new_dict['val'] = v
            final_sorted_list.append(new_dict)
            print(final_sorted_list)

        return final_sorted_list
