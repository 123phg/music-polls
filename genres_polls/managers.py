from django.db import models


class QuestionManager(models.Manager):
    def actual_for_user(self, user):
        return self.filter(
            user=user,
            selected_answer=None
        )
