from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "spouse")
    fieldsets = UserAdmin.fieldsets + (
        ("HomeBase", {"fields": ("spouse", "timezone")}),
    )
