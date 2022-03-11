from django.urls import path

from .views import (
    PublicBlogDetailsView,
    PublicBlogsListView,
    user_become_writter_view,
    CreatePublicBlogPostView,
    UpdatePublicBlogPostView,
    following_management_view,
    WritterOwnBlogsListView
)

app_name = "public_blog"
urlpatterns = [
    
    path('blog-financiero/', PublicBlogsListView.as_view(), name="blog_list"),
    path('p/<slug>/', PublicBlogDetailsView.as_view(), name="blog_details"),

    path('management/escritos/<slug>/', WritterOwnBlogsListView.as_view(), name="manage_blogs"),

    path('create-blog', CreatePublicBlogPostView.as_view(), name="create_blog"),
    path('update-blog/<id>', UpdatePublicBlogPostView.as_view(), name="update_blog"),

    path('become-writter', user_become_writter_view, name="user_become_writter"),
    path('start-following-writter', following_management_view, name="following_management_view"),
    
]