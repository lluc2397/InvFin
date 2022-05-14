import sys 
import random
import uuid
import logging

from django.db.models import Manager


class TitlesManager(Manager):
    @property
    def random_title(self):
        titles = [title for title in self.all()]
        return random.choice(titles)


class EmojisManager(Manager):
    def random_emojis(self, num):
        emojis = []        
        for i in range(num):            
            emojis.append(random.choice(list(self.all())))
        return emojis  
        

class HashtagsManager(Manager):
    def random_hashtags(self, platform):
        hashtags = [hashtag for hashtag in self.filter(platform = platform)]
        return hashtags  
