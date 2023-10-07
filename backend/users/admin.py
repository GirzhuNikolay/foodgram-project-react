from django.contrib import admin

from .models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "password")
    list_filter = ("first_name", "email",)


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('user', 'author',)


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
