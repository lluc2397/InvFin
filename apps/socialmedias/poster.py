from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from apps.translate.google_trans_new import google_translator
from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter


User = get_user_model()
DOMAIN = Site.objects.get_current().domain


class SocialPosting:
    def __init__(self, model, content_shared=None, company_related=None) -> None:
        self.model = model
        self.content_shared = content_shared
        self.company_related = company_related
    
    def generate_content(self, post_type, model_type):

        if self.content_shared:
            content = self.content_shared
            
            media_url = content.image

            if model_type == 5:# Company
                title = content.name
                description = content.presentation
            else:
                title = content.title

            if model_type == 1:# Quesiton
                description = content.content

            else:
                description = content.resumen
        
        if self.company_related:# News
            content = self.company_related
            news = content.show_news[0]
            title = content.headline
            description = content.summary
            description = google_translator().translate(description, lang_src='en', lang_tgt='es')
            media_url = news.image

        link = content.get_absolute_url()

        if post_type == 1:# Video
            pass
        if post_type == 2:# Image
            pass
        if post_type == 3:# Text
            pass
        if post_type == 4:# Repost
            pass
        if post_type == 5:# Text and video
            pass
        if post_type == 6:# Text and image
            pass

        return title, link, description, description, media_url
    
    def share_content(self):
        fb_response = Facebook.post_on_facebook
        self.save_post(fb_response)
        tw_response = Twitter.tweet
        self.save_post(tw_response)

    def save_post(self, data:dict):
        data['user'] = User.objects.get(username = 'Lucas')
        data['content_shared'] = self.content_shared
        if self.company_related:
            data['company_related'] = self.company_related
        
        self.model.objects.create(**data)