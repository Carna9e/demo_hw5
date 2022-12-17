from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # вызываем конструктор, вспоминаем уроки ООП
        super().__init__(*args, **kwargs)
        # вызываем конструктор базового класса, чтобы не
        # переопределить полностью конструктор а лишь добавить нужное.
        # Помнишь что такое `super()`?
        self.fields['text'].widget.attrs['placeholder'] = (
            'Введите какой нибудь текст... 😥'  # вот тут и вводим наш текст
        )
        self.fields['group'].empty_label = (
            'Выберите группу, если желаете 🙂'
            # вот тут задаем текст какой мы хотим вместо умолчального ------
        )

    class Meta:  # лейблы как я понял в модели прописаны
        model = Post
        fields = ('text', 'group')
        help_texts = {
            'text': 'Введите текст для поста',
            'group': 'Выберите группу из списка'
        }
