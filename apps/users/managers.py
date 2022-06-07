import uuid
import secrets
import string
from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager


class UserExtraManager(BaseUserManager):
    
    def get_or_create_quick_user(self, email, request, just_newsletter:bool=False, just_correction:bool=False, local_request:bool=True):
        if self.filter(email = email).exists():
            user = self.get(email = email)

        else:
            user = self.create(
            username = email.split('@')[0],
            email = email,
            password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20))),
            just_newsletter = just_newsletter,
            just_correction = just_correction)
            
            if local_request:
                user.create_new_user(request)
                request.session['F-E'] = email

        return user


class ProfileManager(Manager):
    
    def create_ref_code(self) -> uuid:
        ref_code = str(uuid.uuid4())[:100]
        if self.filter(ref_code = ref_code).exists():
            return self.create_ref_code()
        else:
            return ref_code
    

