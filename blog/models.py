from django.db import models
from django.urls import reverse
from category.models import Category
from account.models import Author
from tag.models import Tags


class Blogs(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.CharField(
        max_length=400, default="something", verbose_name="Short description"
    )
    context = models.TextField(verbose_name="Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="blogs")
    tag = models.ManyToManyField(Tags, related_name="blogstag")
    category = models.ForeignKey(
        Category,
        related_name="blogscat",
        null=True,
        on_delete=models.CASCADE,
    )
    image_file = models.ImageField(
        upload_to="product_images/",
        verbose_name="Image",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", args=[self.pk])
