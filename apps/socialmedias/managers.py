import sys 
import random
import uuid
import logging

from django.db.models import Manager 


class TitlesManager(Manager):
    @property
    def random_title(self):
        pass
        # titles = [title for title in self.all()]
        # return random.choice(titles)


class EmojisManager(Manager):
    def random_emojis(self, num):
        pass  
        # emojis = []
        # for i in range(num):
        #     emojis.append(self.get(id = random.randint(1,self.all().count())))
        # return emojis

class HashtagsManager(Manager):
    def random_hashtags(self, platform):
        pass
        # hashtags = [hashtag for hashtag in self.filter(platform = platform)]
        # return hashtags
