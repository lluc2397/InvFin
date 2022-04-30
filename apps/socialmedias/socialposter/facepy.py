from numpy import random
import requests
import sys
import logging
import datetime

from django.conf import settings

from ..models import (
    DefaultTilte,
    Emoji,
    Hashtag
)

# logger = logging.getLogger('longs')

OLD_FB_PAGE_ACCESS_TOKEN = settings.OLD_FB_PAGE_ACCESS_TOKEN
NEW_FB_PAGE_ACCESS_TOKEN = settings.NEW_FB_PAGE_ACCESS_TOKEN
FACEBOOK_APP_SECRET = settings.FACEBOOK_APP_SECRET
OLD_FACEBOOK_ID = settings.OLD_FACEBOOK_ID
NEW_FACEBOOK_ID = settings.NEW_FACEBOOK_ID
INSTAGRAM_ID = settings.INSTAGRAM_ID
FB_USER_ACCESS_TOKEN = settings.FB_USER_ACCESS_TOKEN


class Facebook():
    def __init__(
        self, 
        user_token=FB_USER_ACCESS_TOKEN, 
        app_id = '',
        facebook_page_name = 'InversionesyFinanzas',
        app_secret=FACEBOOK_APP_SECRET, 
        long_lived_user_token=FB_USER_ACCESS_TOKEN, 
        page_access_token=NEW_FB_PAGE_ACCESS_TOKEN, 
        page_id=''):

        self.page_id = page_id
        self.facebook_page_name = facebook_page_name
        self.user_token = user_token
        self.app_id = app_id
        self.app_secret = app_secret
        self.long_lived_user_token = long_lived_user_token
        self.page_access_token = page_access_token
        self.facebook_url = 'https://graph.facebook.com/'
        self.facebook_video_url = "https://graph-video.facebook.com/"
        self.post_facebook_url = self.facebook_url + self.page_id
        self.post_facebook_video_url = self.facebook_video_url + self.page_id
    
    def get_long_live_user_token(self):
        url = f'{self.facebook_url}oauth/access_token'

        parameters = {
            'grant_type':'fb_exchange_token',
            'client_id' : self.app_id,
            'client_secret' : self.app_secret,
            'fb_exchange_token' : self.user_token
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

    
    def post_fb_video(self, video_url= "", description= "" , title= "", post_time='', post_now = False):
        """
        Post_now is False if the post has to be scheduled, True to post it now
        """

        files = {'source': open(video_url, 'rb')}

        if post_now is True:
            data ={
                'access_token': self.page_access_token,
                'title':title,
                'description': description
            }

        else:
            data ={
                'access_token': self.page_access_token,
                'published' : False,
                'scheduled_publish_time': post_time,
                'title': title,
                'description': description
            }

        return self._send_content('video', data, files)

    
    def post_text(self, text= "", post_time= "", post_now = True, link=''):

        if post_now is False:
            pass
        else:
            data ={
                'access_token': self.page_access_token,
                'message': text
            }
        
        if link !='':
            data['link'] = link

        return self._send_content('text', data)



    def post_image(self, description= "", photo_url= "", title= "", post_time=datetime.datetime.now(), post_now = False):
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
        post_type = 1,
        num_emojis = 1,
        hashtags = Hashtag.objects.random_hashtags('facebook'),
        has_default_title = True,
        default_title = DefaultTilte.objects.random_title,
        custom_title = None,
        caption = None,
        link='',
        ):

        emojis = Emoji.objects.random_emojis(num_emojis)

        if not custom_title and has_default_title is True:
            custom_title = f'{emojis[0].emoji}{default_title}'

        if not caption:
            caption = self.create_fb_description([hashtag.name for hashtag in hashtags])
        
        if post_type == 1 or post_type == 5 or post_type == 7:
            content_type = 'video'
            video_url = ''
            post_response = self.post_fb_video(video_url= video_url, description= caption, title= custom_title, post_now = True)

        elif post_type == 2 or post_type == 6:
            content_type = 'image'
            post_response = self.post_image()

        elif post_type == 3 or post_type == 4:
            content_type = 'text'
            post_response = self.post_text(text= caption, link=link)

        if post_response['result'] == 'success':
            facebook_post = {
                'post_type': post_type ,
                'social_id': post_response['extra'] ,
                'emojis': emojis ,
                'hashtags': hashtags ,
                'has_default_title': has_default_title ,
                'default_title': default_title ,
                'custom_title': custom_title ,
                'caption': caption
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
    


    

    # def schedule_video_posts_on_facebook(self, year, month, day, hour, number_to_post):
    #     folders = [folder for folder in os.listdir(to_post_dir)]

    #     for folder in folders[:number_to_post]:
    #         complete_url_folder = f'{to_post_dir}{folder}'        

    #         horizontal_url = f'{complete_url_folder}/{horizontal_video_string}'

    #         hour += random.randrange(6, 9)
    #         minute = random.randrange(0, 59)
    #         if hour >= 24:
    #             hour = 0
    #             day += 1
    #         if day >=31:
    #             day = 1
    #             month += 1
    #         if month >= 13:
    #             month = 1
    #             year += 1
        
    #         fb_desc = self.create_fb_description()
    #         fb_title = random.choice(frases_para_descripcion)
    #         fb_date = datetime.datetime(year, month, day,hour,minute).timestamp()

    #         fb_post = self.post_fb_video(
    #             description = fb_desc,
    #             video_url= horizontal_url,
    #             title=fb_title,
    #             post_time = int(fb_date)
    #         )

    #         if fb_post['status'] == 200:
    #             shutil.move(complete_url_folder, posted_dir+folder)
    #             fb_id = fb_post['vid_id']
    #             desktop_notification('Facebook', f"Video id {fb_id} was successfully uploaded.")
                

    #         else:
    #             desktop_notification('Facebook', f"Error con el post {complete_url_folder}")
    


    def create_fb_description(self, hashtags):
        hashtags = '#'.join(hashtags)
        face_description = f"""
        Prueba las herramientas que todo inversor inteligente necesita: https://inversionesyfinanzas.xyz

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
        {hashtags}
        """
        return face_description




            




