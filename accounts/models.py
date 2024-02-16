from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GENDER_CHOICES = {
        ("M", "مرد"),
        ("F", "زن"),
    }
    phone_number = models.CharField(
        max_length=14, blank=True, null=True, unique=True, verbose_name="شماره تماس"
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name="جنسیت"
    )
    profile_picture = models.ImageField(
        upload_to="profiles/", blank=True, verbose_name="عکس پروفایل"
    )
