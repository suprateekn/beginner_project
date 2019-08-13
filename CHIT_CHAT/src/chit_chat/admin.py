from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (UserProfile, Message)
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    verbose_name_plural = 'Profile'
    # filter_horizontal = ['profile_pic']


class CustomAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return list()
        return super(CustomAdmin, self).get_inline_instances(request, obj)


admin.site.register(Message)
admin.site.unregister(User)
admin.site.register(User, CustomAdmin)
