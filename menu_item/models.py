from django.db import models


class MenuItem(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    url = models.CharField(
        max_length=300,
        verbose_name="Link",
        help_text="نام url",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordering")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return self.title
