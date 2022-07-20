from typing import List, Dict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.html import format_html, strip_tags
from django.template.loader import render_to_string

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog

from apps.socialmedias import constants
from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter
from .models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    NewsSharedHistorial,
    ProfileSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)

from apps.translate.google_trans_new import google_translator

User = get_user_model()
DOMAIN = settings.CURRENT_DOMAIN
FULL_DOMAIN = settings.FULL_DOMAIN

# render_to_string(self.newsletter_template, {
#             'usuario': receiver,
#             'introduction':introduction,
#             'content':content,
#             'despedida':despedida,
#             'image_tag':image_tag
#         })

class SocialPosting:
    facebook_poster = Facebook
    # instagram_poster
    twitter_poster = Twitter
    # youtube_poster
    
    def news_content(self, content:Company=None):
        if not content:
            content = Company.objects.get_random_most_visited_clean_company()
        news = content.show_news[0]
        title = news['headline']
        description = news['summary']
        description = google_translator().translate(description, lang_src='en', lang_tgt='es')
        title = google_translator().translate(title, lang_src='en', lang_tgt='es')
        shared_model_historial = NewsSharedHistorial
        return {
            "title": title,
            "description": description,
            "link": FULL_DOMAIN + content.get_absolute_url(),
            "company_related": content,
            "shared_model_historial": shared_model_historial,
        }

    def company_content(self, content:Company=None):
        if not content:
            content = Company.objects.get_random_most_visited_clean_company()
        title = content.name
        description = f'{content.short_introduction} {content.description}'
        shared_model_historial = CompanySharedHistorial
        return {
            "title": title,
            "description": description,
            "link": FULL_DOMAIN + content.get_absolute_url(),
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }

    def question_content(self, content:Question=None):
        if not content:
            content = Question.objects.get_random()
        description = content.content
        title = content.title
        description = strip_tags(format_html(description))
        title = strip_tags(format_html(title))
        shared_model_historial = QuestionSharedHistorial
        return {
            "title": title,
            "description": description,
            "link": FULL_DOMAIN + content.get_absolute_url(),
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }

    def term_content(self, content:Term=None):
        if not content:
            content = Term.objects.get_random()
        title = content.title
        description = content.resume
        shared_model_historial = TermSharedHistorial
        return {
            "title": title,
            "description": description,
            "link": FULL_DOMAIN + content.get_absolute_url(),
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }

    def publicblog_content(self, content:PublicBlog=None):
        if not content:
            content = PublicBlog.objects.get_random()
        title = content.title
        description = content.resume
        link = content.custom_url
        shared_model_historial = BlogSharedHistorial
        return {
            "title": title,
            "description": description,
            "link": link,
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }
    
    def generate_utm_url(self):
        pass

    def generate_content(self, social_medias:List, content:Dict):
        social_media_actions = {
            constants.FACEBOOK : self.facebook_poster,
            constants.TWITTER : self.twitter_poster,
            constants.INSTAGRAM : "",
            constants.YOUTUBE : "",
            constants.REDDIT : "",
            constants.WHATSAPP : "",
            constants.LINKEDIN : "",
            constants.PINTEREST : "",
            constants.TUMBLR : "",
        }
        social_media_content = []
        for social_media in social_medias:
            social_media_fnct = social_media_actions[social_media["platform"]]
            social_media_content.append({
                **social_media_fnct(**content),
                "platform_shared": social_media
            })
            
        return social_media_content
    
    @classmethod
    def share_content(cls, model_for_social_medias_content:int, social_medias:List):
        social_media_content = {
            constants.MODEL_QUESTION: cls.question_content,
            constants.MODEL_NEWS: cls.news_content,
            constants.MODEL_TERM: cls.term_content,
            constants.MODEL_BLOG: cls.publicblog_content,
            constants.MODEL_COMPANY: cls.company_content,
        }
        generate_content = social_media_content[model_for_social_medias_content]
        content = generate_content()
        cls.generate_content(social_medias, content)

        fb_response = Facebook().post_on_facebook(title=title, caption=description, post_type=3, link=link)
        tw_response = Twitter().tweet(caption=description, post_type=3, link=link, title=title)

        data_to_save = {} 
        data_to_save.update()
        cls.save_post(data_to_save)

    def save_post(self, data:dict):
        data['user'] = User.objects.get(username = 'Lucas')
        
        #Create a list inside the dict returned to generate multiples models and saved them in bulk
        shared_model_historial = data.pop("shared_model_historial")
        default_manager = shared_model_historial._default_manager
        default_manager.bulk_create([shared_model_historial(**post) for post in data['posts']])
