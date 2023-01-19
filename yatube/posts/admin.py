from django.contrib import admin

from .models import Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Модель для администратора"""
    list_display = (
        'pk',
        'text',
        # 'pub_date',
        'created',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    # list_filter = ('pub_date',)
    list_filter = ('created',)
    # ordering = ('pub_date',)
    ordering = ('created',)

    empty_value_display = '-пусто-'


admin.site.register(Group)
