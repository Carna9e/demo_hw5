from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = (
            'Введите какой нибудь текст... 😥'
        )
        self.fields['group'].empty_label = (
            'Выберите группу, если желаете 🙂'
        )

    class Meta:
        # лейблы как я понял в модели прописаны
        model = Post
        fields = ('text', 'group')
        help_texts = {
            'text': 'Введите текст для поста',
            'group': 'Выберите группу из списка'
        }
