import requests
import time
import logging
import sys

from django.conf import settings

import cloudinary.uploader

from ..constants import INSTAGRAM_GRAPH_URL, FACEBOOK_GRAPH_URL

# logger = logging.getLogger('longs')


class Instagram():
    ig_account_id = settings.INSTAGRAM_ID
    page_access_token = settings.OLD_FB_PAGE_ACCESS_TOKEN
    user_access_token = settings.FB_USER_ACCESS_TOKEN
    main_instagram_url = INSTAGRAM_GRAPH_URL
    main_facebook_url = FACEBOOK_GRAPH_URL

    def __init__(self):
        self.ig_access_token_url = f'access_token={self.page_access_token}'    
        self.instagram_url = f'{self.main_facebook_url}{self.ig_account_id}/'

    def get_ig_access_token(self, app_id):
        url = f'{self.main_instagram_url}access_token'
        parameters = {
            'grant_type': 'ig_exchange_token',
            'client_secret': app_id,
            'access_token': self.user_access_token
        }
        re = requests.get(url, params=parameters)
        if re.status_code == 200:
            access_token = re.json()['access_token']

    def refresh_long_live_user_token(self):
        url = f'{self.main_instagram_url}refresh_access_token'
        parameters = {
            'grant_type': 'ig_refresh_token',
            'access_token': self.user_access_token
        }
        re = requests.get(url, params=parameters)
        if re.status_code == 200:
            access_token = re.json()['access_token']

    def get_quota(self):
        extra = 'fields=config,quota_usage'
        cuota = requests.get(f'{self.instagram_url}content_publishing_limit?{extra}\
        &{self.ig_access_token_url}').json()
        return cuota['data'][0]

    def check_post_status(self, post_id):
        extra = 'fields=status_code,status'
        status_url = f'{self.main_facebook_url}{post_id}?{extra}&{self.ig_access_token_url}'
        response = requests.get(status_url)
        return response.json()    

    def _upload_to_cloudinary(self, content_url, resource_type):
        uploaded_content = cloudinary.uploader.upload(content_url,resource_type = resource_type)
        content_url = uploaded_content['secure_url']
        cloudinary_asset_id = uploaded_content['public_id']
        return {
            'content_url':content_url,
            'asset_id': cloudinary_asset_id
        }
    
    def _send_content_to_instagram(self, caption, content_url, resource_type, send_from):        
        if send_from == 'cloudinary':
            upload_response = self._upload_to_cloudinary(content_url, resource_type)

        if resource_type == "video":

            data = {
                'media_type':"VIDEO",
                'video_url': upload_response['content_url'],
                'caption': caption,
                'access_token': self.page_access_token
            }

        else:
            data = {
                'image_url': upload_response['content_url'],
                'caption': caption,
                'access_token': self.page_access_token
            }
        
        try:
            pre_post = requests.post(f'{self.instagram_url}media', data = data)

            pre_post_data = {
                'instagram_pre_published_id': pre_post.json()['id'],
                'uploaded_asset_id': upload_response['asset_id'],
                'resource_type': resource_type,
                'content_url': upload_response['content_url'],
                'caption':caption
            }

            response = {
                'result':'success',
                'extra': pre_post_data
            }
        
        except Exception as e:
            # logger.exception(f'Error while publishing sending content to instagram {e}')
            response = {
                'result':'error',
                'where':'instagram sending post',
                'message': e
            }
        return response
    
    def _publish_uploaded_content(self, content_pre_published_data):
        try:
            post_id = content_pre_published_data['instagram_pre_published_id']

            status = self.check_post_status(post_id)

            post_url = f'{self.instagram_url}media_publish?{self.ig_access_token_url}&creation_id='

            if status['status_code'] == 'FINISHED':
                requests.post(f'{post_url}{post_id}')

                time.sleep(10)
                return self._publish_uploaded_content(content_pre_published_data)

            elif status['status_code'] == 'PUBLISHED':
                response = {
                    'result':'success',
                    'extra':content_pre_published_data
                }
            
            elif status['status_code'] == 'IN_PROGRESS':
                time.sleep(10)
                return self._publish_uploaded_content(content_pre_published_data)
            
            elif status['status_code'] == 'EXPIRED':
                # logger.error(f'Error while publishing uploaded content to instagram{status}')
                response = {
                    'result':'error',
                    'where':'status expired',
                    'message': status,
                    'extra': content_pre_published_data
                }

            elif status['status_code'] == 'ERROR':
                # logger.error(f'Error while publishing uploaded content to instagram{status}')
                response = {
                    'result':'error',
                    'where':'status error',
                    'message': status,
                    'extra': content_pre_published_data
                }

        except Exception as e:
            # logger.exception('Error while publishing uploaded content to instagram')
            response = {
                'result':'error',
                'where':'instagram post publishing',
                'message':f'{e}'
            }
    
        return response
        
    def post_on_instagram(
        self,
        caption,
        local_content,
        post_type,
        send_from = 'cloudinary',
        is_original = False,
        destroy_asset = True,
        **kwargs
        ):
            """
            send_from indicates the location, default is cloudinary
            destroy_asset eliminates the previous uploaded    
            """
            emojis = Emoji.objects.random_emojis(num_emojis)

            if custom_title == '' and has_default_title is True:
                custom_title = f'{emojis[0].emoji}{default_title}'

            if local_content is not None:
                resource_type = "image"
                content_url = local_content.local_resized_image_path
                if post_type == 1:
                    content_url = local_content.local_vertical_short_path
                    resource_type = "video"

            if caption == '':
                caption = self.create_ig_caption(custom_title, ' #'.join([hashtag.name for hashtag in hashtags]))

            content_pre_published_data = self._send_content_to_instagram(caption, content_url, resource_type=resource_type, send_from=send_from)
            
            if content_pre_published_data['result'] == 'error':
                sys.exit()
            
            instagram_post_result = self._publish_uploaded_content(content_pre_published_data['extra'])
            
            if instagram_post_result['result'] == 'error':
                sys.exit()
            
            instagram_post = InstagramPostRecord.general_manager.save_record(
                local_content = local_content ,
                post_type = post_type ,
                is_original = is_original ,
                social_id = instagram_post_result['extra']['instagram_pre_published_id'] ,
                emojis = emojis ,
                hashtags = hashtags ,
                has_default_title = has_default_title ,
                default_title = default_title ,
                custom_title = custom_title ,
                caption = caption
            )

            if destroy_asset is True:
                if send_from == 'cloudinary':
                    cloudinary.uploader.destroy(
                        instagram_post_result['extra']['uploaded_asset_id'],
                        resource_type = instagram_post_result['extra']['resource_type'])
                
            return instagram_post_result
    
    def get_media_info(self, media_id):
        url = f'{self.main_instagram_url}/{media_id}'
        params = {
            'fields':'media_url',
            'access_token':self.user_access_token
        }
        response = requests.get(url, params = params)
        return response.json()
    
    def create_ig_caption(self, title, hashtags):        
        instagram_caption = f"""
        {title}
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        {hashtags}
        """
        return instagram_caption