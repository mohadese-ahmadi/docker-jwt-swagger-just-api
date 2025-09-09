from django.db import models
from django.contrib.auth.models import AbstractUser


class Author(AbstractUser):
    """مدل کاربر سفارشی با فیلد جنسیت."""

    SEX_CHOICES = [
        ("male", "MALE"),
        ("female", "FEMALE"),
    ]

    sex = models.CharField(choices=SEX_CHOICES, max_length=8)
