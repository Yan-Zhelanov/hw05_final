from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


def get_username(self):
    return self.username


User.add_to_class('__str__', get_username)
User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название Группы',
        help_text='Укажите название группы',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Ключ ссылки',
        help_text=('Укажите ключ для страницы группы, используйте только '
                   'латиницу, цифры, дефисы и подчёркивания.'),
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Расскажите о вашей группе по подробнее',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст',
        help_text='Расскажите о чём ваш пост',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата',
        help_text='Дата публикации поста',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Автор данного поста',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Укажите группу, если такая есть',
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
    )

    def __str__(self):
        pub_date = self.pub_date.strftime('%d.%m.%Y %H:%M')
        return (
            f'Автор: {self.author.username}; '
            f'Группа: {self.group}; '
            f'Дата: {pub_date}; '
            f'Текст: {self.text[:15]}...'
        )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date', )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Оставьте комментарий',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
