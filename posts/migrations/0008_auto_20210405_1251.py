# Generated by Django 3.1.7 on 2021-04-05 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20210330_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, help_text='Дата публикации поста', verbose_name='Дата'),
        ),
    ]