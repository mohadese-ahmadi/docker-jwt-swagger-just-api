from django.db import models
from account.models import Author
from blog.models import Blogs

class Comment(models.Model):
    post = models.ForeignKey(
        Blogs, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"

    @property
    def children(self):
        return self.replies.all()

    def is_parent(self):
        return self.parent is None