from django.urls import path

from .views import (
    CreateQuestionView,
    QuestionDetailsView,
    QuestionsView,
    UpdateQuestionView,
    accept_answer,
    create_answer_view,
)

app_name = "preguntas_respuestas"
urlpatterns = [
    path('preguntas/', QuestionsView.as_view(), name="list_questions"),

    path('acceptar-answer/<question_id>/<answer_id>', accept_answer, name="is_accepted"),

    path('question/<slug>/', QuestionDetailsView.as_view(), name="question"),

    path('create-question', CreateQuestionView.as_view(), name="create_question"),
    path('update/<slug>/', UpdateQuestionView.as_view(), name="update_question"),

    path('create-answer/<slug>', create_answer_view, name="create_answer"),

    # path('', CreateQuestionView.as_view(), name="update_question"),

    # path('', CreateQuestionView.as_view(), name="delete_question"),
]