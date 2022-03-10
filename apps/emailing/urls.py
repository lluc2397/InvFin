from django.urls import path
from .views import (
    email_opened_view
)

app_name = "emailing"
urlpatterns = [
    path('email-image/<uidb64>', email_opened_view, name='email_opened_view'),
]