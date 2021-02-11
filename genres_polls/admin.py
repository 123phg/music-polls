from django.contrib import admin
from genres_polls import models


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'options',
        'correct_answer',
        'selected_answer',
        'created_at',
        'updated_at'
    ]
    list_display_links = ['user']
