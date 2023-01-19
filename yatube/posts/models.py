from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    """Модель для групп постов"""
    title = models.CharField('title для страницы группы', max_length=200)
    slug = models.SlugField('url-адрес для страницы группы', unique=True)
    description = models.TextField('Описание для страницы группы')

    class Meta:
        verbose_name = 'Группа постов'
        verbose_name_plural = 'Группы постов'

    def __str__(self):
        return self.title


class Post(CreatedModel):
    """Модель для постов"""
    text = models.TextField(
        verbose_name = 'Текст поста',
        help_text='Введите текст для поста',
    )
    #pub_date = models.DateTimeField(
    #    verbose_name = 'Дата публикации',
    #    auto_now_add=True,
    #)
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Группа поста',
        related_name='posts',
        help_text='Выберите группу из списка',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор поста',
        related_name='posts',
    )
    image = models.ImageField(
        verbose_name = 'Картинка',
        upload_to='posts/image/',
        blank=True
    )  

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        # ordering = ('-pub_date',)
        # ordering = ('-created',)

    def __str__(self):
        return self.text[:15]

class Comment(CreatedModel):
    """Модель комментариев"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Комментарий',
        related_name='comments',
        help_text='Опишите комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
    )
    text = models.TextField(
        verbose_name = 'Текст комментария',
        help_text='Введите текст для комментария',
    )
    #created = models.DateTimeField(
    #    verbose_name = 'Дата создания комментария',
    #    auto_now_add=True,
    #)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return self.text
