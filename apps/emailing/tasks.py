from config import celery_app
from django.utils import timezone
from .utils import enviar_email
from apps.public_blog.models import PublicBlog, PublicBlogAsNewsletter, NewsletterFollowers

from django.contrib.auth import get_user_model
User = get_user_model()


@celery_app.task()
def enviar_email_task(newsletter, user_id):
    enviar_email(newsletter, user_id)


@celery_app.task()
def check_programmed_blog_posts_task():
    for blog_post in PublicBlog.objects.filter(status = 3):
        if blog_post.date_to_publish <= timezone.now():
            return #publicar los blogs


@celery_app.task()
def check_programmed_newsletters_task():
    for blog_newsletter in PublicBlogAsNewsletter.objects.filter(sent = False):
        if blog_newsletter.date_to_send <= timezone.now():
            return enviar_email_task.delay()


@celery_app.task()
def send_newsletter_to_followers_task(id):
    writter = User.objects.get(id = id)
    for follower in NewsletterFollowers.objects.get(user = writter):
        return enviar_email_task.delay()


@celery_app.task()
def send_website_email_task(
    newsletter
):
    for user in User.objects.all()[:2]:
        enviar_email_task.delay(newsletter, user.id)
    return 