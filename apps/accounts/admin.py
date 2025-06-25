from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User

    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'email_verified',
        'is_active',
        'is_staff',
        'is_superuser',
        'created',
    )

    list_filter = (
        'is_active', 'is_staff', 'email_verified',
    )

    search_fields = ('username', 'email')
