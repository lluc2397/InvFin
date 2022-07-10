from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.html import strip_tags, format_html

from apps.translate.google_trans_new import google_translator
from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter


User = get_user_model()
DOMAIN = settings.CURRENT_DOMAIN
FULL_DOMAIN = settings.FULL_DOMAIN


class SocialPosting:
    def __init__(self, model, content_shared=None, company_related=None) -> None:
        self.model = model
        self.content_shared = content_shared
        self.company_related = company_related
    
    def generate_content(self):
        link = None
        if self.content_shared:
            content = self.content_shared
            model_type = str(content.__class__._meta)
            
            if model_type == 'preguntas_respuestas.question':# Quesiton
                description = content.content
                title = content.title
                description = strip_tags(format_html(description))
                title = strip_tags(format_html(title))
            
            elif model_type == 'empresas.company':# Company:
                title = content.name
                description = f'{content.short_introduction} {content.description}'

            elif model_type == 'public_blog.publicblog':# Company:
                title = content.title
                description = content.resume
                link = content.custom_url

            elif model_type == 'escritos.term':# term:
                title = content.title
                description = content.resume
            
        elif self.company_related:# News
            content = self.company_related
            news = content.show_news[0]
            title = news['headline']
            description = news['summary']
            description = google_translator().translate(description, lang_src='en', lang_tgt='es')
            title = google_translator().translate(title, lang_src='en', lang_tgt='es')

        if link is None:
            link = FULL_DOMAIN + content.get_absolute_url()

        return title, link, description
    
    def share_content(self, post_type=3):
        title, link, description = self.generate_content()
        fb_response = Facebook().post_on_facebook(title=title, caption=description, post_type=3, link=link)
        self.save_post(fb_response)
        
        tw_response = Twitter().tweet(caption=description, post_type=3, link=link, title=title)
        self.save_post(tw_response)

    def save_post(self, data:dict):
        data['user'] = User.objects.get(username = 'Lucas')
        
        if self.company_related:
            data['company_related'] = self.company_related
        else:
            data['content_shared'] = self.content_shared
        
        #Create a list inside the dict returned to generate multiples models and saved them in bulk
        if 'multiple_posts' in data:
            self.model.objects.bulk_create([self.model(**post) for post in data['posts']])
        else:
            self.model.objects.create(**data)