import tweepy
import random
import logging

from django.conf import settings

site = 'https://inversionesyfinanzas.xyz'

# logger = logging.getLogger('longs')

from ..models import (
    DefaultTilte,
    Emoji,
    Hashtag
)


class Twitter:
    def __init__(self) -> None:
        self.consumer_key = settings.TWITTER_CONSUMER_KEY
        self.consumer_secret = settings.TWITTER_CONSUMER_SECRET
        self.access_token = settings.TWITTER_ACCESS_TOKEN
        self.access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    def do_authenticate(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        twitter_api = tweepy.API(auth)
        return twitter_api

    def tweet_text(self, status):
        twitter_api = self.do_authenticate()
        response = twitter_api.update_status(status)
        json_response = response._json
        return json_response['id']

    def tweet_with_media(self, media_url, status):
        twitter_api = self.do_authenticate()
        post_id = twitter_api.media_upload(media_url)
        response = twitter_api.update_status(status=status, media_ids=[post_id.media_id_string])
        json_response = response._json
        return json_response['id']

    def tweet(
        self,
        caption:str, 
        num_emojis:int=1,
        post_type:int=2,
        media_url:str=None,
        link:str=None
        ):
            emojis = Emoji.objects.random_emojis(num_emojis)

            hashtags = Hashtag.objects.random_hashtags('twitter')
            hashtag1 = random.choice(hashtags)
            hashtag2 = random.choice(hashtags)
            hashtag3 = random.choice(hashtags)

            caption = f'{emojis[0].emoji}{caption} Más en {link} {hashtag1.name} {hashtag2.name} {hashtag3.name}'
                    
            if post_type == 3 or post_type == 4:
                content_type = 'text'
                post_response = self.tweet_text(caption)
            
            else:
                if post_type == 1 or post_type == 5:
                    content_type = 'video'
                    
                elif post_type == 2 or post_type == 6:
                    content_type = 'image'

                post_response = self.tweet_with_media(media_url, caption)
            

            twitter_post = {
                'post_type': post_type ,
                'social_id': post_response,
                'description': caption,
                'platform_shared': 'twitter'
            }
                
            return twitter_post