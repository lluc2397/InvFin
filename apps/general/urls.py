from django.urls import path

from .views import (
    create_comment_view,
    create_vote_view,
    EscritosView,
    suggest_list_search,
    search_results,
    update_favorites,
    coming_soon,
    email_opened_view
)

app_name = "general"
urlpatterns = [

    path('create-comment/<url_encoded>', create_comment_view, name="create_comment_view"),

    path('create-vote/<url_encoded>', create_vote_view, name="create_vote_view"),

    path('escritos-financieros/', EscritosView.as_view(), name="escritos"),

    path('suggestions-buscador/', suggest_list_search, name="searcher_suggestions"),
    path('buscador/', search_results, name="searcher"),

    path('update-favs/', update_favorites, name="update_favorites"),

    path('coming-soon/', coming_soon, name="coming_soon"),

    path('email-image/<uidb64>', email_opened_view, name='email_opened_view'),
]