from rest_framework import routers

from genres_polls import views as genres_polls_views

router = routers.DefaultRouter()
router.register(r'questions', genres_polls_views.GenresPollsQuestionViewSet, basename='genres_polls_questions')
