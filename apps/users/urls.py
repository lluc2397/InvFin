from django.urls import path

from .views import (
    UserDetailView,
    UserHistorialView,
    UserPublicProfileDetailView,
    invitation_view,
    user_update_profile,
)

app_name = "users"
urlpatterns = [
    path('invitacion/<invitation_code>', invitation_view, name="invitation"),
    path("~update/", user_update_profile, name="update"),
    path("inicio/", UserDetailView.as_view(), name="user_inicio"),
    path("perfil/<username>/", UserPublicProfileDetailView.as_view(), name="user_public_profile"),

    path("historial-perfil/<slug>", UserHistorialView.as_view(), name="user_historial"),
]
