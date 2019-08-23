from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text=False,
                                 widget=forms.TextInput(attrs={'autocomplete': 'new-password'}))
    last_name = forms.CharField(max_length=30, required=True, help_text=False)
    email = forms.EmailField(max_length=254, required=True, help_text=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
