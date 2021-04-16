from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

from . import constants


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=constants.GROUP_NAME,
            slug=constants.GROUP_SLUG,
            description=constants.GROUP_DESCRIPTION,
        )
        cls.user = User.objects.create_user(
            username=constants.USERNAME,
        )
        cls.another_user = User.objects.create_user(
            username=constants.USERNAME2,
        )
        cls.post = Post.objects.create(
            text=constants.POST_TEXT,
            author=cls.user,
        )
        cls.POST_URL = reverse('posts:post',
                               args=[cls.user.username, cls.post.id])
        cls.POST_EDIT_URL = reverse('posts:post_edit',
                                    args=[cls.user.username, cls.post.id])
        cls.ADD_COMMENT_URL = reverse('posts:add_comment',
                                      args=[cls.user.username, cls.post.id])
        cls.LOGIN_URL = reverse('login')
        cls.guest_client = Client()
        cls.author_client = Client()
        cls.author_client.force_login(cls.user)
        cls.other_client = Client()
        cls.other_client.force_login(cls.another_user)

    def test_response_codes_pages(self):
        """Проверка доступности страниц"""
        urls = [
            [constants.INDEX_URL, self.guest_client, 200],
            [constants.GROUP_URL, self.guest_client, 200],
            [constants.PROFILE_URL, self.guest_client, 200],
            [constants.NEW_POST_URL, self.guest_client, 302],
            [constants.NEW_POST_URL, self.author_client, 200],
            [self.POST_URL, self.guest_client, 200],
            [self.POST_EDIT_URL, self.guest_client, 302],
            [self.POST_EDIT_URL, self.author_client, 200],
            [self.POST_EDIT_URL, self.other_client, 302],
            [self.ADD_COMMENT_URL, self.guest_client, 302],
            [self.ADD_COMMENT_URL, self.author_client, 302],
            [constants.PROFILE_FOLLOW_URL, self.guest_client, 302],
            [constants.PROFILE_FOLLOW_URL, self.other_client, 302],
            [constants.PROFILE_UNFOLLOW_URL, self.guest_client, 302],
            [constants.PROFILE_UNFOLLOW_URL, self.other_client, 302],
            ['ZXiz0vKDN25CsTl4Jb5VwT6iLOmnHbJxYSZRgz', self.guest_client, 404]
        ]
        for url, client, expected_status_code in urls:
            with self.subTest(url=url):
                self.assertEqual(
                    client.get(url).status_code,
                    expected_status_code
                )

    def test_redirects(self):
        """Проверка корректно работающих перенаправлений"""
        urls = [
            [constants.NEW_POST_URL, self.guest_client,
             f'{self.LOGIN_URL}?next={constants.NEW_POST_URL}'],
            [self.ADD_COMMENT_URL, self.guest_client,
             f'{self.LOGIN_URL}?next={self.ADD_COMMENT_URL}'],
            [self.ADD_COMMENT_URL, self.author_client, self.POST_URL],
            [constants.PROFILE_FOLLOW_URL, self.guest_client,
             f'{self.LOGIN_URL}?next={constants.PROFILE_FOLLOW_URL}'],
            [constants.PROFILE_FOLLOW_URL, self.other_client,
             constants.PROFILE_URL],
            [constants.PROFILE_UNFOLLOW_URL, self.guest_client,
             f'{self.LOGIN_URL}?next={constants.PROFILE_UNFOLLOW_URL}'],
            [constants.PROFILE_UNFOLLOW_URL, self.other_client,
             constants.PROFILE_URL],
            [self.POST_EDIT_URL, self.guest_client,
             f'{self.LOGIN_URL}?next={self.POST_EDIT_URL}'],
            [self.POST_EDIT_URL, self.other_client,
             self.POST_URL],
        ]
        for url, client, expected_url in urls:
            with self.subTest(url=url):
                self.assertRedirects(client.get(url), expected_url)

    def test_correct_templates_as_used(self):
        """Проверка на использование верного шаблона"""
        urls = [
            [constants.INDEX_URL, 'index.html'],
            [constants.GROUP_URL, 'group.html'],
            [constants.PROFILE_URL, 'profile.html'],
            [constants.FOLLOW_URL, 'follow.html'],
            [constants.NEW_POST_URL, 'post-form.html'],
            [self.POST_URL, 'post.html'],
            [self.POST_EDIT_URL, 'post-form.html'],
        ]
        for url, expected_template in urls:
            with self.subTest(url=url):
                self.assertTemplateUsed(
                    self.author_client.get(url),
                    expected_template
                )
