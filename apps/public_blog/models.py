from django.db.models import (
    CharField,
    ForeignKey,
    DateTimeField,
    SET_NULL,
    Model,
    IntegerField,
    CASCADE,
    DateField,
    BooleanField,
    ManyToManyField,
    OneToOneField
)

from ckeditor.fields import RichTextField
from django.urls import reverse
from django.db.models import Avg, Sum
from django.contrib.auth import get_user_model
User = get_user_model()

from apps.general.bases import BaseEmail, BaseEscrito, BaseComment, BaseNewsletter

from .managers import PublicBlogManager

class WritterProfile(Model):
    user = OneToOneField(User, on_delete=SET_NULL, null=True, related_name="writter_profile")
    created_at = DateTimeField(auto_now_add=True)
    host_name = CharField(max_length=500, null=True, blank=True, unique=True)
    long_description = RichTextField(default='', config_name='writter')
    facebook = CharField(max_length=500, null=True, blank=True)
    twitter = CharField(max_length=500, null=True, blank=True)
    insta = CharField(max_length=500, null=True, blank=True)
    youtube = CharField(max_length=500, null=True, blank=True)
    linkedin = CharField(max_length=500, null=True, blank=True)
    tiktok = CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "User writter profile"
        db_table = "writter_profile"
    
    @property
    def all_self_blogs(self):
        return PublicBlog.objects.filter(author = self.user)
    
    @property
    def number_of_blogs(self):
        return self.all_self_blogs.count()
    
    @property
    def average_opening_rate(self):
        total = sum(item.opening_rate for item in self.all_self_blogs)
        return total if total else 0

    @property
    def total_visits(self):
        return self.all_self_blogs.aggregate(total_visits=Sum('total_views'))
    
    @property
    def total_interactions(self):
        return self.all_self_blogs.aggregate(total_interactions=Sum('total_votes'))

    @property
    def total_followers(self):
        return self.user.main_writter_followed.followers.all().count()


class FollowingHistorial(Model):
    user_following = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        related_name = 'user_following')
    user_followed = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        related_name = 'user_followed')
    started_following = BooleanField(default=False)
    stop_following = BooleanField(default=False)
    date = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Users following historial"
        db_table = "writter_followers_historial"


class NewsletterFollowers(Model):
    user = OneToOneField(
        User,
        on_delete=SET_NULL,
        null=True,
        related_name = 'main_writter_followed')
    followers = ManyToManyField(User, blank=True)
    
    class Meta:
        verbose_name = "Base de seguidores del blog"
        db_table = "writter_followers_newsletters"


class PublicBlog(BaseEscrito):
    send_as_newsletter = BooleanField(default=False)
    content = RichTextField(config_name='writter')
    upvotes = ManyToManyField(User, blank=True, related_name="user_upvote_blog")
    downvotes = ManyToManyField(User, blank=True, related_name="user_downvote_blog")
    published_correctly = BooleanField(default=False)
    date_to_publish = DateTimeField(null=True, blank=True)
    objects = PublicBlogManager()

    class Meta:
        ordering = ['total_views']
        verbose_name = "Public blog post"
        db_table = "blog_post"
    
    def get_absolute_url(self):
        return reverse ('public_blog:blog_details', kwargs={"slug": self.slug})
    
    @property
    def custom_url(self):
        return f"https://{self.author.custom_url}/p/{self.slug}"
    
    @property
    def has_newsletter(self):
        has_newsletter = False
        if self.public_blog_newsletter.exists():
            has_newsletter = True
        return has_newsletter
    
    @property
    def number_comments(self):
        number_comments = self.comments_related.all().count()
        return number_comments
    
    @property
    def opening_rate(self):
        result = 0
        if self.public_blog_newsletter.email_related.exists():
            total = self.public_blog_newsletter.email_related.all().count()
            opened = self.public_blog_newsletter.email_related.filter(opened = True).count()
            result = total/opened if opened != 0 else 0
        return result


class PublicBlogAsNewsletter(BaseNewsletter):
    blog_related = OneToOneField(
        PublicBlog,
        on_delete=SET_NULL,
        null=True,
        related_name = 'public_blog_newsletter')
    

class PublicBlogComment(BaseComment):
    content_related = ForeignKey(PublicBlog,
        on_delete=CASCADE,
        null=True,
        related_name = "comments_related")

    class Meta:
        verbose_name = "Blog's comment"
        db_table = "blog_comments"


class EmailPublicBlog(BaseEmail):
    email_related = ForeignKey(PublicBlogAsNewsletter,null = True, blank=True, on_delete=SET_NULL, related_name = 'email_related')

    class Meta:
        verbose_name = "Email from public blog"
        db_table = "emails_public_blog"