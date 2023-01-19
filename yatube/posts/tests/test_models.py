from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый супер-пупер очень крутой пост',
        )

    def test_models_have_correct_object_name(self):
        """Проверяем, что у моделей корректно работает __str__."""
        str_text = {
            self.group: PostModelTest.group.title,
            self.post: PostModelTest.post.text[:15],
        }
        for field, expected_value in str_text.items():
            with self.subTest(field=field):
                self.assertEqual(str(field), expected_value)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = PostModelTest.post
        field_verboses = {
            'group': 'Группа поста',
            'author': 'Автор поста',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        task = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст для поста',
            'group': 'Выберите группу из списка',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).help_text, expected_value)
