from django.db.models import Q
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Message
from django.contrib.auth.models import User
from .serializers import MessagingSerializer, UserSerializer


class MessageAPIView(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = MessagingSerializer
    authentication_classes = (IsAuthenticated,)

    def get_queryset(self):
        client = self.request.GET.get('userid')
        if client:
            queryset = Message.objects.filter(
                (Q(receiver=self.request.user) & Q(sender=client)) | (
                        Q(receiver=client) & Q(sender=self.request.user)))
        else:
            queryset = Message.objects.all()

        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class UserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class MessageRetrieveView(generics.RetrieveAPIView):
    serializer_class = MessagingSerializer
    queryset = Message.objects.all()
