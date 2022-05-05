from django.contrib.auth import get_user_model

from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter


User = get_user_model()


class SocialPosting:
    def __init__(self, model, content_shared=None, company_related=None) -> None:
        self.model = model
        self.content_shared = content_shared
        self.company_related = company_related
    
    def generate_content(self, post_type):

        if self.content_shared:
            content = self.content_shared
            
        if self.company_related:
            content = self.company_related

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

        title = content.title
        link = content.slug
        description = content.resumen
        description = content.content
        

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