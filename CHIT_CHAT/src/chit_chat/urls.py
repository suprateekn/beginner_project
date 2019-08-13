from .views import (MessageRetrieveView, MessageAPIView, UserAPIView)
from django.urls import path

urlpatterns = (
    path('user/', UserAPIView.as_view(), name='list-user'),
    path('message/', MessageAPIView.as_view(), name='list-msg'),
    path('<int:pk>/', MessageRetrieveView.as_view(), name='retrieve-msg'),
)