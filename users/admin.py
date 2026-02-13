from django.contrib import admin

# Register your models here.
# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     fieldsets = (*UserAdmin.fieldsets, ('Roles', {'fields': ('is_observer','is_action_owner','is_safety_manager')}),)
#     list_display = ('username','email','is_observer','is_action_owner','is_safety_manager')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    ordering = ("email",)

    list_display = (
        "email",
        "organization",
        "is_manager",
        "is_superuser",
        "is_active",
    )

    list_filter = (
        "is_manager",
        "is_superuser",
        "is_active",
        "organization",
    )

    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Organization", {"fields": ("organization",)}),
        ("Permissions", {"fields": ("is_manager", "is_superuser", "is_active")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "organization", "is_manager"),
        }),
    )

    filter_horizontal = ()
