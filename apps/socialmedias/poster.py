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
    
    def generate_content(self, model_type):

        if self.content_shared:
            content = self.content_shared

            if content.__class__._meta == 'preguntas_respuestas.question':# Quesiton
                description = content.content
                media_url = None
            
            else:
                description = content.resume
            
                media_url = content.image

            if content.__class__._meta == 'empresas.company':# Company
                title = content.name
                description = content.presentation
            else:
                title = content.title

            
        
        if self.company_related:# News
            content = self.company_related
            news = content.show_news[0]
            title = content.headline
            description = content.summary
            description = google_translator().translate(description, lang_src='en', lang_tgt='es')
            media_url = news.image

        link = content.get_absolute_url()

        # if post_type == 1:# Video
        #     pass
        # if post_type == 2:# Image
        #     pass
        # if post_type == 3:# Text
        #     pass
        # if post_type == 4:# Repost
        #     pass
        # if post_type == 5:# Text and video
        #     pass
        # if post_type == 6:# Text and image
        #     pass

        return title, link, description, media_url
    
    def share_content(self, post_type):
        title, link, description, media_url = self.generate_content()
        fb_response = Facebook.post_on_facebook(title=title, caption=description, post_type=3, link=link)
        self.save_post(fb_response)
        tw_response = Twitter.tweet(caption=description, post_type=post_type, media_url=media_url, link=link)
        self.save_post(tw_response)

    def save_post(self, data:dict):
        data['user'] = User.objects.get(username = 'Lucas')
        
        if self.company_related:
            data['company_related'] = self.company_related
        else:
            data['content_shared'] = self.content_shared
        
        self.model.objects.create(**data)