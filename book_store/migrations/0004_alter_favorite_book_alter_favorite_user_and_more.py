# Generated by Django 5.0 on 2024-02-13 14:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store', '0003_alter_favorite_book_alter_favorite_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_favorite', to='book_store.book', verbose_name='نام کتاب'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite', to=settings.AUTH_USER_MODEL, verbose_name='نام کاربر'),
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'book')},
        ),
    ]
