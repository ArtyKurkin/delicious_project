from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    User admin
    """
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('username', 'email', )
    empty_value_display = '-пусто-'
