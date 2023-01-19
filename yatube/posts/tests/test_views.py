from random import randint
import shutil, tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post

from ..forms import PostForm

User = get_user_model()

# MEDIA_ROOT_TEST = tempfile.TemporaryDirectory() как сделать этой функцией?
MEDIA_ROOT_TEST = tempfile.mkdtemp(dir=settings.BASE_DIR)

@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.small_gif = (            
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый пост',
            image=cls.uploaded,
        )
        cls.url_post_edit = reverse('posts:post_edit',
                                    kwargs={'post_id': cls.post.id})
        cls.url_post_detail = reverse('posts:post_detail',
                                      kwargs={'post_id': cls.post.id})
        cls.form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT_TEST, ignore_errors=True)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = (
            ('posts/index.html', reverse('posts:index')),
            ('posts/group_list.html',
                (reverse('posts:group_list', kwargs={'slug': self.group.slug}))
             ),
            ('posts/profile.html',
                (reverse('posts:profile',
                         kwargs={'username': self.user.username}))
             ),
            ('posts/post_detail.html',
                (reverse('posts:post_detail',
                         kwargs={'post_id': self.post.id}))
             ),
            ('posts/create.html', reverse('posts:post_create')),
            ('posts/create.html',
                (reverse('posts:post_edit', kwargs={'post_id': self.post.id}))
             ),
        )

        for template, reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def response_test(self, response):
        self.assertIn('page_obj', response.context)
        self.assertLess(0, (len(response.context.get('page_obj'))))
        first_object = response.context.get('page_obj')[0]
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.author, self.post.author)
        self.assertEqual(first_object.group, self.post.group)
        self.assertEqual(first_object.pk, self.post.pk)
        self.assertEqual(first_object.image, self.post.image)

    # решил сделать две функции чтобы самому себе понятно было=)
    def post_test(self, post):
        object_post = post.context.get('post')
        self.assertEqual(object_post.text, self.post.text)
        self.assertEqual(object_post.author, self.post.author)
        self.assertEqual(object_post.group, self.post.group)
        self.assertEqual(object_post.pk, self.post.pk)
        self.assertEqual(object_post.image, self.post.image)

    def test_index_show_correct_context(self):
        """Проверяем index контекст"""
        '''response = self.authorized_client.get(
            reverse('posts:index')).context['page_obj'][0]
                self.assertEqual(response, self.post)'''
        response = self.authorized_client.get(reverse('posts:index'))
        self.response_test(response)

    def test_group_list_show_correct_context(self):
        """Проверяем  контекст шаблона group_list"""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        self.response_test(response)
        self.assertIn('group', response.context)
        self.assertEqual(response.context['group'], self.group)

    def test_profile_show_correct_context(self):
        """Проверяем  контекст шаблона profile"""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.post.author}))
        self.response_test(response)
        self.assertIn('author', response.context)
        self.assertEqual(response.context['author'], self.user)

    def test_detail_post_context(self):
        """Проверяем контекст шаблона страницы поста"""
        response = self.authorized_client.get(
            self.url_post_detail)
        self.post_test(response)
        self.assertIn('post', response.context)
        self.assertEqual(response.context['post'], self.post)

    def test_post_create_form(self):
        """Проверяем контекс и форму страницы создания поста"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        for value, expected in self.form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_form(self):
        """Проверяем контекс и форму страницы редактирования поста"""
        response = self.authorized_client.get(self.url_post_edit)
        for value, expected in self.form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIn('is_edit', response.context)
                # проверка переменной редактирования
                self.assertTrue(response.context['is_edit'])
                # поверка наличия формы в контексте
                self.assertIn('form', response.context)
                # проверка существования формы
                self.assertIsInstance(response.context['form'], PostForm)
                # поверка названий полей
                self.assertIsInstance(form_field, expected)

    def test_check_group_in_pages(self):
        """Проверяем создание поста на страницах с выбранной группой"""
        form_fields = {
            reverse('posts:index'): Post.objects.get(group=self.post.group),
            reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}
            ): Post.objects.get(group=self.post.group),
            reverse(
                'posts:profile', kwargs={'username': self.post.author}
            ): Post.objects.get(group=self.post.group),
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                self.assertIn('page_obj', response.context)
                form_field = response.context['page_obj']
                self.assertIn(expected, form_field)

    def test_check_group_not_in_mistake_group_list_page(self):
        """Проверяем чтобы созданный Пост с группой не попал в чужую группу."""
        form_fields = {
            reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}
            ): Post.objects.exclude(group=self.post.group),
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                self.assertIn('page_obj', response.context)
                form_field = response.context['page_obj']
                self.assertNotIn(expected, form_field)


class PaginatorViewsTest(TestCase):
    """Здесь создаются фикстуры: клиент и 13 тестовых записей."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='VasyaPupkin')
        cls.group1 = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.posts_p2 = randint(1, settings.LIMIT - 1)
        cls.posts = [
            Post(
                author=cls.user,
                text=f'Тестовый пост {i}.',
                group=cls.group1,
            ) for i in range(settings.LIMIT + cls.posts_p2)
        ]
        Post.objects.bulk_create(cls.posts)
        cls.url_index = reverse('posts:index')
        cls.url_group1 = reverse('posts:group_list',
                                 kwargs={'slug': cls.group1.slug})
        cls.url_profile = reverse('posts:profile',
                                  kwargs={'username': cls.user.username})

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.user)

    def test_paginator_first_page(self):
        """Проверяем работу паджинатора, первая страница"""
        url_tuple = (
            (self.url_index, settings.LIMIT),
            (self.url_group1, settings.LIMIT),
            (self.url_profile, settings.LIMIT),
        )
        for url, expected in url_tuple:
            with self.subTest(url=url):
                self.assertIn('page_obj', self.author_client.get(url).context)
                response = self.author_client.get(url).context['page_obj']
                self.assertEqual(len(response), expected)

    def test_paginator_second_page(self):
        """Проверяем работу паджинатора, вторая страница"""
        url_tuple = (
            (self.url_index + '?page=2', self.posts_p2),
            (self.url_group1 + '?page=2', self.posts_p2),
            (self.url_profile + '?page=2', self.posts_p2),
        )
        for url, expected in url_tuple:
            with self.subTest(url=url):
                self.assertIn('page_obj', self.author_client.get(url).context)
                response = self.author_client.get(url).context['page_obj']
                self.assertEqual(len(response), expected)
