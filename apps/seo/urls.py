from django.urls import path

from .views import (
    redirect_old_urls
)

app_name = "seo"
urlpatterns = [
    path('question/<ques_slug>/', redirect_old_urls, name="question_redirect"),
    path('definicion/<term_slug>/', redirect_old_urls, name="terms_redirect"),
    path('publicaciones/<publs_slug>/', redirect_old_urls, name="publs_redirect"),
    
]