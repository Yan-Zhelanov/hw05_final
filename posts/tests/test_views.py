import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Paginator
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Follow, Group, Post, User
from posts.settings import POSTS_PER_PAGE

from . import constants

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username=constants.USERNAME,
        )
        cls.another_user = User.objects.create_user(
            username=constants.USERNAME2,
        )
        cls.group = Group.objects.create(
            title=constants.GROUP_NAME,
            slug=constants.GROUP_SLUG,
            description=constants.GROUP_DESCRIPTION,
        )
        cls.group2 = Group.objects.create(
            title=constants.GROUP2_NAME,
            slug=constants.GROUP2_SLUG,
            description=constants.GROUP2_DESCRIPTION,
        )
        cls.IMAGE_FILE = SimpleUploadedFile(
            name='image.jpg',
            content=constants.IMAGE,
            content_type='image/jpg',
        )
        cls.post = Post.objects.create(
            text=constants.POST_TEXT,
            group=cls.group,
            author=cls.user,
            image=cls.IMAGE_FILE,
        )
        cls.another_user.follower.create(author=cls.user)
        cls.POST_URL = reverse('posts:post',
                               args=[cls.user.username, cls.post.id])
        cls.POST_EDIT_URL = reverse('posts:post_edit',
                                    args=[cls.user.username, cls.post.id])
        cls.author_client = Client()
        cls.author_client.force_login(cls.user)
        cls.another_client = Client()
        cls.another_client.force_login(cls.another_user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_post_in_someone_else_group(self):
        """???????????????? ???? ?????????????? ?????????? ?? ???????????????????????? ????????????"""
        response = self.author_client.get(constants.GROUP2_URL)
        self.assertNotIn(self.post, response.context['page'])

    def test_post_in_someone_follow_feed(self):
        """???????????????? ???? ?????????????? ?????????? ?? ???????????????????????????? ????????????????????????"""
        response = self.author_client.get(constants.FOLLOW_URL)
        self.assertNotIn(self.post, response.context['page'])

    def test_post_correct_view_on_pages(self):
        """???????????????? ?????????????????????? ?????????????????????? ?????????? ???? ??????????????????"""
        urls = [
            [constants.INDEX_URL, 'page'],
            [constants.PROFILE_URL, 'page'],
            [constants.GROUP_URL, 'page'],
            [constants.FOLLOW_URL, 'page'],
            [self.POST_URL, 'post'],
        ]
        for url, context_name in urls:
            with self.subTest(url=url):
                response = self.another_client.get(url)
                if context_name == 'post':
                    post = response.context[context_name]
                elif context_name == 'page':
                    context = response.context[context_name]
                    self.assertEqual(len(context.object_list), 1)
                    post = context.object_list[0]
                self.assertEqual(post.text, self.post.text)
                self.assertEqual(post.group, self.post.group)
                self.assertEqual(post.author, self.post.author)
                self.assertEqual(post.image, self.post.image)

    def test_author_appearence_on_pages(self):
        """???????????????? ?????????????????????? ???????????? ???? ??????????????????"""
        urls = [
            constants.PROFILE_URL,
            self.POST_URL,
        ]
        for url in urls:
            with self.subTest(url=url):
                author = self.author_client.get(url).context['author']
                self.assertEqual(author.username, self.user.username)
                self.assertEqual(author.id, self.user.id)

    def test_group_correct_context(self):
        """???????????????? ?????????????????????? ?????????????????? ???????????????? ????????????"""
        response = self.author_client.get(constants.GROUP_URL)
        group = response.context['group']
        self.assertEqual(group.title, self.group.title)
        self.assertEqual(group.slug, self.group.slug)
        self.assertEqual(group.description, self.group.description)
        self.assertEqual(group.id, self.group.id)

    def test_cache_working(self):
        """???????????????? ???????????? ????????"""
        response = self.author_client.get(constants.INDEX_URL)
        Post.objects.create(
            text='test',
            author=self.user,
        )
        response2 = self.author_client.get(constants.INDEX_URL)
        self.assertEqual(response.content, response2.content)
        cache.clear()
        response3 = self.author_client.get(constants.INDEX_URL)
        self.assertNotEqual(response2.content, response3.content)

    def test_subscribe_work(self):
        """???????????????? ?????????????????? ???????????????????? ????????????????"""
        Follow.objects.all().delete()
        self.another_client.get(constants.PROFILE_FOLLOW_URL)
        self.assertTrue(Follow.objects.filter(user=self.another_user,
                                              author=self.user).exists())

    def test_unsubscribe_work(self):
        """???????????????? ?????????????????? ???????????????????? ??????????????"""
        Follow.objects.all().delete()
        Follow.objects.create(user=self.another_user, author=self.user)
        self.another_client.get(constants.PROFILE_UNFOLLOW_URL)
        self.assertFalse(Follow.objects.filter(user=self.another_user,
                                               author=self.user).exists())


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username=constants.USERNAME,
        )
        cls.group = Group.objects.create(
            title=constants.GROUP_NAME,
            slug=constants.GROUP_SLUG,
            description=constants.GROUP_DESCRIPTION,
        )
        cls.another_user = User.objects.create_user(
            username=constants.USERNAME2,
        )
        cls.another_user.follower.create(author=cls.user)
        for i in range(POSTS_PER_PAGE + 2):
            Post.objects.create(
                text=f'Test-{i}',
                author=cls.user,
                group=cls.group,
            )
        Post.objects.create(
            text='Another Post',
            author=cls.user
        )
        cls.posts = Post.objects.all()
        cls.author_client = Client()
        cls.author_client.force_login(cls.another_user)

    def test_pages_contains_correct_records(self):
        """???????????????? ???????????????????? ???????????? ???? ?????????????????? ??????????????, ?????????????? ?? ????????????"""
        urls = [
            [constants.INDEX_URL, Paginator(self.posts, POSTS_PER_PAGE)],
            [constants.PROFILE_URL, Paginator(self.user.posts.all(),
                                              POSTS_PER_PAGE)],
            [constants.GROUP_URL, Paginator(self.group.posts.all(),
                                            POSTS_PER_PAGE)],
            [constants.FOLLOW_URL, Paginator(self.user.posts.all(),
                                             POSTS_PER_PAGE)],
        ]
        for url, paginator in urls:
            for page in range(1, paginator.num_pages + 1):
                with self.subTest(page=page):
                    response = self.author_client.get(
                        f'{url}?page={page}'
                    )
                    posts_count = len(response.context['page'])
                    self.assertLessEqual(posts_count, POSTS_PER_PAGE)
