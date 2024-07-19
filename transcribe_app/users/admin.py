from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    list_display = (
        'id', 'username', 'email', 'password', 'is_staff', 'last_login', 'is_active',)
    search_fields = ('id', 'username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active',)
    ordering = ('id', 'username', 'email', 'is_active',)
    readonly_fields = ('last_login', 'date_joined')
