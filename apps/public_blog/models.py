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
from django.contrib.auth import get_user_model
User = get_user_model()

from apps.general.models import BaseEscrito, BaseComment, BaseContentShared, Newsletter, BaseEmail

class WritterProfile(Model):
    user = OneToOneField(User, on_delete=SET_NULL, null=True, related_name="writter_profile")
    created_at = DateTimeField(auto_now_add=True)
    host_name = CharField(max_length=100000, null=True, blank=True, unique=True)
    long_description = RichTextField(default='', config_name='simple')
    facebook = CharField(max_length=100000, null=True, blank=True)
    twitter = CharField(max_length=100000, null=True, blank=True)
    insta = CharField(max_length=100000, null=True, blank=True)
    youtube = CharField(max_length=100000, null=True, blank=True)
    linkedin = CharField(max_length=100000, null=True, blank=True)
    tiktok = CharField(max_length=100000, null=True, blank=True)

    class Meta:
        verbose_name = "User writter profile"
        db_table = "writter_profile"
    
    @property
    def number_of_blogs(self):
        return PublicBlog.objects.filter(author = self.user).count()


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
    content = RichTextField(config_name='simple')
    upvotes = ManyToManyField(User, blank=True, related_name="user_upvote_blog")
    downvotes = ManyToManyField(User, blank=True, related_name="user_downvote_blog")
    published_correctly = BooleanField(default=False)
    date_to_publish = DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['total_views']
        verbose_name = "Public blog post"
        db_table = "blog_post"
    
    def get_absolute_url(self):
        return reverse ('public_blog:blog_details', kwargs={"slug": self.slug})
    
    @property
    def custom_url(self):
        domain = 'inversionesyfinanzas.xyz'
        return f"https://{self.author}.{domain}/p/{self.slug}"


class PublicBlogAsNewsletter(Newsletter):
    blog_related = ForeignKey(
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


class BlogSharedHistorial(BaseContentShared):
    content_shared = ForeignKey(
        PublicBlog,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name = 'blogs_shared')

    class Meta:
        verbose_name = "Blog shared"
        db_table = "shared_blogs"


class ProfileSharedHistorial(BaseContentShared):
    content_shared = ForeignKey(
        WritterProfile,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name = 'profiles_shared')
    
    class Meta:
        verbose_name = "Proflie shared"
        db_table = "shared_profiles"


class EmailPublicBlog(BaseEmail):
    email_related = ForeignKey(PublicBlogAsNewsletter,null = True, blank=True, on_delete=SET_NULL)

    class Meta:
        verbose_name = "Email from public blog"
        db_table = "emails_public_blog"