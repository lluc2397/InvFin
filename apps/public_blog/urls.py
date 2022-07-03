from django.urls import path

from .views import (
    PublicBlogDetailsView,
    PublicBlogsListView,
    UpdateBlogNewsletterView,
    user_become_writter_view,
    CreatePublicBlogPostView,
    UpdatePublicBlogPostView,
    following_management_view,
    WritterOwnBlogsListView,
    create_newsletter_for_blog,
    UpdateBlogNewsletterView
)

app_name = "public_blog"

subdomains_urls = [
    path('p/<slug>/', PublicBlogDetailsView.as_view(), name="blog_details"),
    path('management/escritos/<slug>/', WritterOwnBlogsListView.as_view(), name="manage_blogs"),
    path('create-newsletter-blog/<slug>', create_newsletter_for_blog, name="create_newsletter_blog"),
    path('update-newsletter-blog/<pk>', UpdateBlogNewsletterView.as_view(), name="update_newsletter_blog"),
    path('create-blog', CreatePublicBlogPostView.as_view(), name="create_blog"),
    path('update-blog/<pk>', UpdatePublicBlogPostView.as_view(), name="update_blog"),
]

urlpatterns = [
    path('blog-financiero/', PublicBlogsListView.as_view(), name="blog_list"),
    path('become-writter', user_become_writter_view, name="user_become_writter"),
    path('start-following-writter', following_management_view, name="following_management_view"),
    
] + subdomains_urls