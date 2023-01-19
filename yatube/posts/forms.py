from django import forms

from .models import Post, Comment


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
        fields = ('text', 'group', 'image')
        '''
        help_texts = {
            'text': 'Введите текст для поста',
            'group': 'Выберите группу из списка'
        }'''

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = (
            'Введите комментарий... 😥'
        )

    class Meta:
        model = Comment
        fields = ('text',)
