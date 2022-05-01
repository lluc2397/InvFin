from django.contrib.auth import get_user_model

from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter


User = get_user_model()


class SocialPosting:
    def __init__(self, model, content) -> None:
        self.model = model
        self.content = content
    
    def generate_content(self):
        pass
    
    def share_content(self):
        fb_response = Facebook.post_on_facebook
        tw_response = Twitter.tweet

    def save_post(self, data:dict, company_related=None):
        data['user'] = User.objects.get(username = 'Lucas')
        if company_related:
            data['company_related'] = company_related
        
        self.model.objects.create(**data)