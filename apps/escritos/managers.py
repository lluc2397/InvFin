import random

from django.db.models import Manager


class TermManager(Manager):
    def get_random(self, query=None):
        query = query if query else self.all()
        models_list = list(query)
        return random.choice(models_list)

    def clean_terms(self):
        return self.filter(status = 1)