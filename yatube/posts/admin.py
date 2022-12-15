from django.contrib import admin
from .models import Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Модель для администратора"""
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    ordering = ('pub_date',)

    empty_value_display = '-пусто-'


admin.site.register(Group)
