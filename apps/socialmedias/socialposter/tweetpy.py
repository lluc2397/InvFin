import tweepy
import random
import logging
import math
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
    
    def create_thread(self, title, media_url, caption, tweet_len, hashtags):
        post_type = 8 # Thread
        twitter_api = self.do_authenticate()
        parts = int(math.ceil(tweet_len / 186))
        hashtag1 = random.choice(hashtags)
        hashtag2 = random.choice(hashtags)
        hashtag3 = random.choice(hashtags)
        list_tweets = []

        for part in range(parts + 1):
            pagination = f'[{part}/{parts}]'
            if part == 0:
                text_part = f"""
                {media_url} {title} {pagination} #{hashtag1.name} #{hashtag2.name} #{hashtag3.name}
                """
                response = twitter_api.update_status(text_part)
                twitter_post = {
                    'post_type': post_type ,
                    'social_id': response.id,
                    'description': text_part,
                    'platform_shared': 'twitter'
                }
                list_tweets.append(twitter_post)
                continue
            if part == 1:
                current_position = 0
            else:
                current_position = 177*part
            last_position = current_position + 177
            extra = f'... {pagination}'
            if part == parts:
                last_position = current_position + 186
                extra = f'{pagination}'
            
            text_part = caption[current_position: last_position]+extra

            response = twitter_api.update_status(status=text_part, 
                                        in_reply_to_status_id=response.id, 
                                        auto_populate_reply_metadata=True)
            twitter_post = {
                'post_type': post_type ,
                'social_id': response.id,
                'description': text_part,
                'platform_shared': 'twitter'
            }
            list_tweets.append(twitter_post)
        
        return list_tweets

    def tweet(
        self,
        caption:str, 
        num_emojis:int=1,
        post_type:int=2,
        media_url:str=None,
        link:str=None,
        title:str=None,
        ):
            emojis = Emoji.objects.random_emojis(num_emojis)

            hashtags = Hashtag.objects.random_hashtags('twitter')
            hashtag1 = random.choice(hashtags)
            hashtag2 = random.choice(hashtags)
            hashtag3 = random.choice(hashtags)

            tweet = f'{media_url} {emojis[0].emoji} {caption} Más en {link} #{hashtag1.name} #{hashtag2.name} #{hashtag3.name}'
                    
            if post_type == 3 or post_type == 4:
                tweet_len = len(tweet)
                if tweet_len > 186:
                    post_response = self.create_thread(title, media_url, caption, tweet_len, hashtags)
                else:
                    post_response = self.tweet_text(tweet)
            
            else:
                if post_type == 1 or post_type == 5:
                    content_type = 'video'
                    
                elif post_type == 2 or post_type == 6:
                    content_type = 'image'

                post_response = self.tweet_with_media(media_url, caption)
            
            #Create the posibility of returning a list with all the posts in case of a thread
            if type(post_response) == list:
                twitter_post = {
                    'multiple_posts': True,
                    'posts': post_response
                }
            else:
                twitter_post = {
                    'post_type': post_type ,
                    'social_id': post_response,
                    'description': caption,
                    'platform_shared': 'twitter'
                }
                
            return twitter_post