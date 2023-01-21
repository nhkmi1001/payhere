from django.contrib import admin
from .models import User

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('email', 'is_admin')
    fields = (
        'email',
        'is_admin',
        'is_active',
    )