from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


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
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.post_two = Post.objects.create(
            author=User.objects.create_user(username='VasyaPupkin'),
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        """Проверка доступа к открытым страницам любого пользователя.
            '/profile/StasBasov/'"""
        page_verboses = {
            'index': '/',
            'group_list': f'/group/{self.group.slug}/',
            'post_detail': f'/posts/{self.post.id}/',
            'profile': f'/profile/{self.post.author}/',
        }
        for field, expected_value in page_verboses.items():
            with self.subTest(field=field):
                response = self.guest_client.get(expected_value)
                self.assertEqual(response.status_code, 200)

    def test_homepage_two(self):
        """Проверка редактора и создавателя постов на
           доступность авторизованному."""
        page_verboses = {
            'editor': (reverse('posts:post_edit', args=[self.post.id])),
            'creater': '/create/',
        }
        for field, expected_value in page_verboses.items():
            with self.subTest(field=field):
                response = self.authorized_client.get(expected_value)
                self.assertEqual(response.status_code, 200)

    def test_homepage_three(self):
        """Проверка редактора постов на недоступность
           авторизованному НЕ автору и его перенаправление."""
        response = self.authorized_client.get(reverse('posts:post_edit',
                                              args=[self.post.id + 1]))
        self.assertRedirects(response, (reverse('posts:post_detail',
                             args=[self.post.id + 1])))

    def test_homepage_four(self):
        """Проверка перенаправления неавторизованного
           пользователя на авторизацию из редактора."""
        back = reverse('posts:post_edit', args=[self.post.id])
        response = self.guest_client.get(back)
        self.assertRedirects(response, f'/auth/login/?next={back}')

    def test_homepage_five(self):
        """Проверка перенаправления неавторизованного
           пользователя на авторизацию из создателя."""
        response = self.guest_client.get('/create/')
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_homepage_six(self):
        """Проверка доступности любого пользователя на ошибку 404"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_urls_uses_correct_template(self):
        """Проверка шаблонов по адресам"""
        templates_url_names = {
            '/': 'posts/index.html',
            '/create/': 'posts/create.html',
            (reverse('posts:post_edit',
                     args=[self.post.id])): 'posts/create.html',
            # '/posts/1/edit/'
            (reverse('posts:group_list',
                     args=[self.group.slug])): 'posts/group_list.html',
            (reverse('posts:post_detail',
                     args=[self.post.id])): 'posts/post_detail.html',
            (reverse('posts:profile',
                     args=[self.user.username])): 'posts/profile.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
