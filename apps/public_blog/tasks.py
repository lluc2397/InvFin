from config import celery_app

from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.public_blog.models import PublicBlog, PublicBlogAsNewsletter, NewsletterFollowers
from apps.general.tasks import enviar_email_task

User = get_user_model()


@celery_app.task()
def check_programmed_blog_posts_task():
    for blog_post in PublicBlog.objects.filter(status = 3):
        if blog_post.date_to_publish <= timezone.now():
            return #publicar los blogs


@celery_app.task()
def send_newsletter_to_followers_task(writter_id, newsletter):
    writter = User.objects.get(id = writter_id)
    for follower in NewsletterFollowers.objects.get(user = writter):
        enviar_email_task.delay(newsletter, follower.id, 'news')