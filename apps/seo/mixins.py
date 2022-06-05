from django.conf import settings

SITE = settings.FULL_DOMAIN

class SEOViewMixin:
    meta_description = None
    meta_tags = None
    meta_title = None
    meta_url = None
    meta_image = None
    meta_author = None

    def get_meta_url(self):
        meta_url = self.meta_url
        if not meta_url:
            meta_url = self.request.path
        return meta_url
    
    def get_meta_author(self, instance: object = None):
        meta_author = self.meta_author
        if not meta_author:
            if instance:
                meta_author = getattr(instance, 'author')
            else:
                meta_author = 'InvFin'
        return meta_author

    def get_meta_title(self, instance: object = None):
        meta_title = self.meta_title
        if not meta_title:
            if instance:
                meta_title = getattr(instance, 'name', None)
                if not meta_title:
                    meta_title = getattr(instance, 'title', None)
            else:
                meta_title = 'Invierte correctamente'
        return meta_title
    
    def get_meta_description(self, instance: object = None):
        meta_description = self.meta_description
        if not meta_description:
            if instance:
                meta_description = getattr(instance, 'description', None)
                if not meta_description:
                    meta_description = getattr(instance, 'resume', None)
            else:
                meta_description = 'Todo lo que necesitas para ser un mejor inversor'            
        return meta_description
    
    def get_meta_image(self, instance: object = None):
        meta_image = self.meta_image
        if not meta_image:
            if instance:
                meta_image = getattr(instance, 'meta_image', None)
                if not meta_image:
                    meta_image = getattr(instance, 'image', None)
                if not meta_image:
                    meta_image = getattr(instance, 'thumbnail', None)
            else:
                meta_image = f'{SITE}/static/general/assets/img/favicon/favicon.ico'
        return meta_image
    
    def get_meta_tags(self):
        meta_tags = self.meta_tags
        if not meta_tags:
            meta_tags = 'finanzas, blog financiero, blog el financiera, invertir'
        return meta_tags
    
    def get_meta_information(self, instance: object = None):
        return {
            "meta_desc": self.get_meta_description(instance),
            "meta_tags": self.get_meta_tags(),
            "meta_title": self.get_meta_title(instance),
            "meta_url": self.get_meta_url(),
            "meta_img": self.get_meta_image()
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            instance = self.object
        except:
            instance = None
        context.update(self.get_meta_information(instance))
        return context