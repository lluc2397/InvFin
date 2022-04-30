from django.contrib.auth import get_user_model

from .models import (
    DefaultTilte,
    Emoji,
    Hashtag,
    CompanySharedHistorial,
    BlogSharedHistorial,
    NewsSharedHistorial,
    TermSharedHistorial,
    ProfileSharedHistorial,
    QuestionSharedHistorial
)

from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter


User = get_user_model()


class SocialPosting:
    def __init__(self, model) -> None:
        self.model = model

    def generate_post(self):
        user = User.objects.get(username = 'Lucas')

        # platform_shared
        # social_id
        # title
        # description
        # extra_description
        # inside_information

        # content_shared
    
    def share_content(self, post_type=5):
        Facebook.post_on_facebook
        Twitter.tweet

    def save_post(self, data:dict, company_related=None):
        if company_related:
            data['company_related'] = company_related
        
        self.model.objects.create(**data)