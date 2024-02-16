from django import forms
from .models import Comment, Order, Weblog, Subscriber
from django.contrib.auth import get_user_model


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "text",
            "star",
        ]


class OrderForm(forms.ModelForm):
    address = forms.CharField(
        label="آدرس",
        required=True,
        min_length=4,
        max_length=1000,
        error_messages={
            "required": "آدرس خود را وارد کنید",
            "min_length": "آدرس شما نمی تواند کمتر از 4 کاراکتر باشد",
            "max_length": "آدرس شما نمی تواند بیشتر از 1000 کاراکتر باشد",
        },
    )

    class Meta:
        model = Order
        fields = [
            "address",
        ]


class WeblogForm(forms.ModelForm):
    title = forms.CharField(
        label="عنوان مقاله",
        required=True,
        min_length=4,
        max_length=100,
        error_messages={
            "required": "عنوان خود را وارد کنید",
            "min_length": "عنوان شما نمی تواند کمتر از 4 کاراکتر باشد",
            "max_length": "عنوان شما نمی تواند بیشتر از 100 کاراکتر باشد",
        },
    )
    text = forms.Textarea()
    image = forms.ImageField(
        label="تصویر مقاله",
        required=True,
        error_messages={
            "required": "تصویر مقاله خود را وارد کنید",
            "invalid_image": "فایل ارسال شده یک تصویر نیست",
        },
    )

    class Meta:
        model = Weblog
        fields = [
            "title",
            "text",
            "image",
        ]
        error_messages = {
            "text": {
                "required": "متن خود را وارد کنید",
            },
        }


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = [
            "email",
        ]


class ProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "gender",
            "profile_picture",
        ]
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "email": "پست الکترونیک",
            "phone_number": "شماره تماس",
            "gender": "جنسیت",
            "profile_picture": "آواتار",
        }
