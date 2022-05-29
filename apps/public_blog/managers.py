import random

from django.db.models import Manager


class PublicBlogManager(Manager):
    def get_random(self, query=None):
        query = query if query else self.all()
        models_list = list(query)
        return random.choice(models_list)