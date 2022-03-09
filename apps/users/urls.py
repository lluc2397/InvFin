from django.urls import path

from .views import (
    UserDetailView,
    user_update_profile,
    UserRedirectView,
    UserPublicProfileDetailView
)

app_name = "users"
urlpatterns = [
    path("~redirect/", UserRedirectView.as_view(), name="redirect"),
    path("~update/", user_update_profile, name="update"),
    path("inicio/", UserDetailView.as_view(), name="user_inicio"),
    path("perfil/<username>", UserPublicProfileDetailView.as_view(), name="user_public_profile"),
]
