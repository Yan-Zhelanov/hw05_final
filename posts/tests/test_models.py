from django.test import TestCase

from posts.models import Group, Post, User

from . import constants


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=constants.GROUP_NAME,
            slug=constants.GROUP_SLUG,
            description=constants.GROUP_DESCRIPTION,
        )

    def test_verbose_names(self):
        """Проверка у всех полей группы verbose_name"""
        field_verboses = {
            'title': 'Название Группы',
            'slug': 'Ключ ссылки',
            'description': 'Описание',
        }
        for field, expected_verbose_name in field_verboses.items():
            with self.subTest(field=field):
                verbose_name = Group._meta.get_field(field).verbose_name
                self.assertEqual(verbose_name, expected_verbose_name)

    def test_help_texts(self):
        """Проверка у всех полей группы help_text"""
        field_help_texts = {
            'title': 'Укажите название группы',
            'slug': ('Укажите ключ для страницы группы, используйте только '
                     'латиницу, цифры, дефисы и подчёркивания.'),
            'description': 'Расскажите о вашей группе по подробнее',
        }
        for field, expected_help_text in field_help_texts.items():
            with self.subTest(field=field):
                help_text = Group._meta.get_field(field).help_text
                self.assertEqual(help_text, expected_help_text)

    def test_str_returns_title(self):
        """Проверка, что группа возвращает свой заголовок на запрос str"""
        group_to_str = str(self.group)
        expected_object_name = self.group.title
        self.assertEqual(group_to_str, expected_object_name)


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username=constants.USERNAME,
        )
        cls.group = Group.objects.create(
            title=constants.GROUP_NAME,
            slug=constants.GROUP_SLUG,
            description=constants.GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            text=constants.POST_TEXT,
            author=cls.user,
            group=cls.group,
        )

    def test_verbose_names(self):
        """Проверка у всех полей поста verbose_name"""
        field_verbose_names = {
            'text': 'Текст',
            'pub_date': 'Дата',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_verbose_name in field_verbose_names.items():
            with self.subTest(field=field):
                verbose_name = Post._meta.get_field(field).verbose_name
                self.assertEqual(verbose_name, expected_verbose_name)

    def test_help_texts(self):
        """Проверка у всех полей поста help_text"""
        field_help_texts = {
            'text': 'Расскажите о чём ваш пост',
            'pub_date': 'Дата публикации поста',
            'author': 'Автор данного поста',
            'group': 'Укажите группу, если такая есть',
        }
        for field, expected_help_text in field_help_texts.items():
            with self.subTest(field=field):
                help_text = Post._meta.get_field(field).help_text
                self.assertEqual(help_text, expected_help_text)

    def test_str_returned_correctly(self):
        """Проверка, что пост возвращает правильный ответ на запрос str"""
        post_str = str(self.post)
        pub_date = self.post.pub_date.strftime('%d.%m.%Y %H:%M')
        expected_post_str = (
            f'Автор: {self.post.author.username}; '
            f'Группа: {self.post.group}; '
            f'Дата: {pub_date}; '
            f'Текст: {self.post.text[:15]}...'
        )
        self.assertEqual(post_str, expected_post_str)
