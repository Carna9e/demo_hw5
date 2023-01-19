'''from http import HTTPStatus
import shutil, tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post, User

User = get_user_model()

MEDIA_ROOT_TEST = tempfile.mkdtemp(dir=settings.BASE_DIR)

@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.authorized_author = Client()
        small_gif = (            
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            image=Test.uploaded,
            group=Group.objects.latest('id'),
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(Test.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT_TEST, ignore_errors=True)

    def test_create_post(self):
        """Проверка создания поста и подсчёт кол-ва записей в Post"""
        posts_count = Post.objects.count()
        small2_gif = (            
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        uploaded2 = SimpleUploadedFile(
            name='small2.gif',
            content=small2_gif,
            content_type='image/gif'
        )
        form_data = {'text': 'Текст для поста',
                     'image': uploaded2,
                     'group': Test.group.id,
                     }

        response = self.authorized_client.post(reverse('posts:post_create'),
                                               data=form_data,
                                               follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        latest_post = Post.objects.latest('id')

        assert_fields = {
            latest_post.author: self.post.author,
            latest_post.text: form_data['text'],
            latest_post.image.name: ('posts/image/' + form_data['image'].name),
            latest_post.group.pk: form_data['group'],
        }

        # self.assertEqual(latest_post.image.read(), self.form_data['image'])
        for value, ex_value in assert_fields.items():
            with self.subTest(value=value):
                self.assertEqual(value, ex_value)
        self.assertEqual(Post.objects.count(), posts_count + 1, 
                         'Поcт не добавлен в БД')

    def test_can_edit_post(self):
        """Проверка прав редактирования"""
        self.post = Post.objects.create(text='test_text',
                                        author=self.user,
                                        group=self.group)
        posts_count = Post.objects.count()
        self.group2 = Group.objects.create(title='test_group2',
                                           slug='test-group',
                                           description='test_description')
        form_data = {'text': 'Текст для поста',
                     'group': self.group2.id,
                     }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=[self.post.id]),
            data=form_data,
            follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        latest_post = Post.objects.latest('id')
        assert_fields = {
            latest_post.pub_date: self.post.pub_date,
            latest_post.author: self.post.author,
            latest_post.group.id: form_data['group'],
            latest_post.text: form_data['text'],
        }
        for value, ex_value in assert_fields.items():
            with self.subTest(value=value):
                self.assertEqual(value, ex_value)
        self.assertEqual(posts_count, latest_post.id,
                         'Поcт добавлен в БД')
        self.assertEqual(self.post.text, 'test_text',
                         'Пользователь не может изменить текст поста')
        self.assertEqual(self.post.group, self.group,
                         'Пользователь не может изменить группу поста')

    def test_can_edit_post_guest_client(self):
        """Проверка прав редактирования незарегистрированного чувака"""
        form_data = {'text': 'Текст для поста'}
        response = self.guest_client.post(
            reverse('posts:post_edit', args=[self.post.id]),
            data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)'''
