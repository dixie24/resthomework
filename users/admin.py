from django.contrib import admin

from users.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin): 
    list_display = ("id", "email", "phone_number")

    fieldsets = (
        (None, {"fields": ("email", "phone_number", "password", "is_active", "is_staff")}),
        ("Important dates", {"fields": ("last_login",)}), 
    )
    
    ordering = ("last_login",)