from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified',)
    list_filter = ('is_verified',)
    actions = ['verify_users']

    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)
    verify_users.short_description = "Mark selected users as verified"

admin.site.register(Profile, ProfileAdmin)

