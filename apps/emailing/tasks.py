from config import celery_app
from django.utils import timezone
from .utils import send_email
from apps.public_blog.models import PublicBlog, PublicBlogAsNewsletter



@celery_app.task()
def check_programmed_blog_posts_task():
    for blog_post in PublicBlog.objects.filter(status = 3):
        if blog_post.date_to_publish <= timezone.now():
            send_email


@celery_app.task()
def check_programmed_newsletters_task():
    for blog_newsletter in PublicBlogAsNewsletter.objects.filter(sent = False):
        if blog_newsletter.date_to_send <= timezone.now():
            send_email


@celery_app.task()
def send_newsletter_email():
    pass


@celery_app.task()
def send_notification_email():
    pass