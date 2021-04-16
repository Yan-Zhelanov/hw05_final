import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post, User

from . import constants


class TestPostForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()
        cls.user = User.objects.create_user(
            username=constants.USERNAME,
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
        cls.group3 = Group.objects.create(
            title='Test-Group-3',
            slug='test-group-3',
            description='Test description for Group 3.',
        )
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.IMAGE_FILE = SimpleUploadedFile(
            name='image.jpg',
            content=constants.IMAGE,
            content_type='image/jpg',
        )
        cls.IMAGE_FILE2 = SimpleUploadedFile(
            name='image2.jpg',
            content=constants.IMAGE,
            content_type='image/jpg',
        )
        cls.IMAGE_FILE3 = SimpleUploadedFile(
            name='image3.jpg',
            content=constants.IMAGE,
            content_type='image/jpg',
        )
        cls.post = Post.objects.create(
            text=constants.POST_TEXT,
            author=cls.user,
            image=cls.IMAGE_FILE,
        )
        cls.POST_URL = reverse('posts:post',
                               args=[cls.user.username, cls.post.id])
        cls.POST_EDIT_URL = reverse('posts:post_edit',
                                    args=[cls.user.username, cls.post.id])
        cls.LOGIN_URL = reverse('login')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.guest_client = Client()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_form_labels(self):
        """Проверка лейблов полей формы"""
        fields = self.form.fields.items()
        expected_labels = {'text': 'Введите текст',
                           'group': 'Выберите группу',
                           'image': 'Загрузите картинку'}
        for name_field, field in fields:
            with self.subTest(name_field=name_field):
                label = field.label
                expected_label = expected_labels[name_field]
                self.assertEqual(label, expected_label)

    def test_post_create(self):
        """Проверка корректного создания поста"""
        id_posts = list(Post.objects.values_list('id', flat=True))
        post_data = {
            'text': 'Тест-тест',
            'group': self.group.id,
            'image': self.IMAGE_FILE2,
        }
        response = self.authorized_client.post(
            constants.NEW_POST_URL,
            data=post_data,
            follow=True,
        )
        self.assertRedirects(response, constants.INDEX_URL)
        posts = response.context['page'].paginator.object_list
        self.assertEqual(len(posts), len(id_posts) + 1)
        created_posts = posts.exclude(id__in=id_posts)
        for post in created_posts:
            self.assertEqual(post.text, post_data['text'])
            self.assertEqual(post.group.id, post_data['group'])
            self.assertEqual(post.author, self.user)
            image_file_name = post.image.name.split('/')[1]
            self.assertEqual(image_file_name, post_data['image'].name)

    def test_correct_change_post(self):
        """Проверка корректного редактирования поста"""
        expected_posts_count = Post.objects.count()
        modified_post_data = {
            'text': 'Изменённый текст',
            'group': self.group2.id,
            'image': self.IMAGE_FILE3,
        }
        response = self.authorized_client.post(
            self.POST_EDIT_URL,
            data=modified_post_data,
            follow=True,
        )
        self.assertRedirects(response, self.POST_URL)
        self.assertEqual(Post.objects.all().count(), expected_posts_count)
        post = response.context['post']
        self.assertEqual(post.text, modified_post_data['text'])
        self.assertEqual(post.group.id, modified_post_data['group'])
        self.assertEqual(post.author, self.user)
        image_file_name = post.image.name.split('/')[1]
        self.assertEqual(image_file_name, modified_post_data['image'].name)

    def test_guest_creation_post(self):
        """Проверка, что гость не может создать пост"""
        expected_posts_count = Post.objects.count()
        post_data = {
            'text': 'Тест-тестовый',
            'group': self.group.id,
            'image': self.IMAGE_FILE3,
        }
        response = self.guest_client.post(
            constants.NEW_POST_URL,
            data=post_data,
            follow=True,
        )
        self.assertRedirects(response,
                             f'{self.LOGIN_URL}?next={constants.NEW_POST_URL}')
        self.assertEqual(Post.objects.count(), expected_posts_count)

    def test_guest_edit_post(self):
        """Проверка, что гость не может редактировать пост"""
        expected_post = self.post
        modified_post_data = {
            'text': 'Changed text',
            'group': self.group3.id,
            'image': self.IMAGE_FILE3,
        }
        self.guest_client.post(
            self.POST_EDIT_URL,
            data=modified_post_data,
        )
        self.assertEqual(self.post.text, expected_post.text)
        self.assertEqual(self.post.group, expected_post.group)
        self.assertEqual(self.post.image, expected_post.image)
