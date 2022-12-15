from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    '''Модель для групп постов'''
    title = models.CharField('title для страницы группы', max_length=200)
    slug = models.SlugField('url-адрес для страницы группы', unique=True)
    description = models.TextField('Описание для страницы группы')

    class Meta:
        verbose_name = 'Группа постов'
        verbose_name_plural = 'Группы постов'

    def __str__(self):
        return self.title


class Post(models.Model):
    '''Модель для постов'''
    text = models.TextField('Текст поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Группа поста',
        related_name='posts',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор поста',
        related_name='posts',
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
