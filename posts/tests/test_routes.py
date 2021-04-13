from django.test import TestCase
from django.urls import reverse

from posts.models import Post, User

from . import constants


class RoutesTest(TestCase):
    def test_correct_urls_as_used(self):
        """Проверка использования верных маршрутов страниц"""
        user = User.objects.create_user(
            username=constants.USERNAME,
        )
        post = Post.objects.create(
            text=constants.POST_TEXT,
            author=user,
        )
        urls = [
            [constants.INDEX_URL, '/'],
            [constants.GROUP_URL, f'/group/{constants.GROUP_SLUG}/'],
            [constants.PROFILE_URL, f'/{user.username}/'],
            [constants.NEW_POST_URL, '/new/'],
            [reverse('posts:post', args=[user.username, post.id]),
             f'/{user.username}/{post.id}/'],
            [reverse('posts:post_edit', args=[user.username, post.id]),
             f'/{user.username}/{post.id}/edit/'],
        ]
        for url, expected_url in urls:
            self.assertEqual(url, expected_url)
