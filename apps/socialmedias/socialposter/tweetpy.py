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

TWITTER_CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET
TWITTER_ACCESS_TOKEN = settings.TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET = settings.TWITTER_ACCESS_TOKEN_SECRET


class Twitter:
    def __init__(self):
        self.consumer_key = TWITTER_CONSUMER_KEY
        self.consumer_secret = TWITTER_CONSUMER_SECRET
        self.access_token = TWITTER_ACCESS_TOKEN
        self.access_token_secret = TWITTER_ACCESS_TOKEN_SECRET
    

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
        local_content = None,
        caption= "", 
        hashtags=Hashtag.objects.random_tw_hashtags,
        has_default_title = True,
        default_title = DefaultTilte.objects.random_title,
        num_emojis = 1,
        post_type=2,
        is_original = False,
        content_url='',
        ):
            emojis = Emoji.objects.random_emojis(num_emojis)

            hashtag1 = random.choice(hashtags)
            hashtag2 = random.choice(hashtags)
            hashtag3 = random.choice(hashtags)

            hashtags_used = [hashtag1, hashtag2, hashtag3]

            if caption == '' and has_default_title is True:
                default_caption = f'{emojis[0].emoji}{default_title}'
                caption = f'{default_caption} #{hashtag1.name} #{hashtag2.name} #{hashtag3.name}'
                if len(caption) > 280:
                    hashtags_used = [hashtag1]
                    caption = f'{default_caption} #{hashtag1.name}'
                    
            if post_type == 3 or post_type == 4:
                content_type = 'text'
                post_response = self.tweet_text(caption)
            
            else:
                if post_type == 1 or post_type == 5:
                    content_type = 'video'
                    media_url = local_content.local_vertical_short_path
                    
                elif post_type == 2 or post_type == 6:
                    content_type = 'image'
                    media_url =  local_content.local_resized_image_path

                post_response = self.tweet_with_media(media_url, caption)
            
            if post_response['result'] == 'success':
                twitter_post = TwitterPostRecord.general_manager.save_record(
                    local_content = local_content,
                    post_type = post_type ,
                    is_original = is_original ,
                    social_id = post_response['extra'],
                    emojis = emojis ,
                    hashtags = hashtags_used ,
                    has_default_title = has_default_title,
                    default_title = default_title,
                    caption = caption
                )

            return post_response