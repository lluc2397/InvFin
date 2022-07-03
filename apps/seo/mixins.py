from django.conf import settings

SITE = settings.FULL_DOMAIN

class SEOViewMixin:
    meta_description = None
    meta_tags = None
    meta_title = None
    meta_url = None
    meta_image = None
    meta_author = None

    def get_possible_meta_attribute(self, instance:object, fields:list, default:str):
        meta_field = default
        if instance:
            for field in fields:
                possible_meta_field = getattr(instance, field, None)
                if possible_meta_field is not None:
                    meta_field = possible_meta_field
                    break
        return meta_field

    def get_meta_url(self):
        meta_url = self.meta_url
        if not meta_url:
            meta_url = self.request.path
        return meta_url
    
    def get_meta_author(self, instance: object=None):
        meta_author = self.meta_author
        if not meta_author:
            meta_author = self.get_possible_meta_attribute(
                instance, ['author'], 'InvFin'
                )
        return meta_author

    def get_meta_title(self, instance: object=None):
        meta_title = self.meta_title
        if not meta_title:
            meta_title = self.get_possible_meta_attribute(
                instance, ['meta_title', 'name', 'title'], 'Invierte correctamente'
                )
        return meta_title
    
    def get_meta_description(self, instance:object=None):
        meta_description = self.meta_description
        if not meta_description:
            meta_description = self.get_possible_meta_attribute(
                instance, ['meta_description', 'resume', 'description'], 'Todo lo que necesitas para ser un mejor inversor'
                )
        return meta_description
    
    def get_meta_image(self, instance: object = None):
        meta_image = self.meta_image
        if not meta_image:
            meta_image = self.get_possible_meta_attribute(
                instance, ['meta_image', 'image', 'thumbnail'], f'{SITE}/static/general/assets/img/favicon/favicon.ico'
                )
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
            "meta_img": self.get_meta_image(instance)
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            instance = self.object
        except:
            instance = None
        context.update(self.get_meta_information(instance))
        return context