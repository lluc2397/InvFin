import random
import binascii
import os

from django.db.models import Manager
from django.template.defaultfilters import slugify


class BaseSharedManager(Manager):

    def get_random(self, query=None):
        query = query if query else self.all()
        models_list = list(query)
        return random.choice(models_list)
    
    def create_unique_field(self, value, field, original_value=None, extra=None):
        if self.filter(**{field:value}).exists():
            if field.verbose_name == 'Key':
                value = self.generate_key()
            else:
                value = self.generate_slug(original_value, extra)
            return self.create_unique_field(value, field)
        return value
    
    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()
    
    @classmethod
    def generate_slug(cls, value=None, extra=None):
        return slugify(value + extra)
