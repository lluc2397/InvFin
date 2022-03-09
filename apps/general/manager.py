from django.db.models import (
    Manager
)
from django.contrib.contenttypes.models import ContentType

class VotesManager(Manager):

    def check_vote_existence(self, user, model):
        model_type = ContentType.objects.get_for_model(model)
        return self.filter(user=user, object_id=model.id, content_type=model_type).exists()
            
    def retreive_vote(self, user, model):
        model_type = ContentType.objects.get_for_model(model)
        return self.get(user=user, object_id=model.id, content_type=model_type)

    def vote(self, user, model, action):
        if action == 'down':
            is_downvote = True
        move = 1
        vote_object = False
        if self.check_vote_existence(user, model):
            vote_object = self.retreive_vote(user, model)
            move = 2            
        
        if vote_object == False:
            vote_object = self.create()
        
        if is_downvote == True:
            move = -move
        
        model.total_votes += move