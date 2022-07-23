from django.urls import path

from .views import (
    NotificationsListView,
    coming_soon,
    create_comment_view,
    create_vote_view,
    delete_notification,
    email_opened_view,
    search_results,
    suggest_list_search,
    update_favorites,
    MessagesTemplateview
)

app_name = "general"
urlpatterns = [

    path('create-comment/<url_encoded>', create_comment_view, name="create_comment_view"),
    path('create-vote/<url_encoded>', create_vote_view, name="create_vote_view"),
    path('suggestions-buscador/', suggest_list_search, name="searcher_suggestions"),
    path('buscador/', search_results, name="searcher"),
    path('update-favs/', update_favorites, name="update_favorites"),
    path('coming-soon/', coming_soon, name="coming_soon"),
    path('email-image/<uidb64>', email_opened_view, name='email_opened_view'),
    path('tus-notificaciones/', NotificationsListView.as_view(), name="notifications_list"),
    path('delete-notif/<notif_id>', delete_notification, name="notification_delete"),
    path('return-nav-messages', MessagesTemplateview.as_view(), name="nav_messages"),
]