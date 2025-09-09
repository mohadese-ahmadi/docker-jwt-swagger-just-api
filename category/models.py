from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name="Category name")
    description = models.TextField(verbose_name="Description")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title
