import random

from django.db.models import Manager


class TitlesManager(Manager):
    @property
    def random_title(self):
        return random.choice(list(self.all()))


class EmojisManager(Manager):
    def random_emojis(self, num):
        return random.choices(list(self.all()), k=num)  
        

class HashtagsManager(Manager):
    def random_hashtags(self, platform):
        hashtags = [hashtag for hashtag in self.filter(platform = platform)]
        return hashtags  
