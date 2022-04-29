import sys 
import random
import uuid
import logging

from django.db.models import Manager 


class TitlesManager(Manager):

    @property
    def random_title(self):
        titles = [al_title for al_title in self.all()]
        return random.choice(titles)


class EmojisManager(Manager):

    def random_emojis(self, num):        
        emojis = []
        for i in range(num):
            emojis.append(self.get(id = random.randint(1,self.all().count())))
        return emojis

class HashtagsManager(Manager):

    @property
    def random_ig_hashtags(self):
        hashtags = [hashtag for hashtag in self.filter(for_ig = True)]
        return hashtags
    
    @property
    def random_tw_hashtags(self):
        hashtags = [hashtag for hashtag in self.filter(for_tw = True)]
        return hashtags
    
    @property
    def random_fb_hashtags(self):
        hashtags = [hashtag for hashtag in self.filter(for_fb = True)]
        return hashtags
    
    @property
    def random_yb_hashtags(self):
        hashtags = [hashtag for hashtag in self.filter(for_yb = True)]
        return hashtags