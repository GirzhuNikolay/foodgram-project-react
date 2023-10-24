from django.contrib import admin

from .models import User

L_P_P = 10


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'is_admin'
    )
    empty_value_display = '--пусто--'
    list_editable = ('is_admin',)
    list_filter = ('username', 'email')
    list_per_page = L_P_P
    search_fields = ('username',)
