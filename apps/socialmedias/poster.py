from django.contrib.auth import get_user_model

from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter


User = get_user_model()


class SocialPosting:
    def __init__(self, model, content_shared=None, company_related=None) -> None:
        self.model = model
        self.content_shared = content_shared
        self.company_related = company_related
    
    def generate_content(self):

        title = self.content_shared.title
        link = self.content_shared.slug
        description = self.content_shared.resumen
        description = self.content_shared.content
        media_url = self.content_shared.non_thumbnail_url

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