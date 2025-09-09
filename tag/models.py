from django.db import models


class Tags(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tag name")
    description = models.TextField(verbose_name="Description")

    class Meta:
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.title