from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "user_type", "is_active", "is_staff")
    search_fields = ("email", "full_name")
