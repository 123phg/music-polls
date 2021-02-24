from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Question(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    question_image_url = models.URLField(
        max_length=512
    )
    options = ArrayField(
        base_field=models.CharField(
            max_length=128,
            null=False,
            blank=False
        )
    )
    correct_answer = models.CharField(
        max_length=128,
    )
    selected_answer = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
