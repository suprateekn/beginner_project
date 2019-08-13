from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="UserProfile")
    profile_pic = models.ImageField(upload_to='image/', blank=True, null=True)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='receiver')
    text_msg = models.TextField(blank=True, null=True)
    sent_time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(f"To {self.receiver.username} from {self.sender.username}")
