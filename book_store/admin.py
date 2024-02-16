from django.contrib import admin
from .models import (
    Discount,
    Genre,
    Book,
    Favorite,
    Comment,
    Order,
    OrderItem,
    Weblog,
    Subscriber,
)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "label",
        "price",
    ]
    list_display_links = [
        "id",
        "label",
        "price",
    ]
    ordering = ["-id"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "label",
    ]
    list_display_links = [
        "id",
        "label",
    ]
    ordering = ["-id"]


@admin.register(Book)
class GenreAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "author",
        "translator",
        "publisher",
        "price",
        "datetime_created",
        "datetime_modified",
    ]
    list_display_links = [
        "id",
        "title",
        "author",
        "translator",
        "publisher",
        "price",
        "datetime_created",
        "datetime_modified",
    ]
    ordering = ["-id"]


@admin.register(Favorite)
class GenreAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "book",
    ]
    list_display_links = [
        "id",
        "user",
        "book",
    ]
    ordering = ["-id"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "book",
        "is_active",
        "datetime_created",
        "datetime_modified",
    ]
    list_display_links = [
        "id",
        "user",
        "book",
        "is_active",
        "datetime_created",
        "datetime_modified",
    ]
    ordering = ["-id"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "address",
        "pay_price",
        "is_paid",
        "datetime_created",
        "datetime_modified",
    ]
    list_display_links = [
        "id",
        "user",
        "address",
        "pay_price",
        "is_paid",
        "datetime_created",
        "datetime_modified",
    ]
    ordering = ["-id"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order",
        "book",
        "price",
        "pay_price",
        "count",
    ]
    list_display_links = [
        "id",
        "order",
        "book",
        "price",
        "pay_price",
        "count",
    ]
    ordering = ["-id"]


@admin.register(Weblog)
class WeblogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "author",
        "datetime_created",
        "datetime_modified",
    ]
    list_display_links = [
        "id",
        "title",
        "author",
        "datetime_created",
        "datetime_modified",
    ]
    ordering = ["-id"]

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
    ]
    list_display_links = [
        "id",
        "email",
    ]
    ordering = ["-id"]
 