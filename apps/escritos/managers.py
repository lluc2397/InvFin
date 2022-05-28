from django.db.models import Manager


class TermManager(Manager):
    def clean_terms(self):
        return self.filter(status = 1)