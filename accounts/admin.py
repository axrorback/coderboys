from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'department','is_active')
    list_filter = ('is_active','department')
    search_fields = ('username',)
    ordering = ('username',)

