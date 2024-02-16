from django.db import models
from django.contrib.auth import get_user_model

class Discount(models.Model):
    label = models.CharField(max_length=100, verbose_name="عنوان تخفیف")
    price = models.PositiveIntegerField(verbose_name="مبلغ تخفیف")

    def __str__(self):
        return self.label


class Genre(models.Model):
    label = models.CharField(max_length=255, unique=True, verbose_name="عنوان ژانر")

    def __str__(self):
        return self.label


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان کتاب")
    author = models.CharField(max_length=100, verbose_name="نویسنده")
    genre = models.ManyToManyField(
        to=Genre, related_name="genre_books", verbose_name="ژانر"
    )
    translator = models.CharField(max_length=100, verbose_name="مترجم", blank=True)
    publisher = models.CharField(max_length=100, verbose_name="انتشارات", blank=True)
    price = models.IntegerField(verbose_name="قیمت")
    description = models.TextField(verbose_name="جزئیات کتاب")
    cover = models.ImageField(
        upload_to="covers/", verbose_name="تصویر کتاب", blank=True
    )
    datetime_created = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ایجاد کتاب"
    )
    datetime_modified = models.DateTimeField(
        auto_now=True, verbose_name="زمان تغییر کتاب"
    )
    discount = models.ForeignKey(
        to=Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="discount_books",
        verbose_name="تخفیف",
    )
    star = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.author}: {self.title}"


class Favorite(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="user_favorite",
        verbose_name="نام کاربر",
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name="book_favorite",
        verbose_name="نام کتاب",
    )
    class Meta:
        unique_together = (("user", "book"),)


class Comment(models.Model):
    STAR_CHOICES = (
        (1, "😣"),
        (2, "😔"),
        (3, "😐"),
        (4, "😄"),
        (5, "😍"),
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="user_comments",
        verbose_name="کاربر",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="book_comments",
        verbose_name="نام کتاب",
    )
    text = models.TextField(verbose_name='متن پیام')
    datetime_created = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ایجاد"
    )
    datetime_modified = models.DateTimeField(
        auto_now=True, verbose_name="آخرین زمان تغییر"
    )
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    star = models.IntegerField(choices=STAR_CHOICES, default=3)

    def __str__(self):
        return f"{self.user}: {self.text}"


class Order(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="کاربر",
        related_name="user_orders",
    )
    address = models.TextField(verbose_name="آدرس")
    datetime_created = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ایجاد"
    )
    datetime_modified = models.DateTimeField(
        auto_now=True, verbose_name="آخرین زمان تغییر"
    )
    is_paid = models.BooleanField(default=False)
    pay_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        verbose_name="فاکتور",
        related_name="order_orderItems",
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        verbose_name="کتاب",
        related_name="book_orderItems",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ")
    pay_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="مبلغ پرداخت شده"
    )
    count = models.PositiveSmallIntegerField(default=1, verbose_name="تعداد")
    discount = models.ForeignKey(
        to=Discount,
        on_delete=models.CASCADE,
        related_name="discount_orderItems",
        verbose_name="تخفیف",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.book.title


class Weblog(models.Model):
    image = models.ImageField(
        upload_to="weblog/", verbose_name="تصویر بلاگ", blank=True
    )
    title = models.CharField(max_length=100, verbose_name="عنوان بلاگ")
    text = models.TextField(verbose_name="جزئیات بلاگ")
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="نویسنده",
        related_name="user_weblogs",
    )
    datetime_created = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ایجاد بلاگ"
    )
    datetime_modified = models.DateTimeField(
        auto_now=True, verbose_name="زمان تغییر بلاگ"
    )

    def __str__(self):
        return self.title

class Subscriber(models.Model):
    email = models.EmailField(max_length=254)
