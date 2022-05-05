from django.urls import path

from .views import RetreiveUserCarteraAPIView


app_name = "carteraAPI"
urlpatterns = [
    path('get/user/cartera', RetreiveUserCarteraAPIView.as_view(), name='cartera_inicio'),
]