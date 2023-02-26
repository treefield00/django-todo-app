from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Task(models.Model):
    title = models.CharField("タイトル", max_length=30)
    description = models.TextField("説明", blank=True)
    deadline = models.DateField("締切日")
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self) -> str:
        return self.title