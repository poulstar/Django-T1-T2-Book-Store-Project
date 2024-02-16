# Generated by Django 5.0 on 2024-02-10 12:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان کتاب')),
                ('author', models.CharField(max_length=100, verbose_name='نویسنده')),
                ('translator', models.CharField(blank=True, max_length=100, verbose_name='مترجم')),
                ('publisher', models.CharField(blank=True, max_length=100, verbose_name='انتشارات')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('description', models.TextField(verbose_name='جزئیات کتاب')),
                ('cover', models.ImageField(blank=True, upload_to='covers/', verbose_name='تصویر کتاب')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد کتاب')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='زمان تغییر کتاب')),
                ('star', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, verbose_name='عنوان تخفیف')),
                ('price', models.PositiveIntegerField(verbose_name='مبلغ تخفیف')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, unique=True, verbose_name='عنوان ژانر')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن پیام')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='آخرین زمان تغییر')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال')),
                ('star', models.IntegerField(choices=[(1, '😣'), (2, '😔'), (3, '😐'), (4, '😄'), (5, '😍')], default=3)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_comments', to='book_store.book', verbose_name='نام کتاب')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='discount_books', to='book_store.discount', verbose_name='تخفیف'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_favorite', to='book_store.book', verbose_name='نام کتاب')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite', to=settings.AUTH_USER_MODEL, verbose_name='نام کاربر')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(related_name='genre_books', to='book_store.genre', verbose_name='ژانر'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='آخرین زمان تغییر')),
                ('is_paid', models.BooleanField(default=False)),
                ('pay_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='مبلغ')),
                ('pay_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='مبلغ پرداخت شده')),
                ('count', models.PositiveSmallIntegerField(default=1, verbose_name='تعداد')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_orderItems', to='book_store.book', verbose_name='کتاب')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discount_orderItems', to='book_store.discount', verbose_name='تخفیف')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_orderItems', to='book_store.order', verbose_name='فاکتور')),
            ],
        ),
        migrations.CreateModel(
            name='Weblog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='weblog/', verbose_name='تصویر بلاگ')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان بلاگ')),
                ('text', models.TextField(verbose_name='جزئیات بلاگ')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد بلاگ')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='زمان تغییر بلاگ')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_weblogs', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
            ],
        ),
    ]