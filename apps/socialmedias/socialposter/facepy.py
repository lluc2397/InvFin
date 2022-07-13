import datetime

import requests
from django.conf import settings

from ..models import DefaultTilte, Emoji, Hashtag

# logger = logging.getLogger('longs')

INSTAGRAM_ID = settings.INSTAGRAM_ID
PROD_FACEBOOK_ACCESS_TOKEN = settings.OLD_FB_PAGE_ACCESS_TOKEN
PROD_FACEBOOK_PAGE_ID = settings.OLD_FACEBOOK_ID


class Facebook():
    def __init__(self, page_id=PROD_FACEBOOK_PAGE_ID, page_access_token=PROD_FACEBOOK_ACCESS_TOKEN) -> None:
        self.page_id = page_id
        self.facebook_page_name = 'InversionesyFinanzas'
        self.app_secret = settings.FACEBOOK_APP_SECRET
        self.long_lived_user_token = settings.FB_USER_ACCESS_TOKEN
        self.page_access_token = page_access_token
        self.facebook_url = 'https://graph.facebook.com/'
        self.facebook_video_url = "https://graph-video.facebook.com/"
        self.post_facebook_url = self.facebook_url + self.page_id
        self.post_facebook_video_url = self.facebook_video_url + self.page_id
    
    
    def get_long_live_user_token(self, app_id, user_token):
        url = f'{self.facebook_url}oauth/access_token'

        parameters = {
            'grant_type':'fb_exchange_token',
            'client_id' : app_id,
            'client_secret' : self.app_secret,
            'fb_exchange_token' : user_token
        }

        re = requests.get(url, params=parameters)

        # if re.status_code == 200:
        #     token = str(re.json()['access_token'])
        #     FB_USER_ACCESS_TOKEN
        #     return token
    

    def get_long_live_page_token(self, old=False):
        url = f'{self.facebook_url}{self.page_id}'

        parameters = {
            'fields':'access_token',
            'access_token' : self.long_lived_user_token
        }

        re = requests.get(url, params=parameters)

        # if re.status_code == 200:
        #     token = str(re.json()['access_token'])
        #     if old is False:
        #         NEW_FB_PAGE_ACCESS_TOKEN
        #     else:
        #         OLD_FB_PAGE_ACCESS_TOKEN
        #     return token

    
    def post_fb_video(self, video_url= "", description= "" , title= "", post_time=datetime.datetime.now(), post_now = False):
        """
        Post_now is False if the post has to be scheduled, True to post it now
        """
        files = {'source': open(video_url, 'rb')}
        access_token = self.page_access_token

        data = {
            'access_token': access_token,
            'title':title,
            'description': description
        }

        if post_now is False:
            data.update(
                {
                    'published' : False,
                    'scheduled_publish_time': post_time
                }
            )

        return self._send_content('video', data, files)

    
    def post_text(self, text= "", post_time=datetime.datetime.now(), post_now=True, link=None, title=''):

        if post_now is False:
            pass
        else:
            data ={
                'access_token': self.page_access_token,
                'message': text,
                'title': title
            }
        
        if link:
            data['link'] = link

        return self._send_content('text', data)



    def post_image(self, description= "", photo_url= "", title= "", post_time=datetime.datetime.now(), post_now=False):
        data ={
            'access_token': self.page_access_token,
            'url': photo_url
        }
        return self._send_content('image', data)
        

    def _send_content(self, content_type:str, content, files = None):        
        if content_type == 'video':
            re = requests.post(f'{self.post_facebook_video_url}/videos',files=files, data = content)
        elif content_type == 'text':
            re = requests.post(f'{self.post_facebook_url}/feed', data = content)
        elif content_type == 'image':
            re = requests.post(f'{self.post_facebook_url}/photos', data = content)        
        
        response = {}
        json_re = re.json()
        if re.status_code == 200:
            response['result'] = 'success'
            response['extra'] = str(json_re['id'])

        elif json_re['error']['code'] == 190:
            # logger.error(f'{json_re}, Need new user token')            
            response['result'] = 'error'
            response['where'] = 'send content facebook'
            response['message'] = 'Need new user token'

        else:
            # logger.error(f'{json_re}')
            response['result'] = 'error'
            response['where'] = 'send content facebook'
            response['message'] = f'{json_re}'
        
        return response
    

    def post_on_facebook(
        self,
        title:str,
        caption:str=None,
        num_emojis:int=1,
        post_type:int=3,
        link:str=None,
        media_url:str=None
        ):
        platform = 'facebook'
        emojis = Emoji.objects.random_emojis(num_emojis)
        hashtags = Hashtag.objects.random_hashtags(platform)
        
        custom_title = f'{emojis[0].emoji} {title}'

        utm_source = f'utm_source={platform}'
        utm_medium = f'utm_medium={platform}'
        utm_campaign = f'utm_campaign=post-shared-auto'
        utm_term = f'utm_term={title}'
        link = f'{link}?{utm_source}&{utm_medium}&{utm_campaign}&{utm_term}'

        caption = self.create_fb_description(caption=caption, link=link, hashtags=[hashtag.name for hashtag in hashtags])
        
        if post_type == 1 or post_type == 5 or post_type == 7:
            content_type = 'video'
            video_url = ''
            post_response = self.post_fb_video(video_url= video_url, description=caption, title= custom_title, post_now = True)

        elif post_type == 2 or post_type == 6:
            content_type = 'image'
            post_response = self.post_image()

        elif post_type == 3 or post_type == 4:
            content_type = 'text'
            caption = f'{caption}'

            post_response = self.post_text(text= caption, link=link, title=title)

        if post_response['result'] == 'success':
            facebook_post = {
                'post_type': post_type ,
                'social_id': post_response['extra'],
                'title': custom_title ,
                'description': caption,
                'platform_shared': platform
            }            

            return facebook_post
    

    def share_facebook_post(self, post_id, yb_title):
        default_title = DefaultTilte.objects.random_title
        url_to_share = f'https://www.facebook.com/{self.facebook_page_name}/posts/{post_id}&show_text=true'
        return self.post_on_facebook(
            post_type=4,
            default_title = default_title,
            has_default_title = True,
            caption=f'{default_title.title} {yb_title}',
            link = url_to_share)  


    def create_fb_description(self, caption:str, link:str = None, hashtags:list = None):
        hashtags = '#'.join(hashtags)
        if link:
            link = f'Más en {link}'
        else:
            link = 'Prueba las herramientas que todo inversor inteligente necesita: https://inversionesyfinanzas.xyz'
        face_description = f"""{caption}

        {link}
        
        Visita nuestras redes sociales:
        Facebook: https://www.facebook.com/InversionesyFinanzas/
        Instagram: https://www.instagram.com/inversiones.finanzas/
        TikTok: https://www.tiktok.com/@inversionesyfinanzas?
        Twitter : https://twitter.com/InvFinz
        LinkedIn : https://www.linkedin.com/company/inversiones-finanzas
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
        return face_description




            




